"""Inventory every HTML and pipe table in the cloned repositories.

Usage:
  python3 -I survey.py REPOS_DIR SHAS OUT_PREFIX

REPOS_DIR holds one clone per line of SHAS, named as in SHAS (a name that
starts with `cft-` is a cloudfoundry-tutorials repository, minus the prefix).
SHAS has lines `<name> <commit> <date>`; the commit goes into each row's
GitHub link. Writes OUT_PREFIX.json and OUT_PREFIX.csv, one row per table,
and prints the count. Reads files only; runs nothing from the clones.
"""
import csv, json, os, re, sys
from html.parser import HTMLParser

if len(sys.argv) != 4:
    sys.exit(__doc__)
REPOS, SHAS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
EXTS = ('.md', '.erb', '.html', '.haml', '.markdown', '.mdx', '.adoc')
sha = dict(l.split()[:2] for l in open(SHAS) if l.strip())
ORG = {r: ('cloudfoundry-tutorials', r[4:]) if r.startswith('cft-') else ('cloudfoundry', r) for r in sha}

FENCE = re.compile(r'^\s*(```|~~~)')
SEP = re.compile(r'^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$|^\s*\|\s*:?-{2,}:?\s*\|\s*$')
IAL = re.compile(r'^\s*\{:\s*([^}]*)\}\s*$')


