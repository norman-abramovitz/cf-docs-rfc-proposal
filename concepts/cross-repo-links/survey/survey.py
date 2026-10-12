"""Inventory every link in the cloned documentation repositories and
resolve each one against a model of the book's site.

Usage:
  python3 -I survey.py REPOS_DIR SHAS LINKS.csv REDIRECTS.csv [BOOKBINDER_DIR]

REPOS_DIR holds one clone per line of SHAS, named as in SHAS. SHAS has
lines `<name> <commit> <date>`; the commit goes into each row's GitHub
link. BOOKBINDER_DIR, if given, is a checkout of pivotal-cf/bookbinder (its
`master_middleman/source` supplies the layout partials the book does not
override). Writes LINKS.csv (one row per link, per page it renders on) and
REDIRECTS.csv (one row per rule in the book's redirects.rb) and prints a
summary. Reads files only; runs nothing from the clones.

What is a link (outside fenced code blocks and inline code):
  md-inline    [text](url) and ![alt](url) (the latter: md-image)
  md-refdef    a reference definition, [name]: url
  html-a       <a href="url">, html-img for <img src="url">
  autolink     <http://...>
  bare-url     http://..., https://... or www.... in text, which the
               book's Markdown (Redcarpet, autolink: true) makes a link

Where a link is written, and which page it renders on:
  page         a page of the book; renders on itself
  partial      a partial file; renders on each page that includes it
  variable     a value in config/template_variables.yml; renders on each
               page that uses the variable
  subnav       the book's subnav; renders on every page
  layout       a layout file (book or Bookbinder); renders on every page
  mkdocs       a page of bosh.io (docs-bosh) or of the .NET Core tutorial
               (docs-dotnet-core-tutorial), two MkDocs sites outside the book

How a link is resolved (as a browser and the book's server do):
  1. The URL is joined to the page's URL, https://docs.cloudfoundry.org/
     <directory>/<path>.html, where <directory> is the section's
     `directory:` in the book's config.yml.
  2. A path that is a page or file of the built site resolves. So does a
     path ending in `/` whose index.html exists, and a path without a dot
     that is a folder with an index.html (the server adds the slash).
  3. Otherwise a rule in redirects.rb that matches the path resolves it,
     and the rule's target is checked in turn (one hop).
  4. A Markdown link whose path names a file of the site is published as
     that file's root-relative URL: Middleman's link_to helper looks the
     path up in its sitemap (published_href). Other links are published as
     written.
  5. The fragment must be an id on the target page: an `id` or `<a name>`
     in the page's source or in a partial it includes, or the id the book
     generates for a Markdown heading (its text with tags removed,
     lowercased, each space turned into a hyphen). `#top` and an empty
     fragment always resolve.
"""
import csv, os, re, sys, posixpath, unicodedata
from collections import Counter, defaultdict
from urllib.parse import urljoin, urlsplit, unquote

if len(sys.argv) not in (5, 6):
    sys.exit(__doc__)
REPOS, SHAS, OUT_LINKS, OUT_REDIRECTS = sys.argv[1:5]
BB = sys.argv[5] if len(sys.argv) == 6 else None
EXTS = ('.md', '.erb', '.html', '.haml', '.markdown', '.mdx', '.adoc')
SKIP_DIRS = {'.git', 'node_modules', 'vendor'}
BOOK = 'docs-book-cloudfoundry'
HOST = 'docs.cloudfoundry.org'
BASE = f'https://{HOST}/'
MKDOCS = {'docs-bosh': ('content', 'https://bosh.io/docs/'),
          'docs-dotnet-core-tutorial': ('docs', None)}
sha = dict(l.split()[:2] for l in open(SHAS) if l.strip())

