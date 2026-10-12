.PHONY: screenshots install build build-raw serve clean check check-wide

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

PAGES = scale-table-host credential-types metadata troubleshooting_slow_requests uaa-concepts uaa-performance roles-table-host bosh-networks bosh-cpi-api-v2 bosh-director-tasks bpm-config
MODES ?= passthrough extension native native-plain

# Spot checks from the intent files, per mode; prints only failures.
# Asciidoctor wraps a cell's text, and each list item's, in a paragraph;
# UNWRAP removes the wrapper where it holds the whole cell or item.
UNWRAP = 's\#(<t[dh][^>]*>)<p class="tableblock">((?:(?!</?p[ >]).)*)</p>(</t[dh]>)\#$$1$$2$$3\#gs; s\#<li>\s*<p>((?:(?!</?p[ >]).)*)</p>\s*</li>\#<li>$$1</li>\#gs'
check: $(if $(filter passthrough-raw,$(MODES)),build-raw,build)
	@for m in $(MODES); do \
	  mkdir -p .check/$$m; \
	  for p in $(PAGES); do perl -0pe $(UNWRAP) site/$$m/$$p/index.html > .check/$$m/$$p.html 2>/dev/null || : > .check/$$m/$$p.html; done; \
	  echo "== $$m: $$(../../checks/spot-checks.sh .check/$$m | grep -c '^ok') passed"; \
	  ../../checks/spot-checks.sh .check/$$m | grep -v '^ok' || true; \
	done

# Wide tables scroll in their own box (run while make serve is running)
check-wide: ../../checks/node_modules
	node ../../checks/wide-tables.mjs 'http://localhost:$(PORT)/%m/%p/' $(MODES)

# Screenshots of every table for the POC pages, as checks/screenshots.mjs takes
# them (run while make serve is running). HIDE is the page furniture that would
# cover a table's header row. A page that is not built is reported and skipped.
# Images already copied to poc/img are refreshed too, and the two-pane page is
# rebuilt, since it records a hash of each image.
HIDE = 
POC = ../../../../poc
screenshots: ../../checks/node_modules
	@for m in $(MODES); do for p in $(PAGES); do \
	  node ../../checks/screenshots.mjs "http://localhost:$(PORT)/$$m/$$p/" $(POC)/compare/img/antora-$$m-$$p --hide '$(HIDE)' || echo "skipped $$m/$$p"; \
	done; done
	@for f in $(POC)/compare/img/antora-*; do [ ! -f $(POC)/img/$${f##*/} ] || cp $$f $(POC)/img/; done
	python3 -I $(POC)/pair/build.py

../../checks/node_modules: ../../checks/package.json
	npm --prefix ../../checks install --no-audit --no-fund
	touch $@

clean:
	rm -rf site site-playbook.yml .check
