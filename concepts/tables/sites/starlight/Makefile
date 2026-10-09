.PHONY: install build build-raw serve clean check-raw check

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

PAGES = scale-table-host credential-types metadata troubleshooting_slow_requests uaa-concepts
MODES ?= passthrough extension native

# Spot checks from the intent files, per mode; prints only failures. A page
# that was not built (raw troubleshooting) is checked as an empty file.
check: $(if $(filter passthrough-raw,$(MODES)),build-raw,build)
	@for m in $(MODES); do \
	  mkdir -p .check/$$m; \
	  for p in $(PAGES); do cp dist/$$m/$$p/index.html .check/$$m/$$p.html 2>/dev/null || : > .check/$$m/$$p.html; done; \
	  echo "== $$m: $$(../../checks/spot-checks.sh .check/$$m | grep -c '^ok') passed"; \
	  ../../checks/spot-checks.sh .check/$$m | grep -v '^ok' || true; \
	done

clean:
	rm -rf dist .astro vars.json .check
