"""Code blocks on a page, and a check that a built page keeps them.

Finds every code block (<pre> element) in the content area of an HTML page,
in order, and reads its text, its type (the language it declares), the
section and place it sits in, whether it is highlighted, and whether it
has a copy button and what that button copies.

Usage:
  python3 -I codeblocks.py PAGE.html
      List the code blocks, one line each.
  python3 -I codeblocks.py PAGE.html --emit [--section TEXT ...]
      Print the blocks in the expectations format below (the sections
      whose heading text starts with TEXT only, if given), for writing an
      expectations file by hand.
  python3 -I codeblocks.py PAGE.html --expect FILE [--require WHAT]
      Compare the code blocks with FILE. Exit status 1 when a block is
      missing or extra, when its text, place or section differ, when
      template syntax or markup shows in its text, or when it holds block
      elements (<p>, <blockquote>, <li>, <hr>, headings: its text was read
      as Markdown or HTML blocks); and, for each item of
      WHAT (comma-separated: type, highlight, copy), when a block lacks
      that item.

Options:
  --within SPEC   the content area, as in the headings round's outline.py:
                  by default the first of main#js-content
                  (docs.cloudfoundry.org), article.doc (Antora),
                  article.md-content__inner (Zensical),
                  div.theme-doc-markdown (Docusaurus), main (Starlight)

An expectations file holds one entry per code block, in page order:

  === type=console place=list copy=commands | Section heading text
  the block's text, exactly, on as many lines as it has

The header line starts with `===`; fields before `|`, the heading of the
section the block sits in after it (a block's section is the nearest
heading before it; its text must start with the given text). Fields:
  type   the block's type: console, shell, yaml, json, text, nginx, groovy,
         and so on; names a tool uses for the same type count as the same
         (see TYPES below)
  place  body, list (in a list item), note (in a note or admonition),
         table (in a table cell)
  copy   what the copy button should copy: text (the block's text) or
         commands (the commands of a console block, without their `$ `
         prompts, as Antora's default UI copies them); optional
Lines starting with '#' before the first entry are comments. The text runs
to the next `===` line; blank lines at its end are dropped.

What counts as a block's text: the text of the <pre>, with <br> and the
end of a line element (<div>) read as line breaks, copy buttons, line
numbers and screen-reader labels left out, and character references
decoded (a <p>, <blockquote> or <li> that a tool made inside a block ends
a line too). Then (the normalisation): trailing white space on each line is
dropped, and blank lines at the start and the end of the block. Nothing
else changes: indentation, tabs, quotes and blank lines inside a block
must be exactly as expected. The published site's e-mail obfuscation
(Cloudflare replaces an address with "[email protected]" and a script
puts it back in the browser) is undone the way the script does it.

What counts as its type: the first of the code element's data-lang, the
pre's data-language, a `language-X` class on the code, the pre or a
wrapper up to three levels up, the Rouge class `highlight X` (the
published book), and the class `terminal`. Highlighted: a token span
inside the block (see highlighted() below); whether a block has one
depends on its text as well as its type, so it is reported, and required
only when asked. Copy
button: a button whose title, label or class mentions copy or clipboard,
in the block or its wrappers up to four levels up that hold no other
block. What it copies: the
attribute data-copied-text on the <pre>, which codeblocks-browser.mjs
writes after clicking the button, or else Expressive Code's data-code.
"""
import difflib, re, sys
from html.parser import HTMLParser

