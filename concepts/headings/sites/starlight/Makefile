SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build serve clean check

PORT ?= 4321

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

# Outline check: every page in every mode against the published page
check: build
	../../checks/outline-site.sh dist

clean:
	rm -rf dist .astro vars.json .check
