"""Heading outline of a page, and a comparison of two outlines.

Extracts every heading (level, text, ids) from the content area of a built
HTML page. Given two pages, compares their outlines: the heading levels and
text must match in order, and each anchor in an anchors file must still
exist on the second page.

Usage:
  python3 -I outline.py PAGE.html
      Print the outline: one heading per line, indented by level, with
      every id the heading carries (its own and those of elements inside it).
  python3 -I outline.py PUBLISHED.html BUILT.html [--anchors FILE] [--section ID [--until ID]]
      Compare BUILT against PUBLISHED. Exit status 1 when the outlines
      differ or an anchor from FILE is missing from BUILT.

Options:
  --anchors FILE   ids that must exist in BUILT, one per line (first word of
                   the line; blank lines and lines starting with '#' are skipped)
  --section ID     compare only the page title (h1) and the section whose
                   heading carries ID on PUBLISHED (for pages built from an
                   excerpt)
  --until ID       with --section: end the section before the heading that
                   carries ID on PUBLISHED (for an excerpt that stops inside
                   a section)
  --within SPEC    the content area, as tag, tag#id or tag.class; by default
                   the first of: main#js-content (docs.cloudfoundry.org),
                   article.doc (Antora), article.md-content__inner (Zensical),
                   div.theme-doc-markdown (Docusaurus), main (Starlight)

What counts as the heading text: the text inside h1-h6, without the
permalink icons and screen-reader labels the tools add (elements with the
classes headerlink, hash-link, anchor, sl-anchor-link, sr-only). Headings
inside nav and aside elements (tables of contents) are left out. Text is
compared after collapsing white space and turning typographic quotes into
straight ones, because the published book turns straight quotes into curly
ones (SmartyPants) and the tools do not.
"""
import sys, re, difflib
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
HIDDEN = {'headerlink', 'hash-link', 'anchor', 'sl-anchor-link', 'sr-only'}
SKIP_TAGS = {'nav', 'aside', 'script', 'style', 'template'}
DEFAULT_WITHIN = ['main#js-content', 'article.doc', 'article.md-content__inner', 'div.theme-doc-markdown', 'main']


def spec_match(spec, tag, attrs):
    m = re.fullmatch(r'([a-z0-9]+)(?:#([\w-]+)|\.([\w-]+))?', spec)
    t, i, c = m.groups()
    if tag != t:
        return False
    if i and attrs.get('id') != i:
        return False
    if c and c not in (attrs.get('class') or '').split():
        return False
    return True


class Outline(HTMLParser):
    def __init__(self, within):
        super().__init__()
        self.within = within
        self.stack = []
        self.region = None      # stack depth of the content area
        self.done = False
        self.skip = None        # depth of a nav/aside being skipped
        self.hide = None        # depth of a hidden element inside a heading
        self.cur = None         # heading being read
        self.cur_depth = None
        self.headings = []
        self.ids = {}           # every id in the content area, with a count

    def _ids(self, tag, attrs):
        out = []
        if attrs.get('id'):
            out.append(attrs['id'])
        if tag == 'a' and attrs.get('name') and attrs['name'] not in out:
            out.append(attrs['name'])
        return out

    def handle_starttag(self, tag, attrs):
        if self.done:
            return
        attrs = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        depth = len(self.stack)
        if self.region is None:
            if spec_match(self.within, tag, attrs):
                self.region = depth
            else:
                return
        for i in self._ids(tag, attrs):
            self.ids[i] = self.ids.get(i, 0) + 1
            if self.cur is not None:
                self.cur['ids'].append(i)
        if tag in VOID:
            return
        if self.skip is None and tag in SKIP_TAGS:
            self.skip = depth
        if self.cur is not None and self.hide is None and HIDDEN & set((attrs.get('class') or '').split()):
            self.hide = depth
        if self.skip is None and self.cur is None and re.fullmatch(r'h[1-6]', tag):
            self.cur = {'level': int(tag[1]), 'text': '', 'ids': self._ids(tag, attrs)}
            self.cur_depth = depth

    def handle_endtag(self, tag):
        if self.done or tag in VOID or tag not in self.stack:
            return
        while self.stack and self.stack[-1] != tag:
            self.stack.pop()
        self.stack.pop()
        depth = len(self.stack)
        if self.hide is not None and depth < self.hide:
            self.hide = None
        if self.cur is not None and depth < self.cur_depth:
            self.cur['text'] = norm(self.cur['text'])
            self.headings.append(self.cur)
            self.cur = None
        if self.skip is not None and depth < self.skip:
            self.skip = None
        if self.region is not None and depth < self.region:
            self.done = True

    def handle_data(self, data):
        if self.cur is not None and self.hide is None:
            self.cur['text'] += data


