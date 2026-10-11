"""Inventory every note in the cloned documentation repositories.

Usage:
  python3 -I survey.py REPOS_DIR SHAS OUT.csv

REPOS_DIR holds one clone per line of SHAS, named as in SHAS. SHAS has
lines `<name> <commit> <date>`; the commit goes into each row's GitHub
link. Writes OUT.csv, one row per note, and prints a summary. Reads files
only; runs nothing from the clones.

A note is any of:
  html        an HTML element whose class list holds the word `note`
              (<p class="note">, <div class="note important">, ...)
  variable    a value in docs-book-cloudfoundry's template_variables.yml
              that holds such an element
  blockquote  a Markdown blockquote (`> ...`) whose text starts with a
              label such as **Note** or Important:
  label       a paragraph or list item outside any note element that
              starts with a label: **Note:**, <strong>Note</strong>, Note:
  admonition  a Python-Markdown admonition, `!!! note "Title"` (bosh.io)

Lines inside fenced code blocks are skipped for every kind, and the
Markdown kinds also skip lines inside <pre> blocks and inside HTML notes.
"""
import csv, os, re, sys
from collections import Counter

if len(sys.argv) != 4:
    sys.exit(__doc__)
REPOS, SHAS, OUT = sys.argv[1:]
EXTS = ('.md', '.erb', '.html', '.haml', '.markdown', '.mdx', '.adoc')
sha = dict(l.split()[:2] for l in open(SHAS) if l.strip())

FENCE = re.compile(r'^\s*(```|~~~)')
OPEN = re.compile(r'<(p|div)\b[^>]*?\bclass\s*=\s*(["\'“”])([^"\'“”>]*)(["\'“”])[^>]*>', re.I)
LABEL_WORDS = r'(Note|NOTE|Important|IMPORTANT|Warning|WARNING|Caution|CAUTION|Tip|TIP)'
# A label is the word with a colon (Note:, **Note:**, **Note**:, <strong>Note:</strong>)
# or the word alone in bold followed by a capital letter (**Note** The ...).
# "Note that ..." and "Note the GUID ..." are verbs, not labels.
LABEL = re.compile(r'^\s*(?:[*+-]\s+|\d+\.\s+)?(?:'
                   r'(?:\*\*|<strong>|<b>)?' + LABEL_WORDS + r'\s*:\s*(?:\*\*|</strong>|</b>)?'
                   r'|(?:\*\*|<strong>|<b>)' + LABEL_WORDS + r'(?:\*\*|</strong>|</b>)\s*:?(?=\s*[A-Z<`])'
                   r')')
LIST_LINE = re.compile(r'^\s*([*+-]|\d+\.)\s+\S')
ADMON = re.compile(r'^(\s*)(!!!|\?\?\?\+?)\s*([A-Za-z]+)(?:\s+"([^"]*)")?\s*$')


def label_word(m):
    return (m.group(1) or m.group(2)).capitalize()


def url(repo, rel, line):
    return f'https://github.com/cloudfoundry/{repo}/blob/{sha[repo]}/{rel}#L{line}'


def fenced_lines(lines):
    """Set of 0-based line numbers inside fenced code blocks (fences included)."""
    out, fence = set(), None
    for i, l in enumerate(lines):
        m = FENCE.match(l)
        if fence is None and m:
            fence = m.group(1); out.add(i)
        elif fence is not None:
            out.add(i)
            if l.strip().startswith(fence):
                fence = None
    return out


def in_list(lines, i):
    """True when line i is indented under a list item: walking up, the first
    non-blank line with less indentation is a list item."""
    ind = len(lines[i]) - len(lines[i].lstrip())
    if ind == 0:
        return False
    for j in range(i - 1, -1, -1):
        l = lines[j]
        if not l.strip():
            continue
        k = len(l) - len(l.lstrip())
        if k < ind:
            return bool(LIST_LINE.match(l))
    return False


def in_html_li(text, pos):
    before = text[:pos].lower()
    return len(re.findall(r'<li\b', before)) > len(re.findall(r'</li\s*>', before))


