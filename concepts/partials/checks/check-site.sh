#!/usr/bin/env bash
# Partials check, outline check and (where a page has notes) notes check for
# every test page in the given modes of one built site.
# Usage: check-site.sh OUT MAP [MODE...]
#   OUT holds the built pages as <mode>/<page>/index.html. MAP is the
#   admonition type each source kind becomes in native mode, as notes.py
#   --map takes it; other modes keep the source's classes.
#   Every page in OUT/<mode>/ is checked. A page named <page>--<variant>
#   (variable mode) is checked against <page>'s intent. Each page's outline
#   is compared with its published copy, for the excerpt the sites convert.
#   IGNORE_IDS, if set, is passed to partials.py --ignore-ids.
here=$(cd "$(dirname "$0")" && pwd)
outline=$here/../../headings/checks/outline.py
notes=$here/../../notes/checks/notes.py
out=$1; map=$2; shift 2
modes=${*:-passthrough native}
fail=0
for m in $modes; do
  [ -d "$out/$m" ] || { echo "FAIL  $m: not built"; fail=1; continue; }
  for dir in "$out/$m"/*/; do
    page=$(basename "$dir"); p=${page%%--*}
    [ -f "$dir/index.html" ] || continue
    [ -f "$here/../intent/$p.partials" ] || continue
    pub=$here/../published/$p.html; nf=""
    case $p in
      high-availability)       sec=(--section instance-counts) ;;
      architecture)            sec=(--section architecture-references --until system-metrics-agents) ;;
      enabling-tcp-routing)    sec=(--section prerequisites --until tls-tcp-routes); nf=$here/../intent/$p.notes ;;
      troubleshoot-app-health) sec=(--section routing-conflict) ;;
      routes-domains)          sec=(--section map-route-to-mult-apps); pub=$here/../../headings/published/$p.html ;;
      using-vol-services)      sec=(--section nfs --until migrate); pub=$here/../../notes/published/$p.html
                               nf=$here/../../notes/intent/$p.notes ;;
    esac
    echo "== $m/$page"
    python3 -I "$outline" "$pub" "$dir/index.html" "${sec[@]}" --anchors "$here/../intent/$p.anchors" || fail=1
    python3 -I "$here/partials.py" "$dir/index.html" --expect "$here/../intent/$p.partials" \
      ${IGNORE_IDS:+--ignore-ids "$IGNORE_IDS"} || fail=1
    if [ -n "$nf" ]; then
      if [ "$m" = native ] && [ -n "$map" ]; then
        python3 -I "$notes" "$dir/index.html" --expect "$nf" --map "$map" || fail=1
      else
        python3 -I "$notes" "$dir/index.html" --expect "$nf" || fail=1
      fi
    fi
  done
done
exit $fail
