"""Where the version in each category 3 and 4 link could come from.

Usage:
  python3 -I sources.py MENTIONS.csv CF-DEPLOYMENT.yml

CF-DEPLOYMENT.yml is cf-deployment's manifest at a tag (README, How to
rerun). A link's target is the GitHub repository it points to, directly or
through bosh.io; a repository named in the manifest's `releases:` (with or
without `-release`) is a release the manifest pins.
"""
import csv, re, sys
from collections import Counter

if len(sys.argv) != 3:
    sys.exit(__doc__)
MENTIONS, CFD = sys.argv[1:]
text = open(CFD, encoding='utf-8').read()
cfd = set(re.findall(r'^- name: (\S+)\n', text[text.index('\nreleases:'):], re.M))
CF_ORGS = ('cloudfoundry', 'cloudfoundry-incubator', 'pivotal-cf', 'cloudfoundry-community')


def target(u):
    m = re.search(r'(?:github\.com|raw\.githubusercontent\.com)/([^/]+)/([^/#?]+)', u)
    if m:
        return m.group(1).lower(), re.sub(r'\.git$', '', m.group(2)).lower()
    m = re.search(r'bosh\.io/(?:d|releases|jobs)/[^?]*?github\.com/([^/]+)/([^/&?#]+)', u) \
        or re.search(r'source=github\.com/([^/]+)/([^/&#]+)', u)
    if m:
        return m.group(1).lower(), m.group(2).lower()
    return re.search(r'://([^/]+)', u).group(1), ''


def source(u):
    org, repo = target(u)
    if 'v3-apidocs.cloudfoundry.org' in org:
        return 'CC API version (capi-release ships it)'
    if '/api/uaa/' in u:
        return 'UAA version (uaa-release ships it)'
    if '/api/credhub/' in u:
        return 'CredHub version (credhub-release ships it)'
    if org == 'openservicebrokerapi':
        return 'OSBAPI spec version (Cloud Controller supports one)'
    if org == 'bosh.io' and 'stemcell' in u:
        return 'stemcell (cf-deployment.yml pins one)'
    if org in CF_ORGS:
        if repo in cfd or re.sub(r'-release$', '', repo) in cfd:
            return 'release in cf-deployment.yml'
        if repo == 'cf-deployment':
            return 'cf-deployment itself (its tag)'
        if repo.startswith('docs-'):
            return 'a docs repository'
        return 'other CF repository (BOSH, CPIs, bosh-deployment, tools)'
    return 'outside the CF organizations'


rows = [r for r in csv.DictReader(open(MENTIONS, encoding='utf-8')) if r['category'] in ('3', '4')]
c = Counter((r['category'], source(r['link'])) for r in rows)
for (cat, src), n in sorted(c.items()):
    print(f'{cat}  {src:58} {n}')
print('category 4, most linked repositories:')
for t, n in Counter('/'.join(target(r['link'])) for r in rows if r['category'] == '4').most_common(10):
    print(f'   {t:58} {n}')
print('CC API reference versions pinned:',
      ' '.join(sorted({re.search(r'version/([^/]+)', r['link']).group(1) for r in rows if 'v3-apidocs' in r['link']},
                      key=lambda v: [int(x) for x in v.split('.')])))
