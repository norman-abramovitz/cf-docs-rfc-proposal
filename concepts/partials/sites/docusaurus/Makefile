SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build serve clean check check-raw check-probe probe-missing

# The admonition type each source kind becomes in native mode (notes round)
MAP = note=note,important=warning,caution=danger

install: node_modules
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

vars.json: ../../source/template_variables.yml vars.js node_modules
	node vars.js

# The build log keeps Docusaurus's broken-link and broken-anchor warnings
build: vars.json
	mkdir -p .check
	npm run build 2>&1 | tee .check/build.log

serve: build
	npm run serve

# Partials, outline and notes checks: every page in passthrough, native and
# the variable mode
check: build
	../../checks/check-site.sh build $(MAP) passthrough native variable

# The raw mode: the ERB call as written. MDX does not compile it; the page
# stays out of docs/ (raw-mdx/) and mdx-check.mjs prints the first error.
check-raw: node_modules
	node mdx-check.mjs raw-mdx/*.mdx

# One partial with a heading included twice: the ids and the table of contents
check-probe: build
	python3 -I ../../../headings/checks/outline.py build/probe/twice/index.html
	python3 -I ../../checks/partials.py build/probe/twice/index.html | grep '^toc'

# A page that includes a partial that does not exist: the build's message.
# The page is copied in for one build and removed again.
probe-missing: vars.json
	mkdir -p .check
	cp probes/missing.mdx docs/probe/missing.mdx
	npx docusaurus build --out-dir .check/probe-build > .check/probe-missing.log 2>&1; \
	  echo "exit status $$?" >> .check/probe-missing.log; rm -f docs/probe/missing.mdx
	cat .check/probe-missing.log

clean:
	rm -rf build .docusaurus vars.json .check
