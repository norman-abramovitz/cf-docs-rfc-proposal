"""Variables on a built page: leftover syntax, escaped markup, and the
expected values at their places.

Usage:
  python3 -I vars.py PAGE.html [--names FILE]
      Scan the page for variable syntax that was not replaced and for
      markup or Markdown shown as text. FILE lists variable names (a YAML
      file whose keys are indented two spaces, such as the book's
      template_variables.yml); with it, AsciiDoc references {name} to
      those names are found too.
  python3 -I vars.py PAGE.html --expect FILE [--names FILE]
      The scan, then each expectation in FILE. Exit status 1 when the scan
      finds anything or an expectation fails.

An expectations file has one line per variable use, fields separated by
tabs (blank lines and lines starting with '#' are skipped):

  SECTION  PLACE  TEXT  [NOTE]

SECTION  the id of the heading whose section holds the use (the section
         runs to the next heading of the same or a higher level), '-' for
         the opening (before the first heading below the title), or '@'
         for the page as a whole (title, head).
PLACE    where TEXT must appear:
           text      the section's text
           p, li, td, th, a, code, pre
                     the text of such an element in the section (code is
                     inline code, outside pre)
           heading   the section's own heading
           a@href    the href of a link in the section; TEXT is the end
                     of the path (leading ./, ../ and / are ignored)
           title     the page's <title>       (SECTION '@')
           h1        the first <h1> in the content area, or else in the
                     page               (SECTION '@')
           undefined TEXT is a variable name the page uses but no file
                     defines; nothing more is checked here, as the scan
                     already fails on any form of it left on the page
TEXT     compared after collapsing white space and making typographic
         quotes straight; it must be contained in the element's text.
NOTE     free text, shown on failure.

What the scan looks for, in text and in attribute values (href, src, alt,
title, content, id), outside <script> and <style>, over the whole page
(head, navigation and table of contents included):
  - ERB: <% and %>
  - Docusaurus/MDX: {vars.  and vars.name (other than vars.yml/.json/.js)
  - Markdoc: {% and $vars.
  - Jinja (Zensical, MkDocs): {{ name }}, or {{ name at the end of a text
  - AsciiDoc: {name} for a name in --names
  - URL-encoded ERB: %3C%25
and, in the content area only and outside code and pre:
  - markup shown as text: <p, <a , <code>, <ul>, <li>, <strong>, ...
  - Markdown shown as text: [text](url), `code`, **bold**

The content area is the first of: main#js-content (docs.cloudfoundry.org),
article.doc (Antora), article.md-content__inner (Zensical),
div.theme-doc-markdown (Docusaurus), main (Starlight); as in the outline
check. The page title and h1 are looked up in the whole page.
"""
import re
import sys
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
HIDDEN = {'headerlink', 'hash-link', 'anchor', 'sl-anchor-link', 'sr-only'}
SKIP = {'script', 'style', 'template'}
NAV = {'nav', 'aside'}
DEFAULT_WITHIN = ['main#js-content', 'article.doc', 'article.md-content__inner', 'div.theme-doc-markdown', 'main']
ATTRS = ('href', 'src', 'alt', 'title', 'content', 'id')
# a <p>, <li>, <td> or <th> left open is closed by the next one, as HTML does
IMPLIED = {'p': {'p', 'div', 'ul', 'ol', 'table', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'dl'},
           'li': {'li'}, 'td': {'td', 'th', 'tr'}, 'th': {'td', 'th', 'tr'}, 'tr': {'tr'}}


