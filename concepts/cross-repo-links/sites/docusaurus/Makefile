SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build check check-other probe-broken probe-depth probe-redirects clean

# One build per variant, each a whole site in build/<variant>/ served at /.
# A variant sets LAYOUT, PAGES and URLS for docusaurus.config.js.
CHECKED = split-passthrough split-native mono-passthrough mono-native
# Two variants that show what breaks: file links across content sources,
# and the passthrough pages with Docusaurus's default URLs
OTHER = split-filelinks default-passthrough
VARIANTS = $(CHECKED) $(OTHER)
env.split-passthrough   = LAYOUT=split PAGES=passthrough
env.split-native        = LAYOUT=split PAGES=native-split
env.mono-passthrough    = LAYOUT=mono PAGES=passthrough
env.mono-native         = LAYOUT=mono PAGES=native-mono
env.split-filelinks     = LAYOUT=split PAGES=native-mono
env.default-passthrough = LAYOUT=mono PAGES=passthrough URLS=default

install: node_modules
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

# The build logs keep Docusaurus's broken-link and broken-anchor warnings
build: $(addprefix build-,$(VARIANTS))
# Each build starts without .docusaurus/ and the webpack cache: what another
# variant's plugins generated made the next build fail
build-%: install
	mkdir -p .check
	rm -rf .docusaurus node_modules/.cache
	env $(env.$*) npx docusaurus build --out-dir build/$* 2>&1 | tee .check/build-$*.log

# Links and outline checks on every test page, in the four variants a
# conversion would choose from
check: $(addprefix build-,$(CHECKED))
	../../checks/check-site.sh build $(CHECKED)

# The same checks on the two variants that show what breaks
check-other: $(addprefix build-,$(OTHER))
	../../checks/check-site.sh build $(OTHER) || true

# Links that break: a missing page and a missing anchor in another content
# source (split) or directory (mono), in native and passthrough form. The
# probe page is copied in for the builds and removed again; each layout is
# built with broken links set to throw, then to warn (the links check reads
# the second build).
probe-broken: install
	mkdir -p .check
	rm -f .check/probe-broken.log
	for v in split-native mono-native; do \
	  layout=$${v%-native}; \
	  cp probes/broken-$$layout.mdx pages/native-$$layout/concepts/probe-broken.mdx; \
	  for level in throw warn; do \
	    echo "## $$v, ON_BROKEN=$$level" >> .check/probe-broken.log; \
	    rm -rf .docusaurus node_modules/.cache; \
	    LAYOUT=$$layout PAGES=native-$$layout ON_BROKEN=$$level npx docusaurus build --out-dir .check/probe-$$v \
	      >> .check/probe-broken.log 2>&1; echo "exit status $$?" >> .check/probe-broken.log; \
	  done; \
	  python3 -I ../../checks/links.py .check/probe-$$v/concepts/probe-broken.html --root .check/probe-$$v >> .check/probe-broken.log; \
	  rm -f pages/native-$$layout/concepts/probe-broken.mdx; \
	done
	cat .check/probe-broken.log

# Links held in variables and in a partial, on a page one folder deep
# (concepts/) and one two folders deep (devguide/deploy-apps/), each link in
# three forms: the book's relative URL, a root-relative URL, and the tool's
# own form. The probe files are copied in for the build and removed again.
probe-depth: install
	mkdir -p .check
	rm -rf .check/probe-depth.log .docusaurus node_modules/.cache
	cp probes/depth/_probe-partial.mdx pages/native-mono/concepts/_probe-partial.mdx
	cp probes/depth/probe-depth-1.mdx pages/native-mono/concepts/probe-depth.mdx
	cp probes/depth/probe-depth-2.mdx pages/native-mono/devguide/deploy-apps/probe-depth.mdx
	LAYOUT=mono PAGES=native-mono npx docusaurus build --out-dir .check/probe-depth >> .check/probe-depth.log 2>&1; \
	  echo "exit status $$?" >> .check/probe-depth.log
	for p in concepts/probe-depth devguide/deploy-apps/probe-depth; do \
	  echo "## $$p" >> .check/probe-depth.log; \
	  python3 -I ../../checks/links.py .check/probe-depth/$$p.html --root .check/probe-depth >> .check/probe-depth.log; \
	done
	rm -f pages/native-mono/concepts/_probe-partial.mdx pages/native-mono/concepts/probe-depth.mdx \
	  pages/native-mono/devguide/deploy-apps/probe-depth.mdx
	cat .check/probe-depth.log

# Old URLs: two that the book's redirects.rb sends to routes-domains, one in
# the same repository's folder and one in another's, built with the tool's
# redirect feature; redirects.py reports what the site serves at each.
OLD = /devguide/deploy-apps/domains-routes.html /adminguide/manage-domains-routes.html /devguide/deploy-apps/domains-routes /adminguide/manage-domains-routes
# With the default URL style, the plugin also redirects each page's old
# <path>.html, and the passthrough pages are checked against that build.
probe-redirects: install
	mkdir -p .check
	rm -f .check/probe-redirects.log
	for urls in html default; do \
	  echo "## mono-passthrough, URLS=$$urls" >> .check/probe-redirects.log; \
	  rm -rf .docusaurus node_modules/.cache; \
	  LAYOUT=mono PAGES=passthrough URLS=$$urls REDIRECTS=1 npx docusaurus build --out-dir .check/probe-redirects-$$urls \
	    > .check/probe-redirects-$$urls.log 2>&1; echo "exit status $$?" >> .check/probe-redirects.log; \
	  python3 -I ../../checks/redirects.py .check/probe-redirects-$$urls $(OLD) /concepts/http-routing.html >> .check/probe-redirects.log; \
	done
	echo "## links on the passthrough pages, URLS=default with redirects" >> .check/probe-redirects.log
	-../../checks/check-site.sh .check probe-redirects-default >> .check/probe-redirects.log
	cat .check/probe-redirects.log

clean:
	rm -rf build .docusaurus .check
