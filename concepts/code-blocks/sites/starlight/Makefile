# The recipes set pipefail themselves: macOS ships GNU Make 3.81, which
# ignores .SHELLFLAGS, so a failed build piped into tee would pass.
SHELL := /bin/bash

.PHONY: install build serve clean check check-browser check-raw probe

PORT ?= 4103
# The aside type each note kind becomes
MAP = note=note,important=caution,caution=danger
# What native mode requires of every code block: a type, statically; in
# the browser also a copy button that copies the block's text or commands
REQUIRE = type
REQUIRE_BROWSER = type,copy
PAGES = routes-domains troubleshooting_slow_requests gsg-grails backup backup-clean nginx multiple-processes

install: node_modules
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

vars.json: ../../source/template_variables.yml vars.js node_modules
	node vars.js

# One build of both modes into dist/; the log keeps Astro's warnings
build: vars.json
	mkdir -p .check
	set -o pipefail; npx astro build 2>&1 | tee .check/build.log

serve: build
	python3 -m http.server $(PORT) -d dist

# Code-block, outline and notes checks: every page, passthrough and native
check: build
	../../checks/check-site.sh dist $(MAP) $(REQUIRE)

# The same checks on the pages as the browser holds them, with each copy
# button clicked (../../checks/codeblocks-browser.mjs)
check-browser: build
	@python3 -m http.server $(PORT) -d dist > /dev/null 2>&1 & pid=$$!; sleep 1; \
	  node ../../checks/codeblocks-browser.mjs .check/browser $(foreach m,passthrough native,$(foreach p,$(PAGES),http://localhost:$(PORT)/$(m)/$(p)/)); s=$$?; \
	  kill $$pid; ../../checks/check-site.sh .check/browser $(MAP) $(REQUIRE_BROWSER) || s=1; exit $$s

# Markdoc's own errors on the passthrough pages with <pre> blocks as the book
# writes them, before their line breaks were written &#10; (raw/)
check-raw: node_modules
	node markdoc-check.mjs raw/*.mdoc

# How Shiki tokenizes a console line and a bash line (console-tokens.mjs)
probe: node_modules
	node console-tokens.mjs

clean:
	rm -rf dist .astro vars.json .check
