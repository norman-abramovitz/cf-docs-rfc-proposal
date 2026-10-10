"""Groups the table inventory into families and prints a summary.

Usage:
  python3 -I families.py TABLES [OUT_PREFIX]

TABLES is survey.py's OUT_PREFIX.json, or a CSV with the same columns
(tables.csv). Prints one block per family and the traits that cut across
families. With OUT_PREFIX, also writes OUT_PREFIX.json and OUT_PREFIX.csv
with a `family` column added; the input is never changed.
"""
import csv, json, sys, collections as C

INTS = ('line', 'rows', 'body_rows', 'columns', 'row_headers', 'spans', 'cell_styles',
        'nested', 'longest_cell', 'median_cell', 'empty_cells')
BOOLS = ('border', 'table_style', 'header_row', 'spanning_title', 'erb', 'unclosed_thead')


def load(path):
    if path.endswith('.json'):
        return json.load(open(path))
    d = list(csv.DictReader(open(path, newline='', encoding='utf-8')))
    for x in d:
        for k in INTS: x[k] = int(x[k])
        for k in BOOLS: x[k] = x[k] == 'True'
    return d


def fam(x):
    if 'image' in x['kinds']: return 'media'
    if x['columns'] >= 4 and x['median_cell'] <= 5: return 'matrix'
    if x['spanning_title']: return 'titled'
    if x['columns'] == 2: return 'key-value'
    if x['columns'] <= 4: return 'reference-3-4'
    return 'wide'


if len(sys.argv) not in (2, 3):
    sys.exit(__doc__)
d = load(sys.argv[1])
for x in d: x['family'] = fam(x)
if len(sys.argv) == 3:
    out = sys.argv[2]
    json.dump(d, open(out + '.json', 'w'), indent=1)
    with open(out + '.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(d[0].keys())); w.writeheader(); w.writerows(d)
by = C.defaultdict(list)
for x in d: by[x['family']].append(x)
for f, xs in sorted(by.items(), key=lambda kv: -len(kv[1])):
    print(f'== {f}: {len(xs)} (html {sum(x["kind"]=="html" for x in xs)}, pipe {sum(x["kind"]=="pipe" for x in xs)})')
    print('   repos', dict(C.Counter(x['repo'] for x in xs).most_common()))
    br = sorted(x['body_rows'] for x in xs); md = sorted(x['median_cell'] for x in xs); lg = sorted(x['longest_cell'] for x in xs)
    print('   body rows median', br[len(br)//2], 'max', br[-1], '| median cell median', md[len(md)//2], '| longest median', lg[len(lg)//2])
    print('   kinds', dict(C.Counter(k for x in xs for k in x['kinds'].split(',') if k)))
    print('   >=15 rows', sum(x['body_rows'] >= 15 for x in xs), '| short cells (median<=12)', sum(x['median_cell'] <= 12 for x in xs), '| long prose (>300)', sum(x['longest_cell'] > 300 for x in xs))
# traits that cut across families
print('row headers', sum(x['row_headers'] > 0 for x in d), '| cell styles', sum(x['cell_styles'] > 0 for x in d), '| col widths', sum(bool(x['cols']) for x in d), '| border attr', sum(x['border'] for x in d), '| unclosed thead', sum(x['unclosed_thead'] for x in d), '| erb', sum(bool(x['erb']) for x in d))
print('long tables >=15 rows', [(x['repo'], x['file'], x['body_rows'], x['median_cell']) for x in d if x['body_rows'] >= 15])