class T(HTMLParser):
    """Parses one top-level <table> fragment (nested tables counted, not descended into for rows)."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0; self.attrs = {}; self.rows = []; self.cur = None; self.cell = None
        self.in_thead = False; self.cols = []; self.nested = 0; self.cell_styles = 0; self.spans = 0
        self.kinds = set(); self.cells = []; self.thead_closed = False

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == 'table':
            self.depth += 1
            if self.depth == 1: self.attrs = a
            else: self.nested += 1; self.kinds.add('nested-table')
            return
        if self.depth != 1:
            return
        if tag == 'thead': self.in_thead = True
        elif tag == 'col': self.cols.append(a.get('width') or a.get('style') or '')
        elif tag == 'tr': self.cur = {'thead': self.in_thead, 'cells': []}; self.rows.append(self.cur)
        elif tag in ('td', 'th'):
            if self.cur is None: self.cur = {'thead': False, 'cells': []}; self.rows.append(self.cur)
            self.cell = {'tag': tag, 'text': '', 'scope': a.get('scope'), 'colspan': a.get('colspan'), 'rowspan': a.get('rowspan'), 'kinds': set(), 'style': a.get('style') or a.get('width') or a.get('align')}
            self.cur['cells'].append(self.cell)
            if a.get('colspan') not in (None, '1') or a.get('rowspan') not in (None, '1'): self.spans += 1
            if self.cell['style']: self.cell_styles += 1
        elif self.cell is not None:
            k = {'code': 'code', 'pre': 'code', 'ul': 'list', 'ol': 'list', 'p': 'paragraph', 'br': 'br',
                 'img': 'image', 'a': 'link', 'strong': 'bold', 'b': 'bold', 'em': 'italic'}.get(tag)
            if k: self.cell['kinds'].add(k); self.kinds.add(k)

    def handle_endtag(self, tag):
        if tag == 'table': self.depth -= 1
        elif self.depth == 1:
            if tag == 'thead': self.in_thead = False; self.thead_closed = True
            elif tag in ('td', 'th'): self.cell = None

    def handle_data(self, d):
        if self.depth == 1 and self.cell is not None: self.cell['text'] += d


def html_tables(text):
    """Yields (offset, fragment) for each top-level <table>…</table>."""
    out, depth, start = [], 0, None
    for m in re.finditer(r'<table\b|</table\s*>', text, re.I):
        if m.group(0).lower().startswith('<table'):
            if depth == 0: start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0 and start is not None:
                out.append((start, text[start:m.end()])); start = None
            depth = max(depth, 0)
    if start is not None: out.append((start, text[start:]))  # unclosed
    return out


def raw_class(frag):
    m = re.match(r'<table\b([^>]*)>', frag, re.I | re.S)
    head = m.group(1) if m else ''
    c = re.search(r'class\s*=\s*(["“”\'][^"“”\'>]*["“”\']?|[^\s>]+)', head)
    return (c.group(1) if c else ''), head.strip()


def row(repo, path, line, **kw):
    org, name = ORG[repo]
    base = dict(repo=repo, file=path, line=line, url=f'https://github.com/{org}/{name}/blob/{sha[repo]}/{path}#L{line}')
    base.update(kw); return base


def scan_html(repo, path, text):
    for off, frag in html_tables(text):
        line = text.count('\n', 0, off) + 1
        p = T(); p.feed(frag)
        cls, head = raw_class(frag)
        rows = p.rows
        unclosed_thead = sum(r['thead'] for r in rows) > 1 and not p.thead_closed
        if unclosed_thead:  # browsers keep every row in the thead; count rows after the first as data
            for r in rows[1:]: r['thead'] = False
        body = [r for r in rows if not r['thead']]
        header_row = any(r['thead'] for r in rows) or (rows and all(c['tag'] == 'th' for c in rows[0]['cells']) and rows[0]['cells'])
        first_th = rows[0] if rows and all(c['tag'] == 'th' for c in rows[0]['cells']) else None
        data_rows = [r for r in rows if not r['thead'] and r is not first_th]
        row_headers = sum(1 for r in data_rows if r['cells'] and r['cells'][0]['tag'] == 'th')
        spanning_title = bool(rows and len(rows[0]['cells']) == 1 and (rows[0]['cells'][0]['colspan'] or '1') != '1')
        ncols = max((sum(int(c['colspan'] or 1) if str(c['colspan'] or '1').isdigit() else 1 for c in r['cells']) for r in rows), default=0)
        texts = [' '.join(c['text'].split()) for r in rows for c in r['cells']]
        lens = [len(t) for t in texts]
        erb = '<%' in frag
        yield row(repo, path, line, kind='html', cls=cls, attrs=re.sub(r'\s+', ' ', head)[:200],
                  border=bool(re.search(r'\bborder\s*=', head)), table_style=bool(re.search(r'\bstyle\s*=', head)),
                  cols=';'.join(p.cols), rows=len(rows), body_rows=len(data_rows), columns=ncols,
                  header_row=bool(header_row), row_headers=row_headers, spanning_title=spanning_title,
                  spans=p.spans, cell_styles=p.cell_styles, kinds=','.join(sorted(p.kinds)),
                  nested=p.nested, longest_cell=max(lens, default=0), median_cell=sorted(lens)[len(lens)//2] if lens else 0,
                  empty_cells=sum(1 for t in texts if not t), erb=erb, unclosed_thead=unclosed_thead,
                  sample=' | '.join(texts[:4])[:160])


def split_pipe(l):
    l = l.strip()
    if l.startswith('|'): l = l[1:]
    if l.endswith('|') and not l.endswith('\\|'): l = l[:-1]
    return [c.strip() for c in re.split(r'(?<!\\)\|', l)]


def scan_pipe(repo, path, lines):
    fence = False; i = 0
    while i < len(lines):
        l = lines[i]
        if FENCE.match(l): fence = not fence; i += 1; continue
        if fence or i == 0 or not SEP.match(l) or '|' not in lines[i-1]:
            i += 1; continue
        hdr = split_pipe(lines[i-1]); start = i - 1
        # IAL on the line before the header (block IAL) or right after the table
        ial_before = IAL.match(lines[start-1]).group(1) if start > 0 and IAL.match(lines[start-1]) else ''
        body = []; j = i + 1
        while j < len(lines) and '|' in lines[j] and lines[j].strip() and not FENCE.match(lines[j]):
            body.append(split_pipe(lines[j])); j += 1
        ial_after = IAL.match(lines[j]).group(1) if j < len(lines) and IAL.match(lines[j]) else ''
        cells = [c for r in body for c in r] + hdr
        kinds = set()
        for c in cells:
            if '`' in c or '<code' in c: kinds.add('code')
            if re.search(r'<br\s*/?>', c): kinds.add('br')
            if re.search(r'<(ul|ol|li)\b', c): kinds.add('list')
            if re.search(r'!\[|<img', c): kinds.add('image')
            if re.search(r'\]\(|<a\s', c): kinds.add('link')
            if '**' in c or '<strong' in c: kinds.add('bold')
        lens = [len(c) for c in cells]
        ial = (ial_before + ' ' + ial_after).strip()
        yield row(repo, path, start + 1, kind='pipe', cls=' '.join(re.findall(r'\.([\w-]+)', ial)), attrs=ial,
                  border=False, table_style='style' in ial, cols='', rows=len(body) + 1, body_rows=len(body),
                  columns=max([len(hdr)] + [len(r) for r in body]), header_row=any(h for h in hdr),
                  row_headers=0, spanning_title=False, spans=0, cell_styles=0, kinds=','.join(sorted(kinds)),
                  nested=0, longest_cell=max(lens, default=0), median_cell=sorted(lens)[len(lens)//2] if lens else 0,
                  empty_cells=sum(1 for c in cells if not c), erb=any('<%' in c for c in cells), unclosed_thead=False,
                  sample=' | '.join(hdr)[:160])
        i = j


out = []
for repo in sorted(sha):
    root = os.path.join(REPOS, repo)
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ('.git', 'node_modules', 'vendor')]
        for f in fn:
            if not f.endswith(EXTS): continue
            if dp == root and f.endswith(('.md', '.markdown')): continue  # root notes and READMEs: the sites publish none of these files
            full = os.path.join(dp, f); rel = os.path.relpath(full, root)
            try: text = open(full, encoding='utf-8', errors='replace').read()
            except OSError: continue
            if re.search(r'<table\b', text, re.I): out += list(scan_html(repo, rel, text))
            if '|' in text: out += list(scan_pipe(repo, rel, text.split('\n')))

json.dump(out, open(OUT + '.json', 'w'), indent=1, default=str)
with open(OUT + '.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print(len(out), 'tables')