FENCE = re.compile(r'^\s*(```|~~~)')
ERB = re.compile(r'<%(#|=|-)?(.*?)-?%>', re.S)
VAR = re.compile(r'<%=\s*vars\.([A-Za-z0-9_]+)\s*-?%>')
MD_LINK = re.compile(r'(!?)\[((?:[^\[\]\n]|\n(?![ \t]*\n)|\[[^\]\n]*\])*)\]\(\s*<?([^()\s<>]*(?:\([^()\s]*\)[^()\s<>]*)*)>?(?:\s+(?:"[^"]*"|\'[^\']*\'|\([^)]*\)))?\s*\)')
MD_REFDEF = re.compile(r'^ {0,3}\[([^\]]+)\]:\s*<?(\S+?)>?(?:\s+(?:"[^"]*"|\'[^\']*\'|\([^)]*\)))?\s*$', re.M)
TAG_URL = re.compile(r'<(a|img|area)\b[^>]*?\s(href|src)\s*=\s*("([^"]*)"|\'([^\']*)\'|([^\s>]+))', re.I | re.S)
AUTOLINK = re.compile(r'<((?:https?|ftp)://[^\s>]+|mailto:[^\s>]+)>', re.I)
BARE = re.compile(r'(?<![\w/@.:"\'=(\[])((?:https?://|www\.)[^\s<>"\'`]*[^\s<>"\'`.,;:!?)\]])', re.I)
ID_ATTR = re.compile(r'''\b(?:id|name)\s*=\s*(?:"([^"]*)"|'([^']*)')''', re.I)
HEADING_MD = re.compile(r'^\s{0,3}(#{1,6})(.*?)\s*#*\s*$')


def gh(repo, rel, line=None):
    owner = 'pivotal-cf' if repo == 'bookbinder' else 'cloudfoundry'
    ref = 'f608a441572def7787361842f05e42d163d78d54' if repo == 'bookbinder' else sha[repo]
    u = f'https://github.com/{owner}/{repo}/blob/{ref}/{rel}'
    return u + (f'#L{line}' if line else '')


