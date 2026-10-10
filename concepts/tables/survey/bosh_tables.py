"""docs-bosh tables and Markdown dialect, at the surveyed commit.

Usage:
  python3 -I bosh_tables.py tables     DOCS_BOSH_CLONE TABLES_CSV [REPO [PREFIX]]  # one row per pipe table
  python3 -I bosh_tables.py constructs DOCS_BOSH_CLONE              # non-standard Markdown counts

DOCS_BOSH_CLONE is a checkout of cloudfoundry/docs-bosh at the commit named in
shas.txt (20a41223...). TABLES_CSV is tables.csv, or the CSV families.py
writes (it needs the `family` column); only rows with repo == REPO (default
docs-bosh) are read, numbered PREFIX1, PREFIX2, ... (default T). For the bpm
pages: a bpm-release clone, the families.py CSV for it, REPO bpm-release,
PREFIX B. Writes CSV to standard output. Reads files only; runs nothing from
the clone.
"""
import csv, os, re, sys, collections

FENCE = re.compile(r'^\s*(```|~~~)')
SEP_CELL = re.compile(r'^\s*:?-+:?\s*$')


def split_pipe(l):
    l = l.strip()
    if l.startswith('|'): l = l[1:]
    if l.endswith('|') and not l.endswith('\\|'): l = l[:-1]
    return [c.strip() for c in re.split(r'(?<!\\)\|', l)]


def strip_code(s):
    return re.sub(r'`[^`]*`', '', s)


def table_features(lines, start, nrows):
    """start: 0-based index of the header line; nrows: header + body rows."""
    hdr = split_pipe(lines[start]); sep = split_pipe(lines[start + 1])
    body = [split_pipe(lines[start + 2 + k]) for k in range(nrows - 1)]
    cells = hdr + [c for r in body for c in r]
    f = {}
    indent = len(lines[start]) - len(lines[start].lstrip())
    f['indent'] = indent
    # container: look back for the block the table sits in
    ctx = []
    if indent:
        for k in range(start - 1, max(-1, start - 40), -1):
            l = lines[k]
            if not l.strip(): continue
            ind = len(l) - len(l.lstrip())
            if ind < indent:
                if re.match(r'\s*(!!!|\?\?\?)', l): ctx.append('admonition')
                elif re.match(r'\s*([-*+]|\d+\.)\s', l): ctx.append('list')
                else: ctx.append('indented')
                break
    prev = [lines[k] for k in range(max(0, start - 4), start) if lines[k].strip()]
    if prev and re.match(r'\s*!!!', prev[0]) or any(re.match(r'\s*!!!', p) for p in prev[-2:]):
        ctx.append('after-admonition')
    f['container'] = ','.join(ctx)
    aligns = []
    for c in sep:
        aligns.append('c' if c.startswith(':') and c.endswith(':') else 'r' if c.endswith(':') else 'l' if c.startswith(':') else '')
    f['align'] = ''.join(a or '.' for a in aligns) if any(aligns) else ''
    tags = collections.Counter(t.lower() for c in cells for t in re.findall(r'<\s*([a-zA-Z][\w-]*)', strip_code(c)))
    f['html'] = ' '.join(f'{t}x{n}' for t, n in sorted(tags.items()))
    f['code'] = sum(len(re.findall(r'`[^`]+`', c)) for c in cells)
    f['links_inline'] = sum(len(re.findall(r'\]\([^)]*\)', c)) for c in cells)
    f['links_ref'] = sum(len(re.findall(r'\]\[[^\]]*\]', c)) for c in cells)
    urls = [u for c in cells for u in re.findall(r'\]\(([^)]*)\)', c)]
    f['longest_url'] = max((len(u) for u in urls), default=0)
    f['abs_site_links'] = sum(1 for u in urls if u.startswith('/'))
    # longest token as rendered (link URLs dropped, markup stripped)
    def rendered(c):
        c = re.sub(r'\]\([^)]*\)|\]\[[^\]]*\]', ']', c)
        c = re.sub(r'<[^>]+>', ' ', c)
        return re.sub(r'[`*\[\]]', '', c)
    f['longest_token'] = max((len(t) for c in cells for t in rendered(c).split()), default=0)
    f['images'] = sum(len(re.findall(r'!\[|<img', c)) for c in cells)
    after = lines[start + nrows + 1] if start + nrows + 1 < len(lines) else ''
    f['attr_after'] = after.strip() if re.match(r'\s*\{:', after) else ''
    f['esc_pipe'] = sum(c.count('\\|') for c in cells)
    f['empty_hdr'] = sum(1 for c in hdr if not c)
    f['empty_body'] = sum(1 for r in body for c in r if not c)
    f['spacer_rows'] = sum(1 for r in body if not any(r))
    f['bold_hdr'] = sum(1 for c in hdr if re.fullmatch(r'\*\*.*\*\*', c))
    f['bold_col1'] = sum(1 for r in body if r and re.fullmatch(r'\*\*.*\*\*', r[0]))
    f['bold_rows'] = sum(1 for r in body if any(r) and all(re.fullmatch(r'\*\*.*\*\*', c) for c in r if c))
    f['footnote_refs'] = sum(len(re.findall(r'\[\^[^\]]+\]', c)) for c in cells)
    f['sup_marks'] = sum(len(re.findall(r'<sup>', c)) for c in cells)
    f['bare_angle'] = sum(len(re.findall(r'<(?!/?(br|sup|sub|a|code|b|i|em|strong)\b)[a-z][^>]*>', strip_code(c))) for c in cells)
    f['stars'] = sum(len(re.findall(r'(?<!\*)\*(?!\*)', strip_code(c))) for c in cells)
    f['symbols'] = ''.join(sorted({ch for c in cells for ch in c if ord(ch) > 127}))
    f['header'] = ' / '.join(hdr)
    return f


