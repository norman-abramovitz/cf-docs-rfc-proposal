.PHONY: screenshots install build serve clean check-raw check check-wide

install: node_modules
node_modules: package.json
	npm install --no-audit --no-fund
	touch node_modules

vars.json: ../../source/template_variables.yml vars.js node_modules
	node vars.js

build: vars.json
	npm run build

serve: build
	npm run serve

# First MDX error on each unchanged-HTML page
check-raw: node_modules
	node mdx-check.mjs docs/passthrough-raw/*.mdx

PAGES = scale-table-host credential-types metadata troubleshooting_slow_requests uaa-concepts uaa-performance roles-table-host bosh-networks bosh-cpi-api-v2 bosh-director-tasks bpm-config

# Spot checks from the intent files, per mode; prints only failures
check: build
	@for m in passthrough extension native; do \
	  mkdir -p .check/$$m; \
	  for p in $(PAGES); do sed 's/<!-- -->//g; s/ class=""//g' build/$$m/$$p/index.html > .check/$$m/$$p.html; done; \
	  echo "== $$m: $$(../../checks/spot-checks.sh .check/$$m | grep -c '^ok') passed"; \
	  ../../checks/spot-checks.sh .check/$$m | grep -v '^ok' || true; \
	done

# Wide tables scroll in their own box (run while make serve is running;
# PORT=N when the site is served on another port)
PORT ?= 3000
check-wide: ../../checks/node_modules
	node ../../checks/wide-tables.mjs 'http://localhost:$(PORT)/%m/%p' passthrough extension native

# Screenshots of every table for the POC pages, as checks/screenshots.mjs takes
# them (run while make serve is running). HIDE is the page furniture that would
# cover a table's header row. A page that is not built is reported and skipped.
# Images already copied to poc/img are refreshed too, and the two-pane page is
# rebuilt, since it records a hash of each image.
MODES ?= passthrough extension native
HIDE = .navbar, [class*="skipToContent"]
POC = ../../../../poc
screenshots: ../../checks/node_modules
	@for m in $(MODES); do for p in $(PAGES); do \
	  node ../../checks/screenshots.mjs "http://localhost:$(PORT)/$$m/$$p/" $(POC)/compare/img/docusaurus-$$m-$$p --hide '$(HIDE)' || echo "skipped $$m/$$p"; \
	done; done
	@for f in $(POC)/compare/img/docusaurus-*; do [ ! -f $(POC)/img/$${f##*/} ] || cp $$f $(POC)/img/; done
	python3 -I $(POC)/pair/build.py

../../checks/node_modules: ../../checks/package.json
	npm --prefix ../../checks install --no-audit --no-fund
	touch $@

clean:
	rm -rf build .docusaurus vars.json .check
