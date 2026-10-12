"""Links on a built page: where each one leads, in what form, and whether
its page and anchor exist in the built site.

Usage:
  python3 -I links.py PAGE.html [--root SITE] [--expect FILE] [--host HOST]

  PAGE.html      a built page
  --root SITE    the folder that holds the built site, served at the root
                 of HOST (default: the folder above PAGE.html's path, which
                 is right only for a page at the top)
  --expect FILE  the page's links file (intent/<page>.links): every link it
                 lists must be on the page, in order, and resolve as it says
  --host HOST    the host the site stands for (default docs.cloudfoundry.org);
                 absolute links to it are resolved in SITE

Prints one line per link in the page's content area:

  link  TEXT  ->  HREF  [FORM]  TARGET#ANCHOR  STATUS

FORM is how the href is written in the built page: in-page (#id),
page-relative or root-relative, each with `.html`, a folder (`/`) or no
extension; absolute (to HOST); external. TARGET is the page the href
reaches, as a key: its path in SITE without `.html` and without a final
`/index` (so `concepts/x.html` and `concepts/x/index.html` are both
`concepts/x`). STATUS is ok, `no page`, `no anchor`, `redirect page` (the
file found is a page that only redirects, with a meta refresh; it is not
counted as resolving, since the reader needs one more hop, and the anchor
reaches the target only if the redirect page's script passes it on) or
`external`.

How an href is resolved, as a browser and a static host do: it is joined to
the page's own URL (its path in SITE; `x/index.html` is served as `x/`).
The path resolves to a file of SITE when the file exists; a path ending in
`/` to its `index.html`; a path with no extension to `PATH.html` (GitHub
Pages serves `/x` from `x.html`); any other path that is a folder to
`PATH/index.html` (the host adds the slash); each such fallback is named in
the line. The fragment must be an
`id`, or the `name` of an `<a>`, on the target page; an empty fragment and
`#top` always resolve.

With --expect, each line of FILE is

  TEXT <TAB> TARGET <TAB> ANCHOR <TAB> EXPECT

where EXPECT is `resolves`, `no anchor` (a link already broken in the book,
kept as written) or `external`. Lines are matched to the page's links by
their text (white space collapsed), in order. The exit status is 1 when a
listed link is missing from the page, resolves differently, or when the page
has a link the file does not list.

The content area is the first of: div.sl-markdown-content (Starlight),
article.doc (Antora), article.md-content__inner (Zensical),
div.theme-doc-markdown (Docusaurus), main#js-content (docs.cloudfoundry.org).
Links inside nav, aside and the published page's quick links, permalink
icons next to headings, and edit buttons are left out.
"""
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote

WITHIN = [('div', 'class', 'sl-markdown-content'), ('article', 'class', 'doc'),
          ('article', 'class', 'md-content__inner'), ('div', 'class', 'theme-doc-markdown'),
          ('main', 'id', 'js-content')]
SKIP_TAGS = {'nav', 'aside', 'script', 'style', 'template'}
SKIP_CLASSES = {'quick-links', 'js-quick-links', 'headerlink', 'hash-link', 'anchor', 'sl-anchor-link',
                'md-content__button', 'edit-link', 'theme-edit-this-page'}
SKIP_IDS = {'repo-link'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}


def args():
    a = sys.argv[1:]
    if not a or a[0].startswith('-'):
        sys.exit(__doc__)
    opts = {'page': a[0], 'root': None, 'expect': None, 'host': 'docs.cloudfoundry.org'}
    i = 1
    while i < len(a):
        if a[i] in ('--root', '--expect', '--host') and i + 1 < len(a):
            opts[a[i][2:]] = a[i + 1]; i += 2
        else:
            sys.exit(f'unknown argument: {a[i]}\n\n{__doc__}')
    return opts


class Links(HTMLParser):
    """Links in the content area, with their text."""

    def __init__(self, spec):
        super().__init__(convert_charrefs=True)
        self.spec = spec
        self.stack = []          # open tags
        self.region = None       # depth of the content area
        self.skip = None         # depth of a skipped element
        self.cur = None          # link being read: [href, text parts]
        self.cur_depth = None
        self.links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in VOID:
            return
        self.stack.append(tag)
        d = len(self.stack)
        classes = set((a.get('class') or '').split())
        if self.region == -1:
            return
        if self.region is None:
            t, key, val = self.spec
            if tag == t and ((key == 'class' and val in classes) or (key == 'id' and a.get('id') == val)):
                self.region = d
            return
        if self.skip is None and (tag in SKIP_TAGS or classes & SKIP_CLASSES or a.get('id') in SKIP_IDS):
            self.skip = d
        if self.skip is None and tag == 'a' and a.get('href') is not None and self.cur is None:
            self.cur, self.cur_depth = [a['href'], []], d

    def handle_endtag(self, tag):
        if tag in VOID or tag not in self.stack:
            return
        while self.stack:
            d = len(self.stack)
            t = self.stack.pop()
            if self.cur is not None and d == self.cur_depth:
                self.links.append((self.cur[0], ' '.join(''.join(self.cur[1]).split())))
                self.cur = None
            if self.skip is not None and d == self.skip:
                self.skip = None
            if self.region is not None and d == self.region:
                self.region = -1          # done: only the first content area
            if t == tag:
                break

    def handle_data(self, data):
        if self.cur is not None and self.skip is None:
            self.cur[1].append(data)


