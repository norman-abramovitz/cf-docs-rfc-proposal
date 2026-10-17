"""Inventory every version a page writes as text or in a link, in the cloned
documentation repositories and in the book's variables file.

Usage:
  python3 -I survey.py REPOS_DIR SHAS MENTIONS.csv

REPOS_DIR and SHAS as for the variables survey (../../variables/survey/),
whose place rules (place_of, containers) this script loads rather than
repeats. Reads files only; runs nothing from the clones.

MENTIONS.csv has one row per version mention:
  - in text: a token v1.2, v263, 1.2.3 (with a suffix such as -rc.1),
    outside links and ERB tags; IP addresses are counted and dropped;
  - in a link: a URL whose path names a version or a branch;
  - in the variables file: a version in a key's value.
Each row has the rule that sorted it and the category the rule gives
(README, Categories); `undecided` where no rule decides.
"""
import csv, os, re, sys
from collections import Counter

if len(sys.argv) != 4:
    sys.exit(__doc__)
REPOS, SHAS, OUT = sys.argv[1:]

# The variables survey's helpers: everything above its scan section.
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'variables', 'survey', 'survey.py'),
            encoding='utf-8').read().split('# ---------------------------------------------------------------- scan')[0]
_argv, sys.argv = sys.argv, ['survey.py', REPOS, SHAS, os.devnull, os.devnull]
V = {}
exec(compile(_src, 'variables/survey/survey.py', 'exec'), V)
sys.argv = _argv

TOKEN = re.compile(r'(?<![\w./-])(v?\d+\.\d+\.\d+(?:[-+][A-Za-z0-9][\w.]*)?|v\d+(?:\.\d+)?|\d+\.\d+)(\+?)(?![\w/]|\.\d)')
IP = re.compile(r'(?<![\w.])\d{1,3}(?:\.\d{1,3}){3}(?![\w.])')
PATH_TOKEN = re.compile(r'(?<![\w.])v?\d+(?:\.\d+)+(?![\w])|(?<![\w])v\d+(?![\w])')  # in a URL a / or - may come first
URL = re.compile(r'https?://[^\s)"\'<>\]`]+')
NAMED = re.compile(  # a two-part number is a version only when a name or word says so
    r'(?:\b(?:v|version|versions|release|cli|api|ubuntu|go|golang|ruby|python|node|node\.js|java|jdk|jre|php|'
    r'dotnet|\.net|core|bosh|director|stemcell|cflinuxfs\d|buildpack|capi|diego|routing-release|cf-deployment|'
    r'garden-runc|tomcat|spring|boot|nginx|haproxy|mysql|postgres(?:ql)?|redis|openjdk|kubernetes|windows|'
    r'server|rabbitmq|uaa|credhub|loggregator)\s*)$', re.I)
BOUND = re.compile(
    r'\bor (?:later|above|higher|newer|greater|earlier|below|lower|older)\b|\band (?:later|above|higher|newer|earlier)\b|'
    r'>=|≥|<=|\bstarting (?:with|in|from|at)\b|\bavailable (?:from|in|with|since|starting)\b|'
    r'\b(?:introduced|added|deprecated|removed|fixed|changed) in\b|\brequires?\b|\brequired\b|\bsince\b|'
    r'\bprior to\b|\bbefore\b|\buntil\b|\b(?:older|newer|earlier|later|greater|lower|higher) than\b|'
    r'\bat least\b|\bminimum\b|\bup to\b|\bthrough\b|\bas of\b|\bbeginning (?:with|in)\b|\bdelivered in\b|'
    r'\bbetween v?\d[\w.]* and\b|\bfrom v\d|\bbump(?:ed)? to\b|v\d[\w.]*\s*~\s*v?\d', re.I)
NOT_RELEASE = re.compile(r'\b(?:TLS|TLSv|SSL|SSLv|HTTP|HTTPS|IPv|SHA|OAuth|SAML|OpenID|SNMP|SMB|NFS|NFSv|SMBv|'
                         r'JSON|YAML|AMQP|MQTT|gRPC|SPDY|Open Service Broker API|OSBAPI|OSB API|service broker API|'
                         r'broker API|API version|cgroups?|UUID)\s*(?:v?\d[\w.]*\s*(?:and|or|,)\s*)?$', re.I)
COMMAND = re.compile(  # commands that fetch or install a given version; other code with a version is a sample
    r'^\s*(?:[$>]\s*)?(?:sudo\s+)?(?:bosh\s+(?:-\S+\s+)*(?:upload-release|upload-stemcell|create-env|deploy)|'
    r'cf\s+(?:install-plugin|create-buildpack|update-buildpack)|curl|wget|gem\s+install|go\s+(?:install|get)|'
    r'npm\s+(?:install|i)|pip3?\s+install|brew\s+install|apt(?:-get)?\s+install|docker\s+(?:pull|run)|'
    r'helm\s+install|git\s+(?:clone|checkout)|uaac\s+target)\b')
