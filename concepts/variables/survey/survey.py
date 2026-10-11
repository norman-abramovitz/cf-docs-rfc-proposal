"""Inventory every variable and every other ERB expression in the cloned
documentation repositories, and every key of the book's variables file.

Usage:
  python3 -I survey.py REPOS_DIR SHAS USES.csv VALUES.csv

REPOS_DIR holds one clone per line of SHAS, named as in SHAS. SHAS has
lines `<name> <commit> <date>`; the commit goes into each row's GitHub
link. Reads files only; runs nothing from the clones.

USES.csv has one row per expression a page or layout writes:
  - every ERB tag (<%= ... %>, <% ... %>, <%# ... %>) in the book's
    repositories and in docs-book-cloudfoundry's own pages and layouts;
  - in docs-bosh, the ERB tags its pages show as content (BOSH job
    templates);
  - in docs-dotnet-core-tutorial, every {{ name }} expression (MkDocs with
    the markdownextradata plugin).
Each row says what the expression is (a variable, a helper, a build-time
value, a partial, a comment), whether the variable is defined, what its
value holds, and where the expression sits: its place (front matter, code
block, heading, link URL, ...) and the elements around it (table, note,
list, HTML block).

VALUES.csv has one row per key in docs-book-cloudfoundry's
config/template_variables.yml (and in docs-dotnet-core-tutorial's
mkdocs.yml `extra:`), with what the value holds and how often pages use it.

The places are found by reading the source, not by building it; the rules
are in place_of() below. Indented code blocks are found by indentation
alone, the way CommonMark finds them; the book's Markdown processor
(Redcarpet) may differ at the edges.
"""
import csv, os, posixpath, re, sys
from collections import Counter, defaultdict

if len(sys.argv) != 5:
    sys.exit(__doc__)
REPOS, SHAS, USES, VALUES = sys.argv[1:]
EXTS = ('.md', '.erb', '.html', '.haml', '.markdown', '.mdx', '.adoc')
sha = dict(l.split()[:2] for l in open(SHAS) if l.strip())
BOOK = 'docs-book-cloudfoundry'
TV = 'config/template_variables.yml'
SECTIONS = {}  # filled from the book's config.yml below
REDIRECTS = set()  # plain r301 sources in the book's redirects.rb

ERB = re.compile(r'<%(?!%)([=#-]?)(.*?)-?%>', re.S)
JINJA = re.compile(r'\{\{\s*([A-Za-z_][\w.]*)\s*\}\}')
FENCE = re.compile(r'^\s*(```|~~~)')
LIST_ITEM = re.compile(r'^(\s*)([*+-]|\d+\.)(\s+)\S')
SEPARATOR = re.compile(r'^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$')
BLOCK_TAGS = ('table', 'td', 'th', 'li', 'ul', 'ol', 'dl', 'dd', 'dt', 'p', 'div', 'blockquote', 'pre')


def url(repo, rel, line):
    return f'https://github.com/cloudfoundry/{repo}/blob/{sha[repo]}/{rel}#L{line}'


# ---------------------------------------------------------------- values