def walk(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        for f in sorted(files):
            yield os.path.relpath(os.path.join(d, f), root)


def read(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()


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


# --- the book's sections: repository -> URL directory -----------------------
config_text = read(os.path.join(REPOS, BOOK, 'config.yml'))
directory, config_line = {}, {}
for m in re.finditer(r'^- repository:\n\s+name:\s*(\S+)\n(?:.*\n)*?  directory:\s*(\S+)', config_text, re.M):
    name = m.group(1).split('/')[-1]
    directory[name] = m.group(2)
    config_line[name] = config_text[:m.start(2)].count('\n') + 1
repo_of_dir = {d: r for r, d in directory.items()}

# --- the virtual source tree Middleman sees ---------------------------------
tree = {}   # path in the site source -> (repo, path in repo); later mounts win
if BB:
    for rel in walk(os.path.join(BB, 'master_middleman', 'source')):
        tree[rel] = ('bookbinder', 'master_middleman/source/' + rel)
for rel in walk(os.path.join(REPOS, BOOK, 'master_middleman', 'source')):
    tree[rel] = (BOOK, 'master_middleman/source/' + rel)
for repo, d in directory.items():
    if os.path.isdir(os.path.join(REPOS, repo)):
        for rel in walk(os.path.join(REPOS, repo)):
            tree[posixpath.join(d, rel)] = (repo, rel)
folder_files = defaultdict(list)
for p in tree:
    folder_files[posixpath.dirname(p)].append(posixpath.basename(p))
TEMPLATE_EXTS = ('.erb', '.md', '.markdown', '.haml')


def output_path(src):
    """The built file a source file becomes, or None (partials, layouts)."""
    base = posixpath.basename(src)
    if base.startswith('_') or src.startswith(('layouts/', 'subnavs/')):
        return None
    out = src
    while out.endswith(TEMPLATE_EXTS):
        out = out[:out.rfind('.')]
    if out == src:
        return src                                  # a static file
    if '.' not in posixpath.basename(out):
        out += '.html'
    return out


built = {}   # built path -> source path in the site tree
for p in tree:
    o = output_path(p)
    if o and not tree[p][1].startswith('.'):
        built.setdefault(o, p)
built_dirs = {posixpath.dirname(o) for o in built}


def find_partial(path):
    path = posixpath.normpath(path.lstrip('/'))
    if path.startswith('..'):
        return None
    folder, base = posixpath.split(path)
    names = folder_files.get(folder, [])
    for b in (base, re.sub(r'^_', '', base)):
        for n in sorted(names):
            if n == b or (n.startswith(b + '.') and n.endswith(TEMPLATE_EXTS + ('.html',))):
                return posixpath.join(folder, n)
    return None


def resolve_partial(name, caller):
    head, _, tail = name.rpartition('/')
    template = f'{head}/_{tail}' if head else f'_{tail}'
    if not name.startswith('/'):
        hit = find_partial(posixpath.join(posixpath.dirname(caller), template))
        if hit:
            return hit
    return find_partial(template)


# --- variables ----------------------------------------------------------------
var_file = os.path.join(REPOS, BOOK, 'config', 'template_variables.yml')
var_text = read(var_file)
values, value_line = {}, {}
for i, l in enumerate(var_text.split('\n'), 1):
    m = re.match(r'^  ([A-Za-z0-9_]+):\s*(.*)$', l)
    if m:
        v = m.group(2).strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
            v = v[1:-1].replace('\\"', '"') if v[0] == '"' else v[1:-1]
        values[m.group(1)] = v
        value_line[m.group(1)] = i


VTOK = re.compile(r'\{\{vars\.([A-Za-z0-9_]+)\}\}')


def subst_vars(s):
    s = VAR.sub(lambda m: values.get(m.group(1), ''), s)
    return VTOK.sub(lambda m: values.get(m.group(1), ''), s)


def tokens(text):
    """Write each <%= vars.name %> as {{vars.name}}, one word with no
    spaces, so a link whose URL is a variable is found like any other.
    No tag spans a line, so line numbers stay the same."""
    return VAR.sub(lambda m: '{{vars.' + m.group(1) + '}}', text)


# --- ids on each built page ---------------------------------------------------
def gen_id(inner):
    """The id the book gives a Markdown heading (modelled from the
    published pages; checked by ids.py): tags removed, lowercased, every
    space a hyphen."""
    text = re.sub(r'<[^>]+>', '', subst_vars(inner))
    return text.rstrip().lower().replace(' ', '-')


def slugify_pymd(value):
    """Python-Markdown's toc slugify (MkDocs)."""
    value = unicodedata.normalize('NFKD', re.sub(r'<[^>]+>', '', value)).encode('ascii', 'ignore').decode()
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def ids_in(text, mkdocs=False):
    lines = text.split('\n')
    fenced = fenced_lines(lines)
    ids = set()
    seen = Counter()
    for i, l in enumerate(lines):
        if i in fenced:
            continue
        for m in ID_ATTR.finditer(l):
            ids.add(m.group(1) if m.group(1) is not None else m.group(2))
        h = HEADING_MD.match(l)
        if h and not l.lstrip().startswith('#{'):
            inner = h.group(2)
            if mkdocs:
                a = re.search(r'\{[^}]*#([\w-]+)[^}]*\}\s*$', inner)
                if a:
                    ids.add(a.group(1)); continue
                s = slugify_pymd(inner)
                ids.add(s if not seen[s] else f'{s}_{seen[s]}'); seen[s] += 1
            else:
                ids.add(gen_id(inner.lstrip()) if not inner.startswith(' ') else gen_id(inner[1:]))
    return ids


# --- read every file ----------------------------------------------------------
files = {}   # (repo, rel) -> text
for repo in sorted(sha):
    root = os.path.join(REPOS, repo)
    if not os.path.isdir(root):
        print(f'missing clone: {repo}', file=sys.stderr)
        continue
    for rel in walk(root):
        if not rel.endswith(EXTS) or ('/' not in rel and rel.lower().endswith(('.md', '.markdown'))):
            continue
        if repo in MKDOCS and not rel.startswith(MKDOCS[repo][0] + '/'):
            continue
        files[(repo, rel)] = read(os.path.join(root, rel))
if BB:
    for rel in walk(os.path.join(BB, 'master_middleman', 'source', 'layouts')):
        site = 'layouts/' + rel
        if tree.get(site, ('',))[0] == 'bookbinder':
            files[('bookbinder', 'master_middleman/source/' + site)] = read(os.path.join(BB, 'master_middleman', 'source', site))
site_of = {v: k for k, v in tree.items()}

# partial calls: host page -> partial files (nested), partial -> host pages
PARTIAL_CALL = re.compile(r'<%=?\s*partial\s*\(?\s*([\'"])(.*?)\1')
partials_of = defaultdict(list)
for (repo, rel), text in files.items():
    site = site_of.get((repo, rel))
    if site is None:
        continue
    for m in PARTIAL_CALL.finditer(text):
        hit = resolve_partial(m.group(2), site)
        if hit:
            partials_of[site].append(hit)


def expand(site, seen=()):
    out = []
    for p in partials_of.get(site, []):
        if p not in seen:
            out.append(p)
            out.extend(expand(p, seen + (p,)))
    return out


hosts_of = defaultdict(list)   # partial site path -> host built paths
page_ids = {}                  # built path -> ids
for o, src in built.items():
    if not src.endswith(TEMPLATE_EXTS) and not src.endswith('.html'):
        continue
    repo, rel = tree[src]
    text = files.get((repo, rel), '')
    ids = ids_in(text)
    for p in expand(src):
        hosts_of[p].append(o)
        ids |= ids_in(files.get(tree[p], ''))
    page_ids[o] = ids
layout_ids = set()
for (repo, rel), text in files.items():
    if site_of.get((repo, rel), '').startswith('layouts/'):
        layout_ids |= ids_in(text)

# MkDocs sites: page file -> URL path, ids; every file of the repository
mk_pages, mk_ids = {}, {}
mk_files = {repo: set(walk(os.path.join(REPOS, repo))) for repo in MKDOCS if os.path.isdir(os.path.join(REPOS, repo))}
for (repo, rel), text in files.items():
    if repo in MKDOCS and rel.endswith('.md'):
        d = MKDOCS[repo][0]
        r = rel[len(d) + 1:-3]
        url = '' if r == 'index' else (r[:-len('/index')] + '/' if r.endswith('/index') else r + '/')
        mk_pages[(repo, url)] = rel
        mk_ids[(repo, rel)] = ids_in(text, mkdocs=True)

# --- redirects.rb ---------------------------------------------------------------
redirects = []
red_text = read(os.path.join(REPOS, BOOK, 'redirects.rb'))
for i, l in enumerate(red_text.split('\n'), 1):
    m = re.match(r"^\s*(r30[12])\s+(%r\{(.*?)\}|'([^']*)')\s*,\s*'([^']*)'", l)
    if m:
        redirects.append(dict(line=i, code=m.group(1), regex=m.group(3), source=m.group(4), target=m.group(5)))


def redirect_for(path):
    for r in redirects:
        if r['source'] is not None and r['source'] == path:
            return r, r['target']
        if r['regex'] is not None and r['regex'] != '.*':
            m = re.search(r['regex'], path)
            if m:
                t = r['target'].replace('$&', m.group(0))
                for k in range(1, 10):
                    t = t.replace(f'${k}', (m.group(k) or '') if k <= (m.re.groups) else '')
                return r, t
    return None, None


def page_at(path):
    """The built path the server answers for a URL path, or None."""
    p = unquote(path).lstrip('/')
    if p in built:
        return p
    if p == '' or p.endswith('/'):
        q = p + 'index.html'
        return q if q in built else None
    if '.' not in posixpath.basename(p) and (p + '/index.html') in built:
        return p + '/index.html'
    return None


def check_fragment(page, frag, mk=None):
    frag = unquote(frag)
    if frag in ('', 'top'):
        return 'ok'
    ids = mk_ids.get(mk, set()) if mk else (page_ids.get(page, set()) | layout_ids)
    return 'ok' if frag in ids else 'missing'


def resolve_book(path, frag):
    """Resolve a site path on docs.cloudfoundry.org."""
    if unquote(path).startswith('/api/'):
        # The UAA and CredHub API references: published on the same host
        # by their own builds, not by the book
        return dict(target_kind='outside the book', status='outside the book: not checked')
    page = page_at(path)
    hops = []
    while page is None and len(hops) < 5:
        rule, target = redirect_for('/' + unquote(path).lstrip('/'))
        if rule is None:
            if not hops:
                return dict(target_kind='missing', status='broken: no page')
            return dict(target_kind='redirect, missing', status='broken: redirect target missing',
                        redirect='; '.join(hops))
        hops.append(f'redirects.rb L{rule["line"]} -> {target}')
        t = urlsplit(target)
        if t.netloc and t.netloc != HOST:
            return dict(target_kind='redirect, external', status='ok: by redirect', redirect='; '.join(hops))
        path = t.path
        page = page_at(path)
        if t.fragment and not frag:
            frag = t.fragment
    hop = '; '.join(hops)
    if page is None:
        return dict(target_kind='redirect, missing', status='broken: redirect loop', redirect=hop)
    repo, rel = tree[built[page]]
    kind = 'page' if page.endswith('.html') else 'file'
    out = dict(target_kind=kind + (', by redirect' if hop else ''), target_path=page,
               target_repo=repo, target_file=rel, redirect=hop)
    if frag is None:
        out['status'] = 'ok: by redirect' if hop else 'ok'
    elif kind != 'page':
        out['status'] = 'ok'
    else:
        f = check_fragment(page, frag)
        out['fragment_status'] = f
        out['status'] = ('ok' if f == 'ok' else 'broken: no anchor') + (' (by redirect)' if hop and f == 'ok' else '')
    return out


def in_submodule(repo, rel):
    """rel (a path in the repository) lies below a symbolic link, which in
    docs-bosh points into a git submodule this survey does not fetch."""
    parts = rel.split('/')
    return any(os.path.islink(os.path.join(REPOS, repo, *parts[:k])) for k in range(1, len(parts) + 1))


SUBMODULE = dict(target_kind='submodule', status='in a submodule: not checked')


def resolve_mkdocs(repo, url_path, frag, src_rel=None, link=None):
    """Resolve a link on a MkDocs site: a relative .md file, or a URL path
    below the site root."""
    if link is not None and not re.search(r'\.md$', link.split('#')[0]):
        rel = posixpath.normpath(posixpath.join(posixpath.dirname(src_rel), unquote(link.split('#')[0])))
        if rel in mk_files[repo]:
            return dict(target_kind='file', target_repo=repo, target_file=rel, target_path=rel, status='ok')
    if link is not None and re.search(r'\.md$', link.split('#')[0]):
        rel = posixpath.normpath(posixpath.join(posixpath.dirname(src_rel), unquote(link.split('#')[0])))
        if (repo, rel) not in files:
            return dict(SUBMODULE) if in_submodule(repo, rel) else dict(target_kind='missing', status='broken: no page')
        target = rel
    else:
        p = url_path.strip('/')
        p = re.sub(r'\.html$', '', p)
        p = p + '/' if p else ''
        target = mk_pages.get((repo, p))
        if target is None:
            if p and in_submodule(repo, MKDOCS[repo][0] + '/' + p.rstrip('/')):
                return dict(SUBMODULE)
            return dict(target_kind='missing', status='broken: no page')
    out = dict(target_kind='page', target_repo=repo, target_file=target, target_path=target)
    if frag:
        f = check_fragment(None, frag, mk=(repo, target))
        out['fragment_status'] = f
        out['status'] = 'ok' if f == 'ok' else 'broken: no anchor'
    else:
        out['status'] = 'ok'
    return out


# --- find links -------------------------------------------------------------------
def blank_code(text):
    """Replace fenced code and inline code spans by spaces, keeping offsets."""
    lines = text.split('\n')
    fenced = fenced_lines(lines)
    out = [(' ' * len(l)) if i in fenced else l for i, l in enumerate(lines)]
    t = '\n'.join(out)
    t = re.sub(r'(`+)(?!`)(.+?)(?<!`)\1(?!`)', lambda m: ' ' * len(m.group(0)), t, flags=re.S)
    t = re.sub(r'<(code|pre)\b[^>]*>.*?</\1>', lambda m: re.sub(r'[^\n]', ' ', m.group(0)) if '<a ' not in m.group(0) else m.group(0), t, flags=re.S | re.I)
    return t


def find_links(text):
    """Yield (offset, form, url) for every link in a file's text."""
    t = blank_code(tokens(text))
    taken = []
    for m in MD_LINK.finditer(t):
        yield m.start(), 'md-image' if m.group(1) else 'md-inline', m.group(3)
        taken.append((m.start(3), m.end(3)))
    for m in MD_REFDEF.finditer(t):
        yield m.start(2), 'md-refdef', m.group(2)
        taken.append((m.start(2), m.end(2)))
    for m in TAG_URL.finditer(t):
        url = next(g for g in m.group(4, 5, 6) if g is not None)
        yield m.start(), 'html-img' if m.group(1).lower() == 'img' else 'html-a', url
        taken.append((m.start(3), m.end(3)))
    for m in AUTOLINK.finditer(t):
        yield m.start(), 'autolink', m.group(1)
        taken.append((m.start(1), m.end(1)))
    masked = list(t)
    for a, b in taken:
        masked[a:b] = ' ' * (b - a)
    masked = ''.join(masked)
    masked = VTOK.sub(lambda m: ' ' * len(m.group(0)), masked)
    masked = re.sub(r'<%.*?%>', lambda m: ' ' * len(m.group(0)), masked, flags=re.S)
    masked = re.sub(r'<[^>]*>', lambda m: ' ' * len(m.group(0)), masked)
    for m in BARE.finditer(masked):
        yield m.start(), 'bare-url', m.group(1)


def url_kind(url):
    if VTOK.search(url) or VAR.search(url):
        return 'erb-variable'
    if re.search(r'<%', url):
        return 'erb-other'
    if url.startswith('#'):
        return 'anchor'
    if url.startswith('//'):
        return 'protocol-relative'
    s = urlsplit(url)
    if s.scheme in ('http', 'https') or url.lower().startswith('www.'):
        host = (s.netloc or url.split('/')[0]).lower()
        return 'absolute-docs' if host in (HOST, 'www.' + HOST) else 'absolute-other'
    if s.scheme:
        return s.scheme
    if url.startswith('/'):
        return 'root-relative'
    return 'page-relative'


rows = []


def add(repo, rel, line, where, host, form, url, via=''):
    kind = url_kind(url)
    real = subst_vars(url) if kind.startswith('erb') else url
    host_repo = tree.get(built.get(host or '', ''), ('',))[0] if host else (repo if where in ('page', 'mkdocs') else '')
    r = dict(repo=repo, file=rel, line=line, where=where, host_page=host or '', host_repo=host_repo, form=form,
             url=VTOK.sub(lambda m: f'<%= vars.{m.group(1)} %>', url), via=via, kind=kind, url_resolved='', host_name='',
             target_kind='', target_path='', target_repo='', target_file='', crosses='',
             fragment='', fragment_status='', redirect='', status='', gh=gh(repo, rel, line))
    if kind == 'erb-variable':
        r['kind'] = 'erb-variable:' + url_kind(real)
    eff = url_kind(real)
    s = urlsplit(real if not real.lower().startswith('www.') else 'http://' + real)
    r['fragment'] = s.fragment if '#' in real else ''
    frag = s.fragment if '#' in real else None
    if eff in ('mailto', 'javascript', 'tel', 'ftp', 'erb-other') or not real:
        r['status'] = 'not checked: ' + (eff if real else 'empty')
    elif repo in MKDOCS:
        site_root = MKDOCS[repo][1]
        if eff in ('page-relative', 'anchor'):
            page_url = posixpath.dirname(rel[len(MKDOCS[repo][0]) + 1:])
            here = rel[len(MKDOCS[repo][0]) + 1:-3]
            here_url = '/' + ('' if here == 'index' else (here[:-6] if here.endswith('/index') else here + '/'))
            if eff == 'anchor':
                r.update(resolve_mkdocs(repo, here_url, frag, rel))
            else:
                joined = urlsplit(urljoin('https://x' + here_url, real)).path
                r.update(resolve_mkdocs(repo, joined, frag, rel, link=real))
            r['url_resolved'] = r.get('target_path', '')
            r['crosses'] = 'no'
        elif eff == 'absolute-other' and site_root and real.startswith(site_root):
            r['host_name'] = s.netloc
            r.update(resolve_mkdocs(repo, s.path[len('/docs'):], frag))
            r['crosses'] = 'no'
        else:
            r['host_name'] = s.netloc
            r['status'] = 'external: not checked'
    elif eff == 'absolute-other':
        r['host_name'] = s.netloc.lower()
        if s.netloc.lower() == 'bosh.io' and s.path.startswith('/docs'):
            r.update(resolve_mkdocs('docs-bosh', s.path[len('/docs'):], frag))
            r['crosses'] = 'other site (bosh.io)'
            r['status'] += ' (against docs-bosh)'
        else:
            r['status'] = 'external: not checked'
    else:
        base = BASE + (host or '')
        full = urljoin(base, real if not real.startswith('//') else 'https:' + real)
        fs = urlsplit(full)
        if fs.netloc.lower() not in (HOST, 'www.' + HOST):
            r['host_name'] = fs.netloc
            r['status'] = 'external: not checked'
        else:
            r['host_name'] = HOST if eff == 'absolute-docs' else ''
            r['url_resolved'] = fs.path
            r.update(resolve_book(fs.path, frag))
            if r.get('target_repo'):
                if where in ('page', 'partial', 'variable') and host_repo:
                    r['crosses'] = 'yes' if r['target_repo'] != host_repo else 'no'
                elif where in ('subnav', 'layout'):
                    r['crosses'] = 'from the book' if r['target_repo'] != BOOK else 'no'
            # Middleman writes a Markdown link whose path names a file of
            # the site as that file's root-relative URL (index.html dropped)
            if (form in ('md-inline', 'md-refdef') and eff in ('page-relative', 'root-relative')
                    and not r.get('redirect') and r.get('target_path')
                    and unquote(fs.path).lstrip('/') == r['target_path']):
                u = '/' + r['target_path']
                u = u[:-len('index.html')] if u.endswith('/index.html') else u
                r['published_href'] = u + ('#' + s.fragment if '#' in real else '')
    if where != 'mkdocs' and not r.get('published_href'):
        r['published_href'] = real
    rows.append(r)


def line_of(text, pos):
    return text.count('\n', 0, pos) + 1


var_uses = defaultdict(list)   # variable -> built paths that use it
for (repo, rel), text in sorted(files.items()):
    site = site_of.get((repo, rel))
    if repo in MKDOCS:
        where, hosts = 'mkdocs', [None]
    elif site is None:
        continue
    elif site.startswith('subnavs/'):
        where, hosts = 'subnav', ['']
    elif site.startswith('layouts/') or repo == 'bookbinder':
        where, hosts = 'layout', ['']
    elif posixpath.basename(site).startswith('_'):
        where, hosts = 'partial', sorted(hosts_of.get(site, [])) or [None]   # once per inclusion
    elif output_path(site) in page_ids:
        where, hosts = 'page', [output_path(site)]
    else:
        continue
    if where in ('page', 'partial'):
        for m in re.finditer(r'vars\.([A-Za-z0-9_]+)', text):
            for h in hosts:
                if h:
                    var_uses[m.group(1)].append((h, repo, rel, line_of(text, m.start())))
    for pos, form, url in find_links(text):
        ln = line_of(text, pos)
        for h in hosts:
            add(repo, rel, ln, where, h if h is not None else (posixpath.dirname(output_path(site) or site) + '/x.html' if site else None),
                form, url)
            if h is None and where == 'partial':
                rows[-1].update(host_page='(not included)', status='not used', crosses='')

# links inside variable values: one row per page that uses the variable
var_lines = var_text.split('\n')
for name, v in values.items():
    links = list(find_links(v))
    if not links:
        continue
    uses = var_uses.get(name, [])
    for pos, form, url in links:
        if not uses:
            add(BOOK, 'config/template_variables.yml', value_line[name], 'variable', None, form, url, via=f'vars.{name} (not used)')
            rows[-1].update(status='not used', crosses='')
        for h, urepo, urel, uline in sorted(set(uses)):
            add(BOOK, 'config/template_variables.yml', value_line[name], 'variable', h, form, url,
                via=f'vars.{name} used at {urepo}/{urel}#L{uline}')

# --- write ----------------------------------------------------------------------
FIELDS = ['repo', 'file', 'line', 'where', 'host_page', 'host_repo', 'form', 'url', 'via', 'kind',
          'host_name', 'url_resolved', 'target_kind', 'target_path', 'target_repo', 'target_file', 'crosses',
          'fragment', 'fragment_status', 'redirect', 'status', 'published_href', 'gh']
with open(OUT_LINKS, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore')
    w.writeheader()
    for r in sorted(rows, key=lambda r: (r['repo'], r['file'], int(r['line']), r['host_page'], r['url'])):
        w.writerow(r)

red_rows = []
for r in redirects:
    t = urlsplit(r['target'])
    if t.netloc and t.netloc != HOST:
        st = 'external target: not checked'
    else:
        p = page_at(t.path)
        st = 'target exists' if p else 'target missing'
        if p and t.fragment:
            st += '; anchor ' + check_fragment(p, t.fragment)
        if not p:
            again, _ = redirect_for(t.path)
            if again is not None:
                st = f'target redirected again (L{again["line"]})'
    src = r['source'] if r['source'] is not None else '%r{' + r['regex'] + '}'
    shadow = ''
    if r['source'] is not None and page_at(r['source']):
        shadow = 'a page exists at the source path'
    if r['source'] is not None and '#' in r['source']:
        shadow = 'source holds a fragment, which a browser never sends'
    red_rows.append(dict(line=r['line'], code=r['code'], source=src, target=r['target'], target_status=st,
                         note=shadow, gh=gh(BOOK, 'redirects.rb', r['line'])))
with open(OUT_REDIRECTS, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['line', 'code', 'source', 'target', 'target_status', 'note', 'gh'])
    w.writeheader()
    w.writerows(red_rows)

print(f'sections: {len(directory)}; built pages: {sum(1 for o in built if o.endswith(".html"))}; '
      f'links (rows): {len(rows)}; redirect rules: {len(red_rows)}')
