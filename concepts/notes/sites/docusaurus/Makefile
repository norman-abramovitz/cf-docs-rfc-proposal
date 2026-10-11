SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build serve clean check check-raw

# The admonition type each source kind becomes in native mode
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

# Outline and notes checks: every page in every mode
check: build
	../../checks/check-site.sh build $(MAP)

# The raw mode: notes exactly as the source writes them. Pages that do not
# compile stay out of docs/ (raw-mdx/); mdx-check.mjs prints the first MDX
# error of each. routes-domains compiles and is built in docs/raw/.
check-raw: build
	node mdx-check.mjs raw-mdx/*.mdx
	../../checks/check-site.sh build "" raw

clean:
	rm -rf build .docusaurus vars.json .check
