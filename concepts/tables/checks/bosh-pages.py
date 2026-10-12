"""Spot checks for the bosh.io test pages (intent/bosh-networks.md,
intent/bosh-cpi-api-v2.md, intent/bosh-director-tasks.md,
intent/bpm-config.md), added 2026-10-12.
Usage: python3 -I bosh-pages.py DIR — DIR is .check/<mode>, holding
<page>.html as spot-checks.sh describes; the mode is DIR's last part.
Prints "ok    page: check" or "FAIL  page: check"; a page that is missing or
holds no matching table fails every check."""
import html, os, re, sys

D = sys.argv[1]
MODE = os.path.basename(os.path.normpath(D))
PASS = MODE.startswith('passthrough')
EXT = MODE == 'extension'
S = re.S


def load(page):
    try:
        return open(os.path.join(D, page + '.html'), encoding='utf-8').read()
    except OSError:
        return ''


def text(h):
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', h)).split())


def table(s, needle):
    """(start, end, html) of the first table holding needle, else (-1, -1, '')."""
    for m in re.finditer(r'<table\b.*?</table>', s, S):
        if needle in m.group(0):
            return m.start(), m.end(), m.group(0)
    return -1, -1, ''


def rows(t):
    """Header rows and body rows; each row is (tr attributes, cells), each
    cell (tag, attributes, inner HTML)."""
    head = ''.join(re.findall(r'<thead\b.*?</thead>', t, S))
    body = re.sub(r'<thead\b.*?</thead>', '', t, flags=S)
    def parse(h):
        return [(m.group(1), re.findall(r'<(t[dh])\b([^>]*)>(.*?)</t[dh]>', m.group(2), S))
                for m in re.finditer(r'<tr\b([^>]*)>(.*?)</tr>', h, S)]
    return parse(head), parse(body)


def cells_text(r):
    return [text(c[2]) for c in r[1]]


def span(c):
    m = re.search(r'colspan="?(\d+)', c[1], re.I)
    return int(m.group(1)) if m else 1


def target_after(s, end, href):
    """The element with id=href exists after position end."""
    m = re.search(r'\bid="%s"' % re.escape(href), s)
    return bool(m) and m.start() > end


def marker_hrefs(t):
    """For each superscript in t: (marker text, href of the in-page link in
    or around it, or None)."""
    out = []
    for m in re.finditer(r'<sup\b[^>]*>(.*?)</sup>', t, S):
        h = re.search(r'href="#([^"]+)"', m.group(1)) or \
            re.search(r'<a\b[^>]*href="#([^"]+)"[^>]*>\s*$', t[:m.start()])
        out.append((text(m.group(1)), h.group(1) if h else None))
    return out


fail = False


def check(page, msg, fn):
    global fail
    try:
        ok = bool(fn())
    except Exception:
        ok = False
    print(('ok    ' if ok else 'FAIL  ') + page + ': ' + msg)
    fail = fail or not ok


def has_table(t):
    if not t:
        raise ValueError('table not found')


# bosh-networks: T3 and T4 -------------------------------------------------
P = 'bosh-networks'
s = load(P)
a3, e3, t3 = table(s, 'Elastic IP')
a4, e4, t4 = table(s, 'Prefix delegation')
h3, b3 = rows(t3)
h4, b4 = rows(t4)

check(P, 'T3 header row of 4 cells, 4 body rows of 4 cells',
      lambda: has_table(t3) or (len(h3) == 1 and len(h3[0][1]) == 4 and [len(r[1]) for r in b3] == [4] * 4))
check(P, 'T3 line break in both network-type header cells',
      lambda: has_table(t3) or sum('<br' in c[2] for c in h3[0][1]) == 2)
check(P, 'T3 one note marker, superscript 1, in the AWS row',
      lambda: has_table(t3) or ([m for m, _ in marker_hrefs(t3)] == ['1'] and '<sup' in
                                next(r for r in b3 if 'AWS' in cells_text(r)[0])[1][1][2]))
check(P, 'T3 note 1 after T3, before T4, with its links and nic_group code',
      lambda: has_table(t3) is None and has_table(t4) is None and
      'maximum number of network interfaces attached to a VM is limited per instance type' in text(s[e3:a4])
      and 'AvailableIpPerENI.html' in s[e3:a4] and re.search(r'href="[^"]*manifest-v2[^"]*#instance-groups"', s[e3:a4])
      and '<code>nic_group</code>' in s[e3:a4])
check(P, 'T3 "Multiple" links to openstack-multiple-networks',
      lambda: re.search(r'href="[^"]*openstack-multiple-networks[^"]*"[^>]*>\s*Multiple\s*</a>', t3))
check(P, 'T3 vSphere row ends with - and -',
      lambda: cells_text(next(r for r in b3 if 'vSphere' in cells_text(r)))[-2:] == ['-', '-'])
if EXT:
    check(P, 'T3 extension: marker links to its note after the table',
          lambda: all(h and target_after(s, e3, h) for _, h in marker_hrefs(t3)) and marker_hrefs(t3))

