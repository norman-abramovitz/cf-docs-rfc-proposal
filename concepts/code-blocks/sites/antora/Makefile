# The recipes set pipefail themselves: macOS ships GNU Make 3.81, which
# ignores .SHELLFLAGS, so a failed build piped into tee would pass.
SHELL := /bin/bash

.PHONY: install build serve clean check check-browser probe

PORT ?= 4104
ANTORA = npx antora --stacktrace

# The admonition type each note kind becomes: the same name
MAP = note=note,important=important,caution=caution
# What native mode requires of every code block: a type, statically; in
# the browser also a copy button that copies the block's text or commands
# (the default UI adds the button and runs highlight.js in the browser)
REQUIRE = type
REQUIRE_BROWSER = type,copy
PAGES = routes-domains troubleshooting_slow_requests gsg-grails backup backup-clean nginx multiple-processes

# The default UI, pinned to the same build as the earlier rounds
UI_URL = https://gitlab.com/antora/antora-ui-default/-/jobs/15385706035/artifacts/raw/build/ui-bundle.zip
UI_SHA256 = e0ac81aad26961a9cd3cf9bce692a598eff4a1bd2822ce73c9cdc13a15a1e70d

install: node_modules .cache/ui-bundle.zip
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

.cache/ui-bundle.zip:
	mkdir -p .cache
	curl -fsSL -o $@.tmp '$(UI_URL)'
	echo '$(UI_SHA256)  $@.tmp' | shasum -a 256 -c -
	mv $@.tmp $@

# Both modes into site/; the log keeps Asciidoctor's warnings
build: install
	mkdir -p .check
	set -o pipefail; $(ANTORA) antora-playbook.yml 2>&1 | tee .check/build.log

serve: build
	python3 -m http.server $(PORT) -d site

# Code-block, outline and notes checks: every page, passthrough and native
check: build
	../../checks/check-site.sh site $(MAP) $(REQUIRE)

# The same checks on the pages as the browser holds them, with each copy
# button clicked (../../checks/codeblocks-browser.mjs)
check-browser: build
	@python3 -m http.server $(PORT) -d site > /dev/null 2>&1 & pid=$$!; sleep 1; \
	  node ../../checks/codeblocks-browser.mjs .check/browser $(foreach m,passthrough native,$(foreach p,$(PAGES),http://localhost:$(PORT)/$(m)/$(p)/)); s=$$?; \
	  kill $$pid; ../../checks/check-site.sh .check/browser $(MAP) $(REQUIRE_BROWSER) || s=1; exit $$s

clean:
	rm -rf site .check
