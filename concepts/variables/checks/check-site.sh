#!/usr/bin/env bash
# Variables check, outline check and (on the one page with notes) notes
# check for every test page in every mode of one built site.
# Usage: check-site.sh OUT MAP [MODE...]
#   OUT holds the built pages as <mode>/<page>/index.html. MAP is the
#   admonition type each note kind becomes, as the notes round's notes.py
#   --map takes it (note=note,important=warning,caution=danger); every mode
#   writes notes as the tool's admonition, so the map applies to every mode.
#   Each page's variables are compared with ../intent/<page>.vars, its
#   outline with its published copy and anchors file. routes-domains is the
#   Domains section the headings round converted; its notes are compared
#   with the notes round's notes file. A page missing from passthrough or
#   native fails; the raw mode holds only the pages that show what breaks,
#   so a page missing there is skipped.
here=$(cd "$(dirname "$0")" && pwd)
outline=$here/../../headings/checks/outline.py
notes=$here/../../notes/checks/notes.py
names=$here/../source/template_variables.yml
out=$1; map=$2; shift 2
modes=${*:-passthrough native}
fail=0
for m in $modes; do
  for p in app-ssh-overview routes-domains troubleshooting-router-error-responses container-security all_metrics; do
    pub=$here/../published/$p.html; extra=(--anchors "$here/../intent/$p.anchors")
    if [ "$p" = routes-domains ]; then
      pub=$here/../../headings/published/$p.html
      extra=(--section domains --anchors "$here/../../headings/intent/$p.anchors")
    fi
    echo "== $m/$p"
    built=$out/$m/$p/index.html
    if [ ! -f "$built" ]; then
      if [ "$m" = raw ]; then echo "skip  not in this mode"; else echo "FAIL  not built"; fail=1; fi
      continue
    fi
    python3 -I "$here/vars.py" "$built" --expect "$here/../intent/$p.vars" --names "$names" || fail=1
    python3 -I "$outline" "$pub" "$built" "${extra[@]}" || fail=1
    if [ "$p" = routes-domains ]; then
      python3 -I "$notes" "$built" --expect "$here/../../notes/intent/$p.notes" ${map:+--map "$map"} || fail=1
    fi
  done
done
exit $fail