iaas = ['AWS', 'Azure', 'OpenStack', 'vSphere']
data4 = [r for r in b4 if any(c in ('Manual', 'VIP') for c in cells_text(r))]
check(P, 'T4 holds AWS, Azure, OpenStack, vSphere once each, in order',
      lambda: has_table(t4) or [c for r in b4 for c in cells_text(r) if c in iaas] == iaas)
check(P, 'T4 eight data rows (Manual or VIP)', lambda: has_table(t4) or len(data4) == 8)
check(P, 'T4 em dash 11 times', lambda: has_table(t4) or text(t4).count('—') == 11)
check(P, 'T4 three note markers, superscripts 1, 2, 1',
      lambda: has_table(t4) or [m for m, _ in marker_hrefs(t4)] == ['1', '2', '1'])
if PASS:
    check(P, 'T4 passthrough: 11 body rows of 4 cells, spacer rows kept',
          lambda: has_table(t4) or [len(r[1]) for r in b4] == [4] * 11)
else:
    check(P, 'T4 no body row with every cell empty',
          lambda: has_table(t4) or not any(all(c == '' for c in cells_text(r)) for r in b4))
if EXT:
    def groups_ok():
        has_table(t4)
        width = len(h4[0][1])
        g = [r for r in b4 if len(r[1]) == 1 and span(r[1][0]) == width]
        return [cells_text(r)[0] for r in g] == iaas and all(len(r[1]) == width for r in data4)
    check(P, 'T4 extension: four full-width group rows; header as wide as a data row', groups_ok)

    def notes4_ok():
        has_table(t4)
        m3 = dict(marker_hrefs(t3))
        m4 = marker_hrefs(t4)
        return all(h and target_after(s, e4, h) for _, h in m4) and m4 and \
            all(h != m3.get('1') for m, h in m4 if m == '1')
    check(P, 'T4 extension: markers link to notes after the table, not to T3\'s note', notes4_ok)
after4 = s[e4:]
check(P, 'T4 note 1 after the table, with a 4-item list',
      lambda: has_table(t4) is None and
      'maximum number of IP addresses assigned to one NIC' in text(after4) and
      re.findall(r'<li\b[^>]*>(.*?)</li>', after4, S)[:4] and
      [text(x) for x in re.findall(r'<li\b[^>]*>(.*?)</li>', after4, S)[:4]] ==
      ['one IPv4 address', 'one IPv6 address', 'one IPv4 prefix delegation', 'one IPv6 prefix delegation'])
check(P, 'T4 note 2 after note 1, linking to ec2-prefix-eni.html',
      lambda: has_table(t4) is None and
      text(after4).find('Find the currently supported prefix sizes') > text(after4).find('assigned to one NIC') >= 0
      and re.search(r'href="[^"]*ec2-prefix-eni\.html"[^>]*>\s*Prefix delegation for AWS', after4))
check(P, 'T4 Azure "Supported" links to azure-cpi #dual-stack-networks',
      lambda: re.search(r'href="[^"]*azure-cpi[^"]*#dual-stack-networks"[^>]*>\s*Supported\s*</a>', t4))
check(P, 'anchors cpi-limitations and advanced-network-features',
      lambda: 'id="cpi-limitations"' in s and 'id="advanced-network-features"' in s)
check(P, 'no literal {: #id } text', lambda: s and '{: #' not in s)

# bosh-cpi-api-v2: T14 -----------------------------------------------------
P = 'bosh-cpi-api-v2'
s = load(P)
a, e, t = table(s, 'Should update registry')
h, b = rows(t)
check(P, 'T14 header row of 5 cells, 8 body rows of 5 cells',
      lambda: has_table(t) or (len(h) == 1 and len(h[0][1]) == 5 and [len(r[1]) for r in b] == [5] * 8))
check(P, 'T14 row 4 reads 2, 2, 2, Do not write to registry, Yes',
      lambda: cells_text(b[3]) == ['2', '2', '2', 'Do not write to registry', 'Yes'])
row_class = lambda r: re.search(r'\bclass="[^"]*\S', r[0])
all_bold = lambda r: all(re.search(r'<(strong|b)\b', c[2]) for c in r[1])
if EXT:
    check(P, 'T14 extension: row 4 marked as a row, cells not bold',
          lambda: row_class(b[3]) and not any(re.search(r'<(strong|b)\b', c[2]) for c in b[3][1]))
else:
    check(P, 'T14 row 4 marked as a row or all five cells bold',
          lambda: row_class(b[3]) or all_bold(b[3]))
check(P, 'T14 "full agent settings" italic, asterisk outside, user-metadata code',
      lambda: re.search(r'<em>\s*full agent settings\s*</em>', h[0][1][4][2]) and
      not re.search(r'settings\s*\*\s*</em>', t) and '<code>user-metadata</code>' in h[0][1][4][2]
      and '*' in text(h[0][1][4][2]))
if EXT:
    check(P, 'T14 extension: * marker links to the note after the table',
          lambda: (lambda m: m and target_after(s, e, m.group(1)))(re.search(r'href="#([^"]+)"', h[0][1][4][2])))
