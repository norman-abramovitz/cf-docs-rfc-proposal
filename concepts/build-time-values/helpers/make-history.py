"""Makes a small Git repository with known dates, to test each tool's
"last updated" feature and the content-date helper.

Usage:
  python3 -I make-history.py SITE_DIR DEST PAGES_REL EXT VARIANT

SITE_DIR   the site (config, pages); its installed packages are linked, not copied
DEST       a new folder; must not exist
PAGES_REL  the pages folder inside the site (docs, src/content/docs, ...)
EXT        the extension of the converted pages (.mdx, .md, .mdoc, .adoc)
VARIANT    native: the converted pages carry no date (the tool reads Git)
           helper: the converted pages carry the date the converter wrote

History (all times UTC; author and committer date the same unless noted):
  C1 2019-03-01 10:00  add the site and the four pages in the book's format
                       (<page>.html.md.erb, verbatim copies from ../source)
  C2 2024-12-05 22:18  edit architecture (committer date 2025-01-10 09:00)
  C3 2025-06-02 12:00  edit high-availability
  C4 2026-07-21 21:25  "Remove platform-conditional ERB blocks": edit
                       access-control, high-availability, using-vol-services
  C5 2026-10-01 12:00  "Convert pages": the book's files removed, the
                       converted pages added
  C6 2026-10-05 12:00  edit access-control (committer date 2026-10-07 12:00)
C4 and C5 are listed in DEST/.git-blame-ignore-revs. In the helper
variant, C5 writes each page's date as the converter would: the author
date of its newest commit before conversion that is not listed (C1, C2 or
C3). Prints the commit ids.
"""
import os, re, shutil, subprocess, sys

SITE, DEST, PAGES_REL, EXT, VARIANT = sys.argv[1:6]
ROUND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROUND, 'source')
PAGES = ['access-control', 'architecture', 'using-vol-services', 'high-availability']
SKIP = {'node_modules', '.venv', '.docusaurus', '.astro', '.cache', '.check', '.history', 'dist', 'site',
        '__pycache__'}
DATE_LINE = re.compile(r'^(last_update:\n  date: .*\n|lastUpdated: .*\n|revision_date: .*\n|:page-last-updated: .*\n)', re.M)
BASELINE = {'access-control': '2019-03-01', 'architecture': '2024-12-05',
            'using-vol-services': '2019-03-01', 'high-availability': '2025-06-02'}


def git(*a, author=None, committer=None):
    env = dict(os.environ, GIT_AUTHOR_NAME='Test Author', GIT_AUTHOR_EMAIL='author@example.org',
               GIT_COMMITTER_NAME='Test Committer', GIT_COMMITTER_EMAIL='committer@example.org',
               GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_SYSTEM='/dev/null')
    if author:
        env['GIT_AUTHOR_DATE'] = author
        env['GIT_COMMITTER_DATE'] = committer or author
    return subprocess.run(['git', '-C', DEST, *a], env=env, capture_output=True, text=True, check=True).stdout.strip()


def commit(msg, author, committer=None):
    git('add', '-A')
    git('commit', '-q', '-m', msg, author=author, committer=committer)
    return git('rev-parse', 'HEAD')


def edit(rel, line):
    with open(os.path.join(DEST, rel), 'a', encoding='utf-8') as f:
        f.write('\n' + line + '\n')


if os.path.exists(DEST):
    sys.exit(f'{DEST} exists')
shutil.copytree(SITE, DEST, symlinks=True,
                ignore=lambda d, names: [n for n in names if n in SKIP or n.startswith('build')])
for n in ('node_modules', '.venv'):
    if os.path.isdir(os.path.join(SITE, n)):
        os.symlink(os.path.abspath(os.path.join(SITE, n)), os.path.join(DEST, n))
with open(os.path.join(DEST, '.gitignore'), 'a') as f:
    f.write('\nnode_modules\n.venv\n')
pages_dir = os.path.join(DEST, PAGES_REL)
converted = {}
for p in PAGES:
    path = os.path.join(pages_dir, p + EXT)
    converted[p] = open(path, encoding='utf-8').read()
    os.remove(path)
    shutil.copy(os.path.join(SOURCE, p + '.html.md.erb'), os.path.join(pages_dir, p + '.html.md.erb'))

git('init', '-q', '-b', 'main')
ids = {}
ids['C1'] = commit('Add pages', '2019-03-01T10:00:00Z')
edit(f'{PAGES_REL}/architecture.html.md.erb', 'A sentence added in 2024.')
ids['C2'] = commit('Update architecture', '2024-12-05T22:18:28Z', '2025-01-10T09:00:00Z')
edit(f'{PAGES_REL}/high-availability.html.md.erb', 'A sentence added in 2025.')
ids['C3'] = commit('Update high availability', '2025-06-02T12:00:00Z')
for p in ('access-control', 'high-availability', 'using-vol-services'):
    edit(f'{PAGES_REL}/{p}.html.md.erb', '<%# a source-only change %>')
ids['C4'] = commit('Remove platform-conditional ERB blocks, keep OSS content', '2026-07-21T21:25:56Z')
for p in PAGES:
    os.remove(os.path.join(pages_dir, p + '.html.md.erb'))
    text = converted[p]
    if VARIANT == 'native':
        text = DATE_LINE.sub('', text)
    else:
        text = DATE_LINE.sub(lambda m: re.sub(r'\d{4}-\d{2}-\d{2}', BASELINE[p], m.group(0)), text, count=1)
    open(os.path.join(pages_dir, p + EXT), 'w', encoding='utf-8').write(text)
ids['C5'] = commit('Convert pages', '2026-10-01T12:00:00Z')
edit(f'{PAGES_REL}/access-control{EXT}', 'A sentence added after conversion.')
ids['C6'] = commit('Update access control', '2026-10-05T12:00:00Z', '2026-10-07T12:00:00Z')
with open(os.path.join(DEST, '.git-blame-ignore-revs'), 'w') as f:
    f.write(f"# Remove platform-conditional ERB blocks\n{ids['C4']}\n# Convert pages\n{ids['C5']}\n")
for k, v in ids.items():
    print(k, v)
