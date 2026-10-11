SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build serve clean check

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

# Outline check: every page in every mode against the published page
check: build
	../../checks/outline-site.sh build

clean:
	rm -rf build .docusaurus vars.json .check