def norm(s):
    s = s.replace('​', '').replace(' ', ' ').replace('¶', '')
    return ' '.join(s.split())


def key_text(s):
    return s.translate(str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"'}))


def outline(path, within=None):
    html = open(path, encoding='utf-8').read()
    for spec in ([within] if within else DEFAULT_WITHIN):
        o = Outline(spec)
        o.feed(html)
        if o.region is not None:
            return o, spec
    sys.exit(f'{path}: no content area found (tried {", ".join([within] if within else DEFAULT_WITHIN)})')


def show(h):
    ids = ' '.join('#' + i for i in h['ids'])
    return f"{'  ' * (h['level'] - 1)}h{h['level']} {h['text']}" + (f'   {ids}' if ids else '')


def section(headings, anchor, until=None):
    for n, h in enumerate(headings):
        if anchor in h['ids']:
            end = next((m for m in range(n + 1, len(headings)) if headings[m]['level'] <= h['level']), len(headings))
            if until:
                stop = next((m for m in range(n + 1, end) if until in headings[m]['ids']), None)
                if stop is None:
                    sys.exit(f'--until {until}: no heading in the section carries that id')
                end = stop
            return [x for x in headings[:n] if x['level'] == 1] + headings[n:end]
    sys.exit(f'--section {anchor}: no heading carries that id')


def some(ids, n=10):
    ids = ['#' + i for i in ids]
    return ' '.join(ids[:n]) + (f' and {len(ids) - n} more' if len(ids) > n else '')


def main(argv):
    opts, args, i = {}, [], 0
    while i < len(argv):
        if argv[i] in ('--anchors', '--section', '--until', '--within'):
            opts[argv[i][2:]] = argv[i + 1]
            i += 2
        else:
            args.append(argv[i])
            i += 1
    if len(args) == 1:
        o, spec = outline(args[0], opts.get('within'))
        print(f'# {args[0]}: {len(o.headings)} headings in {spec}')
        prev = 0
        for h in o.headings:
            note = f'   (skips from h{prev})' if prev and h['level'] > prev + 1 else ''
            print(show(h) + note)
            prev = h['level']
        return 0
    if len(args) != 2:
        sys.exit(__doc__)
    pub, _ = outline(args[0], opts.get('within'))
    got, spec = outline(args[1], opts.get('within'))
    ph = section(pub.headings, opts['section'], opts.get('until')) if 'section' in opts else pub.headings
    gh = got.headings
    status = 0
    a = [(h['level'], key_text(h['text'])) for h in ph]
    b = [(h['level'], key_text(h['text'])) for h in gh]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    if a == b:
        print(f'ok    outline: {len(a)} headings, same levels and text')
    else:
        status = 1
        print(f'FAIL  outline: published {len(a)} headings, built {len(b)}')
        for op, a1, a2, b1, b2 in sm.get_opcodes():
            if op == 'equal':
                continue
            for h in ph[a1:a2]:
                print(f'        - {show(h).strip()}')
            for h in gh[b1:b2]:
                print(f'        + {show(h).strip()}')
    if 'anchors' in opts:
        want = []
        for line in open(opts['anchors'], encoding='utf-8'):
            line = line.strip()
            if line and not line.startswith('#'):
                want.append(line.split()[0])
        on_heading = {i for h in gh for i in h['ids']}
        missing = [w for w in want if w not in got.ids]
        elsewhere = [w for w in want if w in got.ids and w not in on_heading]
        if missing:
            status = 1
            print(f'FAIL  anchors: {len(want) - len(missing)} of {len(want)} exist; missing: ' + ' '.join('#' + w for w in missing))
        else:
            print(f'ok    anchors: all {len(want)} exist')
        if elsewhere:
            print('info  anchors not on a heading: ' + ' '.join('#' + w for w in elsewhere))
    dups = sorted(i for i, n in got.ids.items() if n > 1)
    if dups:
        print(f'info  ids used more than once on the built page ({len(dups)}): ' + some(dups))
    lost = [i for h in ph for i in h['ids'] if i not in got.ids]
    if lost:
        print(f'info  published heading ids not on the built page ({len(lost)}): ' + some(lost))
    return status


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
