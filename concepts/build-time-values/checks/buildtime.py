"""Build-time values on a built page: the copyright notice and the "last
updated" date. Finds them, checks them against a page's intent, and
compares a converted page with the published page with them masked.

Usage:
  python3 -I buildtime.py PAGE.html
      prints every build-time value found on the page
  python3 -I buildtime.py PAGE.html --expect EXPECTATIONS --page NAME --mode MODE [--build-year YYYY]
      checks the values against the lines for NAME and MODE in EXPECTATIONS
  python3 -I buildtime.py --compare PUBLISHED.html BUILT.html [--no-mask]
      compares the main text of the two pages word by word; build-time
      values are taken out of the text and listed apart, as expected
      differences ([R-25]); --no-mask leaves them in the text

What counts as a build-time value:
  copyright  a year (or a range of years) after "©", "&copy;", "(c)" or
             "Copyright", with the holder's name that follows it
  updated    a "last updated" date: Bookbinder's data-modified-date
             attribute (milliseconds since 1970, UTC), a <time datetime>
             element, or a date in the text within 40 characters after
             "last updated" or "last update" (any case), or in an element
             whose class names a last-updated or source-file box
  meta       a <meta> whose name or property says modified, updated or date

EXPECTATIONS has one line per value: `page mode field value`, with # for
comments. Fields:
  copyright-year  `build` (the build's year: today, or --build-year) or a year
  holder          text the notice's holder must start with
  updated         a date (YYYY-MM-DD), `none` (no date on the page) or `any`
Each field may appear once per page and mode; a field not listed is not
checked. Exit status 1 when a check fails.
"""
import datetime, difflib, html, html.parser, re, sys

MONTHS = {m: i for i, m in enumerate(
    ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], 1)}
DATE_TEXT = re.compile(
    r'(?P<iso>\d{4}-\d{2}-\d{2})'
    r'|(?P<mon>[A-Z][a-z]{2})[a-z]*\.? (?P<d1>\d{1,2}), (?P<y1>\d{4})'
    r'|(?P<d2>\d{1,2}) (?P<mon2>[A-Z][a-z]{2})[a-z]*\.? (?P<y2>\d{4})')
COPYRIGHT = re.compile(
    r'(?:©|\(c\)|\bcopyright\b)\s*(?:©\s*)?(?P<y1>(?:19|20)\d{2})'
    r'(?:\s*[-–]\s*(?P<y2>(?:19|20)\d{2}|present))?[\s,]*(?P<holder>[^.|\n]{0,60})', re.I)
