SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build serve clean check check-raw check-probe probe-missing

PORT ?= 8002
ANTORA = npx antora --stacktrace

# The admonition type each source kind becomes in native mode: the same name
MAP = note=note,important=important,caution=caution

# The default UI, pinned to the same build as the tables round
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

site-playbook.yml: antora-playbook.yml playbook.js ../../source/template_variables.yml node_modules
	node playbook.js

# The build log keeps Asciidoctor's warnings (duplicate ids, missing includes)
build: install site-playbook.yml
	mkdir -p .check
	$(ANTORA) site-playbook.yml 2>&1 | tee .check/build.log

serve: build
	python3 -m http.server $(PORT) -d site

# Partials, outline and notes checks: every page in passthrough, native and
# the variable mode
check: build
	../../checks/check-site.sh site $(MAP) passthrough native variable

# The raw mode: the ERB call as written, which AsciiDoc leaves as text
check-raw: build
	../../checks/check-site.sh site "" raw

# One partial with a heading included twice: the ids and the build's warnings
check-probe: build
	python3 -I ../../../headings/checks/outline.py site/probe/twice/index.html
	grep -i 'already in use' .check/build.log || true

# A missing partial, in this component and in another: the build's message
# and exit status, with Antora's default failure level and with
# --log-failure-level=error. Each page is copied into the probe component
# for the builds and removed again.
PROBES = missing missing-shared
probe-missing: install site-playbook.yml
	mkdir -p .check
	rm -f .check/probe-missing.log
	for p in $(PROBES); do \
	  cp probes/$$p.adoc probe/modules/ROOT/pages/$$p.adoc; \
	  for level in default error; do \
	    echo "## $$p, failure level $$level" >> .check/probe-missing.log; \
	    opt=$$([ $$level = error ] && echo --log-failure-level=error); \
	    $(ANTORA) site-playbook.yml --to-dir .check/probe-site $$opt >> .check/probe-missing.log 2>&1; \
	    echo "exit status $$?" >> .check/probe-missing.log; \
	  done; \
	  rm -f probe/modules/ROOT/pages/$$p.adoc; \
	done
	cat .check/probe-missing.log

clean:
	rm -rf site site-playbook.yml .check
