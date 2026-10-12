# Prints the tables of ../cleanup.md from uses.csv. Usage: python3 cleanup.py <folder with one clone per repository, at the commits in shas.txt>
import csv, os, re, subprocess, sys, collections
C = os.path.dirname(os.path.abspath(__file__)) + '/../../'
REPOS = sys.argv[1]  # folder with one clone per repository
shas = dict(l.split()[:2] for l in open(C + 'variables/survey/shas.txt'))
rows = [r for r in csv.DictReader(open(C + 'variables/survey/uses.csv'))
        if r['kind'] == 'variable' and r['site'] == 'book'
        and (r['defined'] != 'yes' or r['value_kind'] == 'empty')]
assert len(rows) == 82, len(rows)
cache = {}
def line(r):
    k = (r['repo'], r['file'])
    if k not in cache:
        cache[k] = subprocess.run(['git', '-C', f"{REPOS}/{r['repo']}", 'show', f"{shas[r['repo']]}:{r['file']}"],
                                  capture_output=True, text=True, check=True).stdout.split('\n')
    return cache[k][int(r['line']) - 1]
def span(t, name):
    t = t.strip()
    if len(t) > 110:
        i = t.find('vars.' + name)
        a = max(0, min(i - 50, len(t) - 105))
        t = ('…' if a else '') + t[a:a + 105] + ('…' if a + 105 < len(t) else '')
    t = t.replace('|', '\\|')
    return f'`` {t} ``' if '`' in t else f'`{t}`'
by = collections.defaultdict(list)
for r in rows: by[r['repo']].append(r)
for repo in sorted(by):
    rs = sorted(by[repo], key=lambda r: (r['file'], int(r['line'])))
    print(f'## {repo}\n\n| File and line | Name | Kind | Line today | Fix |\n|---|---|---|---|---|')
    for r in rs:
        t = line(r)
        alone = re.fullmatch(r'\s*<%=\s*vars\.\w+\s*%>\s*', t) is not None
        kind = 'not defined' if r['defined'] == 'no' else 'empty'
        fix = 'delete the line' if alone else 'remove the reference'
        print(f"| [{r['file']} L{r['line']}]({r['url']}) | `{r['name']}` | {kind} | {span(t, r['name'])} | {fix} |")
    print()

# Keys with no value: removed from template_variables.yml once the references above are gone.
keys = [v for v in csv.DictReader(open(C + 'variables/survey/values.csv'))
        if v['site'] == 'book' and v['value_kind'] == 'empty']
assert len(keys) == 51, len(keys)
print('## Empty keys\n\n| Key | Line | References today |\n|---|---|---|')
for v in sorted(keys, key=lambda v: int(v['line'])):
    print(f"| `{v['name']}` | [L{v['line']}]({v['url']}) | {v['uses'] if int(v['uses']) else 'none'} |")
