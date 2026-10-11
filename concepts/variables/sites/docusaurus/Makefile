# The recipes set pipefail themselves: macOS ships GNU Make 3.81, which
# ignores .SHELLFLAGS, so a failed build piped into tee would pass.
SHELL := /bin/bash

.PHONY: install build serve clean check check-raw probe

# The admonition type each note kind becomes
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
	set -o pipefail; npm run build 2>&1 | tee .check/build.log

serve: build
	npm run serve

# Variables, outline and notes checks: every page, passthrough and native
check: build
	../../checks/check-site.sh build $(MAP)

# The raw mode: a page exactly as the book writes it, which MDX does not
# compile; mdx-check.mjs prints the first error
check-raw: node_modules
	node mdx-check.mjs raw-mdx/*.mdx

# What a name that is not defined does: each probe page built alone, with
# the native variables module (probe.mdx) and with the JSON file (probe-json.mdx)
probe: vars.json
	mkdir -p .check
	@for p in probe probe-json; do \
	  rm -rf .check/probe-docs && mkdir -p .check/probe-docs && cp probe/$$p.mdx .check/probe-docs/; \
	  echo "== $$p.mdx"; \
	  DOCS_PATH=.check/probe-docs npx docusaurus build --out-dir .check/probe-build > .check/$$p.log 2>&1; echo "exit status $$?"; \
	  grep -o 'Variable not defined: [^ ]*\|Can.t render static file for pathname "[^"]*"' .check/$$p.log | sort -u; \
	  grep -o 'Undefined: [^<]*<!-- -->[^<]*<!-- -->[^<]*' .check/probe-build/$$p/index.html 2>/dev/null || true; \
	done

clean:
	rm -rf build .docusaurus vars.json .check
