# Prints the cleanup tables for links.csv and redirects.csv: links already broken in content, and
# redirect rules whose target is gone, each with a suggested fix where the site model offers one.
# Usage: python3 -I cleanup.py IDS.pkl [BROKEN_LINKS.md]
# IDS.pkl holds survey.py's page_ids (built path -> ids), saved after a run of survey.py.
# Rows whose source line BROKEN_LINKS.md already lists are left out.
import csv, difflib, os, pickle, posixpath, re, sys, collections
D = os.path.dirname(os.path.abspath(__file__))
page_ids = pickle.load(open(sys.argv[1], 'rb'))['page_ids']
listed = set()
if len(sys.argv) > 2:
    listed = set(re.findall(r'github\.com/cloudfoundry/([\w.-]+)/blob/\w+/([^)#]+)#L(\d+)', open(sys.argv[2]).read()))
by_name = collections.defaultdict(list)
for p in page_ids: by_name[posixpath.basename(p)].append(p)

def esc(t): return t.replace('|', '\\|')

def suggest(r):
    frag, page = r['fragment'], r['target_path']
    if r['status'] == 'broken: no anchor':
        near = difflib.get_close_matches(frag, sorted(page_ids.get(page, ())), n=1, cutoff=0.6)
        if near: return f'`#{near[0]}` on the same page (similar id)'
        elsewhere = sorted(p for p, ids in page_ids.items() if frag in ids and p != page)
        if elsewhere: return 'the id is on ' + ', '.join(f'`/{p}`' for p in elsewhere[:3])
        return 'no similar id found; remove the fragment or pick a heading'
    if r['status'] == 'broken: redirect target missing':
        return 'the redirect\'s target is gone; link to the page that now covers it'
    return 'check bosh.io for the heading\'s current id'

PROBLEM = {'broken: no anchor': 'no such id on the target page',
           'broken: redirect target missing': 'redirects to a page that is gone',
           'broken: no anchor (against docs-bosh)': 'no such id on bosh.io'}

rows = [r for r in csv.DictReader(open(f'{D}/links.csv'))
        if r['status'].startswith('broken') and r['where'] in ('page', 'partial')]
assert len(rows) == 55, len(rows)
seen, out, skipped = set(), collections.defaultdict(list), 0
for r in rows:
    k = (r['repo'], r['file'], r['line'], r['url'])
    if k in seen: continue
    seen.add(k)
    if (r['repo'], r['file'], r['line']) in listed: skipped += 1; continue
    out[r['repo']].append(r)
print(f'<!-- {len(rows)} rows, {len(seen)} source links, {skipped} already listed above -->\n')
for repo in sorted(out):
    print(f'#### {repo}\n\n| Source | Link as written | Target page | Problem | Suggested fix |\n|---|---|---|---|---|')
    for r in sorted(out[repo], key=lambda r: (r['file'], int(r['line']))):
        print(f"| [{r['file']} L{r['line']}]({r['gh']}) | `{esc(r['url'])}` | `/{r['target_path']}` | {PROBLEM[r['status']]} | {suggest(r)} |")
    print()

red = [r for r in csv.DictReader(open(f'{D}/redirects.csv')) if r['target_status'] == 'target missing']
assert len(red) == 30, len(red)
print('### Redirect rules whose target is gone\n\n| Rule | From | To (missing) | Suggested target |\n|---|---|---|---|')
for r in sorted(red, key=lambda r: int(r['line'])):
    path = r['target'].split('#')[0].strip('/')
    name = posixpath.basename(path)
    if name == 'index.html':  # match the folder's name, not every index page
        d = posixpath.basename(posixpath.dirname(path))
        cands = sorted(p for p in page_ids if p.endswith(f'/{d}/index.html') or posixpath.basename(p) == f'{d}.html')
    else:
        cands = sorted(by_name.get(name, []))
    s = ', '.join(f'`/{p}`' for p in cands[:3]) if cands else 'none by file name; drop the rule or pick a page'
    print(f"| [L{r['line']}]({r['gh']}) | `{esc(r['source'])}` | `{esc(r['target'])}` | {s} |")