check(P, 'T14 note after the table, user-metadata as code',
      lambda: has_table(t) is None and
      'see below for information on the settings to write to user-metadata' in text(s[e:]) and
      '<code>user-metadata</code>' in s[e:])

# bosh-director-tasks: T18 -------------------------------------------------
P = 'bosh-director-tasks'
s = load(P)
a, e, t = table(s, 'SnapshotDeployments')
h, b = rows(t)
check(P, 'T18 header #, State, Timestamp, User, Description, Result; 2 body rows of 6 cells',
      lambda: has_table(t) or (len(h) == 1 and cells_text(h[0]) == ['#', 'State', 'Timestamp', 'User', 'Description', 'Result']
                               and [len(r[1]) for r in b] == [6, 6]))
check(P, 'T18 Result empty in both rows', lambda: [cells_text(r)[5] for r in b] == ['', ''])
check(P, 'T18 row 1 as printed',
      lambda: cells_text(b[0])[:5] == ['766', 'processing', '2015-01-27 21:39:30 UTC', 'admin', 'create deployment'])
check(P, 'T18 follows the bosh tasks code block and "Should result in:"',
      lambda: (lambda p: p >= 0 and 'bosh tasks' in text(s[p:a].split('</pre>')[0]) and
               'Should result in:' in text(s[p:a]))(s.rfind('<pre', 0, a)) and a >= 0)
if EXT:
    check(P, 'T18 extension: table carries table-output',
          lambda: re.search(r'<table\b[^>]*class="[^"]*\btable-output\b', t))
check(P, 'anchor active', lambda: 'id="active"' in s)
check(P, 'no literal {: #id } text', lambda: s and '{: #' not in s)

# bpm-config: B1-B6 ----------------------------------------------------------
P = 'bpm-config'
s = load(P)
B = [('B1', 'top-level listing', ['processes']),
     ('B2', 'shutdown_signal', ['name', 'executable', 'args', 'env', 'workdir', 'hooks', 'capabilities',
                                'limits', 'ephemeral_disk', 'persistent_disk', 'additional_volumes',
                                'unsafe', 'shutdown_signal']),
     ('B3', 'pre_start', ['pre_start']),
     ('B4', 'open_files', ['memory', 'open_files', 'processes']),
     ('B5', 'host_pid_namespace', ['privileged', 'unrestricted_volumes', 'host_pid_namespace']),
     ('B6', 'allow_executions', ['path', 'writable', 'allow_executions', 'mount_only', 'shared'])]
T = {n: table(s, needle) for n, needle, _ in B}
code_only = lambda c, name: re.fullmatch(r'\s*(?:<div[^>]*>\s*)?<code>%s</code>\s*(?:</div>\s*)?' % re.escape(name), c[2])
check(P, 'six tables, in source order B1-B6',
      lambda: all(T[n][0] >= 0 for n, _, _ in B) and [T[n][0] for n, _, _ in B] == sorted(T[n][0] for n, _, _ in B))
for n, _, names in B:
    def shape(n=n, names=names):
        h, b = rows(T[n][2])
        has_table(T[n][2])
        return len(h) == 1 and len(h[0][1]) == 4 and [len(r[1]) for r in b] == [4] * len(names) and \
            all(code_only(r[1][0], x) for r, x in zip(b, names))
    check(P, '%s header row of 4 cells, %d body rows of 4 cells, Property names as code (%s)'
          % (n, len(names), ', '.join(names) if len(names) < 4 else names[0] + ' ... ' + names[-1]), shape)
t2 = T['B2'][2]
check(P, 'B2 20 code spans', lambda: has_table(t2) or len(re.findall(r'<code\b', t2)) == 20)
check(P, 'B2 env Type reads string => string',
      lambda: cells_text(next(r for r in rows(t2)[1] if cells_text(r)[0] == 'env'))[1] == 'string => string')
check(P, 'B2 capabilities links to the capabilities(7) man page',
      lambda: re.search(r'href="https?://man7\.org/linux/man-pages/man7/capabilities\.7\.html"[^>]*>\s*capabilities\s*</a>', t2))
if not PASS:
    check(P, 'no header cell in B1-B6 wraps its text in bold',
          lambda: all(T[n][2] for n, _, _ in B) and
          not any(re.search(r'<(strong|b)\b', c[2]) for n, _, _ in B for c in rows(T[n][2])[0][0][1]))
e6 = T['B6'][1]
check(P, 'note after B6: "Note: The volumes in additional volumes must have a path inside /var/vcap"',
      lambda: e6 > 0 and 'Note: The volumes in additional volumes must have a path inside /var/vcap' in text(s[e6:])
      and '<code>unrestricted_volumes</code>' in s[e6:])
if not PASS:
    check(P, 'no * before "Note"', lambda: e6 > 0 and 'Note: The volumes' in text(s[e6:]) and '*Note' not in text(s[e6:]))

sys.exit(1 if fail else 0)
