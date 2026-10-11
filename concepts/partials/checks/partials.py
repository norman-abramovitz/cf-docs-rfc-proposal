"""Partials on a built page: is each partial's content there once, in the
right place, with no include syntax left over and no id used twice?

Reads the content area of a built HTML page and compares it with a
partials file, which says, for each place a partial is included, the
words that open and close the partial's text, the host page's words just
before and after it, the section it sits in and whether it sits in a list
item or a table cell.

Usage:
  python3 -I partials.py PAGE.html
      Print the page's text blocks with their section and place, and any
      include syntax left over (to write a partials file).
  python3 -I partials.py BUILT.html --expect FILE [--ignore-ids REGEX]
      Compare BUILT with FILE. Exit status 1 when an inclusion is missing,
      out of place, or there more often than FILE says; when include
      syntax is left on the page; or when an id inside an included span
      is used more than once on the page.

The partials file: one line per inclusion, fields separated by tabs.
Blank lines and lines starting with '#' are skipped.

  include  NAME  SECTION  PLACE  BEFORE  FIRST  LAST  AFTER
      NAME     the partial (for messages only)
      SECTION  text of the nearest heading above the partial's first words
      PLACE    body, list (in a list item) or table (in a table cell), at
               the partial's first and last words; FIRST/LAST (body/table)
               when they differ
      BEFORE   host words just before the partial, or - for none
      FIRST    the partial's first words on the page
      LAST     the partial's last words on the page
      AFTER    host words just after the partial, or - for none
  toc  ID [ID...]
      each ID must be the target of a link in the page's table of
      contents (outside the content area): Docusaurus .table-of-contents,
      Zensical/Material nav.md-nav--secondary, Starlight starlight-toc,
      the published book's .quick-links. Antora builds its table of
      contents in the browser, so the check reports it as not found.

Inclusions are matched in file order, each searched from the first words
of the previous one, so a partial included twice is two lines and a
partial nested in another follows it. Between BEFORE and FIRST only an
admonition's title (Note, Important, Caution) may stand. The place is
checked at the partial's first and at its last words. FIRST must occur
on the page exactly as often as lines name it. Phrases and page text are
compared with white space collapsed, typographic quotes made straight and
zero-width spaces removed.

Options:
  --within SPEC     the content area, as in outline.py
  --ignore-ids RE   ids matching RE are not counted as duplicates (ids a
                    tool makes for its own widgets, such as code line
                    anchors)
"""
import re, sys
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
SKIP_TAGS = {'nav', 'script', 'style', 'template', 'button'}
HIDDEN = {'headerlink', 'hash-link', 'anchor', 'sl-anchor-link', 'sr-only'}
BLOCK = {'p', 'div', 'li', 'ul', 'ol', 'pre', 'br', 'td', 'th', 'tr', 'table', 'blockquote', 'section',
         'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'aside', 'dl', 'dt', 'dd'}
DEFAULT_WITHIN = ['main#js-content', 'article.doc', 'article.md-content__inner', 'div.theme-doc-markdown', 'main']
LEFTOVER = [
    (re.compile(r'<%|&lt;%'), 'ERB tag'),
    (re.compile(r'\{%\s*(partial|include)\b'), 'Markdoc or Jinja include'),
    (re.compile(r'\binclude::'), 'AsciiDoc include'),
    (re.compile(r'-{1,}8<-{1,}'), 'snippet marker'),
    (re.compile(r'\bimport\s+\w+\s+from\s+[\'"]'), 'MDX import'),
    (re.compile(r'Unresolved directive'), 'AsciiDoc unresolved include'),
]


def spec_match(spec, tag, attrs):
    m = re.fullmatch(r'([a-z0-9]+)(?:#([\w-]+)|\.([\w-]+))?', spec)
    t, i, c = m.groups()
    return tag == t and (not i or attrs.get('id') == i) and (not c or c in (attrs.get('class') or '').split())


# a gap allowed between the host's words and a partial's first words: the
# title of an admonition the partial opens with
TITLE = re.compile(r'(?i)(note|important|caution)')


def norm(s):
    s = s.replace('​', '').replace('\xa0', ' ').replace('¶', '')
    s = s.translate(str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"'}))
    return ' '.join(s.split())


class Page(HTMLParser):
    """Text of the content area, with the section and place of every chunk,
    the ids in it (with their text offsets) and the table of contents."""

    def __init__(self, within):
        super().__init__(convert_charrefs=True)
        self.within, self.stack, self.region, self.done = within, [], None, False
        self.skip = self.hide = None
        self.text = ''            # collapsed text of the content area
        self.chunks = []          # (offset, section, place)
        self.ids = []             # (id, offset)
        self.heading, self.h_depth, self.h_text = '', None, ''
        self.li = self.td = 0
        self.tables = []          # per open table: True when it lays out an admonition
        self.raw = []             # raw markup of the content area, for leftovers
        self.toc_depth, self.toc = None, []

    def _add(self, s):
        if not s:
            return
        if self.text and not self.text.endswith(' ') and s[0] != ' ':
            pass
        self.chunks.append((len(self.text), self.heading, 'table' if self.td else 'list' if self.li else 'body'))
        self.text += s

    def _space(self):
        if self.text and not self.text.endswith(' '):
            self.text += ' '

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        cls = set((attrs.get('class') or '').split())
        # table of contents, anywhere on the page
        if self.toc_depth is None and tag not in VOID and (
                'table-of-contents' in cls or 'md-nav--secondary' in cls or tag == 'starlight-toc'
                or 'quick-links' in cls or 'toc' in cls):
            self.toc_depth = len(self.stack) + 1
        if self.toc_depth is not None and tag == 'a' and (attrs.get('href') or '').startswith('#'):
            self.toc.append(attrs['href'][1:])
        if self.done:
            if tag not in VOID:
                self.stack.append((tag, attrs))
            return
        if tag not in VOID:
            self.stack.append((tag, attrs))
        depth = len(self.stack)
        if self.region is None:
            if spec_match(self.within, tag, attrs):
                self.region = depth
            return
        if self.skip is None and (tag in SKIP_TAGS or (tag == 'aside' and 'starlight-aside' not in cls)
                                  or {'quick-links', 'js-quick-links'} & cls):
            self.skip = depth if tag not in VOID else None
        if self.skip is not None:
            return
        self.raw.append(self.get_starttag_text() or '')
        ids = [attrs['id']] if attrs.get('id') else []
        if tag == 'a' and attrs.get('name') and attrs['name'] not in ids:
            ids.append(attrs['name'])
        for i_ in ids:
            self.ids.append((i_, len(self.text)))
        if tag in VOID:
            if tag == 'br':
                self._space()
            return
        if self.hide is None and HIDDEN & cls and not re.fullmatch(r'h[1-6]', tag):
            self.hide = depth
        if re.fullmatch(r'h[1-6]', tag):
            self.h_depth, self.h_text = depth, ''
        if tag in BLOCK:
            self._space()
        if tag == 'table':
            # Antora lays out an admonition as a table; its cells are not table cells
            parent = self.stack[-2][1] if len(self.stack) > 1 else {}
            self.tables.append('admonition' in (parent.get('class') or ''))
        if tag == 'li':
            self.li += 1
        if tag in ('td', 'th') and not (self.tables and self.tables[-1]):
            self.td += 1

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID or tag not in [t for t, _ in self.stack]:
            return
        while self.stack and self.stack[-1][0] != tag:
            self._pop()
        self._pop()

    def _pop(self):
        tag, _ = self.stack.pop()
        depth = len(self.stack)
        if self.toc_depth is not None and depth < self.toc_depth:
            self.toc_depth = None
        if self.done or self.region is None:
            return
        if depth < self.region:
            self.done = True
            return
        if self.skip is not None:
            if depth < self.skip:
                self.skip = None
            return
        if tag in BLOCK:
            self._space()
        if tag == 'li' and self.li:
            self.li -= 1
        if tag in ('td', 'th') and self.td and not (self.tables and self.tables[-1]):
            self.td -= 1
        if tag == 'table' and self.tables:
            self.tables.pop()
        if self.hide is not None and depth < self.hide:
            self.hide = None
        if self.h_depth is not None and depth < self.h_depth:
            self.heading, self.h_depth = norm(self.h_text), None

    def handle_data(self, data):
        if self.region is None or self.done or self.skip is not None:
            return
        self.raw.append(data)
        if self.hide is not None:
            return
        if self.h_depth is not None:
            self.h_text += data
        s = data.replace('​', '').replace('\xa0', ' ')
        s = s.translate(str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"'}))
        s = re.sub(r'\s+', ' ', s)
        if self.text.endswith(' ') and s.startswith(' '):
            s = s[1:]
        self._add(s)

    def where(self, offset):
        """(section, place) of the chunk holding offset."""
        best = ('', 'body')
        for off, sec, place in self.chunks:
            if off > offset:
                break
            best = (sec, place)
        return best


def load(path, within=None):
    html = open(path, encoding='utf-8').read()
    for spec in ([within] if within else DEFAULT_WITHIN):
        p = Page(spec)
        p.feed(html)
        if p.region is not None:
            return p, spec
    sys.exit(f'{path}: no content area found')


def leftovers(page):
    raw = ''.join(page.raw)
    out = []
    for rx, what in LEFTOVER:
        for m in rx.finditer(raw):
            out.append(f'{what}: {norm(raw[max(0, m.start() - 30):m.end() + 50])!r}')
    return out


def find(text, phrase, start):
    i = text.find(phrase, start)
    return i


def main(argv):
    opts, args, i = {}, [], 0
    while i < len(argv):
        if argv[i] in ('--expect', '--within', '--ignore-ids'):
            opts[argv[i][2:]] = argv[i + 1]
            i += 2
        else:
            args.append(argv[i])
            i += 1
    if len(args) != 1:
        sys.exit(__doc__)
    page, spec = load(args[0], opts.get('within'))
    text = page.text
    if 'expect' not in opts:
        print(f'# {args[0]}: content area {spec}, {len(text)} characters')
        last = None
        for off, sec, place in page.chunks:
            if (sec, place) != last:
                print(f'\n[{place}] {sec}')
                last = (sec, place)
            nxt = next((o for o, _, _ in page.chunks if o > off), len(text))
            print('  ' + text[off:nxt].strip()[:120])
        for l in leftovers(page):
            print('leftover ' + l)
        print('toc: ' + ' '.join(page.toc))
        return 0

    status = 0
    lines = [l.rstrip('\n').split('\t') for l in open(opts['expect'], encoding='utf-8')
             if l.strip() and not l.startswith('#')]
    incs = [l for l in lines if l[0] == 'include']
    spans, pos = [], 0
    for f in incs:
        if len(f) != 8:
            sys.exit(f'{opts["expect"]}: an include line needs 8 fields: {f}')
        _, name, section, place, before, first, last, after = [norm(x) if k > 3 else x for k, x in enumerate(f)]
        label = f'{name} ({first[:40]}…)'
        b = pos if before == '-' else find(text, before, pos)
        if b < 0:
            print(f'FAIL  {label}: host text before it not found: {before!r}'); status = 1; continue
        s = find(text, first, b + (0 if before == '-' else len(before)))
        if s < 0:
            print(f'FAIL  {label}: partial not found after {before!r}'); status = 1; continue
        gap = text[b + (0 if before == '-' else len(before)):s].strip()
        e = find(text, last, s)
        if e < 0:
            print(f'FAIL  {label}: its last words not found: {last!r}'); status = 1; continue
        e += len(last)
        problems = []
        if before != '-' and gap and not TITLE.fullmatch(gap):
            problems.append(f'text between the host and the partial: {gap[:60]!r}')
        if after != '-':
            a = find(text, after, e)
            if a < 0:
                problems.append(f'host text after it not found: {after!r}')
            elif text[e:a].strip():
                problems.append(f'text between the partial and the host: {text[e:a].strip()[:60]!r}')
        sec, plc = page.where(s)
        p_first, _, p_last = place.partition('/')
        p_last = p_last or p_first
        if norm(sec) != norm(section):
            problems.append(f'section {sec!r}, expected {section!r}')
        if plc != p_first:
            problems.append(f'place {plc}, expected {p_first}')
        _, plc2 = page.where(e - 1)
        if plc2 != p_last:
            problems.append(f'its last words are in {plc2}, expected {p_last}')
        if problems:
            status = 1
            print(f'FAIL  {label}: ' + '; '.join(problems))
        else:
            print(f'ok    {label}: in {section!r}, {place}')
        spans.append((s, e))
        pos = s + len(first)      # the next inclusion may sit inside this one
    # each partial's first words appear exactly as often as the file says
    for first in sorted({norm(f[5]) for f in incs}):
        want = sum(1 for f in incs if norm(f[5]) == first)
        got = text.count(first)
        if got != want:
            status = 1
            print(f'FAIL  {first[:50]!r} appears {got} times, expected {want}')
    # include syntax left on the page
    left = leftovers(page)
    if left:
        status = 1
        for l in left:
            print(f'FAIL  leftover {l}')
    else:
        print('ok    no include syntax left')
    # ids used more than once, where one use is inside an included span
    ignore = re.compile(opts['ignore-ids']) if 'ignore-ids' in opts else None
    count = {}
    for i_, _ in page.ids:
        count[i_] = count.get(i_, 0) + 1
    dup_in = sorted({i_ for i_, off in page.ids if count[i_] > 1 and any(s <= off <= e for s, e in spans)
                     and not (ignore and ignore.fullmatch(i_))})
    if dup_in:
        status = 1
        print('FAIL  ids used more than once, inside an included span: ' + ' '.join('#' + x for x in dup_in))
    else:
        print('ok    no id inside an included span is used twice')
    other = sorted({i_ for i_, n in count.items() if n > 1} - set(dup_in))
    if other:
        print('info  other ids used more than once: ' + ' '.join('#' + x for x in other[:10]))
    # table of contents
    for f in lines:
        if f[0] == 'toc':
            want = f[1].split()
            missing = [x for x in want if x not in page.toc]
            if not page.toc:
                status = 1
                print(f'FAIL  toc: no table-of-contents links in the static HTML (wanted {len(want)} ids)')
            elif missing:
                status = 1
                print(f'FAIL  toc: {len(want) - len(missing)} of {len(want)} ids; missing ' + ' '.join('#' + x for x in missing))
            else:
                print(f'ok    toc: all {len(want)} ids')
    return status


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
