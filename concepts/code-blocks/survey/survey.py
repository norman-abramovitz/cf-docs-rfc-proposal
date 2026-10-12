"""Inventory every code block in the cloned documentation repositories.

Usage:
  python3 -I survey.py REPOS_DIR SHAS RENDERED.csv COMMONMARK.csv BLOCKS.csv

REPOS_DIR holds one clone per line of SHAS, named as in SHAS. SHAS has
lines `<name> <commit> <date>`; the commit goes into each row's GitHub
link. RENDERED.csv is book-render.rb's output (the code blocks the book's
Redcarpet finds, with the Rouge lexer each gets) and COMMONMARK.csv is
commonmark-render.mjs's (the code blocks a CommonMark parser finds in the
same pages). Writes BLOCKS.csv, one row per code block, and prints a
summary. Reads files only; runs nothing from the clones.

What is a code block:
  fence      a Markdown fenced block: a line of three or more backticks or
             tildes, any indentation, then an optional info string
  indented   a Markdown indented block: found by the book's model or the
             CommonMark parser where no fence is (see "book" and "cm" below)
  pre        an HTML <pre> element, with or without <code> inside

Where a fence ends, as the book's Redcarpet 3.2.3 ends it: at the first
later line that holds only three or more backticks or tildes (either
character, any length), or where its list item ends (a non-blank line
indented less than the fence), or at the end of the file. The column
`close` says which, and whether CommonMark closes it at the same line
(same character, at least as long as the opening).

`after_text` marks a fence on the line right after a line of text, with no
blank line between: Redcarpet reads it as part of that paragraph (an
inline code span), where CommonMark starts a code block.

The columns `book` and `cm` join each block with the two parsers' rows,
by the block's first non-blank line in document order: the kind each
parser makes of it (fenced, indented, html for a <pre>, none), and for
the book the Rouge lexer (`lexer`). Rows that only one parser finds are
added with form `indented`, `fence-as-text` or `pre-as-code` as they
turn out. Lines inside HTML comments and front matter are skipped.
"""
import csv, difflib, os, re, sys
from collections import Counter, defaultdict

if len(sys.argv) != 6:
    sys.exit(__doc__)
REPOS, SHAS, RENDERED, COMMONMARK, OUT = sys.argv[1:]
EXTS = ('.md', '.erb', '.html', '.haml', '.markdown', '.mdx', '.adoc')
SKIP_DIRS = {'.git', 'node_modules', 'vendor'}
BOOK = 'docs-book-cloudfoundry'
sha = dict(l.split()[:2] for l in open(SHAS) if l.strip())

FENCE = re.compile(r'^(\s*)(`{3,}|~{3,})(.*)$')
BARE_FENCE = re.compile(r'^\s*(`{3,}|~{3,})\s*$')
PRE_OPEN = re.compile(r'<pre\b([^>]*)>', re.I)
PRE_CLOSE = re.compile(r'</pre\s*>', re.I)
CODE_OPEN = re.compile(r'^\s*<code\b([^>]*)>', re.I)
LIST_LINE = re.compile(r'^\s*([*+-]|\d+\.)\s+')
ERB_VAR = re.compile(r'<%=\s*vars\.(\w+)\s*-?%>')
ERB_ANY = re.compile(r'<%(?!%)(.*?)%>', re.S)
TAG = re.compile(r'<(/?)(div|p|td|th|li|table|blockquote|ul|ol)\b([^>]*)>', re.I)
PROMPT = re.compile(r'^\s*(\$|#|>|PS [^>]*>|C:\\[^>]*>)\s')
MARKUP = re.compile(r'<(strong|b|em|i|span|a|br|code|var|kbd)\b', re.I)
ENTITY = re.compile(r'&(#\d+|#x[0-9a-f]+|[a-z]+);', re.I)


def url(repo, rel, a, b=None):
    u = f'https://github.com/cloudfoundry/{repo}/blob/{sha[repo]}/{rel}#L{a}'
    return u + (f'-L{b}' if b and b != a else '')


