"""Builds index.html: two outputs of one test-page table side by side, each
side picking Published or a tool and mode, with each side's input below.

Usage: python3 -I build.py

Pages, tools and modes are read from ../compare/build.py; screenshots are
the comparison page's (../compare/img). Inputs are read from the round's
files (concepts/tables/source and concepts/tables/sites), whole and table
by table. The build stops if a file's table count differs from the page's.
"""
import ast, hashlib, html, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
ROUND = os.path.join(REPO, 'concepts', 'tables')
IMG = os.path.join(HERE, '..', 'compare', 'img')


def compare_lists():
    """PAGES, TOOLS and MODES from the comparison page's generator, read without running it."""
    tree = ast.parse(open(os.path.join(HERE, '..', 'compare', 'build.py'), encoding='utf-8').read())
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('PAGES', 'TOOLS', 'MODES', 'ANCHORS'):
            out[node.targets[0].id] = ast.literal_eval(node.value)
    return out['PAGES'], out['TOOLS'], out['MODES'], out['ANCHORS']


PAGES, TOOLS, MODES, ANCHORS = compare_lists()


def input_path(tool, mode, name):
    """The file that holds the page's tables. The scale table lives in a partial."""
    if tool == 'published':
        return f'concepts/tables/source/{name}.html.md.erb'
    if tool == 'docusaurus':
        return f'concepts/tables/sites/docusaurus/docs/{"native" if mode == "native-plain" else mode}/{name}.mdx'
    if tool == 'zensical':
        folder = 'partials' if name.startswith('_') else 'docs'
        return f'concepts/tables/sites/zensical/{folder}/{mode}/{name}.md'
    if tool == 'starlight':
        return f'concepts/tables/sites/starlight/src/content/docs/{mode}/{name}.mdoc'
    folder = 'partials' if name.startswith('_') else 'pages'
    return f'concepts/tables/sites/antora/{mode}/modules/ROOT/{folder}/{name}.adoc'


# A table starts at one of these lines and ends at the first line matching its end
STARTS = [
    (re.compile(r'^\s*<table\b', re.I), re.compile(r'</table>', re.I)),
    (re.compile(r'^\s*\{%\s*table\b'), re.compile(r'\{%\s*/table\s*%\}')),
    (re.compile(r'^\s*:::list-table\b'), re.compile(r'^\s*:::\s*$')),
    (re.compile(r'^\s*///\s*list-table\b'), re.compile(r'^\s*///\s*$')),
    (re.compile(r'^\s*\|===\s*$'), re.compile(r'^\s*\|===\s*$')),
]
PIPE = re.compile(r'^\s*\|')
ATTACHED = re.compile(r'^\s*(\[[^\]]*\]|\.\S.*|\+\+\+\+)\s*$')  # AsciiDoc attribute, block title, passthrough fence


def tables_in(lines):
    """(first, last) line numbers, 1-based, of each table in the file."""
    found, i = [], 0
    while i < len(lines):
        line = lines[i]
        for start, end in STARTS:
            if start.search(line):
                j = i + 1 if start.pattern == end.pattern else i
                while j < len(lines) and not end.search(lines[j]):
                    j += 1
                break
        else:
            if PIPE.match(line):  # a pipe table: the run of lines that start with |
                j = i
                while j + 1 < len(lines) and PIPE.match(lines[j + 1]):
                    j += 1
            else:
                i += 1
                continue
        a = i
        while a > 0 and ATTACHED.match(lines[a - 1]):  # attributes and title written right above
            a -= 1
        b = j
        if b + 1 < len(lines) and lines[b + 1].strip() == '++++':
            b += 1
        found.append((a + 1, b + 1))
        i = j + 1
    return found


def head():
    return subprocess.run(['git', '-C', REPO, 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()


def digest(path):
    return hashlib.sha1(open(path, 'rb').read()).hexdigest()[:12] if os.path.exists(path) else None


def main():
    sha = head()
    texts, pages, problems = {}, [], []
    for slug, name, repo, url, tables in PAGES:
        n = len(tables)
        sides = {}
        for tool, label in [('published', 'Published')] + list(TOOLS):
            for mode in ([None] if tool == 'published' else [m for m, *_ in MODES]):
                path = input_path(tool, mode, name)
                lines = open(os.path.join(REPO, path), encoding='utf-8').read().split('\n')
                spans = tables_in(lines)
                if tool == 'published' and len(spans) > n:  # only the page's first section was converted
                    spans = spans[:n]
                if len(spans) != n:
                    problems.append(f'{path}: {len(spans)} tables, expected {n}')
                texts.setdefault(path, '\n'.join(lines))
                img_mode = 'native' if (tool, mode) == ('docusaurus', 'native-plain') else mode
                shots = [f'{tool}-{img_mode}-{slug}-t{k}.jpg' if mode else f'published-{slug}-t{k}.jpg' for k in range(1, n + 1)]
                sides[f'{tool}/{mode or ""}'] = {
                    'path': path, 'spans': spans,
                    'shots': [s if os.path.exists(os.path.join(IMG, s)) else None for s in shots],
                    'hash': [digest(os.path.join(IMG, s)) for s in shots],
                    # a table that scrolls in its box also has a screenshot of the whole table
                    'full': [s[:-4] + '-full.jpg' if os.path.exists(os.path.join(IMG, s[:-4] + '-full.jpg')) else None for s in shots],
                    'fullhash': [digest(os.path.join(IMG, s[:-4] + '-full.jpg')) for s in shots]}
        pages.append({'slug': slug, 'name': name, 'repo': repo, 'url': url,
                      'tables': [t for t, _ in tables], 'anchors': ANCHORS[slug], 'sides': sides})
    if problems:
        sys.exit('\n'.join(problems))
    data = {'sha': sha, 'pages': pages, 'texts': texts,
            'tools': [['published', 'Published']] + [list(t) for t in TOOLS],
            'modes': [[m, l] for m, l, _ in MODES]}
    page = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    page = page.replace('{{DATA}}', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
    open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(page)
    print(f'{len(pages)} pages, {len(texts)} input files, {len(page) // 1024} KB')


if __name__ == '__main__':
    main()
