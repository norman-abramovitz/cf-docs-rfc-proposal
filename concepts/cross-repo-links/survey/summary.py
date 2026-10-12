"""Print the counts in the survey's README from links.csv and redirects.csv.

Usage:
  python3 -I summary.py LINKS.csv REDIRECTS.csv
"""
import csv, re, sys
from collections import Counter, defaultdict

if len(sys.argv) != 3:
    sys.exit(__doc__)
rows = list(csv.DictReader(open(sys.argv[1])))
reds = list(csv.DictReader(open(sys.argv[2])))
BOOK = 'docs-book-cloudfoundry'
book = [r for r in rows if r['where'] != 'mkdocs']
mk = [r for r in rows if r['where'] == 'mkdocs']


def written(rs):
    return {(r['repo'], r['file'], r['line'], r['form'], r['url']) for r in rs}


def show(title, c):
    print(f'{title}: ' + ', '.join(f'{k or "-"} {v}' for k, v in c.most_common()))


print(f'rows: {len(rows)} (book {len(book)}, MkDocs sites {len(mk)})')
print(f'links as written: book {len(written(book))}, MkDocs sites {len(written(mk))}')
show('book rows by where', Counter(r['where'] for r in book))
show('book links as written by where', Counter(k[0] == BOOK and 'book repo' or 'content' for k in written(book)))
show('book rows by form', Counter(r['form'] for r in book))
show('book rows by kind', Counter(r['kind'] for r in book))
show('book rows by status', Counter(r['status'] for r in book))

pages = [r for r in book if r['where'] in ('page', 'partial', 'variable')]
print()
print('-- links in content (pages, partials, variable values), per page they render on')
show('kind', Counter(r['kind'] for r in pages))
internal = [r for r in pages if r['target_repo'] or r['status'].startswith('broken')]
show('internal to the book: status', Counter(r['status'] for r in internal))
cross = [r for r in pages if r['crosses'] == 'yes']
print(f'cross a repository boundary: {len(cross)} rows, {len(written(cross))} as written, '
      f'from {len({(r["repo"], r["file"]) for r in cross})} files')
show('  by kind', Counter(r['kind'] for r in cross))
show('  by status', Counter(r['status'] for r in cross))
show('  with a fragment', Counter(bool(r['fragment']) for r in cross))
same = [r for r in pages if r['crosses'] == 'no']
show('same repository: by kind', Counter(r['kind'] for r in same))
show('same repository: by status', Counter(r['status'] for r in same))
broken_cross = [r for r in internal if r['status'].startswith('broken')]
print(f'broken (pages, partials, variables): {len(broken_cross)}; of them crossing: '
      f'{sum(1 for r in broken_cross if r["crosses"] == "yes")}')

print()
print('-- cross-repository links: repository of the page they render on -> target repository (rows)')
m = Counter((r['host_repo'], r['target_repo']) for r in cross)
for (a, b), n in sorted(m.items(), key=lambda x: -x[1]):
    print(f'  {a} -> {b}: {n}')
print()
dirs = {}
for r in pages:
    if r['target_repo'] and r['url_resolved']:
        dirs[r['target_repo']] = r['url_resolved'].strip('/').split('/')[0]
pr = [r for r in cross if r['kind'] == 'page-relative']
names_dir = sum(1 for r in pr if re.search(r'(^|/)\.\./', r['url']))
print(f'page-relative cross links: {len(pr)}; going up with ../: {names_dir}')
own = [r for r in same if r['kind'] == 'page-relative' and
       re.search(r'\.\./(' + re.escape(dirs.get(r['repo'], '@@')) + r')/', r['url'])]
print(f'same-repository links that go up through their own section folder (../<own dir>/): {len(own)}')
for r in own[:10]:
    print('  ', r['repo'], r['file'], r['line'], r['url'])
root_same = [r for r in same if r['kind'] in ('root-relative', 'absolute-docs')]
print(f'same-repository links written root-relative or absolute: {len(root_same)}')

print()
print('-- subnav and layouts')
for w in ('subnav', 'layout'):
    rs = [r for r in book if r['where'] == w]
    show(f'{w}: kind', Counter(r['kind'] for r in rs))
    show(f'{w}: status', Counter(r['status'] for r in rs))
    show(f'{w}: target repository', Counter(r['target_repo'] for r in rs))

print()
print('-- variables')
v = [r for r in book if r['where'] == 'variable']
def vname(r):
    return re.match(r'vars\.(\w+)', r['via']).group(1)


used = {vname(r) for r in v if 'not used' not in r['via']}
print(f'variable values holding a link: {len({vname(r) for r in v})}; used on a page: {len(used)}')
show('kind of the link in the value', Counter(r['kind'] for r in v))
rel = [r for r in v if r['kind'] in ('page-relative',) and 'not used' not in r['via']]
for r in rel:
    print('  relative value:', r['via'], r['url'], '->', r['url_resolved'], r['status'])
show('variable link rows by status', Counter(r['status'] for r in v))

print()
print('-- partials')
p = [r for r in book if r['where'] == 'partial']
show('kind', Counter(r['kind'] for r in p))
show('status', Counter(r['status'] for r in p))
rel = [r for r in p if r['kind'] == 'page-relative']
print(f'page-relative links in partials: {len(rel)} rows')

print()
print('-- fragments')
frag = [r for r in internal if r['fragment']]
show('internal links with a fragment: status', Counter(r['status'] for r in frag))
show('broken anchors by kind', Counter(r['kind'] for r in internal if r['status'] == 'broken: no anchor'))

print()
print('-- absolute links')
ab = [r for r in book if r['kind'].endswith('absolute-other')]
show('hosts (top 15)', Counter(r['host_name'] for r in ab))
bosh = [r for r in book if r['host_name'] == 'bosh.io']
show('bosh.io links: status', Counter(r['status'] for r in bosh))
show('bosh.io links: URL ends', Counter('.html' if re.search(r'\.html(#|$)', r['url']) else '/' if re.search(r'/(#|$)', r['url']) else 'other' for r in bosh))
gh = [r for r in ab if re.match(r'https?://github\.com/cloudfoundry/docs-', r['url'])]
print(f'links to github.com/cloudfoundry/docs-* repositories: {len(gh)}')
ad = [r for r in book if r['kind'] == 'absolute-docs']
show('absolute links to docs.cloudfoundry.org: status', Counter(r['status'] for r in ad))
show('  by where', Counter(r['where'] for r in ad))

print()
print('-- MkDocs sites')
for repo in ('docs-bosh', 'docs-dotnet-core-tutorial'):
    rs = [r for r in mk if r['repo'] == repo]
    show(f'{repo}: kind', Counter(r['kind'] for r in rs))
    show(f'{repo}: status', Counter(r['status'] for r in rs))
    show(f'{repo}: links to docs.cloudfoundry.org', Counter(r['status'] for r in rs if r['kind'] == 'absolute-docs'))

print()
print('-- redirects.rb')
show('rules', Counter(r['code'] for r in reds))
show('target status', Counter(r['target_status'] for r in reds))
show('notes', Counter(r['note'] for r in reds))
show('regex rules', Counter(r['source'].startswith('%r{') for r in reds))
