#!/usr/bin/env bash
# Links check and outline check for every test page in the given variants of
# one built site.
# Usage: check-site.sh OUT VARIANT...
#   OUT/<variant> holds one built site, served at the root of the host. Each
#   test page is looked for as <key>.html and as <key>/index.html. The links
#   check compares the page's links with intent/<page>.links; the outline
#   check compares its headings with the published copy and looks for the
#   ids in intent/<page>.anchors.
here=$(cd "$(dirname "$0")" && pwd)
outline=$here/../../headings/checks/outline.py
out=$1; shift
pages="concepts/http-routing adminguide/troubleshooting-router-error-responses adminguide/enabling-tcp-routing devguide/deploy-apps/routes-domains"
published() {
  case $1 in
    http-routing) echo "$here/../published/http-routing.html" ;;
    troubleshooting-router-error-responses) echo "$here/../../variables/published/$1.html" ;;
    enabling-tcp-routing) echo "$here/../../partials/published/$1.html" ;;
    routes-domains) echo "$here/../../headings/published/$1.html" ;;
  esac
}
fail=0
for v in "$@"; do
  site=$out/$v
  [ -d "$site" ] || { echo "FAIL  $v: not built"; fail=1; continue; }
  for key in $pages; do
    name=${key##*/}
    built=""
    for f in "$site/$key.html" "$site/$key/index.html"; do
      [ -f "$f" ] && { built=$f; break; }
    done
    echo "== $v/$key"
    if [ -z "$built" ]; then echo "FAIL  $key: no page"; fail=1; continue; fi
    python3 -I "$here/links.py" "$built" --root "$site" --expect "$here/../intent/$name.links" || fail=1
    python3 -I "$outline" "$(published "$name")" "$built" --anchors "$here/../intent/$name.anchors" || fail=1
  done
done
exit $fail
