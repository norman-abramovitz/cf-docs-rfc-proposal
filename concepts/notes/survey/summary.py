"""Counts behind the notes survey's README, from notes.csv.

Usage:
  python3 -I summary.py notes.csv

Prints, for the book's repositories (every repository but docs-bosh) and
for bosh.io (docs-bosh) apart: notes per form, per class and kind, title
spans and their text, what the notes hold, Markdown inside HTML notes,
notes in lists, tables and partials, and notes per repository.
"""
import csv, sys
from collections import Counter

if len(sys.argv) != 2:
    sys.exit(__doc__)
rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8')))
book = [r for r in rows if r['repo'] != 'docs-bosh']
bosh = [r for r in rows if r['repo'] == 'docs-bosh']


def show(title, counter):
    print(f'{title}:')
    for k, v in counter.most_common():
        print(f'  {v:4}  {k}')


def traits(rs, field):
    c = Counter()
    for r in rs:
        for t in r[field].split():
            c[t] += 1
    c['(none)'] = sum(1 for r in rs if not r[field].strip())
    return c


print(f'== Book repositories: {len(book)} notes')
show('form', Counter(r['form'] for r in book))
html = [r for r in book if r['form'] in ('html', 'variable')]
pages = [r for r in book if r['form'] == 'html']
print(f'-- HTML notes in pages ({len(pages)}) and in variables ({len(html) - len(pages)})')
show('element and class, as written', Counter(f"<{r['tag']} class=\"{r['cls']}\"> ({r['form']})" for r in html))
show('quotes around the class', Counter(r['quotes'] for r in html))
show('title span', Counter(r['title_span'] for r in html))
show('title text', Counter(r['title'] or '(no span)' for r in html))
show('title markup', Counter(r['title_form'] or '(no span)' for r in html))
show('kind and title', Counter(f"{r['kind']} -> {r['title'] or '(no span)'}" for r in html))
show('holds (a note can hold several)', traits(html, 'holds'))
show('Markdown syntax inside the HTML note', traits(html, 'markdown_inside'))
show('paragraphs after the title', Counter(r['paragraphs'] for r in pages))
show('in a list: markdown = indented under a Markdown list item, html = inside an open <li>', Counter(r['in_list'] for r in pages))
show('indent of the opening tag', Counter(r['indent'] for r in pages))
show('in a table', Counter(r['in_table'] for r in pages))
show('in a partial (file name starts with _)', Counter(r['in_partial'] for r in pages))
show('in an archive/ folder', Counter(r['archive'] for r in pages))
show('closed', Counter(r['closed'] for r in pages))
show('closing tag on its own line', Counter(r['close_own_line'] for r in pages))
show('notes per repository', Counter(r['repo'] for r in pages))
print(f'   pages with notes: {len({(r["repo"], r["file"]) for r in pages})}')
show('label paragraphs', Counter(f"{r['kind']} in_list={r['in_list']}" for r in book if r['form'] == 'label'))
show('blockquotes', Counter(r['kind'] for r in book if r['form'] == 'blockquote'))

print(f'\n== bosh.io (docs-bosh): {len(bosh)} notes')
show('form', Counter(r['form'] for r in bosh))
adm = [r for r in bosh if r['form'] == 'admonition']
show('admonition type, as written', Counter(f"{r['tag']} {r['kind']}" for r in adm))
show('with a title', Counter('yes' if r['title'] else 'no' for r in adm))
show('in a list', Counter(r['in_list'] for r in adm))
show('holds', traits(adm, 'holds'))
print(f'   pages with admonitions: {len({r["file"] for r in adm})}')
show('label paragraphs', Counter(f"{r['kind']} in_list={r['in_list']}" for r in bosh if r['form'] == 'label'))
