"""Print the survey's counts from blocks.csv, rendered.csv and commonmark.csv.

Usage: python3 -I summary.py BLOCKS.csv RENDERED.csv COMMONMARK.csv

Counts are for the book (the 14 repositories other than docs-bosh, and the
book repository) unless a line says bosh.io.
"""
import csv, sys
from collections import Counter, defaultdict

if len(sys.argv) != 4:
    sys.exit(__doc__)
rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8')))
rendered = list(csv.DictReader(open(sys.argv[2], encoding='utf-8')))
cmark = list(csv.DictReader(open(sys.argv[3], encoding='utf-8')))
book = [r for r in rows if r['area'] == 'book']
bosh = [r for r in rows if r['area'] == 'bosh.io']
fences = [r for r in book if r['form'] in ('fence', 'fence-tilde')]
pres = [r for r in book if r['form'] in ('pre', 'pre-code')]


def show(title, counter):
    print(f'{title}:')
    for k, v in counter.most_common():
        print(f'  {v:5}  {k}')


print(f'Code blocks: {len(rows)}; book {len(book)}, bosh.io {len(bosh)}')
show('Book, by form', Counter(r['form'] for r in book))
show('Book, by repository', Counter(r['repo'] for r in book))
print(f'Book, in archive/ folders: {sum(1 for r in book if r["archive"])}; in partials: {sum(1 for r in book if r["partial"])}')
show('bosh.io, by form and info string', Counter((r['form'], r['language']) for r in bosh))

print()
print(f'Fences: {len(fences)}; with an info string {sum(1 for r in fences if r["language"])}')
show('Fences, by info string (first word, lower case)', Counter(r['language'] or '(none)' for r in fences))
show('Fences, info string as written -> Rouge lexer the book uses', Counter((r['info'] or '(none)', r['lexer'] or '(not a code block in the book)') for r in fences))
show('Fences, how they close', Counter(r['close'] for r in fences))
show('Fences, place', Counter(r['place'] for r in fences))
show('Fences, indentation of the opening line', Counter(r['indent'] for r in fences))

print()
show('<pre>, attributes as written', Counter((r['form'], r['info']) for r in pres))
show('<pre>, place', Counter(r['place'] for r in pres))
print(f'<pre> with HTML elements inside (other than the <code> wrapper): {sum(1 for r in pres if r["markup"])}')
print(f'<pre> with character references (&lt; &#95; ...): {sum(1 for r in pres if r["entities"])}; fences with them: {sum(1 for r in fences if r["entities"])}')
print(f'<pre> with a blank line inside: {sum(1 for r in pres if r["blank_line"])}; of them in a list: {sum(1 for r in pres if r["blank_line"] and r["place"] in ("list", "html-list"))}')
print(f'<pre> with characters Markdown reads (* _ `): {sum(1 for r in pres if r["md_chars"])}; with {{ or }}: {sum(1 for r in pres if r["braces"])}')

print()
show('Places of every block', Counter((r['place'], r['form']) for r in book))
show('Variables inside code: blocks, by form', Counter(r['form'] for r in book if r['erb_vars']))
print(f'Variables inside code: uses {sum(int(r["erb_vars"] or 0) for r in book)}; other ERB inside code: {sum(int(r["erb_other"] or 0) for r in book)}; escaped <%%: {sum(int(r["erb_escaped"] or 0) for r in book)}')
print(f'Blocks with {{{{, {{% or {{#: {sum(1 for r in book if r["jinja_markdoc"])}; with tab characters: {sum(1 for r in book if r["tabs"])}')

print()
show('First line starts with a prompt, by form and language', Counter((r['form'], r['language'] or '(none)', r['prompt_first']) for r in book if r['prompt_first']))
show('Blocks with a $ prompt and output lines, by form and language', Counter((r['form'], r['language'] or '(none)') for r in book if r['prompt_lines'] and r['output_lines'] not in ('', '0')))
show('console fences: first line a prompt?', Counter('yes' if r['prompt_first'] else 'no' for r in fences if r['language'] == 'console'))
show('<pre class="terminal">: first line a prompt?', Counter('yes' if r['prompt_first'] else 'no' for r in pres if 'terminal' in r['info']))

print()
print(f'The book model: {len(rendered)} code blocks; commonmark.js: {len(cmark)}')
show('Book model, language as written -> lexer', Counter((r['language'] or '(none)', r['lexer']) for r in rendered))
show('Book vs CommonMark, per block (book kind, CommonMark kind, form)', Counter((r['book'], r['cm'], r['form']) for r in book if r['book'] != r['cm']))
print(f'Fences right after a line of text (not code blocks in the book): {sum(1 for r in fences if r["after_text"])}')
by_file = defaultdict(lambda: [[], []])
for r in rendered:
    by_file[(r['repo'], r['file'])][0].append((r['first_line'], r['lines']))
for r in cmark:
    by_file[(r['repo'], r['file'])][1].append((r['first_line'], r['lines']))
diff = sorted(k for k, (a, b) in by_file.items() if [x[0] for x in a] != [x[0] for x in b])
lines_only = sorted(k for k, (a, b) in by_file.items() if [x[0] for x in a] == [x[0] for x in b] and a != b)
print(f'Files where the two parsers find different code blocks: {len(diff)}')
for k in diff:
    a, b = by_file[k]
    print(f'  {k[0]}/{k[1]}: book {len(a)}, CommonMark {len(b)}')
print(f'Files where they find the same blocks but a block has another line count: {len(lines_only)}')
for k in lines_only:
    print(f'  {k[0]}/{k[1]}')
