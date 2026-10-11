"""Notes on a page, and a check that a built page keeps them.

Finds every note in the content area of an HTML page, in order: the
published book's `<p class="note">` and `<div class="note">`, and each
tool's admonition. For each note it reads the kind, the title, the text,
what the note holds (list items, code, code blocks, links), the heading of
the section it sits in, and whether it sits in a list item or a table cell.

Usage:
  python3 -I notes.py PAGE.html
      Print the notes, one block per note.
  python3 -I notes.py PAGE.html --emit
      Print the notes as lines of a notes file (the format --expect reads).
  python3 -I notes.py BUILT.html --expect FILE [--map KIND=TYPE,...]
      Compare the notes on BUILT with the notes in FILE. Exit status 1
      when a note is missing or extra, or when its kind, title, text,
      contents, section or place differ.

Options:
  --expect FILE   a notes file: one note per line, fields separated by tabs:
                  kind, title, holds, section, place, text. Blank lines and
                  lines starting with '#' are skipped.
  --map KIND=TYPE,...
                  the admonition type each source kind becomes on BUILT
                  (important=info,caution=warning). Kinds not listed must
                  keep their name.
  --within SPEC   the content area, as in outline.py

What counts as a note, and its kind and title:

  published, passthrough  p.note, div.note: the kind is the class after
                          `note` (`note important` -> important), or note;
                          the title is the text of span.note__title
  Docusaurus              div.theme-admonition: the kind from the class
                          theme-admonition-KIND; the title is the heading
  Zensical                div.admonition or details: the kind is the other
                          class; the title is p.admonition-title (or summary)
  Starlight               aside.starlight-aside: the kind from the class
                          starlight-aside--KIND; the title is
                          p.starlight-aside__title
  Antora                  div.admonitionblock: the kind is the other class;
                          the title is div.title if the block has one, else
                          the title attribute of the icon (the label the
                          default UI shows)

The text is the note's text without its title, with white space collapsed,
typographic quotes made straight (the book's SmartyPants curls them),
zero-width spaces removed, and the tools' copy-button labels left out.
Titles are compared without regard to case: the tools show some titles in
capitals through CSS while the HTML holds them in lower case.
"""
import re, sys
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
SKIP_TAGS = {'nav', 'script', 'style', 'template', 'button'}
DEFAULT_WITHIN = ['main#js-content', 'article.doc', 'article.md-content__inner', 'div.theme-doc-markdown', 'main']
HIDDEN = {'headerlink', 'hash-link', 'anchor', 'sl-anchor-link', 'sr-only'}
BLOCK = {'p', 'div', 'li', 'ul', 'ol', 'pre', 'br', 'td', 'th', 'tr', 'table', 'blockquote', 'section'}


def spec_match(spec, tag, attrs):
    m = re.fullmatch(r'([a-z0-9]+)(?:#([\w-]+)|\.([\w-]+))?', spec)
    t, i, c = m.groups()
    return tag == t and (not i or attrs.get('id') == i) and (not c or c in (attrs.get('class') or '').split())


def note_kind(tag, attrs):
    """(kind, tool) when the element opens a note, else None."""
    cls = (attrs.get('class') or '').split()
    if tag in ('p', 'div') and 'note' in cls and not {'admonition', 'admonitionblock'} & set(cls):
        rest = [c for c in cls if c != 'note']
        return (' '.join(rest) or 'note', 'html')
    if tag == 'div' and 'theme-admonition' in cls:
        k = [c[len('theme-admonition-'):] for c in cls if c.startswith('theme-admonition-')]
        return (k[0] if k else '?', 'docusaurus')
    if tag in ('div', 'details') and ('admonition' in cls or tag == 'details'):
        rest = [c for c in cls if c not in ('admonition',)]
        return (rest[0] if rest else 'note', 'material')
    if tag == 'aside' and 'starlight-aside' in cls:
        k = [c[len('starlight-aside--'):] for c in cls if c.startswith('starlight-aside--')]
        return (k[0] if k else '?', 'starlight')
    if tag == 'div' and 'admonitionblock' in cls:
        rest = [c for c in cls if c != 'admonitionblock']
        return (rest[0] if rest else '?', 'antora')
    return None


def is_title(tool, tag, attrs):
    cls = (attrs.get('class') or '').split()
    if tool == 'html':
        return 'note__title' in cls
    if tool == 'docusaurus':
        return any(c.startswith('admonitionHeading') for c in cls)
    if tool == 'material':
        return 'admonition-title' in cls or tag == 'summary'
    if tool == 'starlight':
        return 'starlight-aside__title' in cls
    if tool == 'antora':
        return 'title' in cls
    return False


