SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build serve clean check check-raw

PORT ?= 4321
# The aside type each source kind becomes in native mode
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

# Outline and notes checks: every page in every mode
check: build
	../../checks/check-site.sh dist $(MAP)

# The raw mode: notes exactly as the source writes them. A page that stops
# the build stays out of src/ (raw-mdoc/); markdoc-check.mjs prints its errors.
check-raw: build
	node markdoc-check.mjs raw-mdoc/*.mdoc
	../../checks/check-site.sh dist "" raw

clean:
	rm -rf dist .astro vars.json .check
