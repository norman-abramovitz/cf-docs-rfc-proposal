"""What a built static site serves at old URLs: a page, a redirect page, or
nothing.

Usage:
  python3 -I redirects.py SITE URL_PATH...

For each URL path (for example /devguide/deploy-apps/domains-routes.html)
the file a static host would serve is looked up in SITE, as links.py does:
the file itself, PATH/index.html for a path ending in `/`, PATH.html for a
path without an extension, or PATH/index.html for a folder. Prints one line per path:

  PATH  ->  FILE  KIND  TARGET  TARGET_STATUS  SCRIPT

KIND is `redirect page` when the file holds a meta refresh, `page`
otherwise, or `missing`. TARGET is the refresh URL joined to PATH, and
TARGET_STATUS whether SITE has a file for it. A static host such as GitHub
Pages cannot answer with an HTTP redirect, so a redirect page is the only
redirect a static build can make. SCRIPT says whether the page's script
passes the old URL's fragment on (`passes #fragment`), redirects without it
(`drops #fragment`), or there is no script (`no script`).
"""
import os, re, sys
from urllib.parse import urljoin, urlsplit, unquote

if len(sys.argv) < 3:
    sys.exit(__doc__)
site = sys.argv[1]


def lookup(path):
    p = unquote(path).lstrip('/')
    cands = [p + 'index.html'] if p.endswith('/') or p == '' else [p]
    if not p.endswith('/') and '.' not in p.rsplit('/', 1)[-1]:
        cands += [p + '.html']
    if not p.endswith('/') and p:
        cands += [p + '/index.html']
    for c in cands:
        if os.path.isfile(os.path.join(site, c)):
            return c
    return None


for path in sys.argv[2:]:
    f = lookup(path)
    if f is None:
        print(f'{path}  ->  -  missing')
        continue
    html = open(os.path.join(site, f), encoding='utf-8', errors='replace').read()
    m = re.search(r'<meta[^>]+http-equiv=["\']?refresh["\']?[^>]*content=["\']\s*\d+\s*;\s*url=([^"\'>]+)', html, re.I)
    if not m:
        print(f'{path}  ->  {f}  page')
        continue
    target = urljoin('https://site' + path, m.group(1).strip())
    t = urlsplit(target)
    status = 'target exists' if lookup(t.path) else 'target missing'
    script = re.search(r'<script>(.*?)</script>', html, re.S)
    if not script:
        js = 'no script'
    else:
        js = 'passes #fragment' if re.search(r'\.hash|hash\.substr', script.group(1)) else 'drops #fragment'
    print(f'{path}  ->  {f}  redirect page  {t.path}{"#" + t.fragment if t.fragment else ""}  {status}  {js}')
