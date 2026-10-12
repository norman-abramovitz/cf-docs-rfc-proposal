"""Inventory the build-time values of the book, and the date each page's
"Page last updated" line shows.

Usage:
  python3 -I survey.py REPOS_DIR HIST_DIR SHAS GEM_DIR PUBLISHED_DIR... -o OUT_DIR

REPOS_DIR  one clone per line of SHAS, checked out at the commit SHAS names
HIST_DIR   one full-history clone per repository, named <name>.git (bare,
           blobless is enough); used for `git log`
SHAS       lines `<name> <commit> <date>`
GEM_DIR    the unpacked bookbindery 9.12.1 gem (lib/ and master_middleman/)
PUBLISHED_DIR  folders of saved published pages (*.html); each page's
           "View the source" link names its repository and file

Writes to OUT_DIR:
  buildtime.csv   every place a value is set or printed at build time, and
                  every copyright notice, with a link to the line
  pages.csv       every page of the 12 book repositories: the commit that
                  sets its "Page last updated" date today (Bookbinder's rule),
                  and the commit it would be with the candidate list skipped;
                  the published date, for pages saved under PUBLISHED_DIR
  candidates.txt  commits whose subject says they change markup only or
                  remove content the open-source book did not render, in
                  the format of git's blame.ignoreRevsFile
and prints a summary. Reads files and runs `git log`, `git ls-tree` and
`git show` only; runs nothing from the clones or the gem.

Bookbinder's rule (bookbindery 9.12.1, master_middleman/bookbinder_helpers.rb
`page_last_modified_date`, lib/bookbinder/ingest/git_accessor.rb
`author_date`): the author date of the newest commit that touches the
page's own source file, among the newest 30 (ruby-git's default log
count), skipping commits whose message contains "[exclude]". Partials and
variables the page uses do not count; renames are not followed.
"""
import csv, os, re, subprocess, sys
from collections import Counter

args = sys.argv[1:]
if '-o' not in args or len(args) < 7:
    sys.exit(__doc__)
OUT = args[args.index('-o') + 1]
args = args[:args.index('-o')]
REPOS, HIST, SHAS, GEM = args[:4]
PUBLISHED = args[4:]
sha = {l.split()[0]: l.split()[1] for l in open(SHAS) if l.strip()}
BOOK_REPOS = ['docs-bbr', 'docs-buildpacks', 'docs-cf-admin', 'docs-cf-cli',
              'docs-cloudfoundry-concepts', 'docs-credhub', 'docs-deploying-cf',
              'docs-dev-guide', 'docs-loggregator', 'docs-running-cf',
              'docs-services', 'docs-uaa']
BOOKBINDER = 'https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54'
SKIP_DIRS = {'node_modules', 'vendor'}  # and every folder whose name starts with "."
PAGE = re.compile(r'\.html(\.md)?(\.erb)?$')
ERB = re.compile(r'<%(#|=|-)?(.*?)-?%>', re.S)
TIME_CODE = re.compile(r'\b(Time|Date|DateTime)\b|\.year\b|strftime|modified_date|author_date|ENV\b')
FENCE = re.compile(r'^\s*(```|~~~)')
COPYRIGHT = re.compile(r'(copyright|&copy;|©)', re.I)
# Subjects that say a commit changes markup only, or removes content the
# open-source book did not render (conditional branches for the commercial
# book). Chosen by reading the subjects of 2026 commits; for review.
CANDIDATE = re.compile(
    r'closing </?p>|closing tags?|</p> closing|p tags that interfere|note__title spans'
    r'|Redcarpet HTML block|naked markdown|exposed Markdown|a-name with a-id'
    r'|platform-conditional ERB|commercial-only ERB|PCF/PCF-or-CF conditionals'
    r'|blockquote notes? to HTML|change note to html|standard note class'
    r'|trailing newline|blank line (after|before)', re.I)
SINCE = '2026-01-01'


def git(repo, *a):
    return subprocess.run(['git', '-C', os.path.join(HIST, repo + '.git'), *a],
                          capture_output=True, text=True, check=True).stdout


def url(repo, rel, line=None):
    u = f'https://github.com/cloudfoundry/{repo}/blob/{sha[repo]}/{rel}'
    return u + (f'#L{line}' if line else '')


def walk(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and not x.startswith('.'))
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(d, f), root)
            # Markdown files at a repository's root are notes about the
            # repository, not pages (the earlier surveys' rule)
            if not (f.endswith('.md') and os.sep not in rel):
                yield rel