def walk(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        for f in sorted(files):
            yield os.path.relpath(os.path.join(d, f), root)


def indent_of(l):
    return len(l.expandtabs(4)) - len(l.expandtabs(4).lstrip())


def in_md_list(lines, i):
    """Line i is indented under a Markdown list item."""
    ind = indent_of(lines[i])
    if ind == 0:
        return False
    for j in range(i - 1, -1, -1):
        l = lines[j]
        if not l.strip():
            continue
        if indent_of(l) < ind:
            return bool(LIST_LINE.match(l))
    return False


# --- the book's variables, one-line values only (enough to match first lines)
values = {}
for l in open(os.path.join(REPOS, BOOK, 'config', 'template_variables.yml'), encoding='utf-8'):
    m = re.match(r'^  (\w+):\s*(.*?)\s*$', l)
    if m:
        v = m.group(2)
        values[m.group(1)] = '' if v in ('', '|', '|-', '>', '>-') else v.strip('"\'')


def first_line(text):
    """The first non-blank line, as the parsers' rows give it."""
    t = ERB_VAR.sub(lambda m: values.get(m.group(1), ''), text)
    t = ERB_ANY.sub('', t)
    for l in t.split('\n'):
        if l.strip():
            return l.strip()[:80]
    return ''


def parser_rows(path, kindcol, infocol):
    out = defaultdict(list)
    for r in csv.DictReader(open(path, encoding='utf-8')):
        out[(r['repo'], r['file'])].append(r)
    return out


rendered = parser_rows(RENDERED, None, 'language')
cmark = parser_rows(COMMONMARK, 'kind', 'info')


def scan(repo, rel, text):
    """The fences and <pre> blocks of one file, in order."""
    lines = text.split('\n')
    n = len(lines)
    skip = [False] * n
    # front matter
    if lines and lines[0].strip() == '---':
        for j in range(1, n):
            if lines[j].strip() == '---':
                for k in range(0, j + 1):
                    skip[k] = True
                break
    blocks = []
    stack = []          # open HTML elements: (tag, is_note)
    in_comment = False
    i = 0
    while i < n:
        l = lines[i]
        if skip[i]:
            i += 1
            continue
        if in_comment:
            if '-->' in l:
                in_comment = False
            i += 1
            continue
        if '<!--' in l and '-->' not in l.split('<!--', 1)[1]:
            in_comment = True
            i += 1
            continue
        if not l.strip():
            stack = [e for e in stack if e[0] != 'p']   # a blank line ends an open <p>
        m = FENCE.match(l)
        if m and not (m.group(2)[0] == '`' and '`' in m.group(3)):
            ind, fence, info = indent_of(l), m.group(2), m.group(3).strip()
            end, close = None, 'eof'
            for j in range(i + 1, n):
                lj = lines[j]
                if BARE_FENCE.match(lj):
                    f = BARE_FENCE.match(lj).group(1)
                    end = j
                    close = 'fence' if (f[0] == fence[0] and len(f) >= len(fence)) else 'fence-redcarpet'
                    break
                if ind and lj.strip() and indent_of(lj) < ind:
                    end, close = j - 1, 'end-of-item'
                    while end > i and not lines[end].strip():
                        end -= 1
                    break
            if end is None:
                end = n - 1
            body = lines[i + 1:end] if close.startswith('fence') else lines[i + 1:end + 1]
            looks = [lines[k] for k in range(i + 1, end + (0 if close.startswith('fence') else 1))
                     if re.match(r'^\s*(```|~~~)\S', lines[k])]
            blocks.append(dict(form='fence' if fence[0] == '`' else 'fence-tilde', start=i, end=end,
                               info=info, fence=fence, indent=ind, close=close, body=body,
                               stray_fence=len(looks), ctx=context(lines, i, stack)))
            i = end + 1
            continue
        pm = PRE_OPEN.search(l)
        if pm:
            rest = l[pm.end():]
            body, end = [], i
            if PRE_CLOSE.search(rest):
                body = [PRE_CLOSE.split(rest, 1)[0]]
            else:
                body = [rest] if rest.strip() else []
                for j in range(i + 1, n):
                    if PRE_CLOSE.search(lines[j]):
                        before = PRE_CLOSE.split(lines[j], 1)[0]
                        if before.strip():
                            body.append(before)
                        end = j
                        break
                    body.append(lines[j])
                else:
                    end = n - 1
            attrs = pm.group(1).strip()
            joined = '\n'.join(body)
            cm_ = CODE_OPEN.match(joined)
            form = 'pre-code' if cm_ else 'pre'
            info = attrs + ((' / code ' + cm_.group(1).strip()) if cm_ and cm_.group(1).strip() else '')
            for t in TAG.finditer(l[:pm.start()]):
                track(stack, t)
            blocks.append(dict(form=form, start=i, end=end, info=info, fence='', indent=indent_of(l),
                               close='closed' if end < n - 1 or PRE_CLOSE.search(lines[end]) else 'unclosed',
                               body=body, stray_fence=0, ctx=context(lines, i, stack)))
            i = end + 1
            continue
        for t in TAG.finditer(l):
            track(stack, t)
        i += 1
    return blocks


def track(stack, t):
    close, tag, attrs = t.group(1), t.group(2).lower(), t.group(3)
    if close:
        for k in range(len(stack) - 1, -1, -1):
            if stack[k][0] == tag:
                del stack[k:]
                break
    elif not attrs.rstrip().endswith('/'):
        stack.append((tag, bool(re.search(r'class\s*=\s*["\'][^"\']*\bnote\b', attrs))))


def context(lines, i, stack):
    if any(note for _, note in stack):
        return 'note'
    tags = [t for t, _ in stack]
    if 'td' in tags or 'th' in tags:
        return 'table'
    if 'li' in tags:
        return 'html-list'
    if lines[i].lstrip().startswith('>'):
        return 'blockquote'
    if in_md_list(lines, i):
        return 'list'
    if 'div' in tags or 'blockquote' in tags:
        return 'html'
    return 'top'


def language(form, info):
    if form.startswith('fence'):
        w = info.strip('{} ').split()
        return w[0].lstrip('.').lower() if w else ''
    m = re.search(r'class\s*=\s*["\'‘’]?([^"\'‘’\s>]+)', info)
    return m.group(1) if m else ''


rows = []
for repo in sorted(sha):
    root = os.path.join(REPOS, repo)
    if not os.path.isdir(root):
        continue
    for rel in walk(root):
        if not rel.endswith(EXTS):
            continue
        if '/' not in rel and rel.endswith('.md'):
            continue
        text = open(os.path.join(root, rel), encoding='utf-8', errors='replace').read()
        blocks = scan(repo, rel, text)
        lines = text.split('\n')
        # join with the two parsers' rows by first line, in order
        md_file = re.search(r'\.(md|markdown)(\.erb)?$', rel) and repo != 'docs-bosh'
        R = rendered.get((repo, rel), []) if md_file else []
        K = cmark.get((repo, rel), []) if md_file else []
        for b in blocks:
            b['first'] = first_line('\n'.join(b['body'])) if b['form'].startswith('fence') else \
                first_line(re.sub(r'<[^>]+>', '', '\n'.join(b['body'])))
            b['book'] = b['cm'] = ('html' if b['form'].startswith('pre') else 'none') if md_file else 'n/a'
            b['lexer'] = ''
        fences = [b for b in blocks if b['form'].startswith('fence')]
        for P, key in ((R, 'book'), (K, 'cm')):
            sm = difflib.SequenceMatcher(None, [b['first'] for b in fences], [r['first_line'] for r in P], autojunk=False)
            used = set()
            for a, c, size in sm.get_matching_blocks():
                for k in range(size):
                    fb, r = fences[a + k], P[c + k]
                    fb[key] = r.get('kind', 'fenced') if key == 'cm' else 'fenced'
                    if key == 'book':
                        fb['lexer'] = r['lexer']
                    used.add(c + k)
            for c, r in enumerate(P):
                if c in used:
                    continue
                # a block only this parser finds where the source has no fence of
                # that first line: an indented block, a fence read as text, or a
                # <pre> read as code
                pre = next((b for b in blocks if b['form'].startswith('pre') and b.get(key) == 'html'
                            and lines[b['start']].strip()[:80] == r['first_line']), None)
                if pre is not None:
                    pre[key] = 'indented'   # the <pre> tag itself shown as code
                    continue
                other = [x for x in blocks if x.get('extra') and x['first'] == r['first_line']]
                if other:
                    other[0][key] = r.get('kind', 'indented') if key == 'cm' else 'indented'
                    if key == 'book':
                        other[0]['lexer'] = r['lexer']
                    continue
                start = next((k for k in range(len(lines)) if lines[k].strip()[:80] == r['first_line']
                              and indent_of(lines[k]) >= 4), None)
                if start is None:
                    start = next((k for k in range(len(lines)) if r['first_line'] and r['first_line'] in lines[k]), 0)
                nb = dict(form='fence-as-text' if re.match(r'^(```|~~~)', r['first_line']) else 'indented',
                          start=start, end=start + int(r['lines']) - 1, info='', fence='', indent=indent_of(lines[start]),
                          close='', body=lines[start:start + int(r['lines'])], stray_fence=0,
                          ctx=context(lines, start, []), first=r['first_line'], extra=True,
                          book='none' if md_file else 'n/a', cm='none' if md_file else 'n/a', lexer='')
                nb[key] = (r.get('kind', 'indented') if key == 'cm' else 'indented')
                if key == 'book':
                    nb['lexer'] = r['lexer']
                blocks.append(nb)
        blocks.sort(key=lambda b: b['start'])
        for b in blocks:
            body = '\n'.join(b['body'])
            plain = [re.sub(r'<[^>]+>', '', x) for x in b['body']] if b['form'].startswith('pre') else b['body']
            code_lines = [x for x in plain if x.strip()]
            prompts = [x for x in code_lines if PROMPT.match(x)]
            fp = PROMPT.match(code_lines[0]) if code_lines else None
            prev = next((lines[k] for k in range(b['start'] - 1, -1, -1) if lines[k].strip()), '') \
                if b['start'] > 0 and lines[b['start'] - 1].strip() else ''
            area = 'bosh.io' if repo == 'docs-bosh' else 'book'
            rows.append({
                'repo': repo, 'file': rel, 'line': b['start'] + 1, 'end': b['end'] + 1,
                'area': area, 'archive': 'yes' if '/archive/' in '/' + rel else '',
                'partial': 'yes' if os.path.basename(rel).startswith('_') else '',
                'form': b['form'], 'info': b['info'], 'language': language(b['form'], b['info']),
                'fence': b['fence'], 'indent': b['indent'], 'close': b['close'],
                'stray_fence': b['stray_fence'] or '', 'place': b['ctx'],
                'lines': len(b['body']),
                'book': b['book'], 'lexer': b['lexer'], 'cm': b['cm'],
                'erb_vars': len(ERB_VAR.findall(body)) or '',
                'erb_other': len([x for x in ERB_ANY.findall(body) if not re.match(r'=\s*vars\.', x)]) or '',
                'erb_escaped': body.count('<%%') or '',
                'after_text': 'yes' if b['form'].startswith('fence') and prev and not re.match(
                    r'^\s*(#|<|```|~~~|[*+-]\s*$|\d+\.\s*$)', prev) else '',
                'prompt_first': fp.group(1) if fp else '',
                'prompt_lines': len(prompts) or '',
                'output_lines': (len(code_lines) - len(prompts)) if prompts else '',
                'markup': (len(MARKUP.findall(body)) - (b['form'] == 'pre-code')) or '' if b['form'].startswith('pre') else '',
                'entities': len(ENTITY.findall(body)) or '',
                'blank_line': 'yes' if any(not x.strip() for x in b['body'][1:-1]) else '',
                'braces': 'yes' if re.search(r'[{}]', body) else '',
                'jinja_markdoc': 'yes' if re.search(r'\{\{|\{%|\{#', body) else '',
                'md_chars': 'yes' if b['form'].startswith('pre') and re.search(r'\*\S|\S\*|(?<!\w)_\S.*\S_(?!\w)|`', re.sub(r'<[^>]+>', '', body)) else '',
                'tabs': 'yes' if '\t' in body else '',
                'first_line': b['first'],
                'url': url(repo, rel, b['start'] + 1, b['end'] + 1),
            })

cols = list(rows[0].keys())
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

book = [r for r in rows if r['area'] == 'book']
print(f'{len(rows)} code blocks: {len(book)} in the book, {len(rows) - len(book)} in bosh.io')
print('forms (book):', dict(Counter(r['form'] for r in book).most_common()))
