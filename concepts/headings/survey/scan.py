"""Inventory every heading in the cloned repositories.

Usage:
  python3 -I scan.py REPOS_DIR SHAS OUT_PREFIX

REPOS_DIR holds one clone per line of SHAS, named as in SHAS. SHAS has lines
`<name> <commit> <date>`; the commit goes into each row's GitHub link. Pages
are the files the table survey reads (../../tables/survey/survey.py): `.md`,
`.erb`, `.html`, `.haml`, `.markdown`, `.mdx` and `.adoc`, minus Markdown
files at a repository's root, in every folder but `.git`, `node_modules` and
`vendor`.

Outside front matter, fenced code blocks, `<pre>` blocks and HTML comments it
finds Markdown ATX headings (`#` to `######` at the start of a line, at most
three spaces in, with or without a space after the `#`s) and HTML `<h1>` to
`<h6>` elements. A fence closes at the next line that starts with the same
fence character, whatever its length and whatever follows it. Setext
underlines (`===` or `---` under a line of text) and `#` lines indented four
or more spaces are counted per page but not taken as headings.

Writes OUT_PREFIX.csv (one row per heading) and OUT_PREFIX-pages.csv (one row
per page, pages without headings included) and prints the totals. Reads
files only; runs nothing from the clones.
"""
import collections, csv, os, re, sys

if len(sys.argv) != 4:
    sys.exit(__doc__)
REPOS, SHAS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
EXTS = ('.md', '.erb', '.html', '.haml', '.markdown', '.mdx', '.adoc')
SKIP_DIRS = ('.git', 'node_modules', 'vendor')
sha = dict(l.split()[:2] for l in open(SHAS) if l.strip())

FENCE = re.compile(r'^\s*(`{3,}|~{3,})')
ATX = re.compile(r'^( {0,3})(#{1,6})(?!#)(.*)$')
INDENTED_HASH = re.compile(r'^(?: {4,}|\t)\s*#')
SETEXT = re.compile(r'^ {0,3}(=+|-+)\s*$')
HTML_H = re.compile(r'<h([1-6])\b([^>]*)>(.*?)</h\1\s*>', re.I | re.S)
ANCHOR = re.compile(r'<a\b[^>]*?\b(?:id|name)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))[^>]*>', re.I)
ANCHOR_LINE = re.compile(r'^\s*(?:<a\b[^>]*>\s*</a>\s*)+$', re.I)
ATTR_ID = re.compile(r'\bid\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))', re.I)
ERB = re.compile(r'<%.*?%>', re.S)
TAG = re.compile(r'<[^>]*>')
LINK = re.compile(r'\]\(|\]\[|<a\b[^>]*\bhref\s*=', re.I)


def ids(found):
    """The value of each (double, single, unquoted) match."""
    return [next((g for g in m if g), '') for m in found]


def strip_tags(s):
    """Removes HTML tags, keeps ERB tags as written, collapses spaces."""
    keep = []
    s = ERB.sub(lambda m: keep.append(m.group(0)) or f'\0{len(keep) - 1}\0', s)
    s = TAG.sub('', s)
    s = re.sub(r'\0(\d+)\0', lambda m: keep[int(m.group(1))], s)
    return ' '.join(s.split())


def mask(lines):
    """Returns (lines with skipped regions blanked, count of #-lines indented 4+ outside them)."""
    out = list(lines); fence = None; pre = comment = False; indented = 0; start = 0
    if lines and lines[0].strip() == '---':  # YAML front matter
        for j in range(1, len(lines)):
            if lines[j].strip() in ('---', '...'):
                for k in range(j + 1): out[k] = ''
                start = j + 1
                break
    for i in range(start, len(lines)):
        l = lines[i]
        skip = fence is not None or pre or comment
        m = FENCE.match(l)
        if fence is None and not pre and not comment and m:
            fence = m.group(1); skip = True
        elif fence is not None and m and m.group(1)[0] == fence[0]:  # as the book's engine: any length, any text after
            fence = None; skip = True
        if fence is None and not comment:
            if re.search(r'<pre\b', l, re.I): pre = True; skip = True
            if pre and re.search(r'</pre\s*>', l, re.I): pre = False; skip = True
        if fence is None and not pre:
            if '<!--' in l and '-->' not in l[l.index('<!--'):]: comment = True; skip = True
            elif comment and '-->' in l: comment = False; skip = True
            elif '<!--' in l: l = re.sub(r'<!--.*?-->', '', l); out[i] = l
        if skip: out[i] = ''
        elif INDENTED_HASH.match(l): indented += 1
    return out, indented


def setext(masked):
    """Counts lines of only = or - under a text line that is not a list item or table row."""
    return sum(1 for i in range(1, len(masked)) if SETEXT.match(masked[i]) and masked[i - 1].strip()
               and not re.match(r'^\s*([-*+]\s|\d+\.\s|\|)', masked[i - 1]))


