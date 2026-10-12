SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build check check-other probe-broken probe-depth probe-redirects clean
# Keep the link folder between builds
.SECONDARY:

# One build per variant, each a whole site in dist/<variant>/ served at /.
#   mono:    the pages come from pages/<mode>, one folder whose subfolders
#            are the URL directories (one repository with directories)
#   linked:  the pages come from linked/native, whose subfolders are
#            symbolic links to the folders of pages/native, as checkouts of
#            separate repositories would be linked in
#   default: Astro's default URLs (<path>/index.html)
CHECKED = mono-passthrough mono-native linked-native
OTHER = default-passthrough
VARIANTS = $(CHECKED) $(OTHER)
env.mono-passthrough    = PAGES_DIR=./pages/passthrough
env.mono-native         = PAGES_DIR=./pages/native
env.linked-native       = PAGES_DIR=./linked/native
env.default-passthrough = PAGES_DIR=./pages/passthrough URLS=default
DIRS = concepts adminguide devguide running cf-cli

install: node_modules
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

linked/%:
	mkdir -p $@
	ln -sfn ../../pages/$*/index.mdoc $@/index.mdoc
	for d in $(DIRS); do ln -sfn ../../pages/$*/$$d $@/$$d; done

# Astro keeps a content cache in .astro/; each variant starts without it
build: $(addprefix build-,$(VARIANTS))
build-%: install linked/native
	mkdir -p .check
	rm -rf .astro node_modules/.astro
	env $(env.$*) npx astro build --outDir dist/$* 2>&1 | tee .check/build-$*.log

check: $(addprefix build-,$(CHECKED))
	../../checks/check-site.sh dist $(CHECKED)

check-other: $(addprefix build-,$(OTHER))
	../../checks/check-site.sh dist $(OTHER) || true

# Links that break: a missing page and a missing anchor in another
# directory, in native and passthrough form. The probe page is copied in for
# the build and removed again.
probe-broken: install
	mkdir -p .check
	rm -rf .check/probe-broken.log .astro node_modules/.astro
	cp probes/broken.mdoc pages/native/concepts/probe-broken.mdoc
	echo "## mono-native" >> .check/probe-broken.log
	PAGES_DIR=./pages/native npx astro build --outDir .check/probe-mono-native >> .check/probe-broken.log 2>&1; \
	  echo "exit status $$?" >> .check/probe-broken.log
	python3 -I ../../checks/links.py .check/probe-mono-native/concepts/probe-broken.html --root .check/probe-mono-native >> .check/probe-broken.log
	rm -f pages/native/concepts/probe-broken.mdoc
	cat .check/probe-broken.log

# Links held in variables and in a partial, on a page one folder deep
# (concepts/) and one two folders deep (devguide/deploy-apps/), each link in
# three forms: the book's relative URL, a root-relative URL, and the tool's
# own form. The probe files are copied in for the build and removed again.
probe-depth: install
	mkdir -p .check
	rm -rf .check/probe-depth.log .astro node_modules/.astro
	cp probes/depth/_probe-partial.mdoc pages/native/concepts/_probe-partial.mdoc
	cp probes/depth/probe-depth-1.mdoc pages/native/concepts/probe-depth.mdoc
	cp probes/depth/probe-depth-2.mdoc pages/native/devguide/deploy-apps/probe-depth.mdoc
	PAGES_DIR=./pages/native npx astro build --outDir .check/probe-depth >> .check/probe-depth.log 2>&1; \
	  echo "exit status $$?" >> .check/probe-depth.log
	for p in concepts/probe-depth devguide/deploy-apps/probe-depth; do \
	  echo "## $$p" >> .check/probe-depth.log; \
	  python3 -I ../../checks/links.py .check/probe-depth/$$p.html --root .check/probe-depth >> .check/probe-depth.log; \
	done
	rm -f pages/native/concepts/_probe-partial.mdoc pages/native/concepts/probe-depth.mdoc \
	  pages/native/devguide/deploy-apps/probe-depth.mdoc
	cat .check/probe-depth.log

# Old URLs: two that the book's redirects.rb sends to routes-domains, one in
# the same repository's folder and one in another's, built with the tool's
# redirect feature; redirects.py reports what the site serves at each.
OLD = /devguide/deploy-apps/domains-routes.html /adminguide/manage-domains-routes.html /devguide/deploy-apps/domains-routes /adminguide/manage-domains-routes
probe-redirects: install
	mkdir -p .check
	rm -rf .check/probe-redirects.log .astro node_modules/.astro
	PAGES_DIR=./pages/native REDIRECTS=1 npx astro build --outDir .check/probe-redirects > .check/probe-redirects-build.log 2>&1; \
	  echo "exit status $$?" >> .check/probe-redirects.log
	python3 -I ../../checks/redirects.py .check/probe-redirects $(OLD) >> .check/probe-redirects.log
	cat .check/probe-redirects.log

clean:
	rm -rf dist .astro linked .check
