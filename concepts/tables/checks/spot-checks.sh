#!/usr/bin/env bash
# Spot checks from the intent files, run against built pages.
# Usage: spot-checks.sh DIR — DIR holds one built page per test page, named
# <page>.html (scale-table-host, credential-types, metadata,
# troubleshooting_slow_requests, uaa-concepts), with React's <!-- --> text
# markers and empty class attributes removed:
#   sed 's/<!-- -->//g; s/ class=""//g' build/<mode>/<page>/index.html > DIR/<page>.html
B=$1; fail=0
chk() { if grep -q -- "$2" "$B/$1.html"; then echo "ok    $1: $3"; else echo "FAIL  $1: $3"; fail=1; fi; }
nchk() { if grep -q -- "$2" "$B/$1.html"; then echo "FAIL  $1: $3"; fail=1; else echo "ok    $1: $3"; fi; }
cnt() { n=$(grep -o -- "$2" "$B/$1.html" | wc -l | tr -d ' '); [ "$n" = "$3" ] && echo "ok    $1: $4 ($n)" || { echo "FAIL  $1: $4 (got $n, want $3)"; fail=1; }; }
# _oss_scale_table (host page)
cnt scale-table-host '≥ [12]' 12 '≥ rendered'
nchk scale-table-host '&amp;ge;' 'no literal &ge;'
chk scale-table-host '<code>0</code> if Postgres' 'code 0 in PostgreSQL row'
chk scale-table-host 'Cloud Foundry recommends scaling NATS VMs' 'recommended_by var'
chk scale-table-host 'The following table provides recommended instance counts' 'partial inside host'
# credential-types
for c in value json user password certificate rsa ssh; do chk credential-types "<t[dh][^>]*>\(<div[^>]*>\)\?<code>$c</code>\(</div>\)\?</t[dh]>" "code $c"; done
nchk credential-types '[“”]' 'no curly quotes'
# metadata
cnt metadata 'Alphanumeric  *( \[a-z0-9A-Z\] )' 4 'brackets without backslashes'
nchk metadata '\\\[a-z' 'no backslash escapes'
chk metadata '<li><code>-</code></li>' 'one-char code spans'
chk metadata '<th colspan="4"[^>]*>Label requirements</th>' 'title row spans the table'
body() { sed -n '/<article/,/<\/article>/p' "$B/$1.html" > "$B/$1.body"; }
body metadata; body troubleshooting_slow_requests
nchkb() { if grep -q -- "$2" "$B/$1.body"; then echo "FAIL  $1: $3"; fail=1; else echo "ok    $1: $3"; fi; }
nchkb metadata '{vars\.' 'no literal var expressions in page body'
nchk metadata 'name="description" content="[^"]*{vars' 'meta description free of var expressions'
nchk troubleshooting_slow_requests 'name="description" content="[^"]*{vars' 'meta description free of var expressions'
nchk metadata 'metadata_ref' 'undefined var renders empty'
chk metadata '<code>KEY==VALUE</code>' 'pipe table code'
chk metadata '<code>!KEY</code>' 'pipe table !KEY'
# troubleshooting
chk troubleshooting_slow_requests 'did not reach Cloud Foundry' 'var in table 1 row 4'
chk troubleshooting_slow_requests '<code>Could not resolve host: NONEXISTENT.com</code>' 'code in table 1 row 3'
chk troubleshooting_slow_requests 'href="#gorouter-latency"' 'link in table 5'
chk troubleshooting_slow_requests 'href="#total-latency"' 'link in table 6'
nchk troubleshooting_slow_requests 'bosh_cli_link' 'undefined var renders empty'
chk troubleshooting_slow_requests 'locate delays in Cloud Foundry' 'var in heading'
# uaa
chk uaa-concepts 'in a Cloud Foundry deployment' 'platform_name 1'
chk uaa-concepts 'in the Cloud Foundry ecosystem' 'platform_name 2'
chk uaa-concepts 'href="#clientid"' 'clientid link'
chk uaa-concepts '<code>allowed providers=&quot;ldap&quot;</code>\|<code>allowed providers="ldap"</code>' 'straight quotes in code'
chk uaa-concepts '{OIDC provider alias}' 'literal braces in prose'
chk uaa-concepts "<t[dh][^>]*>\(<div[^>]*>\)\?<code>client_credentials</code>\(</div>\)\?</t[dh]>" "implicit row closed before client_credentials"
nest=$(python3 -I - "$B/troubleshooting_slow_requests.html" <<'PY'
import sys,re; s=open(sys.argv[1]).read()
a=s.find('id="within-cf"'); b=s.find('id="duplicate-latency"', a); d=0; out=[]
for close,t in re.findall(r'<(/?)(ol|ul|li|table)[ >]', s[a:b]):
    if t in('ol','ul'): d += -1 if close else 1
    elif t=='table' and not close: out.append(d)
print(out)
PY
)
[ "$nest" = "[1]" ] && echo "ok    troubleshooting_slow_requests: table 2 inside its list step" || { echo "FAIL  troubleshooting_slow_requests: table 2 nesting $nest"; fail=1; }
exit $fail
