.PHONY: screenshots install build build-raw serve clean check-raw check check-wide

PORT ?= 4321

install: node_modules
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

vars.json: ../../source/template_variables.yml vars.js node_modules
	node vars.js

build: vars.json
	npm run build

# Also builds the raw passthrough pages that parse
build-raw: vars.json
	RAW=1 npm run build

serve: build
	npx astro preview --port $(PORT)

# Markdoc errors on each unchanged-HTML page
check-raw: vars.json
	node markdoc-check.mjs src/content/docs/passthrough-raw/*.mdoc

PAGES = scale-table-host credential-types metadata troubleshooting_slow_requests uaa-concepts uaa-performance roles-table-host bosh-networks bosh-cpi-api-v2 bosh-director-tasks bpm-config
MODES ?= passthrough extension native native-plain

# Spot checks from the intent files, per mode; prints only failures. A page
# that was not built (raw troubleshooting) is checked as an empty file.
check: $(if $(filter passthrough-raw,$(MODES)),build-raw,build)
	@for m in $(MODES); do \
	  mkdir -p .check/$$m; \
	  for p in $(PAGES); do cp dist/$$m/$$p/index.html .check/$$m/$$p.html 2>/dev/null || : > .check/$$m/$$p.html; done; \
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
HIDE = .right-sidebar-container
POC = ../../../../poc
screenshots: ../../checks/node_modules
	@for m in $(MODES); do for p in $(PAGES); do \
	  node ../../checks/screenshots.mjs "http://localhost:$(PORT)/$$m/$$p/" $(POC)/compare/img/starlight-$$m-$$p --hide '$(HIDE)' || echo "skipped $$m/$$p"; \
	done; done
	@for f in $(POC)/compare/img/starlight-*; do [ ! -f $(POC)/img/$${f##*/} ] || cp $$f $(POC)/img/; done
	python3 -I $(POC)/pair/build.py

../../checks/node_modules: ../../checks/package.json
	npm --prefix ../../checks install --no-audit --no-fund
	touch $@

clean:
	rm -rf dist .astro vars.json .check
