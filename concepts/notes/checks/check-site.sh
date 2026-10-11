#!/usr/bin/env bash
# Outline check and notes check for every test page in every mode of one
# built site.
# Usage: check-site.sh OUT MAP [MODE...]
#   OUT holds the built pages as <mode>/<page>/index.html. MAP is the
#   admonition type each source kind becomes in native mode, as notes.py
#   --map takes it (important=info,caution=warning); passthrough keeps the
#   source's classes, so no map applies there.
#   Each page's outline is compared with its published copy; its notes with
#   ../intent/<page>.notes. Two pages are excerpts: routes-domains (the
#   Domains section, with the headings round's anchors) and
#   using-vol-services (the opening and the NFS section up to "Migrate").
#   A page missing from passthrough or native fails. The raw mode holds only
#   the pages whose notes, as written, differ from passthrough and still
#   build, so a page missing there is skipped.
here=$(cd "$(dirname "$0")" && pwd)
outline=$here/../../headings/checks/outline.py
out=$1; map=$2; shift 2
modes=${*:-passthrough native}
fail=0
for m in $modes; do
  for p in cf-backup using-vol-services healthchecks routes-domains; do
    pub=$here/../published/$p.html; extra=()
    case $p in
      routes-domains) pub=$here/../../headings/published/$p.html
                      extra=(--section domains --anchors "$here/../../headings/intent/$p.anchors") ;;
      using-vol-services) extra=(--section nfs --until migrate) ;;
    esac
    echo "== $m/$p"
    if [ ! -f "$out/$m/$p/index.html" ]; then
      if [ "$m" = raw ]; then echo "skip  not in this mode"; else echo "FAIL  not built"; fail=1; fi
      continue
    fi
    python3 -I "$outline" "$pub" "$out/$m/$p/index.html" "${extra[@]}" || fail=1
    if [ "$m" = native ] && [ -n "$map" ]; then
      python3 -I "$here/notes.py" "$out/$m/$p/index.html" --expect "$here/../intent/$p.notes" --map "$map" || fail=1
    else
      python3 -I "$here/notes.py" "$out/$m/$p/index.html" --expect "$here/../intent/$p.notes" || fail=1
    fi
  done
done
exit $fail
