.PHONY: install build build-raw serve clean check

PORT ?= 8002
ANTORA = npx antora --stacktrace

# The default UI, pinned to one build of its stable bundle
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

build: install site-playbook.yml
	$(ANTORA) site-playbook.yml

# Also builds the unchanged-HTML pages
build-raw: install
	RAW=1 node playbook.js
	$(ANTORA) site-playbook.yml
	rm site-playbook.yml

serve: build
	python3 -m http.server $(PORT) -d site

clean:
	rm -rf site site-playbook.yml .check