LAST_UPDATED = re.compile(r'(page )?last updated?( on)?:?', re.I)
UPDATED_CLASS = re.compile(r'last-updated|lastupdated|source-file|modified-date|page-date', re.I)
BLOCK = {'p', 'li', 'td', 'th', 'tr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'pre', 'ul', 'ol',
         'table', 'thead', 'tbody', 'caption', 'br', 'section', 'figure', 'blockquote', 'footer',
         'aside', 'nav', 'header', 'main', 'article', 'span', 'time', 'b', 'strong'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
SKIP = ('script', 'style', 'nav', 'button', 'svg')
# Heading permalinks and page furniture the earlier rounds' text
# comparison also leaves out (../../tables/checks/text-diff.py)
SKIP_CLASS = re.compile(r'headerlink|hash-link|anchor-link|theme-doc-toc|breadcrumbs|theme-doc-version')


def parse_date(text):
    m = DATE_TEXT.search(text)
    if not m:
        return None
    if m.group('iso'):
        return m.group('iso')
    mon, d, y = (m.group('mon'), m.group('d1'), m.group('y1')) if m.group('mon') else \
        (m.group('mon2'), m.group('d2'), m.group('y2'))
    if mon.lower()[:3] not in MONTHS:
        return None
    return f'{int(y):04d}-{MONTHS[mon.lower()[:3]]:02d}-{int(d):02d}'


class Page(html.parser.HTMLParser):
    """Collects the page's visible text (in order, with block breaks), the
    text of the main content element, and the build-time markup."""

    def __init__(self, mask_boxes=False):
        super().__init__(convert_charrefs=True)
        self.mask_boxes = mask_boxes  # leave last-updated boxes out of the text
        self.text, self.main = [], []
        self.stack = []          # (tag, classes, in_main, skipping)
        self.main_depth = None
        self.values = []         # (field, value, where)
        self.in_updated = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get('class') or ''
        if tag == 'meta':
            key = (a.get('name') or a.get('property') or a.get('itemprop') or '').lower()
            if re.search(r'modified|updated|date', key) and a.get('content'):
                self.values.append(('meta', a['content'], f'<meta {key}>'))
        if 'data-modified-date' in a and (a['data-modified-date'] or '').isdigit():
            t = datetime.datetime.fromtimestamp(int(a['data-modified-date']) / 1000, datetime.timezone.utc)
            self.values.append(('updated', t.strftime('%Y-%m-%d'), 'data-modified-date'))
        if tag == 'time' and a.get('datetime'):
            self.values.append(('updated', a['datetime'][:10], '<time datetime>'))
        if tag in VOID:
            if tag == 'br':
                self._out(' ')
            return
        skipping = tag in SKIP or bool(SKIP_CLASS.search(cls)) or bool(self.stack and self.stack[-1][3])
        updated = bool(UPDATED_CLASS.search(cls))
        if self.main_depth is None and self._is_main(tag, a):
            self.main_depth = len(self.stack) + 1
        self.stack.append((tag, cls, updated, skipping))
        if updated:
            self.in_updated += 1
        if tag in BLOCK:
            self._out(' ')

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        # close up to the matching tag (tolerates unclosed <p> and <li>)
        while self.stack:
            t, cls, updated, skipping = self.stack.pop()
            if updated:
                self.in_updated -= 1
            if self.main_depth is not None and len(self.stack) < self.main_depth:
                self.main_depth = -1
            if t == tag:
                break
        if tag in BLOCK:
            self._out(' ')

    def handle_data(self, data):
        if self.stack and self.stack[-1][3]:
            return
        if self.in_updated:
            d = parse_date(data)
            if d:
                self.values.append(('updated', d, 'last-updated box'))
            if self.mask_boxes:
                return
        self._out(data)

    def _out(self, s):
        self.text.append(s)
        if self.main_depth not in (None, -1):
            self.main.append(s)

    @staticmethod
    def _is_main(tag, a):
        return (tag == 'main' and a.get('id') == 'js-content') or tag == 'article'


def read(path, mask_boxes=False):
    p = Page(mask_boxes)
    p.feed(open(path, encoding='utf-8').read())
    text = ' '.join(''.join(p.text).replace('​', '').replace('\xa0', ' ').split())
    main = ' '.join(''.join(p.main).replace('​', '').replace('\xa0', ' ').split())
    if not main:  # no <article> (Starlight): fall back to <main>
        q = re.search(r'<main\b.*?</main>', open(path, encoding='utf-8').read(), re.S)
        if q:
            sub = Page(mask_boxes)
            sub.feed('<article>' + q.group(0) + '</article>')
            main = ' '.join(''.join(sub.main).replace('\xa0', ' ').split())
    values = list(p.values)
    for m in COPYRIGHT.finditer(text):
        years = m.group('y1') + (f"-{m.group('y2')}" if m.group('y2') else '')
        values.append(('copyright', years, ' '.join(m.group('holder').split())))
    for m in LAST_UPDATED.finditer(text):
        d = parse_date(text[m.end():m.end() + 40])
        if d and not any(v[0] == 'updated' and v[1] == d for v in values):
            values.append(('updated', d, 'text after "last updated"'))
    return values, text, main


def unique(values, field):
    seen = []
    for v in values:
        if v[0] == field and v[1] not in [s[1] for s in seen]:
            seen.append(v)
    return seen


def show(path):
    values, _, _ = read(path)
    for f, v, where in values:
        print(f'{f:10} {v:12} {where}')
    if not values:
        print('no build-time values found')


def expect(path, file, page, mode, build_year):
    values, _, _ = read(path)
    want = {}
    for line in open(file):
        line = line.split('#', 1)[0].split()
        if len(line) >= 4 and line[0] == page and line[1] == mode:
            want[line[2]] = ' '.join(line[3:])
    if not want:
        print(f'FAIL  {page} {mode}: no expectations')
        return False
    ok = True
    cr = unique(values, 'copyright')
    if 'copyright-year' in want:
        year = str(build_year) if want['copyright-year'] == 'build' else want['copyright-year']
        got = [c[1] for c in cr]
        good = got == [year]
        ok &= good
        print(f"{'ok  ' if good else 'FAIL'}  copyright year {got or 'none'}, expected {year}"
              f"{' (build year)' if want['copyright-year'] == 'build' else ''}")
    if 'holder' in want:
        good = bool(cr) and all(c[2].startswith(want['holder']) for c in cr)
        ok &= good
        print(f"{'ok  ' if good else 'FAIL'}  holder {[c[2] for c in cr] or 'none'}, expected {want['holder']!r}")
    if 'updated' in want:
        got = sorted({v[1] for v in values if v[0] == 'updated'})
        exp = want['updated']
        good = (got == [] if exp == 'none' else bool(got) if exp == 'any' else got == [exp])
        ok &= good
        print(f"{'ok  ' if good else 'FAIL'}  updated {got or 'none'}, expected {exp}")
    return ok


def mask(text):
    """Takes the build-time values out of a page's text: copyright notices
    and last-updated phrases with their dates."""
    text = COPYRIGHT.sub(' ', text)
    text = re.sub(r'all rights reserved\.?', ' ', text, flags=re.I)
    text = re.sub(LAST_UPDATED.pattern + r'\s*(' + DATE_TEXT.pattern + r')?', ' ', text, flags=re.I)
    return text


def compare(pub_path, got_path, masked=True):
    pv, ptext, pmain = read(pub_path, masked)
    gv, gtext, gmain = read(got_path, masked)
    print('build-time values (expected differences):')
    for field in ('copyright', 'updated'):
        a = ', '.join(v[1] for v in unique(pv, field)) or 'none'
        b = ', '.join(v[1] for v in unique(gv, field)) or 'none'
        print(f"  {field:10} published {a:12} built {b:12} {'same' if a == b else 'differs'}")
    if masked:
        pmain, gmain = mask(pmain), mask(gmain)
    pw, gw = pmain.split(), gmain.split()
    sm = difflib.SequenceMatcher(None, pw, gw, autojunk=False)
    print(f"content{' (build-time values masked)' if masked else ''}: "
          f'published {len(pw)} words, built {len(gw)} words, matching {sm.ratio():.3f}')
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op != 'equal':
            print(f'  {op:8} published: {" ".join(pw[a1:a2])[:150]!r}\n'
                  f'           built:     {" ".join(gw[b1:b2])[:150]!r}')


def main(argv):
    if '--compare' in argv:
        i = argv.index('--compare')
        compare(argv[i + 1], argv[i + 2], '--no-mask' not in argv)
        return 0
    if not argv or argv[0].startswith('-'):
        sys.exit(__doc__)
    if '--expect' in argv:
        opt = dict(zip(argv[1::2], argv[2::2]))
        year = int(opt.get('--build-year', datetime.date.today().year))
        return 0 if expect(argv[0], opt['--expect'], opt['--page'], opt['--mode'], year) else 1
    show(argv[0])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
