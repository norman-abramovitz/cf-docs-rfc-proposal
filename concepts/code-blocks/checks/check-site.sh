#!/usr/bin/env bash
# Code-block check, outline check and (where a page has notes) notes check
# for every test page in the given modes of one built site.
# Usage: check-site.sh OUT MAP REQUIRE [MODE...]
#   OUT holds the built pages as <mode>/<page>/index.html, or, for pages
#   the browser check saved, as <mode>-<page>.html (then OUT is that folder).
#   MAP is the admonition type each note kind becomes, as the notes round's
#   notes.py --map takes it; notes are admonitions in every mode (the notes
#   round's native form), so the map applies to every mode. REQUIRE is what
#   codeblocks.py --require asks of every block in native mode (type,
#   highlight, copy); passthrough is checked for text, place and leaks only.
#   Each page's code blocks are compared with ../intent/<page>.code, its
#   outline with its published copy (the section the page converts) and its
#   anchors file. A page missing from a mode fails.
here=$(cd "$(dirname "$0")" && pwd)
outline=$here/../../headings/checks/outline.py
notes=$here/../../notes/checks/notes.py
out=$1; map=$2; require=$3; shift 3
modes=${*:-passthrough native}
pages="routes-domains troubleshooting_slow_requests gsg-grails backup backup-clean nginx multiple-processes"
fail=0
for m in $modes; do
  for p in $pages; do
    pub=$here/../published/$p.html; sec=(); nf=""; anchors=$here/../intent/$p.anchors
    case $p in
      routes-domains)                pub=$here/../../headings/published/$p.html; sec=(--section create-route); nf=$here/../intent/$p.notes ;;
      troubleshooting_slow_requests) pub=$here/../../headings/published/$p.html; anchors=$here/../../headings/intent/$p.anchors ;;
      gsg-grails)                    sec=(--section step-5:-create-and-bind-a-service-instance-for-a-grails-application); nf=$here/../intent/$p.notes ;;
      backup)                        sec=(--section connect-to-jumpbox); nf=$here/../intent/$p.notes ;;
      backup-clean)                  pub=$here/../published/backup.html; sec=(--section manual-clean); nf=$here/../intent/$p.notes ;;
      nginx)                         sec=(--section templating) ;;
      multiple-processes)            nf=$here/../intent/$p.notes ;;
    esac
    echo "== $m/$p"
    built=$out/$m/$p/index.html
    [ -f "$built" ] || built=$out/$m-$p.html
    if [ ! -f "$built" ]; then echo "FAIL  not built"; fail=1; continue; fi
    req=""; [ "$m" = native ] && req=$require
    python3 -I "$here/codeblocks.py" "$built" --expect "$here/../intent/$p.code" ${req:+--require "$req"} || fail=1
    python3 -I "$outline" "$pub" "$built" "${sec[@]}" --anchors "$anchors" || fail=1
    if [ -n "$nf" ]; then
      python3 -I "$notes" "$built" --expect "$nf" ${map:+--map "$map"} || fail=1
    fi
  done
done
exit $fail