def unquote_double(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            n = s[i + 1]
            out.append({'n': '\n', 't': '\t', '"': '"', '\\': '\\', '/': '/'}.get(n, '\\' + n))
            i += 2
        else:
            out.append(c); i += 1
    return ''.join(out)


def parse_variables(path):
    """The book's variables file: a mapping under `template_variables:` whose
    keys sit at two spaces. Values are plain, quoted, or block scalars (|-).
    Returns [(key, line, raw_value_or_None, style)]; checked against a full
    YAML parser (README, How to rerun)."""
    lines = open(path, encoding='utf-8').read().split('\n')
    out, i = [], 0
    key = re.compile(r'^  (\S[^:]*?):(?:[ \t]+(.*?))?[ \t]*$')
    while i < len(lines):
        l = lines[i]
        m = key.match(l)
        if not m:
            i += 1; continue
        k, v = m.group(1), m.group(2)
        start = i + 1
        i += 1
        if v is None or v == '':
            out.append((k, start, None, 'empty')); continue
        if v[0] in '|>':
            body = []
            while i < len(lines) and (not lines[i].strip() or len(lines[i]) - len(lines[i].lstrip()) > 2):
                body.append(lines[i]); i += 1
            while body and not body[-1].strip():
                body.pop()
            ind = min(len(b) - len(b.lstrip()) for b in body if b.strip())
            text = '\n'.join(b[ind:] for b in body)
            out.append((k, start, text if v.endswith('-') else text + '\n', 'block')); continue
        if v[0] == '"':
            out.append((k, start, unquote_double(v[1:v.rindex('"')]), 'double')); continue
        if v[0] == "'":
            out.append((k, start, v[1:v.rindex("'")].replace("''", "'"), 'single')); continue
        # plain scalar, folded onto further lines indented more than the key
        parts = [v]
        while i < len(lines) and lines[i].strip() and len(lines[i]) - len(lines[i].lstrip()) > 2:
            parts.append(lines[i].strip()); i += 1
        out.append((k, start, ' '.join(parts), 'plain'))
    return out


def html_elements(v):
    return sorted({t.lower() for t in re.findall(r'<([a-zA-Z][a-zA-Z0-9]*)\b', v or '')})


def markdown_features(v):
    v = v or ''
    t = []
    if re.search(r'\[[^\]\n]+\]\([^)\n]+\)', v): t.append('link')
    if re.search(r'(?<!`)`[^`\n]+`', v): t.append('code')
    if re.search(r'\*\*[^*\n]+\*\*', v): t.append('bold')
    if re.search(r'(?<![\w*])_[^_\n]+_(?!\w)', v) or re.search(r'(?<![\w*])\*[^*\s][^*\n]*\*(?!\w)', v): t.append('emphasis')
    if re.search(r'^\s*([*+-]|\d+\.)\s+\S', v, re.M): t.append('list')
    if re.search(r'^\s*(```|~~~)', v, re.M): t.append('fence')
    if '|' in v and not re.search(r'<[^>]*\|', v): t.append('pipe')
    if re.search(r'\\[_*\[\]]', v): t.append('escape')
    return t


def value_kind(v):
    """One word for what a value is."""
    if v is None or v == '':
        return 'empty'
    if '<%' in v:
        return 'erb'
    h, md = html_elements(v), markdown_features(v)
    if h and md:
        return 'html+markdown'
    if h:
        return 'html'
    if md:
        return 'markdown'
    if re.fullmatch(r'https?://\S+', v):
        return 'url'
    if re.fullmatch(r'\.{0,2}/?[\w./#-]+', v) and ('/' in v or v.startswith('_') or re.fullmatch(r'[a-z0-9_]+_oss|oss_\w+|_\w+', v)):
        return 'path'
    return 'text'


def relative_links(v):
    """Link targets in a value that are relative to the page that uses it."""
    targets = re.findall(r'\]\(([^)\s]+)\)', v or '') + re.findall(r'href\s*=\s*["\']([^"\']+)', v or '')
    return [t for t in targets if not re.match(r'(https?:|mailto:|/|#)', t)]


def book_sections(path):
    """Repository name -> published directory, from the book's config.yml."""
    out, repo = {}, None
    for l in open(path, encoding='utf-8'):
        m = re.match(r'^-\s+repository:\s*$', l)
        if m:
            repo = None
        m = re.match(r'^\s{4}name:\s*cloudfoundry/(\S+)', l)
        if m and l.startswith('    name'):
            repo = m.group(1)
        m = re.match(r'^\s{2}directory:\s*(\S+)', l)
        if m and repo:
            out[repo] = m.group(1)
    return out


def resolves(repo, rel, target):
    """Whether a relative link in a value, used on the page repo/rel, reaches
    a page of the book: the link is resolved against the page's published
    directory and the target looked up in the repository that the book's
    config.yml publishes there."""
    page_dir = posixpath.join('/', SECTIONS[repo], posixpath.dirname(rel))
    path = posixpath.normpath(posixpath.join(page_dir, target.split('#')[0]))
    parts = path.strip('/').split('/', 1)
    if path in REDIRECTS:
        return 'redirect'
    to = {d: r for r, d in SECTIONS.items()}.get(parts[0])
    if not to or len(parts) < 2:
        return False
    stem = re.sub(r'\.html$', '', parts[1])
    root = os.path.join(REPOS, to)
    return any(os.path.exists(os.path.join(root, stem + ext)) for ext in ('.html.md.erb', '.html.md', '.html.erb', '.html'))


# ---------------------------------------------------------------- places

def fenced_lines(lines):
    out, fence = set(), None
    for i, l in enumerate(lines):
        m = FENCE.match(l)
        if fence is None and m:
            fence = m.group(1); out.add(i)
        elif fence is not None:
            out.add(i)
            if l.strip().startswith(fence):
                fence = None
    return out


def list_content_col(lines, i):
    """Content column of the list item that line i belongs to, or None.
    Walks up past continuation lines (indented, or lazy at the margin) to
    the item; a line at the margin after a blank line ends the list."""
    l = lines[i]
    m = LIST_ITEM.match(l)
    if m:
        return len(m.group(1)) + len(m.group(2)) + len(m.group(3))
    ind = len(l) - len(l.lstrip())
    if ind == 0:
        return None
    for j in range(i - 1, -1, -1):
        p = lines[j]
        if not p.strip():
            continue
        m = LIST_ITEM.match(p)
        k = len(p) - len(p.lstrip())
        if m and k < ind:
            return len(m.group(1)) + len(m.group(2)) + len(m.group(3))
        if k == 0 and not m and (j == 0 or not lines[j - 1].strip()):
            return None
    return None


def indented_code_lines(lines, fenced, html_open):
    """Lines of indented code blocks: indented four columns past the
    enclosing list item's content (or past the margin outside lists),
    after a blank line or another such line, outside fences and HTML."""
    out = set()
    for i, l in enumerate(lines):
        if i in fenced or not l.strip():
            continue
        ind = len(l.expandtabs(4)) - len(l.expandtabs(4).lstrip())
        if ind < 4 or html_open(i):
            continue
        if LIST_ITEM.match(l) and ind < 4:
            continue
        base = list_content_col(lines, i) if ind else None
        need = (base or 0) + 4
        if ind < need:
            continue
        prev = i - 1
        while prev >= 0 and not lines[prev].strip() and (prev - 1) in out:
            prev -= 1
        if prev < 0 or not lines[prev].strip() or prev in out:
            out.add(i)
    return out


def blank_erb(text):
    """The text with every ERB tag replaced by x's of the same length, so
    that its %> does not end an HTML tag and its brackets are not read."""
    return ERB.sub(lambda m: re.sub(r'[^\n]', 'x', m.group(0)), text)


IMPLIED = {  # the tags that end an element whose end tag may be left out
    'td': r'<t[dh]\b|</?tr\b|</?table\b|</t[dh]\s*>',
    'th': r'<t[dh]\b|</?tr\b|</?table\b|</t[dh]\s*>',
    'li': r'<li\b|</li\s*>|</?[uo]l\b',
}


def open_element(flat, pos, tag):
    """Start of the innermost <tag> open at pos (not closed before it). A
    table cell or list item ends where HTML ends it without an end tag: at
    the next cell, row or item."""
    if tag in IMPLIED:
        last = None
        for m in re.finditer(IMPLIED[tag], flat[:pos], re.I):
            last = m
        if last and re.match(r'<%s\b' % tag, last.group(0), re.I):
            return last.start()
        return None
    opens = [(m.start(), 1) for m in re.finditer(r'<%s\b[^>]*>' % tag, flat[:pos], re.I)]
    closes = [(m.start(), -1) for m in re.finditer(r'</%s\s*>' % tag, flat[:pos], re.I)]
    stack = []
    for p, d in sorted(opens + closes):
        if d == 1:
            stack.append(p)
        elif stack:
            stack.pop()
    return stack[-1] if stack else None


def open_inline(flat, pos, tag):
    """True when an inline <tag> (a, code, h1-h6) is open at pos. Only the
    text since the last blank line or closed block (</td>, </th>, </li>,
    </p>) is read, because the browser ends an inline element there even
    when the source never closes it."""
    seg_start = 0
    for m in re.finditer(r'\n[ \t]*\n|</(td|th|li|p)\s*>', flat[:pos], re.I):
        seg_start = m.end()
    seg = flat[seg_start:pos]
    opens = len(re.findall(r'<%s\b[^>]*>' % tag, seg, re.I))
    if tag == 'a':
        opens -= len(re.findall(r'<a\b[^>]*/>', seg, re.I))
    return opens > len(re.findall(r'</%s\s*>' % tag, seg, re.I))


def note_open(flat, pos):
    """True when pos sits inside an HTML note (<p|div class="note ...">)."""
    for m in re.finditer(r'<(p|div)\b[^>]*class\s*=\s*["\'][^"\']*\bnote\b[^"\']*["\'][^>]*>', flat[:pos], re.I):
        tag = m.group(1).lower()
        between = flat[m.end():pos]
        if tag == 'p':
            if not re.search(r'</p\s*>|\n[ \t]*\n', between, re.I):
                return True
        else:
            d = 1 + len(re.findall(r'<div\b', between, re.I)) - len(re.findall(r'</div\s*>', between, re.I))
            if d > 0:
                return True
    return False


def place_of(text, flat, lines, starts, fm_end, fenced, indented, pos, length, tag):
    """(place, detail) of the expression at pos."""
    li = line_of(starts, pos)
    line = lines[li]
    col = pos - starts[li]
    fline = flat[starts[li]:starts[li] + len(line)]
    if pos < fm_end:
        key = re.match(r'\s*([\w-]+)\s*:', line)
        return 'front-matter', key.group(1) if key else ''
    if tag in ('', '-'):
        return 'erb-code', ''
    if tag == '#':
        return 'erb-comment', ''
    if li in fenced:
        return 'fenced-code', ''
    if li in indented:
        return 'indented-code', ''
    if open_element(flat, pos, 'pre') is not None:
        return 'pre', ''
    # inside an HTML tag: an attribute value
    for m in re.finditer(r'<[a-zA-Z][^<>]*>', fline):
        if m.start() < col < m.end():
            for a in re.finditer(r'([\w:-]+)\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)', m.group(0)):
                if m.start() + a.start(2) <= col < m.start() + a.end(2):
                    name = a.group(1).lower()
                    return ('link-url', 'html ' + name) if name in ('href', 'src') else ('html-attribute', name)
            return 'html-attribute', 'tag'
    if open_inline(flat, pos, 'code'):
        return 'code-span', 'html'
    ticks = [m.start() for m in re.finditer(r'(?<!\\)`', fline[:col])]
    if len(ticks) % 2 == 1:
        return 'code-span', 'markdown'
    # Markdown links: [text](url) and reference definitions
    for m in re.finditer(r'(!?)\[([^\]\n]*)\]\(([^)\n]*)\)', fline):
        if m.start(3) <= col < m.end(3):
            return 'link-url', 'markdown image' if m.group(1) else 'markdown'
        if m.start(2) <= col < m.end(2):
            return 'link-text', 'markdown'
    if re.match(r'\s*\[[^\]]+\]:\s*\S', fline) and col > fline.index(']'):
        return 'link-url', 'markdown reference'
    if re.match(r'\s*#{1,6}(\s|\S)', line) and not re.match(r'\s*#{1,6}[^#\s]*\(', line):
        return 'heading', 'markdown' + (' with <a id>' if re.search(r'<a\s[^>]*(id|name)\s*=', line) else '')
    for h in range(1, 7):
        if open_inline(flat, pos, 'h%d' % h):
            return 'heading', 'html'
    if open_inline(flat, pos, 'a'):
        return 'link-text', 'html'
    return 'prose', ''


def line_of(starts, pos):
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid] <= pos: lo = mid
        else: hi = mid - 1
    return lo


