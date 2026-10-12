#!/usr/bin/env bash
# The links check on the published copies of the four test pages, placed at
# their paths in a folder that stands for docs.cloudfoundry.org, so that links
# between them resolve against the pages as served (other pages are absent and
# show as `no page`).
# Usage: check-published.sh [WORKDIR]   (default: a new temporary folder)
here=$(cd "$(dirname "$0")" && pwd)
site=${1:-$(mktemp -d)}
copy() { mkdir -p "$site/$(dirname "$2")"; cp "$1" "$site/$2"; }
copy "$here/../published/http-routing.html" concepts/http-routing.html
copy "$here/../../variables/published/troubleshooting-router-error-responses.html" adminguide/troubleshooting-router-error-responses.html
copy "$here/../../partials/published/enabling-tcp-routing.html" adminguide/enabling-tcp-routing.html
copy "$here/../../headings/published/routes-domains.html" devguide/deploy-apps/routes-domains.html
for key in concepts/http-routing adminguide/troubleshooting-router-error-responses adminguide/enabling-tcp-routing devguide/deploy-apps/routes-domains; do
  echo "== published/$key"
  (cd "$site" && python3 -I "$here/links.py" "$key.html" --root .)
done