HISTORY = re.compile(r'(^|/)(archive|release[-_]notes|recent|changelog|whats[-_]new|deprecations?)(/|[-_.]|$)', re.I)

def link_kind(u):
    """(rule, category) of a URL, or None when it names no version or branch."""
    host, _, path = u.split('://', 1)[1].partition('/')
    if re.match(r'(localhost|0\.0\.0\.0|\d+\.\d+\.\d+\.\d+|[\w-]+:[^@/]*@)', host) or re.search(r':\d+$', host):
        return ('local-host', '7') if PATH_TOKEN.search(path) or IP.search(host) else None
    if re.search(r'^[^/]+/[^/]+/(?:blob|tree|raw|edit)/(?:master|main|develop)(?:/|$)', path) and host == 'github.com' \
            or host == 'raw.githubusercontent.com' and re.search(r'^[^/]+/[^/]+/(?:master|main|develop)/', path):
        return 'branch-link', '4'
    if re.search(r'\.git#v?\d', path):
        return 'release-tag', '3'
    path = path.split('#')[0]  # a fragment's numbers are section numbers
    if host in ('www.youtube.com', 'youtube.com', 'youtu.be') or re.search(r'(?:^|/)(?:rfc\d+|LICENSE-)', path):
        return None
    if not PATH_TOKEN.search(path) and not re.search(r'[?&](?:v|version)=', path):
        return None
    if host in ('cdnjs.cloudflare.com', 'cdn.jsdelivr.net', 'unpkg.com'):
        return 'site-asset', '7'
    if re.search(r'(?:^|/)version/v?\d', path):
        return 'docs-version-pin', '3'
    if re.search(r'/releases/tag/|/(?:tree|blob)/v?\d|/compare/', path):
        return 'release-tag', '3'
    if re.search(r'\.(?:tgz|tar\.gz|zip|jar|war|deb|rpm|msi|exe|gem|pkg)(?:$|[?#])|/releases/download/|/dist/v?\d', path):
        return 'download', '3'
    if host != 'docs.cloudfoundry.org' and re.search(r'(?:^|/)(?:docs/|doc/refman/|en/[^/]+/|previous-versions/)', path + '/') \
            and re.search(r'/v?\d+(?:\.\d+)+/', '/' + path):
        return 'third-party-docs-version', '3'
    if host == 'bosh.io' and re.search(r'[?&](?:v|version)=', path):
        return 'bosh-io-version', '3'
    if re.search(r'(?:^|/)v\d+(?:\.\d+)?(?:/|$|[?#])', path) and not re.search(r'\.html', path):
        return 'api-path', '7'
    if re.search(r'-v\d|/v\d+\.html', path):
        return 'page-name', '7'
    return 'link-other', 'undecided'

def component(before):
    m = re.search(r'([A-Za-z][\w.+-]*(?:[ -](?:release|CLI|buildpack|API|Director|stemcell|CPI))?)\s*$', before)
    return m.group(1) if m else ''

def sentence(flat, a, b):
    s = max(flat.rfind('. ', 0, a), flat.rfind('\n\n', 0, a), flat.rfind('|', 0, a), a - 120)
    e = [x for x in (flat.find('. ', b), flat.find('\n\n', b), flat.find('|', b), b + 80) if x >= 0]
    return flat[s + 1:min(e)]

def text_kind(flat, lines, starts, pos, end, tok, place, rel):
    before = flat[max(0, pos - 40):pos]
    if re.search(r'/$', before) or re.search(r'[\w]-$', before):
        return 'api-path-or-name', '7'
    if NOT_RELEASE.search(before):
        return 'not-release', '7'
    if place not in ('fenced-code', 'indented-code', 'pre') and re.match(r'(?:\]\[[^\]]*\])?\+', flat[end:end + 40]):
        return 'bound', '1'
    if re.match(r'v\d+$', tok) and (re.search(r'\bAPI\s*$', before) or
                                    re.match(r'\s*(?:API|endpoints?|format|manifests?|schema)\b', flat[end:end + 20], re.I)):
        return 'not-release', '7'
    if place in ('fenced-code', 'indented-code', 'pre'):
        line = lines[V['line_of'](starts, pos)]
        if COMMAND.match(line):
            return 'code-command', '2'
        return 'code-other', '6'
    if BOUND.search(sentence(flat, pos, end)) or flat[end:end + 1] == '+':
        return 'bound', '1'
    if re.search(r'\bUbuntu\s*$', before):  # an Ubuntu release is named by its version
        return 'name-fact', '8'
    if HISTORY.search(rel):
        return 'history-page', '1'
    return 'prose', 'undecided'

rows, dropped = [], Counter()

def add(**kw):
    base = dict(repo='', file='', line='', url='', site='', archive='', partial_file='', found_in='', token='',
                component='', rule='', category='', link='', place='', detail='', table='', note='', list='', html='',
                context='')
    base.update(kw)
    rows.append(base)

