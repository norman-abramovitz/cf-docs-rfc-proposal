"""Print the counts in README.md from calls.csv and partials.csv.

Usage:
  python3 -I summary.py calls.csv partials.csv
"""
import csv, sys
from collections import Counter

if len(sys.argv) != 3:
    sys.exit(__doc__)
calls = list(csv.DictReader(open(sys.argv[1])))
parts = list(csv.DictReader(open(sys.argv[2])))
BOOK = 'docs-book-cloudfoundry'


def show(title, counter):
    print(f'{title}: ' + ', '.join(f'{k} {v}' for k, v in counter.most_common()))


erb = [c for c in calls if c['form'] == 'erb']
content = [c for c in erb if c['repo'] != BOOK]
book = [c for c in erb if c['repo'] == BOOK]
print(f'rows: {len(calls)}; ERB calls {len(erb)} (content {len(content)} in '
      f'{len({(c["repo"], c["file"]) for c in content})} files, book {len(book)}); '
      f'snippets {sum(c["form"] == "snippet" for c in calls)}; comments {sum(c["form"] == "comment" for c in calls)}')
show('content calls per repository', Counter(c['repo'] for c in content))
for k in ('tag', 'quotes', 'name_kind', 'path_style', 'locals', 'in_conditional', 'place', 'where', 'resolved_by'):
    show(f'content calls, {k}', Counter(c[k] for c in content))
show('book calls, where', Counter(c['where'] for c in book))
print('calls not at top level: ' + '; '.join(f'{c["repo"]}/{c["file"]}:{c["line"]} ({c["place"]})'
                                            for c in content if c['place'] != 'top level'))
print('calls that leave the folder: ' + '; '.join(f'{c["repo"]}/{c["file"]}:{c["line"]} {c["name"]}'
                                                 for c in content if c['path_style'] not in ('name',)))

cp = [p for p in parts if p['repo'] != BOOK]
print(f'\npartial files: {len(parts)} (content {len(cp)}, book {len(parts) - len(cp)})')
show('content partials per repository', Counter(p['repo'] for p in cp))
never = [p for p in parts if p['included_times'] == '0' and not p['included_by']]
print('never included: ' + '; '.join(f'{p["repo"]}/{p["file"]}' for p in never))
for k, label in (('headings', 'with headings'), ('notes', 'with notes'), ('tables', 'with tables'),
                 ('code_blocks', 'with code blocks'), ('variables', 'with variables'),
                 ('explicit_ids', 'with explicit ids'), ('partial_calls', 'calling another partial'),
                 ('other_erb', 'with other ERB')):
    hit = [p for p in cp if p[k] != '0']
    print(f'{label}: {len(hit)}' + (': ' + '; '.join(f'{p["file"]} ({p[k]})' for p in hit) if len(hit) <= 12 else ''))
print('with front matter: ' + str(sum(p['front_matter'] == 'yes' for p in parts)))
print('nested depth > 0: ' + str(sum(p['nested_depth'] != '0' for p in cp)))
show('included by how many files (content partials)', Counter(p['included_by_files'] for p in cp))
print('included more than once on one page: ' + '; '.join(f'{p["file"]} ({p["included_times"]} times)'
                                                        for p in cp if p['twice_on_one_page'] == 'yes'))
print('included from more than one file: ' + '; '.join(f'{p["file"]} ({p["included_by"]})'
                                                     for p in cp if int(p['included_by_files']) > 1))
print('included from another repository: ' + str(sum(p['from_other_repo'] == 'yes' for p in parts)))
print('named in a variable: ' + '; '.join(f'{p["file"]} [{p["named_in_variable"]}]' for p in parts if p['named_in_variable']))
