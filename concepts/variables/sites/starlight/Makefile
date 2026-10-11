# The recipes set pipefail themselves: macOS ships GNU Make 3.81, which
# ignores .SHELLFLAGS, so a failed build piped into tee would pass.
SHELL := /bin/bash

.PHONY: install build serve clean check check-raw probe

PORT ?= 4321
# The aside type each note kind becomes
MAP = note=note,important=caution,caution=danger

install: node_modules
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

vars.json: ../../source/template_variables.yml vars.js node_modules
	node vars.js

# One build per mode, merged into dist/. Native pages are checked for
# variables that are not defined first, since the build does not report them.
build: vars.json
	mkdir -p .check
	set -o pipefail; MODE=native node vars-check.mjs src/content/docs/native/*.mdoc 2>&1 | tee .check/vars-check-native.log
	set -o pipefail; MODE=passthrough npx astro build 2>&1 | tee .check/build-passthrough.log
	set -o pipefail; MODE=native npx astro build 2>&1 | tee .check/build-native.log
	rm -rf dist && mkdir -p dist && cp -R .build/passthrough/. dist/ && cp -R .build/native/. dist/

serve: build
	python3 -m http.server $(PORT) -d dist

# Variables, outline and notes checks: every page, passthrough and native
check: build
	../../checks/check-site.sh dist $(MAP)

# The raw mode: a page exactly as the book writes it. Markdoc reports no
# error on it (markdoc-check.mjs); built, it shows its ERB tags as text.
check-raw: vars.json
	node markdoc-check.mjs src/content/docs/raw/*.mdoc
	set -o pipefail; MODE=raw npx astro build 2>&1 | tee .check/build-raw.log
	rm -rf dist/raw && mkdir -p dist && cp -R .build/raw/raw dist/
	../../checks/check-site.sh dist "" raw

# What a name that is not defined does: the probe page, checked by
# vars-check.mjs and built with the passthrough variables
probe: vars.json
	mkdir -p .check
	-node vars-check.mjs probe/probe.mdoc
	rm -rf .check/probe && mkdir -p .check/probe && cp probe/probe.mdoc src/content/docs/probe.mdoc
	MODE= npx astro build --silent > .check/probe.log 2>&1; echo "exit status $$?"; grep -i 'undefined\|error' .check/probe.log | head -3; \
	  grep -o 'Undefined: [^<]*' .build/all/probe/index.html || true; rm -f src/content/docs/probe.mdoc

clean:
	rm -rf dist .build .astro vars.json .check