STRUCTURE = {'p', 'blockquote', 'ul', 'ol', 'li', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table'}
P_CLOSERS = {'pre', 'div', 'ul', 'ol', 'table', 'blockquote', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'dl', 'figure'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
DEFAULT_WITHIN = ['main#js-content', 'article.doc', 'article.md-content__inner', 'div.theme-doc-markdown', 'main']
SKIP_TEXT = {'button', 'script', 'style', 'template'}
SKIP_CLASS = {'sr-only', 'lineno', 'linenos', 'copy', 'md-clipboard', 'source-toolbox', 'headerlink', 'hash-link'}
NOTE_CLASS = {'note', 'admonition', 'theme-admonition', 'starlight-aside', 'admonitionblock'}
TYPES = [   # the first name of each list is the one the check reports
    ['console', 'shell-session', 'shellsession', 'sh-session', 'shell_session', 'terminal'],
    ['bash', 'shell', 'sh', 'zsh'],
    ['yaml', 'yml'],
    ['text', 'plaintext', 'plain', 'txt', 'none'],
    ['groovy', 'gradle'],
]
LEAKS = [
    (r'<%|%>', 'ERB tag'),
    (r'\{%|%\}', 'Markdoc tag'),
    (r'\$?\{\s*vars\.\w+|\bvars\.\w+', 'variable reference'),
    (r'\{(app_domain|private_app_domain|tcp_app_domain)\}', 'AsciiDoc attribute'),
    (r'</?(span|code|strong|b|em|i|a|br|p|div|pre|blockquote)\b[^>]*>', 'HTML tag'),
    (r'&(lt|gt|amp|quot|#\d+|#x[0-9a-fA-F]+);', 'character reference'),
    (r'^\s*(```|~~~)', 'fence marker'),
]


def family(t):
    t = (t or '').lower()
    for f in TYPES:
        if t in f:
            return f[0]
    return t


class Node:
    __slots__ = ('tag', 'attrs', 'parent', 'children')

    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.children = tag, attrs, parent, []

    def cls(self):
        return set((self.attrs.get('class') or '').split())

    def walk(self):
        yield self
        for c in self.children:
            if isinstance(c, Node):
                yield from c.walk()

    def ancestors(self):
        p = self.parent
        while p is not None:
            yield p
            p = p.parent


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('#root', {}, None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        # a block element ends an open <p>, as an HTML parser does; a </p>
        # with no <p> open is then ignored (handle_endtag finds none)
        if tag in P_CLOSERS and self.cur.tag == 'p':
            self.cur = self.cur.parent
        node = Node(tag, {k: (v or '') for k, v in attrs}, self.cur)
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
            if tag == 'p' and p.tag in P_CLOSERS:
                return      # no <p> open inside this block
            p = p.parent
        if p is not None and p.parent is not None:
            self.cur = p.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def spec_match(spec, node):
    m = re.fullmatch(r'([a-z0-9]+)(?:#([\w-]+)|\.([\w-]+))?', spec)
    t, i, c = m.groups()
    return node.tag == t and (not i or node.attrs.get('id') == i) and (not c or c in node.cls())


def cf_email(hexstr):
    try:
        key = int(hexstr[:2], 16)
        return ''.join(chr(int(hexstr[i:i + 2], 16) ^ key) for i in range(2, len(hexstr), 2))
    except ValueError:
        return None


def text_of(node):
    out = []

    def rec(n):
        for c in n.children:
            if isinstance(c, str):
                out.append(c)
                continue
            if c.tag in SKIP_TEXT or SKIP_CLASS & c.cls():
                continue
            if c.tag == 'a' and '__cf_email__' in c.cls() and cf_email(c.attrs.get('data-cfemail', '')):
                out.append(cf_email(c.attrs['data-cfemail']))
                continue
            if c.tag == 'br':
                out.append('\n')
                continue
            rec(c)
            if c.tag in ('div', 'p', 'blockquote', 'li') and out and not ''.join(out).endswith('\n'):
                out.append('\n')
    rec(node)
    return ''.join(out)


def normalise(t):
    lines = [l.rstrip() for l in t.replace('\r\n', '\n').replace('\r', '\n').split('\n')]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return '\n'.join(lines)


def heading_text(h):
    return norm_ws(text_of(h)).replace('¶', '').strip()


def norm_ws(s):
    s = s.replace('​', '').replace('\xa0', ' ')
    s = s.translate(str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"'}))
    return ' '.join(s.split())


def block_type(pre):
    code = next((c for c in pre.children if isinstance(c, Node) and c.tag == 'code'), None)
    if code is not None and code.attrs.get('data-lang'):
        return code.attrs['data-lang']
    if pre.attrs.get('data-language'):
        return pre.attrs['data-language']
    cands = ([code] if code is not None else []) + [pre] + list(pre.ancestors())[:3]
    for n in cands:
        for c in n.cls():
            if c.startswith('language-'):
                return c[len('language-'):]
    cl = (pre.attrs.get('class') or '').split()
    if 'highlight' in cl and len(cl) > 1:
        return [c for c in cl if c != 'highlight'][0]
    if 'terminal' in cl:
        return 'terminal'
    return ''


WRAPPERS = {'token', 'plain', 'token-line', 'line', 'ec-line', 'code', 'hljs'}


def highlighted(pre):
    """True when a highlighter marked tokens in the block: a span with a
    token class (Prism's `token X` other than `plain`, Pygments' and
    Rouge's short classes, highlight.js's `hljs-X`), or spans in at least
    two inline styles (Expressive Code)."""
    styles = set()
    for n in pre.walk():
        if n is pre or n.tag != 'span':
            continue
        if not any(isinstance(x, str) and x.strip() for x in n.children):
            continue
        if n.cls() - WRAPPERS:
            return True
        if n.attrs.get('style') and not n.cls():
            styles.add(n.attrs['style'])
    return len(styles) >= 2


def copy_button(pre):
    scope = [pre]
    for a in list(pre.ancestors())[:4]:
        if sum(1 for n in a.walk() if n.tag == 'pre') > 1:
            break       # a wrapper of more than this block
        scope.append(a)
    for s in scope:
        for n in s.walk():
            if n.tag == 'button':
                label = ' '.join([n.attrs.get('title', ''), n.attrs.get('aria-label', ''), n.attrs.get('class', '')]).lower()
                if 'copy' in label or 'clipboard' in label:
                    return n
    return None


def place(pre):
    for a in pre.ancestors():
        if NOTE_CLASS & a.cls() or a.tag == 'aside' and 'starlight-aside' in a.cls():
            return 'note'
    for a in pre.ancestors():
        if a.tag in ('td', 'th'):
            return 'table'
    for a in pre.ancestors():
        if a.tag == 'li':
            return 'list'
    return 'body'


def commands(text):
    """The commands of a console block: each `$ ` line without its prompt,
    with backslash continuations joined, as Antora's default UI does."""
    out, cur = [], None
    for line in text.split('\n'):
        if cur is not None:
            cur += ' ' + line.strip()
            if not line.rstrip().endswith('\\'):
                out.append(cur)
                cur = None
            continue
        if line.startswith('$ '):
            cmd = line[2:]
            if cmd.rstrip().endswith('\\'):
                cur = cmd
            else:
                out.append(cmd)
    if cur is not None:
        out.append(cur)
    return [re.sub(r'\s*\\\s+', ' ', c) for c in out]


def blocks_of(path, within=None):
    tree = Tree()
    tree.feed(open(path, encoding='utf-8').read())
    region = None
    for spec in ([within] if within else DEFAULT_WITHIN):
        region = next((n for n in tree.root.walk() if spec_match(spec, n)), None)
        if region is not None:
            break
    if region is None:
        sys.exit(f'{path}: no content area found')
    out, heading = [], ''
    for n in region.walk():
        if re.fullmatch(r'h[1-6]', n.tag) and not any(a.tag in ('nav', 'aside') and 'starlight-aside' not in a.cls()
                                                      for a in n.ancestors()):
            heading = heading_text(n)
        if n.tag != 'pre' or any(a.tag == 'pre' for a in n.ancestors()):
            continue
        if any(a.tag == 'nav' for a in n.ancestors()):
            continue
        btn = copy_button(n)
        copied = n.attrs.get('data-copied-text')
        if copied is None and btn is not None and 'data-code' in btn.attrs:
            copied = btn.attrs['data-code'].replace('\x7f', '\n')
        blocks_in = sorted({d.tag for d in n.walk() if d is not n and d.tag in STRUCTURE})
        out.append({'text': normalise(text_of(n)), 'type': block_type(n), 'section': heading, 'blocks_in': blocks_in,
                    'place': place(n), 'highlight': highlighted(n), 'copy': btn is not None,
                    'copied': copied})
    return out


def read_expect(path):
    out, cur = [], None
    for line in open(path, encoding='utf-8').read().split('\n'):
        if line.startswith('==='):
            head, _, sec = line[3:].partition('|')
            fields = dict(f.split('=', 1) for f in head.split() if '=' in f)
            cur = {'type': fields.get('type', ''), 'place': fields.get('place', 'body'),
                   'copy': fields.get('copy', ''), 'section': norm_ws(sec), 'lines': []}
            out.append(cur)
        elif cur is not None:
            cur['lines'].append(line)
        elif line.strip() and not line.startswith('#'):
            sys.exit(f'{path}: text before the first === line')
    for e in out:
        e['text'] = normalise('\n'.join(e['lines']))
    return out


def short(t, n=60):
    t = t.split('\n')[0] if t else '(empty)'
    return t if len(t) <= n else t[:n - 1] + '…'


def copy_kind(b):
    if b['copied'] is None:
        return None
    c = normalise(b['copied'])
    if c == b['text']:
        return 'text'
    cmds = commands(b['text'])
    if cmds and c in ('\n'.join(cmds), ' && '.join(cmds)):
        return 'commands'
    return 'other'


def first_diff(a, b):
    al, bl = a.split('\n'), b.split('\n')
    for i in range(max(len(al), len(bl))):
        x = al[i] if i < len(al) else '(no line)'
        y = bl[i] if i < len(bl) else '(no line)'
        if x != y:
            return f'line {i + 1}: expected {x!r}, got {y!r}'
    return ''


def leaks(want, got):
    out = []
    for pat, what in LEAKS:
        for m in re.finditer(pat, got, re.M):
            if not re.search(re.escape(m.group(0)), want):
                out.append(f'{what} {m.group(0).strip()!r}')
                break
    return out


def check(path, expect_path, require, within):
    want = read_expect(expect_path)
    got = blocks_of(path, within)
    sections = {e['section'] for e in want}
    cand = [b for b in got if any(b['section'].startswith(s) for s in sections)]
    fail = 0
    j = 0
    used = set()
    tally = {'text': 0, 'type': 0, 'highlight': 0, 'copy': 0}
    copies = {}
    for n, e in enumerate(want, 1):
        best, best_r = None, 0.0
        for k in range(j, min(j + 4, len(cand))):
            if k in used:
                continue
            r = 1.0 if cand[k]['text'] == e['text'] else difflib.SequenceMatcher(None, e['text'], cand[k]['text']).ratio()
            if r > best_r:
                best, best_r = k, r
            if r == 1.0:
                break
        if (best is None or best_r < 0.5) and j < len(cand) and j not in used and \
                cand[j]['text'].split('\n')[0] == e['text'].split('\n')[0]:
            best, best_r = j, 0.5     # same first line: the same block, its text differs
        if best is None or best_r < 0.5:
            fail = 1
            print(f'FAIL  {n:2} missing: no code block like {short(e["text"])!r} in "{e["section"][:40]}"')
            continue
        used.add(best)
        j = best + 1
        b = cand[best]
        problems, notes = [], []
        if b['text'] == e['text']:
            tally['text'] += 1
        else:
            problems.append('text differs, ' + first_diff(e['text'], b['text']))
        if b['blocks_in']:
            problems.append('holds ' + ' '.join(f'<{t}>' for t in b['blocks_in']) + ' (its text read as Markdown or HTML blocks)')
        lk = leaks(e['text'], b['text'])
        if lk:
            problems.append('shows ' + ', '.join(lk))
        if not b['section'].startswith(e['section']):
            problems.append(f'section "{b["section"][:40]}"')
        if b['place'] != e['place']:
            problems.append(f'place {b["place"]}, expected {e["place"]}')
        t_ok = bool(e['type']) and family(b['type']) == family(e['type'])
        tally['type'] += t_ok
        tally['highlight'] += b['highlight']
        tally['copy'] += b['copy']
        notes.append(f'type {b["type"] or "(none)"}' + ('' if t_ok else f' (expected {e["type"]})'))
        notes.append('highlighted' if b['highlight'] else 'not highlighted')
        ck = copy_kind(b)
        if b['copy']:
            notes.append('copy button' + (f', copies {ck}' if ck else ''))
            if ck:
                copies[ck] = copies.get(ck, 0) + 1
        else:
            notes.append('no copy button')
        if 'type' in require and not t_ok:
            problems.append(f'type {b["type"] or "(none)"}, expected {e["type"]}')
        if 'highlight' in require and not b['highlight']:
            problems.append('not highlighted')
        if 'copy' in require:
            if not b['copy']:
                problems.append('no copy button')
            elif ck == 'other' or (e['copy'] and ck and ck != e['copy']):
                problems.append(f'copy button copies {ck}' + (f', expected {e["copy"]}' if e['copy'] else ''))
        status = 'FAIL' if problems else 'ok'
        fail |= bool(problems)
        print(f'{status:5} {n:2} {e["place"]:5} {"; ".join(problems + notes)}   | {short(e["text"], 50)}')
    extra = [b for k, b in enumerate(cand) if k not in used]
    for b in extra:
        fail = 1
        print(f'FAIL     extra code block in "{b["section"][:40]}": {short(b["text"])!r}')
    print(f'{"FAIL" if fail else "ok":5} code blocks: {len(want)} expected; '
          f'text {tally["text"]}/{len(want)}, type {tally["type"]}/{len(want)}, highlighted {tally["highlight"]}/{len(want)}, '
          f'copy button {tally["copy"]}/{len(want)}' + (f' (copies: {", ".join(f"{k} {v}" for k, v in sorted(copies.items()))})' if copies else '')
          + (f', {len(extra)} extra' if extra else ''))
    return fail


def main(argv):
    opts, args, i = {'section': []}, [], 0
    while i < len(argv):
        a = argv[i]
        if a in ('--expect', '--require', '--within'):
            opts[a[2:]] = argv[i + 1]
            i += 2
        elif a == '--section':
            opts['section'].append(norm_ws(argv[i + 1]))
            i += 2
        elif a == '--emit':
            opts['emit'] = True
            i += 1
        else:
            args.append(a)
            i += 1
    if len(args) != 1:
        sys.exit(__doc__)
    if 'expect' in opts:
        req = set(filter(None, opts.get('require', '').split(',')))
        return check(args[0], opts['expect'], req, opts.get('within'))
    blocks = blocks_of(args[0], opts.get('within'))
    if opts.get('emit'):
        for b in blocks:
            if opts['section'] and not any(b['section'].startswith(s) for s in opts['section']):
                continue
            print(f'=== type={family(b["type"]) or "?"} place={b["place"]} | {b["section"]}')
            print(b['text'])
        return 0
    print(f'# {args[0]}: {len(blocks)} code blocks')
    for n, b in enumerate(blocks, 1):
        flags = [b['type'] or '(no type)', b['place'], 'highlighted' if b['highlight'] else 'plain',
                 'copy' if b['copy'] else 'no copy']
        print(f'{n:3} {", ".join(flags):45} {b["section"][:35]:35} | {short(b["text"], 50)}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
