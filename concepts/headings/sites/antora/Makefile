SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build serve clean check

PORT ?= 8002
ANTORA = npx antora --stacktrace

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

# The build log keeps Asciidoctor's warnings (section levels, missing ids)
build: install site-playbook.yml
	mkdir -p .check
	$(ANTORA) site-playbook.yml 2>&1 | tee .check/build.log

serve: build
	python3 -m http.server $(PORT) -d site

# Outline check: every page in every mode against the published page
check: build
	../../checks/outline-site.sh site

clean:
	rm -rf site site-playbook.yml .check