class Ids(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'a' and a.get('name'):
            self.ids.add(a['name'])


def read(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()


def content_links(html):
    for spec in WITHIN:
        p = Links(spec)
        p.feed(html)
        if p.region is not None:
            return p.links
    return None


_ids = {}


def ids_of(path):
    if path not in _ids:
        p = Ids(); p.feed(read(path)); _ids[path] = p.ids
    return _ids[path]


def key_of(rel):
    k = re.sub(r'\.html$', '', rel)
    k = re.sub(r'(^|/)index$', '', k)
    k = re.sub(r'\.html$', '', k)          # a redirect page at <path>.html/index.html
    return k or 'index'


REFRESH = re.compile(r'<meta[^>]+http-equiv=["\']?refresh["\']?[^>]*content=["\']\s*\d+\s*;\s*url=([^"\'>]+)', re.I)


def refresh_of(path):
    m = REFRESH.search(read(path)[:4000])
    return m.group(1).strip() if m else None


def page_url(root, page):
    rel = os.path.relpath(os.path.abspath(page), os.path.abspath(root)).replace(os.sep, '/')
    if rel.endswith('/index.html') or rel == 'index.html':
        return '/' + rel[:-len('index.html')]
    return '/' + rel


def resolve(root, host, base, href):
    """(form, key, anchor, status, note) for one href."""
    if href.startswith('#'):
        form = 'in-page'
    s = urlsplit(href)
    if s.scheme and s.scheme not in ('http', 'https'):
        return s.scheme, '', '', 'external', ''
    full = urlsplit(urljoin(f'https://{host}{base}', href))
    if full.netloc != host:
        return 'external', '', '', 'external', ''
    if not href.startswith('#'):
        where = 'absolute' if s.netloc else ('root-relative' if href.startswith('/') else 'page-relative')
        path = s.path
        ext = '.html' if path.endswith('.html') else ('folder' if path.endswith('/') or path == '' else
                                                     ('no extension' if '.' not in path.rsplit('/', 1)[-1] else 'other'))
        form = f'{where}, {ext}'
    path = unquote(full.path).lstrip('/')
    note, target = '', None
    cand = [(path + 'index.html' if path.endswith('/') or path == '' else path, '')]
    if not path.endswith('/') and '.' not in path.rsplit('/', 1)[-1]:
        cand += [(path + '.html', 'served from PATH.html')]
    if not path.endswith('/') and path:
        cand += [(path + '/index.html', 'served from PATH/index.html')]
    for c, n in cand:
        if c and os.path.isfile(os.path.join(root, c)):
            target, note = c, n
            break
    if target is None:
        return form, key_of(path), full.fragment, 'no page', ''
    frag = unquote(full.fragment)
    status = 'ok'
    if target.endswith('.html'):
        r = refresh_of(os.path.join(root, target))
        if r is not None:
            return form, key_of(target), frag, 'redirect page', f'refresh to {r}'
    if frag and frag != 'top' and target.endswith('.html') and frag not in ids_of(os.path.join(root, target)):
        status = 'no anchor'
    return form, key_of(target), frag, status, note


def load_expect(path):
    rows = []
    for line in read(path).split('\n'):
        if not line.strip() or line.startswith('#'):
            continue
        f = line.split('\t')
        if len(f) != 4:
            sys.exit(f'{path}: expected 4 tab-separated fields: {line!r}')
        rows.append(dict(text=' '.join(f[0].split()), target=f[1], anchor=f[2], expect=f[3]))
    return rows


def main():
    o = args()
    page = o['page']
    root = o['root'] or os.path.dirname(page)
    links = content_links(read(page))
    if links is None:
        print(f'FAIL  {page}: no content area found')
        return 1
    base = page_url(root, page)
    results = []
    for href, text in links:
        form, key, anchor, status, note = resolve(root, o['host'], base, href)
        results.append(dict(text=text, href=href, form=form, key=key, anchor=anchor, status=status, note=note))
        tgt = f'{key}#{anchor}' if anchor else key
        print(f'link  {text}  ->  {href}  [{form}]  {tgt if status != "external" else ""}  {status}'
              + (f' ({note})' if note else ''))
    forms = {}
    for r in results:
        forms[r['form']] = forms.get(r['form'], 0) + 1
    print('forms: ' + ', '.join(f'{k} {v}' for k, v in sorted(forms.items())))
    if not o['expect']:
        return 0
    fail = 0
    pending = list(results)
    for e in load_expect(o['expect']):
        i = next((j for j, r in enumerate(pending) if r['text'] == e['text']), None)
        if i is None:
            print(f'FAIL  missing link: {e["text"]!r}')
            fail = 1
            continue
        r = pending.pop(i)
        if e['expect'] == 'external':
            ok = r['status'] == 'external'
        elif e['expect'] == 'resolves':
            ok = r['status'] == 'ok' and r['key'] == e['target'] and r['anchor'] == e['anchor']
        elif e['expect'] == 'no anchor':
            ok = r['status'] == 'no anchor' and r['key'] == e['target'] and r['anchor'] == e['anchor']
        else:
            sys.exit(f'unknown expectation: {e["expect"]}')
        if not ok:
            want = f'{e["target"]}#{e["anchor"]}' if e['anchor'] else e['target']
            got = f'{r["key"]}#{r["anchor"]}' if r['anchor'] else r['key']
            print(f'FAIL  {e["text"]!r}: expected {e["expect"]} {want if e["expect"] != "external" else ""}, '
                  f'got {r["status"]} {got if r["status"] != "external" else ""} ({r["href"]})')
            fail = 1
    for r in pending:
        print(f'FAIL  link not in the links file: {r["text"]!r} ({r["href"]})')
        fail = 1
    n = len(load_expect(o['expect']))
    print(('FAIL' if fail else 'PASS') + f'  {page}: {n} links expected')
    return fail


if __name__ == '__main__':
    sys.exit(main())