def containers(flat, lines, starts, pos, place):
    li = line_of(starts, pos)
    # Markdown pipe table: the paragraph around the line has a separator row
    a = li
    while a > 0 and lines[a - 1].strip():
        a -= 1
    b = li
    while b + 1 < len(lines) and lines[b + 1].strip():
        b += 1
    md_table = '|' in lines[li] and any(SEPARATOR.match(lines[k]) for k in range(a, b + 1))
    td = open_element(flat, pos, 'td') is not None or open_element(flat, pos, 'th') is not None
    table = 'markdown' if md_table else 'html' if td else 'no'
    note = 'yes' if note_open(flat, pos) else 'no'
    in_list = 'html' if open_element(flat, pos, 'li') is not None else 'markdown' if list_content_col(lines, li) is not None else 'no'
    inner = None
    for t in BLOCK_TAGS:
        s = open_element(flat, pos, t)
        if s is not None and (inner is None or s > inner[0]):
            inner = (s, t)
    return table, note, in_list, inner[1] if inner else 'no'


# ---------------------------------------------------------------- scan

SECTIONS.update(book_sections(os.path.join(REPOS, BOOK, 'config.yml')))
REDIRECTS.update(re.findall(r"^r30[12]\s+'(/[^']+)'", open(os.path.join(REPOS, BOOK, 'redirects.rb'), encoding='utf-8').read(), re.M))
defs = {}            # name -> (line, value, style)
dup = []
tv_path = os.path.join(REPOS, BOOK, TV)
for k, ln, v, style in parse_variables(tv_path):
    if k in defs:
        dup.append((k, defs[k][0], ln))
    defs[k] = (ln, v, style)