def untag(s):
    """A commit subject without the trailing tag some commits carry
    ("[no-ai]", "ai=no" and the like): tags are omitted throughout."""
    return re.sub(r'\s*\[(?!exclude\])[a-z-]+\]\s*$|\s+ai(-assisted)?=\w+\s*$', '', s)


def lineno(text, pos):
    return text.count('\n', 0, pos) + 1


# --- 1. Where values are set or printed at build time ----------------------
rows = []
for repo in sorted(sha):
    root = os.path.join(REPOS, repo)
    for rel in walk(root):
        path = os.path.join(root, rel)
        base = os.path.basename(rel)
        try:
            text = open(path, encoding='utf-8').read()
        except (UnicodeDecodeError, OSError):
            continue
        lines = text.split('\n')
        if base in ('NOTICE', 'LICENSE'):
            for i, l in enumerate(lines, 1):
                # LICENSE files are the Apache text; only a filled-in notice counts
                if COPYRIGHT.search(l) and re.search(r'\d{4}', l) and '[yyyy]' not in l:
                    rows.append([repo, rel, i, 'notice', 'static', l.strip(), url(repo, rel, i)])
            continue
        if base in ('mkdocs.yml', 'mkdocs.yaml'):
            for i, l in enumerate(lines, 1):
                if re.match(r'\s*copyright\s*:', l) or re.search(r'git-revision|revision-date|git-committers|git-authors', l):
                    rows.append([repo, rel, i, 'mkdocs-config', 'static', l.strip(), url(repo, rel, i)])
            continue
        if not re.search(r'\.(erb|md|html|haml|markdown|yml|yaml)$', rel):
            continue
        # fenced code is sample text, not template code
        fenced = set()
        fence = None
        for i, l in enumerate(lines):
            m = FENCE.match(l)
            if fence is None and m:
                fence = m.group(1); fenced.add(i)
            elif fence is not None:
                fenced.add(i)
                if l.strip().startswith(fence):
                    fence = None
        for m in ERB.finditer(text):
            n = lineno(text, m.start())
            if n - 1 in fenced or m.group(1) == '#':
                continue
            code = m.group(2)
            if TIME_CODE.search(code):
                kind = 'helper' if re.search(r'modified_date|author_date', code) else 'erb-time'
                rows.append([repo, rel, n, kind, 'build', ' '.join(m.group(0).split()), url(repo, rel, n)])
        if text.startswith('---'):
            end = text.find('\n---', 3)
            for i, l in enumerate(text[:end].split('\n'), 1):
                if re.match(r'\s*modified_date\s*:', l):
                    rows.append([repo, rel, i, 'front-matter', 'switch', l.strip(), url(repo, rel, i)])
        for i, l in enumerate(lines, 1):
            if i - 1 not in fenced and COPYRIGHT.search(l) and 'layouts' in rel:
                rows.append([repo, rel, i, 'layout-notice', 'build', l.strip(), url(repo, rel, i)])

GEM_PATTERNS = re.compile(r'Time\.(now|parse)|author_date|modified_date|data-modified-date'
                          r'|exclusion_flag|getFullYear|DisplayModifiedDate|\.log\b')
for rel in walk(GEM):
    if not (rel.startswith('lib/') or rel.startswith('master_middleman/')):
        continue
    try:
        lines = open(os.path.join(GEM, rel), encoding='utf-8').read().split('\n')
    except (UnicodeDecodeError, OSError):
        continue
    for i, l in enumerate(lines, 1):
        if GEM_PATTERNS.search(l) and not l.strip().startswith('#'):
            rows.append(['bookbinder', rel, i, 'bookbinder', 'build', l.strip(), f'{BOOKBINDER}/{rel}#L{i}'])

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, 'buildtime.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['repo', 'file', 'line', 'kind', 'when', 'text', 'url'])
    w.writerows(rows)

# --- 2. The commits that set "Page last updated" ---------------------------
candidates = []
for repo in BOOK_REPOS:
    for l in git(repo, 'log', '--no-merges', f'--since={SINCE}', '--format=%H%x09%as%x09%s', sha[repo]).splitlines():
        h, d, s = l.split('\t', 2)
        if CANDIDATE.search(s):
            candidates.append((repo, h, d, s))
