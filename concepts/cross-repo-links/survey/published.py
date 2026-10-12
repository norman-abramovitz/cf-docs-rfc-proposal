"""Compare the links survey.py predicts for a page with the links on the
page as docs.cloudfoundry.org serves it.

Usage:
  python3 -I published.py LINKS.csv PUBLISHED.html...

Each published page names its source file in its "View the source for this
page in GitHub" link. The rows of LINKS.csv that render on that page (its
own links, its partials' and its variables') give the expected `href` and
`src` values (published_href). The page's content area (main#js-content
without the "On this page" list, the repo link and the feedback form) gives
the actual ones. Prints, per page, how many expected links were found and
lists the rest both ways. The published page may be built from a later
commit than the clones, so a few differences can be edits made since.
"""
import csv, re, sys
from collections import Counter
from html import unescape

if len(sys.argv) < 3:
    sys.exit(__doc__)
rows = list(csv.DictReader(open(sys.argv[1])))
fail = 0
for page in sys.argv[2:]:
    html = open(page, encoding='utf-8', errors='replace').read()
    m = re.search(r'''id=['"]repo-link['"] href=['"]https://github\.com/cloudfoundry/([^/]+)/(?:blob|tree)/[^/]+/([^'"]+)['"]''', html)
    if not m:
        print(f'{page}: no repo link'); fail = 1; continue
    repo, rel = m.group(1), m.group(2)
    out = re.sub(r'(\.(erb|md|markdown))+$', '', rel)
    host = next((r['host_page'] for r in rows if r['host_repo'] == repo
                 and r['host_page'].endswith('/' + out) and r['host_page'].count('/') == out.count('/') + 1), None)
    if host is None:
        print(f'{page.split("/")[-1]}: {repo}/{rel}: 0 of 0 expected links found (no links in the survey)'); continue
    expected = Counter(r['published_href'] for r in rows
                       if r['host_page'] == host and r['where'] in ('page', 'partial', 'variable')
                       and r['form'] not in ('md-image', 'html-img') and r['published_href'])
    start = html.find('id="js-content"')
    end = html.find('repo-link', start)
    body = html[start:end]
    body = re.sub(r'<div class="js-quick-links">.*?</div>\s*</div>', '', body, flags=re.S)
    # Cloudflare, in front of the site, turns e-mail addresses in the text
    # into links to /cdn-cgi/l/email-protection; they are not in the source
    actual = Counter(unescape(h) for h in re.findall(r'<a\s[^>]*?href="([^"]*)"', body)
                     if not h.startswith('/cdn-cgi/'))
    actual -= Counter({'#top': actual.get('#top', 0)}) if '#top' not in expected else Counter()
    found = sum((expected & actual).values())
    print(f'{page.split("/")[-1]}: {repo}/{rel}: {found} of {sum(expected.values())} expected links found; '
          f'{sum(actual.values())} links on the page')
    for h, n in sorted((expected - actual).items()):
        print(f'  expected, not on the page: {h}' + (f' (x{n})' if n > 1 else ''))
    for h, n in sorted((actual - expected).items()):
        print(f'  on the page, not expected: {h}' + (f' (x{n})' if n > 1 else ''))
sys.exit(fail)