def scan(repo, path, text):
    lines = text.split('\n')
    masked, indented = mask(lines)
    heads = []
    for i, l in enumerate(masked):
        m = ATX.match(l)
        if not m: continue
        raw = m.group(3)
        no_space = bool(raw) and not raw[0].isspace()
        raw = re.sub(r'\s+#+\s*$', '', raw).strip()  # optional closing #s
        found = ids(ANCHOR.findall(raw)); src = 'inline' if found else ''
        if not found and i > 0 and ANCHOR_LINE.match(masked[i - 1]):
            found = ids(ANCHOR.findall(masked[i - 1])); src = 'line-before'
        heads.append(dict(line=i + 1, level=len(m.group(2)), kind='markdown', raw=raw,
                          ids=found, id_source=src, no_space=no_space))
    joined = '\n'.join(masked)
    for m in HTML_H.finditer(joined):
        line = joined.count('\n', 0, m.start()) + 1
        raw = m.group(3)
        found = ids(ATTR_ID.findall(m.group(2))); src = 'attribute' if found else ''
        if not found:
            found = ids(ANCHOR.findall(raw)); src = 'inline' if found else ''
        if not found and line > 1 and ANCHOR_LINE.match(masked[line - 2]):
            found = ids(ANCHOR.findall(masked[line - 2])); src = 'line-before'
        heads.append(dict(line=line, level=int(m.group(1)), kind='html', raw=raw,
                          ids=found, id_source=src, no_space=False))
    heads.sort(key=lambda h: h['line'])
    base = f'https://github.com/cloudfoundry/{repo}/blob/{sha[repo]}/{path}'
    rows = []; skips = []; prev = None
    for h in heads:
        skipped = prev is not None and h['level'] > prev + 1
        if skipped: skips.append(h['line'])
        prev = h['level']
        raw = h['raw']
        rows.append(dict(repo=repo, file=path, line=h['line'], level=h['level'], kind=h['kind'],
                         ids=' '.join(h['ids']), id_source=h['id_source'], text=strip_tags(raw),
                         code='`' in raw or bool(re.search(r'<code\b', raw, re.I)),
                         link=bool(LINK.search(raw)), erb='<%' in raw, no_space=h['no_space'],
                         skipped_level=skipped, url=f"{base}#L{h['line']}"))
    levels = collections.Counter(h['level'] for h in heads)
    page = dict(repo=repo, file=path, partial=os.path.basename(path).startswith('_'),
                headings=len(heads), first_level=heads[0]['level'] if heads else '',
                levels=' '.join(f'h{k}:{levels[k]}' for k in sorted(levels)),
                markdown=sum(h['kind'] == 'markdown' for h in heads),
                html=sum(h['kind'] == 'html' for h in heads),
                with_id=sum(bool(h['ids']) for h in heads),
                without_id=sum(not h['ids'] for h in heads),
                skipped_levels=len(skips), first_skip_line=skips[0] if skips else '',
                indented_hash_lines=indented, setext_lines=setext(masked), url=base)
    return rows, page


heads, pages = [], []
for repo in sorted(sha):
    root = os.path.join(REPOS, repo)
    if not os.path.isdir(root):
        sys.exit(f'missing clone: {root}')
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(d for d in dn if d not in SKIP_DIRS)
        for f in sorted(fn):
            if not f.endswith(EXTS): continue
            if dp == root and f.endswith(('.md', '.markdown')): continue  # root notes and READMEs: no site publishes them
            full = os.path.join(dp, f); rel = os.path.relpath(full, root).replace(os.sep, '/')
            text = open(full, encoding='utf-8', errors='replace').read()
            rows, page = scan(repo, rel, text)
            heads += rows; pages.append(page)


def write(path, data):
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(data[0].keys())); w.writeheader(); w.writerows(data)


write(OUT + '.csv', heads)
write(OUT + '-pages.csv', pages)

by = lambda k: dict(sorted(collections.Counter(h[k] for h in heads).items()))
print(f'{len(sha)} repositories, {len(pages)} pages, {sum(p["headings"] > 0 for p in pages)} with headings')
print(f'{len(heads)} headings; by level {by("level")}; by kind {by("kind")}')
print(f'with explicit ids {sum(bool(h["ids"]) for h in heads)}, without {sum(not h["ids"] for h in heads)}; '
      f'id source {by("id_source")}')
for k in ('code', 'link', 'erb', 'no_space', 'skipped_level'):
    hs = [h for h in heads if h[k]]
    print(f'{k}: {len(hs)} headings on {len({(h["repo"], h["file"]) for h in hs})} pages')
fl = collections.Counter(p['first_level'] for p in pages if p['headings'])
print('first heading level', dict(sorted(fl.items())))
print('pages with HTML headings', [(p['repo'], p['file'], p['html']) for p in pages if p['html']])
print('pages with skipped levels', [(p['repo'], p['file'], p['skipped_levels']) for p in pages if p['skipped_levels']])
print('#-lines indented 4 or more spaces, not counted:', sum(p['indented_hash_lines'] for p in pages))
print('setext underlines, not counted:', sum(p['setext_lines'] for p in pages))
