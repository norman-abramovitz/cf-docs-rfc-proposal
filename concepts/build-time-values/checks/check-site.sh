#!/usr/bin/env bash
# Build-time values check for every test page of one build, and the text
# comparison of access-control with its published page.
# Usage: check-site.sh OUT MODE [BUILD_YEAR]
#   OUT holds the built pages as <page>/index.html. MODE names the lines of
#   intent/expectations.txt to check (published, build, site, page,
#   history). BUILD_YEAR, if given, is the year a `build` expectation means;
#   the default is this year.
#   With MODE build, site or page, access-control is also compared word by
#   word with published/access-control.html, build-time values masked.
here=$(cd "$(dirname "$0")" && pwd)
out=$1; mode=$2; year=${3:-$(date +%Y)}
fail=0
for page in access-control architecture using-vol-services high-availability; do
  f=$out/$page/index.html
  [ "$mode" = published ] && f=$out/$page.html
  echo "== $out ($mode): $page"
  if [ ! -f "$f" ]; then echo "FAIL  not built: $f"; fail=1; continue; fi
  python3 -I "$here/buildtime.py" "$f" --expect "$here/../intent/expectations.txt" \
    --page "$page" --mode "$mode" --build-year "$year" || fail=1
done
case $mode in
  build|site|page)
    echo "== $mode/access-control against the published page"
    python3 -I "$here/buildtime.py" --compare "$here/../published/access-control.html" "$out/access-control/index.html" ;;
esac
exit $fail