class Node:
    __slots__ = ('tag', 'attrs', 'parent', 'children', 'n')

    def __init__(self, tag, attrs, parent, n):
        self.tag, self.attrs, self.parent, self.children, self.n = tag, attrs, parent, [], n

    def text(self, skip_hidden=True):
        out = []
        for c in self.children:
            if isinstance(c, str):
                out.append(c)
            elif c.tag in SKIP:
                continue
            elif skip_hidden and HIDDEN & set((c.attrs.get('class') or '').split()):
                continue
            else:
                out.append(c.text(skip_hidden))
        return ''.join(out)

    def walk(self):
        yield self
        for c in self.children:
            if isinstance(c, Node):
                yield from c.walk()

    def inside(self, tags):
        p = self.parent
        while p is not None:
            if p.tag in tags:
                return True
            p = p.parent
        return False


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('#root', {}, None, 0)
        self.cur = self.root
        self.count = 0

    def handle_starttag(self, tag, attrs):
        attrs = {k: (v or '') for k, v in attrs}
        if tag in IMPLIED.get(self.cur.tag, ()) or (tag in ('td', 'th', 'tr') and self.cur.tag in ('td', 'th')):
            self.cur = self.cur.parent
        self.count += 1
        node = Node(tag, attrs, self.cur, self.count)
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.cur = self.cur.parent

    def handle_endtag(self, tag):
        p = self.cur
        while p is not None and p.tag != tag:
            p = p.parent
        if p is not None and p.parent is not None:
            self.cur = p.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def norm(s):
    s = s.replace('​', '').replace(' ', ' ').replace('¶', '')
    s = s.translate(str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"'}))
    return ' '.join(s.split())


def spec_match(spec, node):
    m = re.fullmatch(r'([a-z0-9]+)(?:#([\w-]+)|\.([\w-]+))?', spec)
    t, i, c = m.groups()
    return node.tag == t and (not i or node.attrs.get('id') == i) and (not c or c in (node.attrs.get('class') or '').split())


def content_area(root):
    for spec in DEFAULT_WITHIN:
        for n in root.walk():
            if spec_match(spec, n):
                return n, spec
    return None, None


def headings(area):
    out = []
    for n in area.walk():
        if re.fullmatch(r'h[1-6]', n.tag) and not n.inside(NAV):
            ids = [x.attrs['id'] for x in n.walk() if x.attrs.get('id')]
            ids += [x.attrs['name'] for x in n.walk() if x.tag == 'a' and x.attrs.get('name')]
            out.append((n, int(n.tag[1]), ids))
    return out


def section_nodes(area, heads, sec):
    """The heading node and the set of node numbers in the section."""
    order = [n for n in area.walk()]
    if sec == '-':
        start = area.n
        first = next((h for h in heads if h[1] > 1), None)
        end = first[0].n if first else 10 ** 9
        return None, {n.n for n in order if start < n.n < end}
    for k, (h, lvl, ids) in enumerate(heads):
        if sec in ids:
            nxt = next((x for x in heads[k + 1:] if x[1] <= lvl), None)
            end = nxt[0].n if nxt else 10 ** 9
            last = max(x.n for x in h.walk())
            return h, {n.n for n in order if last < n.n < end}
    return False, set()


def path_tail(href):
    href = href.split('?')[0]
    while href.startswith(('./', '../', '/')):
        href = href[1:] if href.startswith('/') else href[href.index('/') + 1:]
    return href


LEFTOVER = [
    (r'<%|%>', 'ERB'),
    (r'%3C%25', 'URL-encoded ERB'),
    (r'\{\s*vars\.', 'MDX expression'),
    (r'(?<![\w$])vars\.(?!(?:ya?ml|json|js)\b)[A-Za-z_]\w*', 'vars.name'),
    (r'\{%', 'Markdoc or Jinja tag'),
    (r'\$vars\.', 'Markdoc variable'),
    (r'\{\{\s*[A-Za-z_][^{}]*\}\}|\{\{\s*[A-Za-z_][\w.]*\s*$', 'Jinja expression'),
]
ESCAPED = re.compile(r'<(p|a|code|ul|ol|li|strong|em|span|br|h[1-6]|td|tr|table|div|pre)(\s|>|/)', re.I)
MARKDOWN = [
    (re.compile(r'\[[^\]\n]+\]\([^)\s]+\)'), 'Markdown link'),
    (re.compile(r'(?<![`\w])`[^`\n]+`(?![`\w])'), 'Markdown code span'),
    (re.compile(r'\*\*[^*\n]+\*\*'), 'Markdown bold'),
]


def scan(root, area, names):
    found = []
    pats = list(LEFTOVER)
    if names:
        pats.append((r'\{(?:' + '|'.join(sorted(map(re.escape, names), key=len, reverse=True)) + r')\}', 'AsciiDoc attribute'))

    def where(node):
        p = node
        while p is not None:
            if p is area:
                return 'content'
            if p.tag == 'head':
                return 'head'
            p = p.parent
        return 'page'

    def visit(node):
        if node.tag in SKIP:
            return
        for k in ATTRS:
            v = node.attrs.get(k)
            if v:
                for pat, label in pats:
                    m = re.search(pat, v)
                    if m:
                        found.append(f'{label} in {node.tag}@{k} ({where(node)}): {v[:90]}')
        for c in node.children:
            if isinstance(c, str):
                for pat, label in pats:
                    m = re.search(pat, c)
                    if m:
                        ctx = norm(c[max(0, m.start() - 40):m.end() + 50])
                        found.append(f'{label} in {node.tag} text ({where(node)}): {ctx}')
            else:
                visit(c)
    visit(root)
    if area is not None:
        for n in area.walk():
            if n.tag in ('code', 'pre') or n.inside({'code', 'pre'}) or n.tag in SKIP:
                continue
            for c in n.children:
                if not isinstance(c, str):
                    continue
                m = ESCAPED.search(c)
                if m:
                    found.append(f'markup shown as text in {n.tag}: {norm(c[max(0, m.start() - 30):m.end() + 60])}')
                for pat, label in MARKDOWN:
                    m = pat.search(c)
                    if m:
                        found.append(f'{label} shown as text in {n.tag}: {norm(c[max(0, m.start() - 30):m.end() + 30])}')
    return found


GROUPS = {'p': {'p'}, 'li': {'li'}, 'td': {'td'}, 'th': {'th'}, 'a': {'a'}, 'code': {'code'}, 'pre': {'pre'}}


def check(root, area, heads, line):
    parts = line.rstrip('\n').split('\t')
    sec, place, want = parts[0], parts[1], norm(parts[2]) if len(parts) > 2 else ''
    if place == 'undefined':
        return True, f'{want}: not defined; nothing of it on the page'
    if sec == '@':
        if place == 'title':
            t = next((n for n in root.walk() if n.tag == 'title'), None)
            got = norm(t.text()) if t else ''
        elif place == 'h1':
            t = next((n for n in area.walk() if n.tag == 'h1' and not n.inside(NAV)), None) or \
                next((n for n in root.walk() if n.tag == 'h1' and not n.inside(NAV)), None)
            got = norm(t.text()) if t else ''
        else:
            return False, f'unknown place {place} for the whole page'
        return want in got, f'{place} "{got}"'
    head, nums = section_nodes(area, heads, sec)
    if head is False:
        return False, f'no heading carries #{sec}'
    nodes = [n for n in area.walk() if n.n in nums]
    if place == 'heading':
        got = norm(head.text())
        return want in got, f'heading "{got}"'
    if place == 'text':
        texts = [norm(' '.join(n.text() for n in nodes if n.parent is None or n.parent.n not in nums))]
        return any(want in t for t in texts), 'section text'
    if place == 'a@href':
        hrefs = [n.attrs.get('href', '') for n in nodes if n.tag == 'a']
        ok = any(path_tail(h).endswith(path_tail(want)) or path_tail(h) == path_tail(want) for h in hrefs if h)
        return ok, 'hrefs: ' + ' '.join(h for h in hrefs if h)[:200]
    if place not in GROUPS:
        return False, f'unknown place {place}'
    cands = [n for n in nodes if n.tag in GROUPS[place]]
    if place == 'code':
        cands = [n for n in cands if not n.inside({'pre'})]
    texts = [norm(n.text()) for n in cands]
    if any(want in t for t in texts):
        return True, f'{place}'
    close = max(texts, key=lambda t: len(set(t.split()) & set(want.split())), default='')
    return False, f'{len(cands)} {place} in the section; closest: "{close[:160]}"'


def main(argv):
    opts, args, i = {}, [], 0
    while i < len(argv):
        if argv[i] in ('--expect', '--names'):
            opts[argv[i][2:]] = argv[i + 1]
            i += 2
        else:
            args.append(argv[i])
            i += 1
    if len(args) != 1:
        sys.exit(__doc__)
    t = Tree()
    t.feed(open(args[0], encoding='utf-8').read())
    area, spec = content_area(t.root)
    if area is None:
        sys.exit(f'{args[0]}: no content area found')
    names = []
    if 'names' in opts:
        names = [m.group(1) for m in re.finditer(r'^  (\w+):', open(opts['names'], encoding='utf-8').read(), re.M)]
    status = 0
    found = scan(t.root, area, names)
    if found:
        status = 1
        print(f'FAIL  scan: {len(found)} finding(s)')
        for f in found[:40]:
            print('        ' + f)
        if len(found) > 40:
            print(f'        and {len(found) - 40} more')
    else:
        print('ok    scan: no variable syntax left, no markup or Markdown shown as text')
    if 'expect' in opts:
        heads = headings(area)
        n = bad = 0
        for line in open(opts['expect'], encoding='utf-8'):
            if not line.strip() or line.startswith('#'):
                continue
            n += 1
            ok, info = check(t.root, area, heads, line)
            fields = line.rstrip('\n').split('\t')
            label = f'{fields[0]} {fields[1]} "{fields[2] if len(fields) > 2 else ""}"'
            if not ok:
                bad += 1
                status = 1
                print(f'FAIL  {label}\n        {info}' + (f'\n        note: {fields[3]}' if len(fields) > 3 else ''))
        print(f'{"ok  " if not bad else "FAIL"}  values: {n - bad} of {n} in place')
    return status


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
