"""Checks content-date.py on pages that are only an include (convention 3):
such a page takes the newer of its own date and its partial's. Builds a
throwaway Git repository with one stub page per tool's include form, plus
a page with text of its own, which keeps its own date.

Usage: python3 -I test-content-date.py   (exit status 1 when a check fails)
"""
import os, subprocess, sys, tempfile

HELPER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content-date.py')
FM = '---\nrevision_date: 2019-03-01\n---\n'
FILES = {  # path: (text, the date it is committed at)
    'docs/dus.mdx': (FM + "import Part from './_part.mdx';\n\n<Part />\n", '2023-05-31'),
    'docs/_part.mdx': ('Text.\n', '2025-03-27'),
    'docs/zen.md': (FM + '\n<% include "_part.md" %>\n', '2023-05-31'),
    'partials/_part.md': ('Text.\n', '2025-03-27'),
    'docs/star.mdoc': (FM + '\n{% partial file="./_part.mdoc" /%}\n', '2023-05-31'),
    'docs/_part.mdoc': ('Text.\n', '2025-03-27'),
    'mod/pages/ant.adoc': ('= Title\n:page-last-updated: 2019-03-01\n\ninclude::partial$part.adoc[]\n', '2023-05-31'),
    'mod/partials/part.adoc': ('Text.\n', '2025-03-27'),
    'docs/own.md': (FM + '\nText of its own.\n\n<% include "_part.md" %>\n', '2023-05-31'),
}
EXPECT = {'docs/dus.mdx': '2025-03-27', 'docs/zen.md': '2025-03-27', 'docs/star.mdoc': '2025-03-27',
          'mod/pages/ant.adoc': '2025-03-27', 'docs/own.md': '2023-05-31'}

with tempfile.TemporaryDirectory() as d:
    def git(*a, date=None):
        env = dict(os.environ, GIT_AUTHOR_DATE=f'{date}T12:00:00Z', GIT_COMMITTER_DATE=f'{date}T12:00:00Z') if date else None
        subprocess.run(['git', '-C', d, *a], check=True, capture_output=True, env=env)
    git('init', '-q')
    git('config', 'user.name', 'test'); git('config', 'user.email', 'test@example.org')
    for path, (text, date) in FILES.items():
        os.makedirs(os.path.join(d, os.path.dirname(path)), exist_ok=True)
        open(os.path.join(d, path), 'w').write(text)
        git('add', path); git('commit', '-q', '-m', f'add {path}', date=date)
    ok = True
    for key, pages in (('revision_date', [p for p in EXPECT if not p.endswith('.adoc')]),
                       (':page-last-updated:', ['mod/pages/ant.adoc'])):
        out = subprocess.run([sys.executable, '-I', HELPER, '--key', key, '--git',
                              '--include-dir', os.path.join(d, 'partials'), *(os.path.join(d, p) for p in pages)],
                             check=True, capture_output=True, text=True).stdout
        for line in out.splitlines()[:-1]:
            page, date, src = line.split('\t')
            rel = os.path.relpath(page, d)
            good = date == EXPECT[rel]
            ok &= good
            print(f"{'ok  ' if good else 'FAIL'}  {rel:20} {date}  {src}  expected {EXPECT[rel]}")
sys.exit(0 if ok else 1)