def cmd_tables(clone, csvpath, repo='docs-bosh', prefix='T'):
    rows = [r for r in csv.DictReader(open(csvpath)) if r['repo'] == repo]
    keys = None
    w = csv.writer(sys.stdout)
    for i, r in enumerate(rows, 1):
        lines = open(os.path.join(clone, r['file']), encoding='utf-8').read().split('\n')
        f = table_features(lines, int(r['line']) - 1, int(r['rows']))
        out = {'n': f'{prefix}{i}', 'file': r['file'], 'line': r['line'], 'cols': r['columns'],
               'body_rows': r['body_rows'], 'family': r['family'], **f}
        if keys is None:
            keys = list(out); w.writerow(keys)
        w.writerow([out[k] for k in keys])


def prose_lines(path):
    """Lines outside fenced code blocks, with inline code removed."""
    fence = None; comment = False
    for n, l in enumerate(open(path, encoding='utf-8'), 1):
        m = FENCE.match(l)
        if m and not comment:
            if fence is None: fence = m.group(1); continue
            if l.strip().startswith(fence): fence = None; continue
        if fence: continue
        raw = l.rstrip('\n')
        # drop HTML comments, including ones spanning lines
        if comment:
            if '-->' not in raw: continue
            raw = raw.split('-->', 1)[1]; comment = False
        raw = re.sub(r'<!--.*?-->', '', raw)
        if '<!--' in raw: raw = raw.split('<!--', 1)[0]; comment = True
        yield n, raw, strip_code(raw)


