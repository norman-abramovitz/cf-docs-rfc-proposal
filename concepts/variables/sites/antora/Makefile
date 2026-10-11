# The recipes set pipefail themselves: macOS ships GNU Make 3.81, which
# ignores .SHELLFLAGS, so a failed build piped into tee would pass.
SHELL := /bin/bash

.PHONY: install build serve clean check probe

PORT ?= 8002
ANTORA = npx antora --stacktrace

# The admonition type each note kind becomes: the same name
MAP = note=note,important=important,caution=caution

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

site-passthrough.yml site-native.yml: antora-playbook.yml playbook.js ../../source/template_variables.yml node_modules
	node playbook.js

# One build per mode, into the same site/; the logs keep Asciidoctor's warnings
build: install site-passthrough.yml
	mkdir -p .check
	set -o pipefail; $(ANTORA) site-passthrough.yml 2>&1 | tee .check/build-passthrough.log
	set -o pipefail; $(ANTORA) site-native.yml 2>&1 | tee .check/build-native.log

serve: build
	python3 -m http.server $(PORT) -d site

# Variables, outline and notes checks: every page, passthrough and native
check: build
	../../checks/check-site.sh site $(MAP)

# What native mode does with a name that is not defined: the native
# playbook plus a component holding probe/probe.adoc
probe: install site-native.yml
	mkdir -p .check
	node -e "const y=require('js-yaml'),f=require('fs');const b=y.load(f.readFileSync('site-native.yml','utf8'));b.content.sources[0].start_paths=['concepts/variables/sites/antora/home','concepts/variables/sites/antora/probe'];b.output.dir='./.check/probe-site';f.writeFileSync('site-probe.yml',y.dump(b,{lineWidth:-1}))"
	$(ANTORA) site-probe.yml > .check/probe.log 2>&1; echo "exit status $$?"; grep -o '"msg":"[^"]*"' .check/probe.log | sort | uniq -c; \
	  grep -o 'Undefined: [^<]*' .check/probe-site/probe/probe/index.html || echo '(no page written)'

clean:
	rm -rf site site-passthrough.yml site-native.yml site-probe.yml .check
