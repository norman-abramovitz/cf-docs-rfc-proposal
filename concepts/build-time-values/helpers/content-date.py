"""The date a page's content last changed, and the year of the newest one.

Usage:
  python3 -I content-date.py --key KEY [--git] [--ignore-revs FILE] [--marker TEXT]
                             [--allow-shallow] [--write] [--year] PAGE...

For each PAGE the content date is the later of:
  - the date written in the page under KEY (the converter writes it once,
    from the page's history before conversion), and
  - with --git, the author date of the newest commit that changed the page
    file, skipping every commit listed in --ignore-revs (one full commit
    id per line, # for comments: the format of git's blame.ignoreRevsFile
    and of GitHub's .git-blame-ignore-revs) and every commit whose message
    contains --marker (Bookbinder's "[exclude]", if given).

KEY names where the date is written:
  last_update.date      YAML front matter, nested (Docusaurus)
  lastUpdated           YAML front matter (Starlight)
  revision_date         YAML front matter (Zensical)
  :page-last-updated:   an AsciiDoc header attribute (Antora)

Prints `PAGE<TAB>DATE<TAB>FROM` per page (FROM is `page`, `git <commit>` or
`none`) and a last line `SITE_YEAR=YYYY`: the year of the newest date. With
--year it prints only the year. With --write it writes each date back under
KEY, so the tool shows it; a build does this in its own checkout, not in a
commit. With --git it stops if the repository is a shallow clone, where
every file seems to have changed in the newest commit, unless
--allow-shallow is given.

Python 3 standard library and git only.
"""
import os, re, subprocess, sys
from datetime import datetime, timezone

argv = sys.argv[1:]
if not argv or '--key' not in argv:
    sys.exit(__doc__)
opts, pages = {}, []
flags = {'--git', '--allow-shallow', '--write', '--year'}
i = 0
while i < len(argv):
    if argv[i] in flags:
        opts[argv[i]] = True; i += 1
    elif argv[i].startswith('--'):
        opts[argv[i]] = argv[i + 1]; i += 2
    else:
        pages.append(argv[i]); i += 1
KEY = opts['--key']
DATE = re.compile(r'(\d{4}-\d{2}-\d{2})')


def front_matter_span(text):
    if not text.startswith('---\n'):
        return None
    end = text.find('\n---', 3)
    return (4, end) if end != -1 else None


def read_date(text):
    if KEY.startswith(':'):
        m = re.search(r'^' + re.escape(KEY) + r'\s*(\S+)', text, re.M)
        return DATE.match(m.group(1)).group(1) if m and DATE.match(m.group(1)) else None
    span = front_matter_span(text)
    if not span:
        return None
    fm = text[span[0]:span[1]]
    if '.' in KEY:
        parent, child = KEY.split('.', 1)
        m = re.search(r'^' + parent + r':\s*\n((?:[ \t]+.*\n?)+)', fm + '\n', re.M)
        m = m and re.search(r'^\s+' + child + r':\s*["\']?(\d{4}-\d{2}-\d{2})', m.group(1), re.M)
        if not m:  # flow style: last_update: {date: 2024-12-05}
            m = re.search(r'^' + parent + r':\s*\{[^}]*\b' + child + r':\s*["\']?(\d{4}-\d{2}-\d{2})', fm, re.M)
    else:
        m = re.search(r'^' + KEY + r':\s*["\']?(\d{4}-\d{2}-\d{2})', fm, re.M)
    return m.group(1) if m else None


def write_date(text, date):
    if KEY.startswith(':'):
        line = f'{KEY} {date}'
        if re.search(r'^' + re.escape(KEY), text, re.M):
            return re.sub(r'^' + re.escape(KEY) + r'.*$', line, text, count=1, flags=re.M)
        # after the document title line (= Title), in the header
        return re.sub(r'^(= .*\n)', r'\1' + line + '\n', text, count=1, flags=re.M)
    span = front_matter_span(text)
    if '.' in KEY:
        parent, child = KEY.split('.', 1)
        block = f'{parent}:\n  {child}: {date}'
        pattern = r'^' + parent + r':(?:\s*\{[^}]*\}|\s*\n(?:[ \t]+.*\n?)+)'
    else:
        block = f'{KEY}: {date}'
        pattern = r'^' + KEY + r':.*$'
    if not span:
        return f'---\n{block}\n---\n' + text
    fm = text[span[0]:span[1]]
    if re.search(pattern, fm + '\n', re.M):
        fm = re.sub(pattern, block + ('\n' if '.' in KEY else ''), fm + '\n', count=1, flags=re.M).rstrip('\n')
    else:
        fm = fm + '\n' + block
    return text[:span[0]] + fm + text[span[1]:]


def git(cwd, *a):
    return subprocess.run(['git', *a], cwd=cwd, capture_output=True, text=True, check=True).stdout


ignore = set()
if opts.get('--ignore-revs'):
    for line in open(opts['--ignore-revs']):
        line = line.split('#', 1)[0].strip()
        if line:
            ignore.add(line)
marker = opts.get('--marker')

if opts.get('--git') and pages:
    top = os.path.dirname(os.path.abspath(pages[0]))
    if git(top, 'rev-parse', '--is-shallow-repository').strip() == 'true' and not opts.get('--allow-shallow'):
        sys.exit('content-date: shallow clone: every file seems to change in the newest commit. '
                 'Fetch the full history (for example `fetch-depth: 0` in actions/checkout), '
                 'or pass --allow-shallow.')

newest = None
for page in pages:
    text = open(page, encoding='utf-8').read()
    date, src = read_date(text), 'page'
    if opts.get('--git'):
        d = os.path.dirname(os.path.abspath(page))
        for line in git(d, 'log', '--format=%H%x09%at%x09%B%x00', '--', os.path.basename(page)).split('\0'):
            line = line.strip()
            if not line:
                continue
            h, at, msg = (line.split('\t', 2) + [''])[:3]
            if h in ignore or (marker and marker in msg):
                continue
            # author date, in UTC, as a calendar date
            g = datetime.fromtimestamp(int(at), timezone.utc).strftime('%Y-%m-%d')
            if not date or g > date:
                date, src = g, f'git {h[:10]}'
            break
    if date is None:
        src = 'none'
    elif opts.get('--write'):
        open(page, 'w', encoding='utf-8').write(write_date(text, date))
    if date and (newest is None or date > newest):
        newest = date
    if not opts.get('--year'):
        print(f'{page}\t{date or ""}\t{src}')
print(newest[:4] if opts.get('--year') and newest else f'SITE_YEAR={newest[:4] if newest else ""}')
