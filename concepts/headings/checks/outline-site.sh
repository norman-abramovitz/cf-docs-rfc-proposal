#!/usr/bin/env bash
# Outline check for every test page in every mode of one built site.
# Usage: outline-site.sh OUT [MODE...]
#   OUT holds the built pages as <mode>/<page>/index.html. Each page is
#   compared with its published copy in ../published/, and the anchors in
#   ../intent/<page>.anchors must exist. routes-domains is an excerpt: only
#   its Domains section is compared.
here=$(cd "$(dirname "$0")" && pwd)
out=$1; shift
modes=${*:-passthrough native native-plain}
fail=0
for m in $modes; do
  for p in metadata troubleshooting_slow_requests access-control routes-domains; do
    sec=
    [ "$p" = routes-domains ] && sec='--section domains'
    echo "== $m/$p"
    python3 -I "$here/outline.py" "$here/../published/$p.html" "$out/$m/$p/index.html" \
      --anchors "$here/../intent/$p.anchors" $sec || fail=1
  done
done
exit $fail