for repo in sorted(V['sha']):
    root = os.path.join(REPOS, repo)
    if not os.path.isdir(root):
        continue
    site = 'bosh.io' if repo == 'docs-bosh' else 'mkdocs' if repo == 'docs-dotnet-core-tutorial' \
        else 'book-repo' if repo == V['BOOK'] else 'book'
    for dp, dn, fn in os.walk(root, followlinks=True):
        dn[:] = sorted(d for d in dn if d not in ('.git', 'node_modules', 'vendor'))
        for f in sorted(fn):
            if not f.endswith(V['EXTS']) or dp == root and f.endswith(('.md', '.markdown')):
                continue
            full = os.path.join(dp, f); rel = os.path.relpath(full, root)
            text = open(full, encoding='utf-8', errors='replace').read()
            lines = text.split('\n')
            starts = [0]
            for l in lines:
                starts.append(starts[-1] + len(l) + 1)
            fm = re.match(r'---\n.*?\n---\n', text, re.S)
            fm_end = fm.end() if fm else 0
            flat = V['blank_erb'](text)
            fenced = V['fenced_lines'](lines)
            html_block = lambda i: any(V['open_element'](flat, starts[i], t) is not None for t in ('table', 'pre', 'div', 'ul', 'ol', 'p'))
            indented = V['indented_code_lines'](lines, fenced, html_block)
            common = dict(repo=repo, file=rel, site=site, archive='yes' if '/archive/' in '/' + rel else 'no',
                          partial_file='yes' if f.startswith('_') else 'no')

            def where(pos, length):
                place, detail = V['place_of'](text, flat, lines, starts, fm_end, fenced, indented, pos, length, '=')
                table, note, in_list, html = V['containers'](flat, lines, starts, pos, place)
                li = V['line_of'](starts, pos) + 1
                return dict(line=li, url=V['url'](repo, rel, li), place=place, detail=detail, table=table,
                            note=note, list=in_list, html=html)

            spans = []
            for m in URL.finditer(flat):
                u = m.group(0).rstrip('.,;:')
                spans.append((m.start(), m.start() + len(u)))
                k = link_kind(u)
                if k:
                    t = re.search(r'/(?:blob|tree|raw|edit)/(master|main|develop)\b|/(master|main|develop)/', u) if k[1] == '4' \
                        else re.search(r'[?&](?:v|version)=([\w.-]+)', u) or PATH_TOKEN.search(u.split('://', 1)[1].partition('/')[2])
                    add(**common, **where(m.start(), len(u)), found_in='link', token=next((g for g in t.groups() if g), t.group(0)) if t else '',
                        rule=k[0], category=k[1], link=u[:200])
            for m in IP.finditer(flat):
                spans.append((m.start(), m.end()))
                dropped['ip-address'] += 1
            for m in TOKEN.finditer(flat):
                a, b = m.start(), m.end(1)
                if any(s <= a < e for s, e in spans):
                    continue
                tok = m.group(1)
                if re.fullmatch(r'\d+\.\d+', tok) and not NAMED.search(flat[max(0, a - 30):a]):
                    dropped['two-part number without a name'] += 1
                    continue
                w = where(a, b - a)
                rule, cat = text_kind(flat, lines, starts, a, b, tok, w['place'], rel)
                add(**common, **w, found_in='text', token=tok + m.group(2), component=component(flat[max(0, a - 40):a]),
                    rule=rule, category=cat, context=' '.join(flat[max(0, a - 60):b + 40].split()))

# the book's variables file: versions in values
book = V['BOOK']
for k, ln, v, style in V['parse_variables'](os.path.join(REPOS, book, V['TV'])):
    for m in URL.finditer(v or ''):
        lk = link_kind(m.group(0).rstrip('.,;:'))
        if lk:
            add(repo=book, file=V['TV'], line=ln, url=V['url'](book, V['TV'], ln), site='variables-file', found_in='value',
                token=k, rule=lk[0], category=lk[1], link=m.group(0)[:200], context=(v or '')[:160])
    for m in TOKEN.finditer(URL.sub(' ', v or '')):
        if re.fullmatch(r'\d+\.\d+', m.group(1)) and not NAMED.search((v or '')[max(0, m.start() - 30):m.start()]):
            continue
        s = v[max(0, m.start() - 120):m.end() + 80]
        rule, cat = ('bound', '1') if BOUND.search(s) or m.group(2) else ('value', 'undecided')
        add(repo=book, file=V['TV'], line=ln, url=V['url'](book, V['TV'], ln), site='variables-file', found_in='value',
            token=m.group(1) + m.group(2), component=k, rule=rule, category=cat, context=' '.join((v or '')[:160].split()))

with open(OUT, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

print(f'{len(rows)} mentions')
for (s, c), n in sorted(Counter((r['site'], r['category']) for r in rows).items()):
    print(f'  {s:15} {c:10} {n}')
print('dropped:', dict(dropped))
