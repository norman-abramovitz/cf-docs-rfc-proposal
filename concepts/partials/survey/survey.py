"""Inventory every partial call and every partial file in the cloned
documentation repositories.

Usage:
  python3 -I survey.py REPOS_DIR SHAS CALLS.csv PARTIALS.csv [BOOKBINDER_DIR]

REPOS_DIR holds one clone per line of SHAS, named as in SHAS. SHAS has
lines `<name> <commit> <date>`; the commit goes into each row's GitHub
link. BOOKBINDER_DIR, if given, is the unpacked `bookbindery` gem (its
`master_middleman/source` supplies the layout partials the book does not
override). Writes CALLS.csv (one row per call) and PARTIALS.csv (one row
per partial file) and prints a summary. Reads files only; runs nothing from
the clones.

What is a call:
  erb       an ERB tag whose code starts with `partial` or `render`:
            <%= partial 'name' %>, <%- partial "a/b", locals: {...} %>
  comment   an ERB comment that mentions a partial (<%# ... partial ... %>);
            counted, never resolved
  snippet   a pymdownx.snippets line, `--8<-- "path"` (docs-bosh, MkDocs)

How a name is resolved (Bookbinder 9.12.1 runs Middleman 3.4 with
padrino-helpers 0.12):
  1. `partial 'a/b'` asks for `a/_b` (padrino `partial`).
  2. Middleman looks for that path relative to the calling file's folder,
     then from the site's source root; each with any template extension,
     and also with the leading underscore of the file name removed.
  3. The source root is the book's master_middleman/source (over the
     gem's), with each section's repository mounted at its `directory:`
     from the book's config.yml.
"""
import csv, os, re, sys, posixpath
from collections import Counter, defaultdict

if len(sys.argv) not in (5, 6):
    sys.exit(__doc__)
REPOS, SHAS, OUT_CALLS, OUT_PARTIALS = sys.argv[1:5]
BB = sys.argv[5] if len(sys.argv) == 6 else None
EXTS = ('.md', '.erb', '.html', '.haml', '.markdown', '.mdx', '.adoc')
SKIP_DIRS = {'.git', 'node_modules', 'vendor'}
BOOK = 'docs-book-cloudfoundry'
sha = dict(l.split()[:2] for l in open(SHAS) if l.strip())

FENCE = re.compile(r'^\s*(```|~~~)')
ERB = re.compile(r'<%(#|=|-)?(.*?)-?%>', re.S)
CALL = re.compile(r'^\s*(partial|render|render_partial)\b\s*\(?\s*(.*)$', re.S)
LIST_LINE = re.compile(r'^\s*([*+-]|\d+\.)\s+')
CTRL_OPEN = re.compile(r'^\s*(if|unless|case|while|for)\b|\bdo\s*(\|[^|]*\|)?\s*$')
CTRL_END = re.compile(r'^\s*end\b')
SNIPPET = re.compile(r'^(\s*)-{1,}8<-{1,}\s+"([^"]+)"\s*$')
HEADING_MD = re.compile(r'^\s{0,3}(#{1,6})\s*\S')
HEADING_HTML = re.compile(r'<h([1-6])\b', re.I)


def url(repo, rel, line=None):
    u = f'https://github.com/cloudfoundry/{repo}/blob/{sha[repo]}/{rel}'
    return u + (f'#L{line}' if line else '')