def in_table(text, pos):
    before = text[:pos].lower()
    return before.count('<td') > before.count('</td') or before.count('<table') > before.count('</table')


def close_of(text, tag, start):
    """(end, closed) of the element opened at start. A <div> ends at its
    matching </div>. A <p> holds no block, so it ends at the first </p>,
    or, when it is not closed, at the next <p> tag or blank line, where a
    browser or the Markdown processor ends it; closed is then False."""
    if tag.lower() == 'p':
        gt = text.index('>', start) + 1
        m = re.compile(r'</p\s*>|<p\b|\n[ \t]*\n', re.I).search(text, gt)
        if m is None:
            return len(text), False
        if m.group(0).lower().startswith('</p'):
            return m.end(), True
        return m.start(), False
    depth, pat = 0, re.compile(r'<(/?)div\b[^>]*>', re.I)
    for m in pat.finditer(text, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.end(), True
    return len(text), False


def content_traits(body):
    t = []
    if re.search(r'<(ul|ol)\b', body, re.I) or any(LIST_LINE.match(l) for l in body.splitlines()):
        t.append('list')
    if re.search(r'<pre\b', body, re.I) or re.search(r'^\s*(```|~~~)', body, re.M):
        t.append('code-block')
    if re.search(r'<code\b', body, re.I) or re.search(r'`[^`\n]+`', body):
        t.append('code')
    if re.search(r'<a\s[^>]*href', body, re.I) or re.search(r'\]\([^)]+\)', body):
        t.append('link')
    if re.search(r'<%=\s*vars\.', body):
        t.append('variable')
    if re.search(r'<%=?\s*partial\b', body):
        t.append('partial')
    if re.search(r'<%(?!=\s*(vars\.|partial\b))', body):
        t.append('erb-other')
    if re.search(r'<img\b|!\[', body, re.I):
        t.append('image')
    if re.search(r'<table\b', body, re.I):
        t.append('table')
    return t


def markdown_in_html(body):
    """Markdown syntax inside an HTML note (fenced code excluded)."""
    t = []
    if re.search(r'(?<![`\\])`[^`\n]+`', body):
        t.append('backticks')
    if re.search(r'\*\*[^*\n]+\*\*', body):
        t.append('bold')
    if re.search(r'\[[^\]\n]+\]\([^)\n]+\)', body):
        t.append('link')
    if any(LIST_LINE.match(l) for l in body.splitlines()):
        t.append('list')
    return t


rows = []


def add(**kw):
    base = dict(repo='', file='', line='', url='', form='', tag='', cls='', kind='', quotes='',
                title_span='', title='', title_form='', title_matches='', indent='', in_list='',
                in_table='', in_partial='', archive='', lines='', paragraphs='', holds='',
                markdown_inside='', closed='', close_own_line='', sample='')
    base.update(kw)
    rows.append(base)


def kind_of(cls):
    words = [w for w in cls.split() if w != 'note']
    return ' '.join(words) or 'note'


def scan_html(repo, rel, text, lines, fenced):
    starts = [0]
    for l in lines:
        starts.append(starts[-1] + len(l) + 1)
    def line_of(pos):
        lo, hi = 0, len(starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if starts[mid] <= pos: lo = mid
            else: hi = mid - 1
        return lo
    spans = []
    for m in OPEN.finditer(text):
        cls = m.group(3)
        if 'note' not in cls.split():
            continue
        li = line_of(m.start())
        if li in fenced:
            continue
        tag = m.group(1).lower()
        end, closed = close_of(text, tag, m.start())
        body = re.sub(r'</%s\s*>$' % tag, '', text[m.end():end], flags=re.I)
        spans.append((m.start(), end))
        t = re.search(r'<span\s+class\s*=\s*["\']note__title["\']\s*>(.*?)</span>', body, re.I | re.S)
        title = re.sub(r'<[^>]+>', '', t.group(1)).strip() if t else ''
        tform = ''
        if t:
            inner = t.group(1).strip()
            tform = 'span>strong' if re.fullmatch(r'<strong>[^<]*</strong>', inner) else 'span:' + re.sub(r'[^<>/a-z]', '', inner)[:20]
        kind = kind_of(cls)
        expect = {'note': 'Note', 'important': 'Important', 'caution': 'Caution', 'warning': 'Warning'}.get(kind, '')
        rest = re.sub(r'<span\s+class\s*=\s*["\']note__title["\']\s*>.*?</span>', '', body, count=1, flags=re.I | re.S)
        close_line = text[:end].splitlines()[-1].strip() if closed else ''
        quotes = 'straight' if m.group(2) in '"\'' and m.group(4) == m.group(2) else 'curly-or-mismatched'
        add(repo=repo, file=rel, line=li + 1, url=url(repo, rel, li + 1), form='html', tag=tag, cls=cls,
            kind=kind, quotes=quotes, title_span='yes' if t else 'no', title=title, title_form=tform,
            title_matches=('yes' if title == expect else 'no') if t and expect else '',
            indent=len(lines[li]) - len(lines[li].lstrip()),
            in_list='markdown' if in_list(lines, li) else 'html' if in_html_li(text, m.start()) else 'no',
            in_table='yes' if in_table(text, m.start()) else 'no',
            in_partial='yes' if os.path.basename(rel).startswith('_') else 'no',
            archive='yes' if '/archive/' in '/' + rel else 'no',
            lines=body.count('\n') + 1,
            paragraphs=len([p for p in re.split(r'\n\s*\n', rest.strip()) if p.strip()]) if rest.strip() else 0,
            holds=' '.join(content_traits(rest)), markdown_inside=' '.join(markdown_in_html(rest)),
            closed='yes' if closed else 'no',
            close_own_line=('yes' if re.fullmatch(r'</%s\s*>' % tag, close_line, re.I) else 'no') if closed else '',
            sample=' '.join(re.sub(r'<[^>]+>', '', rest).split())[:90])
    return spans


def scan_md(repo, rel, lines, fenced, spans, text):
    starts = [0]
    for l in lines:
        starts.append(starts[-1] + len(l) + 1)
    inside = lambda i: any(a <= starts[i] < b for a, b in spans)
    i = 0
    while i < len(lines):
        l = lines[i]
        if i in fenced or inside(i):
            i += 1; continue
        a = ADMON.match(l)
        if a:
            ind = len(a.group(1))
            j = i + 1; body = []
            while j < len(lines) and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > ind):
                body.append(lines[j]); j += 1
            while body and not body[-1].strip():
                body.pop()
            b = '\n'.join(body)
            add(repo=repo, file=rel, line=i + 1, url=url(repo, rel, i + 1), form='admonition',
                tag=a.group(2), kind=a.group(3), title=a.group(4) or '', indent=ind,
                in_list='yes' if in_list(lines, i) else 'no', archive='no',
                in_partial='yes' if os.path.basename(rel).startswith('_') else 'no',
                lines=len(body), paragraphs=len([p for p in re.split(r'\n\s*\n', b.strip()) if p.strip()]),
                holds=' '.join(content_traits(b)), sample=' '.join(b.split())[:90])
            i = j; continue
        q = re.match(r'^(\s*)>\s?(.*)$', l)
        if q and LABEL.match(q.group(2)) and (i == 0 or not lines[i - 1].strip().startswith('>')):
            j = i; body = []
            while j < len(lines) and re.match(r'^\s*>', lines[j]):
                body.append(re.sub(r'^\s*>\s?', '', lines[j])); j += 1
            b = '\n'.join(body)
            add(repo=repo, file=rel, line=i + 1, url=url(repo, rel, i + 1), form='blockquote',
                kind=label_word(LABEL.match(q.group(2))), indent=len(q.group(1)),
                in_list='yes' if in_list(lines, i) else 'no',
                in_partial='yes' if os.path.basename(rel).startswith('_') else 'no',
                archive='yes' if '/archive/' in '/' + rel else 'no', lines=len(body),
                holds=' '.join(content_traits(b)), sample=' '.join(b.split())[:90])
            i = j; continue
        lm = LABEL.match(l)
        prev_blank = i == 0 or not lines[i - 1].strip() or LIST_LINE.match(l)
        if lm and prev_blank and not in_table(text, starts[i]):
            add(repo=repo, file=rel, line=i + 1, url=url(repo, rel, i + 1), form='label',
                kind=label_word(lm), indent=len(l) - len(l.lstrip()),
                in_list='yes' if (LIST_LINE.match(l) or in_list(lines, i)) else 'no',
                in_partial='yes' if os.path.basename(rel).startswith('_') else 'no',
                archive='yes' if '/archive/' in '/' + rel else 'no',
                holds=' '.join(content_traits(l)), sample=' '.join(l.split())[:90])
        i += 1


for repo in sorted(sha):
    root = os.path.join(REPOS, repo)
    if not os.path.isdir(root):
        continue
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(d for d in dn if d not in ('.git', 'node_modules', 'vendor'))
        for f in sorted(fn):
            if not f.endswith(EXTS):
                continue
            if dp == root and f.endswith(('.md', '.markdown')):
                continue  # root notes and READMEs: no site publishes them
            full = os.path.join(dp, f); rel = os.path.relpath(full, root)
            text = open(full, encoding='utf-8', errors='replace').read()
            lines = text.split('\n')
            fenced = fenced_lines(lines)
            spans = scan_html(repo, rel, text, lines, fenced)
            pres = [(m.start(), m.end()) for m in re.finditer(r'<pre\b.*?</pre\s*>', text, re.I | re.S)]
            scan_md(repo, rel, lines, fenced, spans + pres, text)

# Notes held in variables: the book's template_variables.yml
tv = os.path.join(REPOS, 'docs-book-cloudfoundry', 'config', 'template_variables.yml')
if os.path.exists(tv):
    used = Counter()
    for repo in sorted(sha):
        for dp, dn, fn in os.walk(os.path.join(REPOS, repo)):
            dn[:] = [d for d in dn if d not in ('.git', 'node_modules', 'vendor')]
            for f in fn:
                if f.endswith(EXTS):
                    for name in re.findall(r'vars\.(\w+)', open(os.path.join(dp, f), encoding='utf-8', errors='replace').read()):
                        used[name] += 1
    for n, l in enumerate(open(tv, encoding='utf-8'), 1):
        m = re.match(r'^\s+(\w+):\s*(.*)$', l)
        if m and OPEN.search(m.group(2)) and 'note' in OPEN.search(m.group(2)).group(3).split():
            v = m.group(2); cls = OPEN.search(v).group(3)
            t = re.search(r'<span\s+class\s*=\s*["\']note__title["\']\s*>(.*?)</span>', v)
            rest = re.sub(r'<span[^>]*note__title[^>]*>.*?</span>', '', v)
            add(repo='docs-book-cloudfoundry', file='config/template_variables.yml', line=n,
                url=url('docs-book-cloudfoundry', 'config/template_variables.yml', n), form='variable',
                tag=OPEN.search(v).group(1), cls=cls, kind=kind_of(cls), quotes='straight',
                title_span='yes' if t else 'no', title=re.sub(r'<[^>]+>', '', t.group(1)) if t else '',
                title_form='span>strong' if t and t.group(1).startswith('<strong>') else '',
                in_partial='no', archive='no', lines=1, paragraphs=1,
                holds=' '.join(content_traits(rest)), markdown_inside=' '.join(markdown_in_html(rest)),
                closed='yes' if re.search(r'</p>', v[OPEN.search(v).end():]) else 'no',
                sample=f'vars.{m.group(1)} (used {used[m.group(1)]} times): ' + ' '.join(re.sub(r'<[^>]+>', '', rest).split())[:60])

FIELDS = list(rows[0].keys()) if rows else []
with open(OUT, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, FIELDS)
    w.writeheader()
    w.writerows(rows)

bosh = lambda r: r['repo'] == 'docs-bosh'
c = Counter((('bosh.io' if bosh(r) else 'book'), r['form']) for r in rows)
print(f'{len(rows)} notes')
for k in sorted(c):
    print(f'  {k[0]:8} {k[1]:11} {c[k]}')