class Notes(HTMLParser):
    def __init__(self, within):
        super().__init__(convert_charrefs=True)
        self.within, self.stack, self.region, self.done = within, [], None, False
        self.skip = None
        self.notes, self.cur, self.cur_depth = [], None, None
        self.title_depth, self.hide = None, None
        self.heading, self.h_depth, self.h_text = '', None, ''
        self.li = 0
        self.td = 0

    def handle_starttag(self, tag, attrs):
        if self.done:
            return
        attrs = dict(attrs)
        if tag not in VOID:
            self.stack.append((tag, attrs))
        depth = len(self.stack)
        if self.region is None:
            if spec_match(self.within, tag, attrs):
                self.region = depth
            return
        if tag in VOID:
            if self.cur is not None and tag == 'img':
                self.cur['holds']['image'] += 1
            if self.cur is not None and tag == 'br':
                self.cur['text'] += ' '
            return
        if self.skip is None and (tag in SKIP_TAGS or (tag == 'aside' and 'starlight-aside' not in (attrs.get('class') or ''))):
            self.skip = depth
        if self.skip is not None:
            return
        cls = set((attrs.get('class') or '').split())
        if re.fullmatch(r'h[1-6]', tag) and self.cur is None:
            self.h_depth, self.h_text = depth, ''
        if self.cur is None:
            k = note_kind(tag, attrs)
            if k:
                place = 'table' if self.td else 'list' if self.li else 'body'
                self.cur = {'kind': k[0], 'tool': k[1], 'title': '', 'text': '', 'section': self.heading,
                            'place': place, 'holds': {'list': 0, 'code': 0, 'pre': 0, 'link': 0, 'image': 0}}
                self.cur_depth = depth
                if k[1] == 'antora':
                    self.cur['icon'] = ''
                return
        else:
            if self.hide is None and (HIDDEN & cls or 'copyButton' in ' '.join(cls) or 'clean-btn' in cls):
                self.hide = depth
            if self.title_depth is None and is_title(self.cur['tool'], tag, attrs) and not self.cur['title']:
                self.title_depth = depth
            if self.cur['tool'] == 'antora' and tag == 'i' and attrs.get('title'):
                self.cur['icon'] = attrs['title']
            if tag in BLOCK:
                self.cur['text'] += ' '
            if tag == 'li':
                self.cur['holds']['list'] += 1
            elif tag == 'code' and not any(t == 'pre' for t, _ in self.stack[self.cur_depth:-1]):
                self.cur['holds']['code'] += 1
            elif tag == 'pre':
                self.cur['holds']['pre'] += 1
            elif tag == 'a' and attrs.get('href'):
                self.cur['holds']['link'] += 1
        if tag == 'li':
            self.li += 1
        if tag in ('td', 'th'):
            self.td += 1

    def handle_endtag(self, tag):
        if self.done or tag in VOID or tag not in [t for t, _ in self.stack]:
            return
        while self.stack and self.stack[-1][0] != tag:
            self._pop()
        self._pop()
        depth = len(self.stack)
        if self.region is not None and depth < self.region:
            self.done = True

    def _pop(self):
        tag, _ = self.stack.pop()
        depth = len(self.stack)
        if self.cur is not None and tag in BLOCK:
            self.cur['text'] += ' '
        if tag == 'li' and self.li:
            self.li -= 1
        if tag in ('td', 'th') and self.td:
            self.td -= 1
        if self.skip is not None and depth < self.skip:
            self.skip = None
        if self.hide is not None and depth < self.hide:
            self.hide = None
        if self.title_depth is not None and depth < self.title_depth:
            self.title_depth = None
        if self.h_depth is not None and depth < self.h_depth:
            self.heading, self.h_depth = norm(self.h_text), None
        if self.cur is not None and depth < self.cur_depth:
            c = self.cur
            c['title'] = norm(c['title']) or c.get('icon', '')
            c['text'] = norm(c['text'])
            self.notes.append(c)
            self.cur = None

    def handle_data(self, data):
        if self.skip is not None or self.region is None or self.done:
            return
        if self.h_depth is not None and self.cur is None:
            self.h_text += data
        if self.cur is None or self.hide is not None:
            return
        if self.title_depth is not None:
            self.cur['title'] += data
        else:
            self.cur['text'] += ' ' + data if self._block_gap() else data

    def _block_gap(self):
        return False