skip = {h for _, h, _, _ in candidates}
with open(os.path.join(OUT, 'candidates.txt'), 'w') as f:
    f.write('# Commits whose subject says they change markup only, or remove content\n'
            '# the open-source book did not render. Candidates for review, not decisions.\n'
            '# Format of git blame.ignoreRevsFile: one full commit id per line.\n')
    for repo, h, d, s in candidates:
        s = untag(s)
        f.write(f'# {repo} {d} {s}\n{h}\n')

published = {}
for d in PUBLISHED:
    for name in sorted(os.listdir(d)):
        if not name.endswith('.html'):
            continue
        html = open(os.path.join(d, name), encoding='utf-8').read()
        m = re.search(r'github\.com/cloudfoundry/(docs-[a-z-]+)/tree/master/([^"\']+)', html)
        t = re.search(r'data-modified-date="(\d+)"', html)
        if m and t:
            published.setdefault((m.group(1), m.group(2)), (os.path.join(d, name), int(t.group(1)) // 1000))

pages = []
for repo in BOOK_REPOS:
    files = git(repo, 'ls-tree', '-r', '--name-only', sha[repo]).splitlines()
    want = {f for f in files if PAGE.search(f) and not os.path.basename(f).startswith('_')}
    seen, rule, alt = Counter(), {}, {}
    for p in sorted(want):
        # `git log -- path` with git's default history simplification, as
        # ruby-git runs it: a merge whose result differs from every parent
        # is listed too
        for n, l in enumerate(git(repo, 'log', '--format=%H%x09%at%x09%aI%x09%cI%x09%s',
                                  sha[repo], '--', p).splitlines(), 1):
            h, at, ai, ci, s = l.split('\t', 4)
            seen[p] += 1
            if p not in rule and n <= 30 and '[exclude]' not in s:
                rule[p] = (h, int(at), ai, ci, s)
            if p not in alt and '[exclude]' not in s and h not in skip:
                alt[p] = (h, int(at), ai, ci, s)
    for p in sorted(want):
        r = rule.get(p)
        a = alt.get(p)
        pub = published.get((repo, p))
        pages.append([repo, p, seen[p],
                      r[0][:10] if r else '', r[2] if r else '', r[3] if r else '', untag(r[4])[:90] if r else '',
                      a[0][:10] if a else '', a[2] if a else '', untag(a[4])[:90] if a else '',
                      '/'.join(pub[0].split(os.sep)[-3:]) if pub else '',
                      ('yes' if r and pub[1] == r[1] else 'no') if pub else '',
                      url(repo, p)])
with open(os.path.join(OUT, 'pages.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['repo', 'page', 'commits', 'commit', 'author_date', 'committer_date', 'subject',
                'commit_skipping_candidates', 'author_date_skipping_candidates', 'subject_skipping_candidates',
                'published_copy', 'published_date_matches', 'url'])
    w.writerows(pages)

# --- Summary ---------------------------------------------------------------
print(f'buildtime.csv: {len(rows)} rows')
for (kind, when), n in sorted(Counter((r[3], r[4]) for r in rows).items()):
    print(f'  {kind:14} {when:7} {n}')
print(f'pages: {len(pages)} in {len(BOOK_REPOS)} repositories')
years = Counter(p[4][:4] for p in pages)
years_alt = Counter(p[8][:4] for p in pages)
print('  year of "Page last updated" today:      ', dict(sorted(years.items())))
print('  year with the candidate commits skipped:', dict(sorted(years_alt.items())))
print(f'  pages whose date moves when candidates are skipped: {sum(p[3] != p[7] for p in pages)}')
print(f'  newest date today: {max(p[4] for p in pages)[:10]}; skipping candidates: {max(p[8] for p in pages)[:10]}')
by = Counter((p[0], p[3], p[4][:10], p[6][:70]) for p in pages)
print('  commits that set the date of 5 or more pages:')
for k, n in by.most_common():
    if n < 5:
        break
    print(f'    {n:3}  {k[0]} {k[1]} {k[2]} {k[3]}')
print(f'candidates.txt: {len(candidates)} commits in {len({c[0] for c in candidates})} repositories')
pub_rows = [p for p in pages if p[10]]
print(f'published copies: {len(pub_rows)}, date matches Bookbinder\'s rule: {sum(p[11] == "yes" for p in pub_rows)}')
excl = Counter()
for repo in BOOK_REPOS:
    for l in git(repo, 'log', '--fixed-strings', '--grep=[exclude]', '--format=%as %s', sha[repo]).splitlines():
        excl[untag(l)] += 1
print('commits with "[exclude]" in the message:', dict(excl))
