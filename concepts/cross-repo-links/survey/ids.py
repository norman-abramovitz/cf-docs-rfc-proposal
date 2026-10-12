"""Check the survey's model of the ids the book generates for Markdown
headings against published pages.

Usage:
  python3 -I ids.py REPOS_DIR PUBLISHED.html...

Each published page names its source file in its "View the source for this
page in GitHub" link (Bookbinder's repo link). The source is read from
REPOS_DIR (clones named by repository), with the partials it includes from
its own folder, and every Markdown heading's id is made the way survey.py
makes it: tags removed, lowercased, every
space a hyphen, with each variable replaced by its value from the book's
config/template_variables.yml. Each `id` attribute on an h1-h6 of the published page must
be among the model's ids or the source's own ids. Prints one line per page
and every id the model misses. The published page may be built from a
later commit than the clone; a heading changed since shows as a miss.
"""
import os, re, sys

if len(sys.argv) < 3:
    sys.exit(__doc__)
REPOS, pages = sys.argv[1], sys.argv[2:]
FENCE = re.compile(r'^\s*(```|~~~)')
HEADING_MD = re.compile(r'^\s{0,3}(#{1,6})(.*?)\s*#*\s*$')
ID_ATTR = re.compile(r'''\b(?:id|name)\s*=\s*(?:"([^"]*)"|'([^']*)')''', re.I)
PARTIAL = re.compile(r'<%=?\s*partial\s*\(?\s*([\'"])(.*?)\1')


values = {}
for l in open(os.path.join(REPOS, 'docs-book-cloudfoundry', 'config', 'template_variables.yml'), encoding='utf-8'):
    m = re.match(r'^  ([A-Za-z0-9_]+):\s*(.*)$', l)
    if m:
        v = m.group(2).strip()
        values[m.group(1)] = v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'' else v


def gen_id(inner):
    text = re.sub(r'<%=\s*vars\.([A-Za-z0-9_]+)\s*-?%>', lambda m: values.get(m.group(1), ''), inner)
    text = re.sub(r'<[^>]+>', '', text)
    return text.rstrip().lower().replace(' ', '-')


def source_ids(path, depth=0):
    text = open(path, encoding='utf-8', errors='replace').read()
    model, own, fence = set(), set(), None
    for l in text.split('\n'):
        if FENCE.match(l):
            fence = None if fence else l
            continue
        if fence:
            continue
        for m in ID_ATTR.finditer(l):
            own.add(m.group(1) if m.group(1) is not None else m.group(2))
        h = HEADING_MD.match(l)
        if h:
            inner = h.group(2)
            model.add(gen_id(inner[1:] if inner.startswith(' ') else inner))
    if depth < 3:
        for m in PARTIAL.finditer(text):
            head, _, tail = m.group(2).rpartition('/')
            folder = os.path.normpath(os.path.join(os.path.dirname(path), head))
            for n in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
                if n.startswith(f'_{tail}.'):
                    a, b = source_ids(os.path.join(folder, n), depth + 1)
                    model |= a; own |= b
    return model, own


fail = 0
for page in pages:
    html = open(page, encoding='utf-8', errors='replace').read()
    m = re.search(r'''id=['"]repo-link['"] href=['"]https://github\.com/cloudfoundry/([^/]+)/(?:blob|tree)/[^/]+/([^'"]+)['"]''', html)
    if not m:
        print(f'{page}: no repo link'); fail = 1; continue
    repo, rel = m.group(1), m.group(2)
    src = os.path.join(REPOS, repo, rel)
    if not os.path.exists(src):
        print(f'{page}: {repo}/{rel} not in the clone'); fail = 1; continue
    model, own = source_ids(src)
    pub = re.findall(r'<h[1-6][^>]*\bid="([^"]+)"', html)
    miss = [i for i in pub if i not in model and i not in own]
    print(f'{os.path.basename(page)}: {repo}/{rel}: {len(pub)} heading ids, {len(pub) - len(miss)} made by the model')
    for i in miss:
        print(f'  missed: {i}')
        fail = 1
sys.exit(fail)