def walk(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        for f in sorted(files):
            yield os.path.relpath(os.path.join(d, f), root)


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


def in_list(lines, i):
    """Line i is indented under a Markdown list item."""
    ind = len(lines[i]) - len(lines[i].lstrip())
    if ind == 0:
        return False
    for j in range(i - 1, -1, -1):
        l = lines[j]
        if not l.strip():
            continue
        if len(l) - len(l.lstrip()) < ind:
            return bool(LIST_LINE.match(l))
    return False


def open_count(before, tag):
    return len(re.findall(rf'<{tag}\b', before, re.I)) - len(re.findall(rf'</{tag}\s*>', before, re.I))


# --- the book's sections: repository -> URL directory -----------------------
config = open(os.path.join(REPOS, BOOK, 'config.yml')).read()
directory = {}
for block in re.split(r'\n- repository:', config)[1:]:
    name = re.search(r'^\s+name:\s*(\S+)', block, re.M).group(1).split('/')[-1]
    d = re.search(r'^  directory:\s*(\S+)', block, re.M)
    if d:
        directory[name] = d.group(1)

# --- the virtual source tree Middleman sees ---------------------------------
# path in the site source -> (repo, path in repo); later mounts win
tree = {}
if BB:
    for rel in walk(os.path.join(BB, 'master_middleman', 'source')):
        tree[rel] = ('bookbinder', 'master_middleman/source/' + rel)
for rel in walk(os.path.join(REPOS, BOOK, 'master_middleman', 'source')):
    tree[rel] = (BOOK, 'master_middleman/source/' + rel)
for repo, d in directory.items():
    if os.path.isdir(os.path.join(REPOS, repo)):
        for rel in walk(os.path.join(REPOS, repo)):
            tree[posixpath.join(d, rel)] = (repo, rel)
site_of = {v: k for k, v in tree.items()}
folder_files = defaultdict(list)
for p in tree:
    folder_files[posixpath.dirname(p)].append(posixpath.basename(p))

TEMPLATE_EXTS = ('.erb', '.md', '.markdown', '.html', '.haml')


def find(path):
    """Middleman's resolve_template for one path (in the site source):
    the path itself, or the path with any template extension, also with
    the file name's leading underscore removed."""
    path = posixpath.normpath(path.lstrip('/'))
    if path.startswith('..'):
        return None
    folder, base = posixpath.split(path)
    names = folder_files.get(folder, [])
    for b in (base, re.sub(r'^_', '', base)):
        for n in sorted(names):
            if n == b or (n.startswith(b + '.') and n.endswith(TEMPLATE_EXTS)):
                return posixpath.join(folder, n)
    return None


def resolve(name, caller_site_path):
    head, _, tail = name.rpartition('/')
    template = f'{head}/_{tail}' if head else f'_{tail}'
    if not name.startswith('/'):
        rel = posixpath.join(posixpath.dirname(caller_site_path), template)
        hit = find(rel)
        if hit:
            return hit, 'relative'
    hit = find(template)
    return (hit, 'root') if hit else (None, '')


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
        with open(os.path.join(root, rel), encoding='utf-8', errors='replace') as f:
            files[(repo, rel)] = f.read()


def is_partial_file(rel):
    return posixpath.basename(rel).startswith('_')


calls = []
for (repo, rel), text in files.items():
    lines = text.split('\n')
    fenced = fenced_lines(lines)
    starts = [0]
    for l in lines:
        starts.append(starts[-1] + len(l) + 1)

    def line_of(pos):
        lo, hi = 0, len(starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if starts[mid] <= pos:
                lo = mid
            else:
                hi = mid - 1
        return lo

    depth = 0
    for m in ERB.finditer(text):
        kind, code = m.group(1) or '', m.group(2)
        if kind == '#':
            if re.search(r'\bpartial', code):
                i = line_of(m.start())
                calls.append(dict(repo=repo, file=rel, line=i + 1, form='comment', call=m.group(0).strip()))
            continue
        if kind == '' and CTRL_END.match(code):
            depth = max(0, depth - 1); continue
        if kind == '' and CTRL_OPEN.search(code) and not CALL.match(code):
            depth += 1; continue
        c = CALL.match(code)
        if not c:
            continue
        i = line_of(m.start())
        args = c.group(2).strip().rstrip(')').strip()
        q = re.match(r'''(['"])(.*?)\1''', args)
        if q:
            name = q.group(2)
            quotes = 'single' if q.group(1) == "'" else 'double'
            name_kind = 'interpolated' if (q.group(1) == '"' and '#{' in name) else 'literal'
        else:
            name = re.split(r'[\s,]', args, 1)[0]
            quotes = 'none'
            name_kind = 'variable' if name.startswith('vars.') else 'expression'
        line = lines[i]
        before = text[:m.start()]
        prefix = line[:m.start() - starts[i]]
        if i in fenced:
            place = 'code block'
        elif open_count(before, 'td') > 0 or open_count(before, 'th') > 0:
            place = 'table cell'
        elif open_count(before, 'li') > 0:
            place = 'html list item'
        elif LIST_LINE.match(prefix):
            place = 'list item, after text' if prefix.strip() not in ('*', '-', '+') and not re.fullmatch(r'\d+\.', prefix.strip()) else 'list item, first'
        elif in_list(lines, i):
            place = 'list item, indented'
        elif any(open_count(before, t) > 0 for t in ('div', 'p', 'table', 'ul', 'ol', 'section')):
            place = 'inside html'
        elif prefix.strip():
            place = 'after text'
        else:
            place = 'top level'
        path_style = ('root' if name.startswith('/') else 'up (../)' if name.startswith('../')
                      else 'dot (./)' if name.startswith('./') else 'folder/name' if '/' in name else 'name')
        row = dict(repo=repo, file=rel, line=i + 1, form='erb', call=m.group(0).strip(),
                   tag='<%' + kind, quotes=quotes, name=name, name_kind=name_kind, path_style=path_style,
                   locals='yes' if re.search(r'\blocals\b', args) else 'no',
                   in_conditional='yes' if depth else 'no', place=place,
                   runs='yes' if rel.endswith('.erb') else 'no (not an ERB file)')
        calls.append(row)
    if repo == 'docs-bosh':
        for i, l in enumerate(lines):
            s = SNIPPET.match(l)
            if s and i not in fenced:
                calls.append(dict(repo=repo, file=rel, line=i + 1, form='snippet', call=l.strip(),
                                  name=s.group(2), name_kind='literal', quotes='double', tag='',
                                  locals='no', in_conditional='no',
                                  place='top level' if not s.group(1) else 'indented',
                                  runs='yes'))

# --- resolve ------------------------------------------------------------------
for c in calls:
    c.update(target_repo='', target_file='', resolved_by='', where='', url=url(c['repo'], c['file'], c['line']))
    if c['form'] == 'snippet':
        p = os.path.join(REPOS, c['repo'], c['name'])
        c['target_repo'], c['target_file'] = (c['repo'], c['name']) if os.path.exists(p) else ('', '')
        c['resolved_by'] = 'base path (repository root)'
        c['where'] = ('other folder, same repository' if os.path.exists(p) else 'missing')
        continue
    if c['form'] != 'erb' or c['name_kind'] != 'literal':
        continue
    site = site_of.get((c['repo'], c['file']))
    if site is None:
        c['where'] = 'not in the book'
        continue
    hit, how = resolve(c['name'], site)
    if not hit:
        c['where'] = 'missing'
        continue
    trepo, tfile = tree[hit]
    c.update(target_repo=trepo, target_file=tfile, resolved_by=how)
    if trepo == 'bookbinder':
        c['where'] = 'bookbinder gem'
    elif trepo != c['repo']:
        c['where'] = 'book repository' if trepo == BOOK else 'other repository'
    elif posixpath.dirname(tfile) == posixpath.dirname(c['file']):
        c['where'] = 'same folder'
    else:
        c['where'] = 'other folder, same repository'

CALL_FIELDS = ['repo', 'file', 'line', 'form', 'call', 'tag', 'quotes', 'name', 'name_kind', 'path_style', 'locals',
               'in_conditional', 'place', 'runs', 'where', 'resolved_by', 'target_repo', 'target_file', 'url']
with open(OUT_CALLS, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=CALL_FIELDS, extrasaction='ignore')
    w.writeheader()
    for c in sorted(calls, key=lambda c: (c['repo'], c['file'], c['line'])):
        w.writerow({k: c.get(k, '') for k in CALL_FIELDS})

# --- partial files ------------------------------------------------------------
included = defaultdict(list)          # (repo, file) -> calls that include it
for c in calls:
    if c.get('target_file') and c['form'] == 'erb':
        included[(c['target_repo'], c['target_file'])].append(c)

# variables whose value names a partial file
varfile = os.path.join(REPOS, BOOK, 'config', 'template_variables.yml')
var_names = {}
for i, l in enumerate(open(varfile), 1):
    m = re.match(r'^  ([A-Za-z0-9_]+):\s*"?([^"\n]*?)"?\s*$', l)
    if m and m.group(2) and re.fullmatch(r'[./A-Za-z0-9_-]+', m.group(2)):
        var_names[m.group(1)] = (m.group(2), i)
# code of every ERB tag that is not a comment, in the content repositories
alltext = '\n'.join(m.group(2) for (r, _), t in files.items() if r != BOOK
                    for m in ERB.finditer(t) if (m.group(1) or '') != '#')
named_in_var = defaultdict(list)
for v, (val, i) in var_names.items():
    # resolved as if called from each section's root
    for repo, d in directory.items():
        hit, _ = resolve(val, posixpath.join(d, 'index.html.md.erb'))
        if hit and is_partial_file(tree[hit][1]):
            named_in_var[tree[hit]].append((v, i, bool(re.search(rf'vars\.{v}\b', alltext))))
            break


def traits(text):
    lines = text.split('\n')
    fenced = fenced_lines(lines)
    md_h = [len(HEADING_MD.match(l).group(1)) for i, l in enumerate(lines)
            if i not in fenced and HEADING_MD.match(l) and not l.lstrip().startswith('#{')]
    html_h = [int(x) for x in HEADING_HTML.findall(text)]
    return dict(
        lines=len(lines),
        front_matter='yes' if text.startswith('---\n') else 'no',
        headings=len(md_h) + len(html_h),
        heading_levels=' '.join(sorted({f'h{n}' for n in md_h + html_h})),
        explicit_ids=len(re.findall(r'<a\s+(?:id|name)\s*=', text)),
        notes=len(re.findall(r'<(?:p|div)\b[^>]*class\s*=\s*["\'][^"\']*\bnote\b', text)),
        tables=len(re.findall(r'<table\b', text, re.I)) + sum(
            1 for i, l in enumerate(lines) if i not in fenced and re.match(r'^\s*\|?\s*:?-{3,}:?\s*\|', l)),
        code_blocks=sum(1 for l in lines if FENCE.match(l)) // 2 + len(re.findall(r'<pre\b', text, re.I)),
        variables=len(re.findall(r'vars\.[A-Za-z0-9_]+', text)),
        partial_calls=len(re.findall(r'<%[=-]?\s*(?:partial|render)\b', text)),
        other_erb=len([m for m in ERB.finditer(text)
                       if (m.group(1) or '') != '#' and not re.match(r'\s*(vars\.|partial\b|render\b)', m.group(2))]),
    )


partial_files = set()
for (repo, rel) in files:
    if is_partial_file(rel) and rel.endswith(('.erb', '.md', '.html')):
        partial_files.add((repo, rel))
for k in included:
    if k[0] != 'bookbinder':
        partial_files.add(k)


# nesting depth: how many partial levels below a file
def depth_of(key, seen=()):
    if key in seen:
        return 0
    kids = [(c['target_repo'], c['target_file']) for c in calls
            if (c['repo'], c['file']) == key and c.get('target_file') and c['form'] == 'erb']
    return 1 + max((depth_of(k, seen + (key,)) for k in kids), default=0) if kids else 0


# partials that Bookbinder's own helpers include: the subnav named by each
# section's subnav_template (yield_for_subnav renders "subnavs/<name>")
helper_use = {}
for t in set(re.findall(r'subnav_template:\s*(\S+)', config)):
    hit = find('subnavs/_' + t)
    if hit:
        helper_use[tree[hit]] = 'bookbinder:yield_for_subnav(config.yml subnav_template)'

rows = []
for key in sorted(partial_files):
    repo, rel = key
    t = traits(files.get(key, ''))
    inc = included.get(key, [])
    pages = sorted({(c['repo'], c['file']) for c in inc})
    per_page = Counter((c['repo'], c['file']) for c in inc)
    rows.append(dict(
        repo=repo, file=rel, url=url(repo, rel), **t,
        included_times=len(inc), included_by_files=len(pages),
        included_by=' '.join(f'{r}:{p}' for r, p in pages) or helper_use.get(key, ''),
        twice_on_one_page='yes' if any(v > 1 for v in per_page.values()) else 'no',
        from_other_repo='yes' if any(r != repo for r, _ in pages) else 'no',
        nested_depth=depth_of(key),
        named_in_variable=' '.join(f'{v}(L{i}{",used" if u else ",unused"})' for v, i, u in named_in_var.get(key, [])),
    ))
P_FIELDS = ['repo', 'file', 'lines', 'front_matter', 'headings', 'heading_levels', 'explicit_ids', 'notes',
            'tables', 'code_blocks', 'variables', 'partial_calls', 'other_erb', 'included_times',
            'included_by_files', 'twice_on_one_page', 'from_other_repo', 'nested_depth',
            'named_in_variable', 'included_by', 'url']
with open(OUT_PARTIALS, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=P_FIELDS)
    w.writeheader()
    for r in rows:
        w.writerow({k: r[k] for k in P_FIELDS})

# --- pages that are only partial calls -----------------------------------------
wrappers = []
for (repo, rel), text in files.items():
    if is_partial_file(rel) or not rel.endswith('.erb'):
        continue
    body = re.sub(r'\A---\n.*?\n---\n', '', text, flags=re.S)
    body = re.sub(r'<%#.*?%>', '', body, flags=re.S)
    rest = re.sub(r'<%[=-]?\s*(?:partial|render)\b.*?%>', '', body, flags=re.S)
    if rest.strip() == '' and body.strip():
        wrappers.append(f'{repo}/{rel}')

# --- summary --------------------------------------------------------------------
erb = [c for c in calls if c['form'] == 'erb']
content = [c for c in erb if c['repo'] != BOOK]
print(f'calls: {len(calls)} ({Counter(c["form"] for c in calls)})')
print(f'erb calls in content repositories: {len(content)} in {len({(c["repo"], c["file"]) for c in content})} files; '
      f'in the book: {len(erb) - len(content)}')
for k in ('tag', 'quotes', 'name_kind', 'path_style', 'locals', 'in_conditional', 'place', 'where', 'resolved_by', 'runs'):
    print(f'  {k}: {dict(Counter(c[k] for c in erb))}')
print(f'partial files: {len(rows)}; never included: '
      f'{sum(1 for r in rows if r["included_times"] == 0 and not r["included_by"])}; '
      f'with headings: {sum(1 for r in rows if r["headings"])}')
print(f'wrapper pages (only partial calls): {wrappers}')
print(f'variables naming a partial: {dict((v, x) for v, x in var_names.items() if any(v == y[0] for l in named_in_var.values() for y in l))}')