mk_defs = {}         # docs-dotnet-core-tutorial's mkdocs.yml extra:
mk = os.path.join(REPOS, 'docs-dotnet-core-tutorial', 'mkdocs.yml')
if os.path.exists(mk):
    in_extra = False
    for n, l in enumerate(open(mk, encoding='utf-8'), 1):
        if re.match(r'^extra:\s*$', l):
            in_extra = True; continue
        if in_extra and re.match(r'^\S', l):
            in_extra = False
        m = re.match(r'^  (\w+):\s*(.*?)\s*$', l)
        if in_extra and m:
            mk_defs[m.group(1)] = (n, m.group(2), 'plain')

HELPERS = re.compile(r'^\s*(?:@)?([A-Za-z_][\w]*(?:\.[A-Za-z_]\w*)?)')
rows = []


def add_row(**kw):
    base = dict(repo='', file='', line='', url='', site='', syntax='', expr='', kind='', name='',
                method='', defined='', value_kind='', place='', detail='', table='', note='', list='',
                html='', partial_file='', archive='', erb_processed='', links_resolve='')
    base.update(kw)
    rows.append(base)


def classify(expr, repo):
    """(kind, name, method) of an ERB expression."""
    e = ' '.join(expr.split())
    m = re.search(r'\bvars\.(\w+)((?:\.\w+|\s*[+]|\s*\[)?)', e)
    if repo == 'docs-bosh':
        return 'bosh-template', (HELPERS.match(e).group(1) if HELPERS.match(e) else e[:20]), ''
    if m:
        rest = e[m.end(1):].strip()
        method = ''
        if re.match(r'\.\w+', rest):
            method = rest.split()[0]
        elif e.strip() != 'vars.' + m.group(1):
            method = 'expression'
        return 'variable', m.group(1), method
    if re.search(r'\bTime\.now|\bDate\.today', e):
        return 'build-time', 'Time.now.year' if 'year' in e else 'Time.now', ''
    if re.match(r'partial\b', e):
        n = re.search(r'partial\s*\(?\s*["\']([^"\']+)', e)
        return 'partial', n.group(1) if n else e, ''
    if re.match(r'(end|else|end\.else.*)$', e):
        return 'control', e, ''
    h = HELPERS.match(e)
    return 'helper', h.group(1) if h else e[:30], ''


