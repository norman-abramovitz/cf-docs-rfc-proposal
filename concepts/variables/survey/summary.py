"""Counts behind the variable survey's README, from uses.csv and values.csv.

Usage:
  python3 -I summary.py uses.csv values.csv

Prints, for the book (the 12 content repositories), the book repository's
own pages and layouts, bosh.io and the MkDocs tutorial apart: expressions per kind, variable uses
per place and per surrounding element, what the values of the variables
used hold, which variables are used but not defined or defined but unused,
and the uses that need care in a conversion.
"""
import csv, sys
from collections import Counter

if len(sys.argv) != 3:
    sys.exit(__doc__)
rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8')))
vals = list(csv.DictReader(open(sys.argv[2], encoding='utf-8')))
book = [r for r in rows if r['site'] == 'book']
var = [r for r in book if r['kind'] == 'variable']
keys = [v for v in vals if v['site'] == 'book' and v['style'] != 'undefined']
kind_of = {v['name']: v['value_kind'] for v in vals if v['site'] == 'book'}


def show(title, counter):
    print(f'{title}:')
    for k, v in counter.most_common():
        print(f'  {v:5}  {k}')


print(f'== Book pages (the 12 content repositories): {len(book)} ERB expressions')
show('kind', Counter(r['kind'] for r in book))
show('syntax of variable uses', Counter(r['syntax'] for r in var))
print(f'   variable uses: {len(var)} in {len({(r["repo"], r["file"]) for r in var})} files, '
      f'{len({r["name"] for r in var})} names')
show('variable uses per repository', Counter(r['repo'] for r in var))
show('in a file that ERB reads (.erb)', Counter(r['erb_processed'] for r in var))
show('in a partial (file name starts with _)', Counter(r['partial_file'] for r in var))
show('in an archive/ folder', Counter(r['archive'] for r in var))
show('defined', Counter(r['defined'] for r in var))
show('value of the variable used', Counter(r['value_kind'] or 'undefined' for r in var))
show('place', Counter(r['place'] for r in var))
show('place, with detail', Counter(f"{r['place']} {r['detail']}".strip() for r in var))
show('in a table', Counter(r['table'] for r in var))
show('in a note', Counter(r['note'] for r in var))
show('in a list', Counter(r['list'] for r in var))
show('innermost HTML block element around the use', Counter(r['html'] for r in var))
show('relative links in the value: do they reach a page from where the variable is used?',
     Counter(r['links_resolve'].split(':')[0] for r in var if r['links_resolve']))
show('method or expression around the variable', Counter(r['method'] for r in var if r['method']))
show('place x value (defined, non-empty)', Counter(f"{r['place']} / {r['value_kind']}" for r in var if r['defined'] == 'yes'))
show('HTML or Markdown values inside an HTML block element',
     Counter(f"{r['value_kind']} in <{r['html']}>" for r in var if r['defined'] == 'yes' and r['html'] != 'no'
             and ('html' in r['value_kind'] or 'markdown' in r['value_kind'])))

print('\n-- Variables used but not defined (uses, files)')
for v in sorted((v for v in vals if v['style'] == 'undefined'), key=lambda v: (-int(v['uses']), v['name'])):
    print(f'  {v["name"]:34} {v["uses"]:>3} {v["files"]:>3}')
print('-- Variables defined with no value but used (uses)')
for v in sorted((v for v in keys if v['value_kind'] == 'empty' and int(v['uses'])), key=lambda v: v['name']):
    print(f'  {v["name"]:34} {v["uses"]:>3}')

print(f'\n== The variables file: {len(keys)} keys')
show('value', Counter(v['value_kind'] for v in keys))
show('YAML style', Counter(v['style'] for v in keys))
show('HTML elements in values', Counter(e for v in keys for e in v['html_elements'].split()))
show('Markdown in values', Counter(m for v in keys for m in v['markdown'].split()))
print(f'   multi-line values: {sum(v["multiline"] == "yes" for v in keys)}')
print(f'   values with links relative to the page: {sum(bool(v["relative_links"]) for v in keys)}')
print(f'   keys not usable as vars.name: {[v["name"] for v in keys if v["addressable"] == "no"]}')
unused = [v for v in keys if v['uses'] == '0']
show(f'defined but unused by any page ({len(unused)})', Counter(v['value_kind'] for v in unused))
used = [v for v in keys if v['uses'] != '0']
show(f'used by pages ({len(used)})', Counter(v['value_kind'] for v in used))

lay = [r for r in rows if r['site'] == 'book-repo']
print(f'\n== The book repository, its own pages and layouts (docs-book-cloudfoundry): {len(lay)} ERB expressions')
show('kind and name', Counter(f"{r['kind']} {r['name']}" for r in lay))

bh = [r for r in book if r['kind'] in ('helper', 'build-time', 'control', 'comment')]
print('\n-- Helpers, build-time values, control and comments in pages')
for r in bh:
    print(f'  {r["kind"]:10} {r["repo"]}/{r["file"]}:{r["line"]}  {r["syntax"]} {r["expr"][:70]}')

bo = [r for r in rows if r['site'] == 'bosh.io']
print(f'\n== bosh.io (docs-bosh): {len(bo)} ERB tags shown as content')
show('place', Counter(r['place'] for r in bo))
mk = [r for r in rows if r['site'] == 'mkdocs']
print(f'\n== MkDocs tutorial (docs-dotnet-core-tutorial): {len(mk)} {{{{ }}}} expressions')
show('name', Counter(r['name'] for r in mk))
show('place', Counter(r['place'] for r in mk))