def norm(s):
    s = s.replace('​', '').replace('\xa0', ' ').replace('¶', '')
    s = s.translate(str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"'}))
    return ' '.join(s.split())


def page_notes(path, within=None):
    html = open(path, encoding='utf-8').read()
    for spec in ([within] if within else DEFAULT_WITHIN):
        p = Notes(spec)
        p.feed(html)
        if p.region is not None:
            return p.notes, spec
    sys.exit(f'{path}: no content area found')


def holds_str(h):
    return ' '.join(f'{k}={v}' for k, v in h.items() if v) or '-'


def line(n):
    return '\t'.join([n['kind'], n['title'] or '-', holds_str(n['holds']), n['section'] or '-', n['place'], n['text']])


def words(s):
    """Text compared as words: punctuation that the tools place differently
    around inline markup (a space before a period after a code span) does
    not count."""
    return re.findall(r"[\w'./:=<>@$%&*+-]+", s)


def main(argv):
    opts, args, i = {}, [], 0
    while i < len(argv):
        if argv[i] in ('--expect', '--map', '--within'):
            opts[argv[i][2:]] = argv[i + 1]; i += 2
        elif argv[i] == '--emit':
            opts['emit'] = True; i += 1
        else:
            args.append(argv[i]); i += 1
    if len(args) != 1:
        sys.exit(__doc__)
    notes, spec = page_notes(args[0], opts.get('within'))
    if 'expect' not in opts:
        if opts.get('emit'):
            print(f'# notes on {args[0]} ({spec}): kind, title, holds, section, place, text')
            for n in notes:
                print(line(n))
            return 0
        print(f'# {args[0]}: {len(notes)} notes in {spec}')
        for k, n in enumerate(notes, 1):
            print(f"{k:2}. {n['tool']}:{n['kind']}  title={n['title']!r}  holds={holds_str(n['holds'])}  place={n['place']}")
            print(f"    section: {n['section'] or '-'}")
            print(f"    text: {n['text'][:160]}")
        return 0
    want = []
    for l in open(opts['expect'], encoding='utf-8'):
        l = l.rstrip('\n')
        if l.strip() and not l.startswith('#'):
            f = l.split('\t')
            want.append({'kind': f[0], 'title': f[1], 'holds': f[2], 'section': f[3], 'place': f[4], 'text': f[5]})
    kmap = dict(x.split('=') for x in opts['map'].split(',')) if opts.get('map') else {}
    status = 0
    if len(notes) != len(want):
        status = 1
        print(f'FAIL  count: expected {len(want)} notes, found {len(notes)}')
    else:
        print(f'ok    count: {len(want)} notes')
    for k in range(max(len(notes), len(want))):
        if k >= len(notes):
            print(f"FAIL  note {k + 1}: missing ({want[k]['kind']}: {want[k]['text'][:60]})"); continue
        if k >= len(want):
            print(f"FAIL  note {k + 1}: extra ({notes[k]['kind']}: {notes[k]['text'][:60]})"); continue
        n, w = notes[k], want[k]
        bad = []
        exp_kind = kmap.get(w['kind'], w['kind'])
        if n['kind'] != exp_kind:
            bad.append(f"kind {n['kind']!r}, expected {exp_kind!r}")
        if n['title'].casefold() != (w['title'] if w['title'] != '-' else '').casefold():
            bad.append(f"title {n['title']!r}, expected {w['title']!r}")
        if holds_str(n['holds']) != w['holds']:
            bad.append(f"holds {holds_str(n['holds'])}, expected {w['holds']}")
        if (n['section'] or '-') != w['section']:
            bad.append(f"section {n['section']!r}, expected {w['section']!r}")
        if n['place'] != w['place']:
            bad.append(f"place {n['place']}, expected {w['place']}")
        if words(n['text']) != words(w['text']):
            a, b = words(w['text']), words(n['text'])
            j = next((j for j in range(min(len(a), len(b))) if a[j] != b[j]), min(len(a), len(b)))
            bad.append(f"text differs at word {j + 1}: expected {' '.join(a[j:j + 6])!r}, found {' '.join(b[j:j + 6])!r}")
        if bad:
            status = 1
            print(f"FAIL  note {k + 1} ({w['kind']}, {n['tool']}:{n['kind']}): " + '; '.join(bad))
        else:
            print(f"ok    note {k + 1}: {w['kind']} -> {n['kind']}, title {n['title']!r}, {len(words(n['text']))} words, {holds_str(n['holds'])}, {n['place']}")
    return status


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