for repo in sorted(sha):
    root = os.path.join(REPOS, repo)
    if not os.path.isdir(root):
        continue
    for dp, dn, fn in os.walk(root, followlinks=True):
        dn[:] = sorted(d for d in dn if d not in ('.git', 'node_modules', 'vendor'))
        for f in sorted(fn):
            if not f.endswith(EXTS):
                continue
            if dp == root and f.endswith(('.md', '.markdown')):
                continue  # root notes and READMEs: no site publishes them
            full = os.path.join(dp, f); rel = os.path.relpath(full, root)
            text = open(full, encoding='utf-8', errors='replace').read()
            jinja = repo == 'docs-dotnet-core-tutorial'
            pat = JINJA if jinja else ERB
            if not pat.search(text):
                continue
            lines = text.split('\n')
            starts = [0]
            for l in lines:
                starts.append(starts[-1] + len(l) + 1)
            fm_end = 0
            fm = re.match(r'---\n.*?\n---\n', text, re.S)
            if fm:
                fm_end = fm.end()
            flat = blank_erb(text) if not jinja else JINJA.sub(lambda m: 'x' * len(m.group(0)), text)
            fenced = fenced_lines(lines)
            html_block = lambda i: any(open_element(flat, starts[i], t) is not None for t in ('table', 'pre', 'div', 'ul', 'ol', 'p'))
            indented = indented_code_lines(lines, fenced, html_block)
            for m in pat.finditer(text):
                if jinja:
                    syntax, expr = '{{ }}', m.group(1)
                    kind, name, method = 'variable', m.group(1), ''
                    tag = '='
                else:
                    tag = m.group(1)
                    syntax = {'=': '<%=', '#': '<%#', '-': '<%-', '': '<%'}[tag]
                    expr = m.group(2).strip()
                    kind, name, method = classify(expr, repo)
                    if tag == '#':
                        kind, method = 'comment', ''
                place, detail = place_of(text, flat, lines, starts, fm_end, fenced, indented,
                                         m.start(), len(m.group(0)), '=' if repo == 'docs-bosh' else tag)
                names = [name]
                if kind == 'variable' and method == 'expression':
                    names = list(dict.fromkeys(re.findall(r'\bvars\.(\w+)', expr)))
                table, note, in_list, html = containers(flat, lines, starts, m.start(), place)
                li = line_of(starts, m.start()) + 1
                d = mk_defs if jinja else defs
                site = 'mkdocs' if jinja else 'bosh.io' if repo == 'docs-bosh' else 'book-repo' if repo == BOOK else 'book'
                for name in names:
                    defined = value = links = ''
                    if kind == 'variable':
                        defined = 'yes' if name in d and d[name][1] not in (None, '') else 'empty' if name in d else 'no'
                        value = value_kind(d[name][1]) if name in d else ''
                        targets = relative_links(d[name][1]) if name in d and not jinja else []
                        if targets and f.startswith('_'):
                            links = 'in a partial'
                        elif targets and repo in SECTIONS:
                            res = {t: resolves(repo, rel, t) for t in targets}
                            bad = [t for t, ok in res.items() if not ok]
                            via = [t for t, ok in res.items() if ok == 'redirect']
                            links = 'no: ' + ' '.join(bad) if bad else 'by redirect: ' + ' '.join(via) if via else 'yes'
                    add_row(repo=repo, file=rel, line=li, url=url(repo, rel, li), site=site, syntax=syntax,
                            expr=' '.join(expr.split())[:120], kind=kind, name=name, method=method,
                            defined=defined, value_kind=value, place=place, detail=detail, table=table,
                            note=note, list=in_list, html=html,
                            partial_file='yes' if f.startswith('_') else 'no',
                            archive='yes' if '/archive/' in '/' + rel else 'no',
                            erb_processed='' if jinja or repo == 'docs-bosh' else ('yes' if f.endswith('.erb') else 'no'),
                            links_resolve=links)

