SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build serve clean check check-raw check-probe probe-missing

PORT ?= 4321
# The aside type each source kind becomes in native mode (notes round)
MAP = note=note,important=caution,caution=danger

install: node_modules
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

vars.json: ../../source/template_variables.yml vars.js node_modules
	node vars.js

build: vars.json
	mkdir -p .check
	npm run build 2>&1 | tee .check/build.log

serve: build
	npx astro preview --port $(PORT)

# Partials, outline and notes checks: every page in passthrough, native and
# the variable mode
check: build
	../../checks/check-site.sh dist $(MAP) passthrough native variable

# The raw mode: the ERB call as written, which Markdoc leaves as text
check-raw: build
	../../checks/check-site.sh dist "" raw

# One partial with a heading included twice: the ids and the table of contents
check-probe: build
	python3 -I ../../../headings/checks/outline.py dist/probe/twice/index.html
	python3 -I ../../checks/partials.py dist/probe/twice/index.html | grep '^toc'

# Pages that stop the build, each copied in for one build and removed again
PROBES = missing inline-partial variable-attribute
probe-missing: vars.json
	mkdir -p .check
	rm -f .check/probe-missing.log
	for p in $(PROBES); do \
	  cp probes/$$p.mdoc src/content/docs/probe/$$p.mdoc; \
	  echo "## $$p" >> .check/probe-missing.log; \
	  npx astro build --outDir .check/probe-dist >> .check/probe-missing.log 2>&1; echo "exit status $$?" >> .check/probe-missing.log; \
	  rm -f src/content/docs/probe/$$p.mdoc; \
	done
	cat .check/probe-missing.log

clean:
	rm -rf dist .astro vars.json .check