CONSTRUCTS = [
    # name, regex on prose line (code removed), extension that needs it
    ('admonition !!!', r'^\s*!!!\s*\w+', 'admonition'),
    ('collapsible ???', r'^\s*\?\?\?\+?\s*\w+', 'pymdownx.details (not enabled)'),
    ('content tabs ===', r'^\s*===\+?\s*"', 'pymdownx.tabbed (not enabled)'),
    ('snippet --8<--', r'--8<--', 'pymdownx.snippets'),
    ('heading attr {: #id }', r'^#{1,6} .*\{:?\s*#[\w-]+[^}]*\}\s*$', 'attr_list'),
    ('other attr_list {: ...} (not on a heading)', r'^(?!#).*\{:\s*[.#\w][^}]*\}', 'attr_list'),
    ('def_list term/definition (": ")', r'RAW^:\s{1,3}\S', 'def_list'),
    ('footnote ref [^x]', r'\[\^[^\]]+\](?!:)', 'footnotes'),
    ('footnote def [^x]:', r'^\[\^[^\]]+\]:', 'footnotes'),
    ('task list - [ ]', r'^\s*[-*]\s\[[ xX]\]\s', 'pymdownx.tasklist'),
    ('mark ==x==', r'(?<![=\w])==[^=\s][^=]*==(?!=)', 'pymdownx.mark'),
    ('caret ^^x^^ / ^x^', r'\^\^[^^]+\^\^|(?<![\w\[^])\^[^\s^]+\^', 'pymdownx.caret'),
    ('tilde ~~x~~', r'~~[^~]+~~', 'pymdownx.tilde'),
    ('critic {++ {-- {~~ {== {>>', r'\{(\+\+|--|~~|==|>>)', 'pymdownx.critic'),
    ('emoji :name:', r'(?<![\w:/]):[a-z0-9_+-]+:(?![\w/])', 'pymdownx.emoji'),
    ('inlinehilite `#!lang`', None, 'pymdownx.inlinehilite'),
    ('math $$ or \\( \\)', r'\$\$|\\\(|(?<![\w$])\$[^$\s][^$]*\$(?![\w$])', 'pymdownx.arithmatex'),
    ('bare URL (magiclink)', r'^(?!\s*\[[^\]]+\]:).*?(?<![(<\["\'=])\bhttps?://[^\s)>\]]+', 'pymdownx.magiclink'),
    ('HTML comment <!-- -->', r'RAW<!--', 'raw HTML'),
    ('smartsymbols (c) (tm) --> +/- 1st', r'\((c|r|tm)\)|(?<!-)-->|(?<!8)<--(?!-)|\+/-|=/=|(?<!\w)\d+(st|nd|rd|th)\b|\b[13]/[24]\b', 'pymdownx.smartsymbols'),
    ('raw HTML <a id/name>', r'<a\s+(id|name)=', 'raw HTML'),
    ('raw HTML <br>', r'<br\s*/?>', 'raw HTML'),
    ('raw HTML <sup>/<sub>', r'<su[pb]>', 'raw HTML'),
    ('raw HTML block <div|<details|<svg|<img', r'<(div|details|svg|img|span|p)\b', 'raw HTML'),
    ('markdown="1" (md_in_html)', r'markdown="(1|block|span)"', 'md_in_html (not enabled)'),
    ('reference link definition', r'^\s*\[[^\]^]+\]:\s*\S', 'core'),
    ('image ![', r'!\[', 'core'),
    ('link to bosh.io app path (/stemcells /releases /jobs /packages /d/)', r'\]\(/(stemcells|releases|jobs|packages|d)/', 'cross-site'),
    ('absolute https://bosh.io link', r'https?://(www\.)?bosh\.io', 'cross-site'),
    ('Jinja/macro {{ }} or {% %}', r'\{\{|\{%', 'macros (not enabled)'),
    ('indented code fence (superfences in list/admonition)', None, 'pymdownx.superfences'),
]


def cmd_constructs(clone):
    root = os.path.join(clone, 'content')
    files = []
    for dp, dn, fn in os.walk(root):  # bpm/ is a symlink into a submodule; not followed
        files += [os.path.join(dp, f) for f in fn if f.endswith('.md')]
    counts = collections.Counter(); pages = collections.defaultdict(set)
    fences = indented = 0; inl = 0
    for p in files:
        rel = os.path.relpath(p, clone)
        for n, raw, l in prose_lines(p):
            inl_hits = len(re.findall(r'`#!\w+ ', raw))
            if inl_hits: counts['inlinehilite `#!lang`'] += inl_hits; pages['inlinehilite `#!lang`'].add(rel)
            for name, rx, _ in CONSTRUCTS:
                if rx is None: continue
                text = l
                if rx.startswith('RAW'):
                    rx = rx[3:]; text = open(p, encoding='utf-8').read().split('\n')[n - 1]
                hits = len(re.findall(rx, text))
                if hits: counts[name] += hits; pages[name].add(rel)
        for l in open(p, encoding='utf-8'):
            m = FENCE.match(l)
            if m:
                fences += 1
                if l.startswith(' ') or l.startswith('\t'):
                    indented += 1; pages['indented code fence (superfences in list/admonition)'].add(rel)
    counts['indented code fence (superfences in list/admonition)'] = indented // 2
    print(f'{len(files)} Markdown files under content/ (bpm/ not followed); {fences // 2} fenced code blocks')
    print('| Construct | Needs | Count | Pages |')
    print('|---|---|---|---|')
    for name, _, ext in CONSTRUCTS:
        print(f'| {name} | {ext} | {counts[name]} | {len(pages[name])} |')
    adm = collections.Counter()
    for p in files:
        for n, raw, l in prose_lines(p):
            m = re.match(r'^\s*!!!\s*(\w+)', l)
            if m: adm[m.group(1)] += 1
    print('admonition types:', dict(adm.most_common()))
    titled = indented_adm = 0
    for p in files:
        for n, raw, l in prose_lines(p):
            if re.match(r'^\s*!!!\s*\w+\s+"', raw): titled += 1
            if re.match(r'^\s+!!!', raw): indented_adm += 1
    print('admonitions with a quoted title:', titled, '| indented (inside a list or block):', indented_adm)


if __name__ == '__main__':
    if len(sys.argv) in (4, 5, 6) and sys.argv[1] == 'tables': cmd_tables(*sys.argv[2:6])
    elif len(sys.argv) == 3 and sys.argv[1] == 'constructs': cmd_constructs(sys.argv[2])
    else: sys.exit(__doc__)