with open(USES, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

# ---------------------------------------------------------------- values

pages = [r for r in rows if r['kind'] == 'variable' and r['site'] in ('book', 'book-repo')]
uses = Counter(r['name'] for r in pages)
files = defaultdict(set)
places = defaultdict(Counter)
for r in pages:
    files[r['name']].add((r['repo'], r['file']))
    places[r['name']][r['place']] += 1
vrows = []
for site, d, src_repo, src in (('book', defs, BOOK, TV), ('mkdocs', mk_defs, 'docs-dotnet-core-tutorial', 'mkdocs.yml')):
    for k, (ln, v, style) in d.items():
        if site == 'mkdocs':
            n = sum(1 for r in rows if r['site'] == 'mkdocs' and r['name'] == k)
            nf = len({r['file'] for r in rows if r['site'] == 'mkdocs' and r['name'] == k})
            pl = Counter(r['place'] for r in rows if r['site'] == 'mkdocs' and r['name'] == k)
        else:
            n, nf, pl = uses[k], len(files[k]), places[k]
        vrows.append(dict(
            site=site, name=k, line=ln, url=url(src_repo, src, ln), style=style,
            value_kind=value_kind(v), html_elements=' '.join(html_elements(v)),
            markdown=' '.join(markdown_features(v)), multiline='yes' if v and '\n' in v.rstrip('\n') else 'no',
            relative_links=' '.join(relative_links(v)), addressable='yes' if re.fullmatch(r'\w+', k) else 'no',
            uses=n, files=nf, places=' '.join(f'{p}={c}' for p, c in sorted(pl.items())),
            value=(v or '').replace('\n', '\\n')[:160]))
for k in sorted(set(r['name'] for r in pages) - set(defs)):
    vrows.append(dict(site='book', name=k, line='', url='', style='undefined', value_kind='undefined',
                      html_elements='', markdown='', multiline='', relative_links='', addressable='yes',
                      uses=uses[k], files=len(files[k]),
                      places=' '.join(f'{p}={c}' for p, c in sorted(places[k].items())), value=''))
with open(VALUES, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, list(vrows[0].keys()))
    w.writeheader()
    w.writerows(vrows)

c = Counter((r['site'], r['kind']) for r in rows)
print(f'{len(rows)} expressions')
for k in sorted(c):
    print(f'  {k[0]:12} {k[1]:14} {c[k]}')
print(f'{len(vrows)} keys and undefined names; duplicate keys: {dup or "none"}')
