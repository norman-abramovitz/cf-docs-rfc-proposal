.PHONY: install build serve clean check-raw check check-wide

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

PAGES = scale-table-host credential-types metadata troubleshooting_slow_requests uaa-concepts uaa-performance

# Spot checks from the intent files, per mode; prints only failures
check: build
	@for m in passthrough extension native; do \
	  mkdir -p .check/$$m; \
	  for p in $(PAGES); do sed 's/<!-- -->//g; s/ class=""//g' build/$$m/$$p/index.html > .check/$$m/$$p.html; done; \
	  echo "== $$m: $$(../../checks/spot-checks.sh .check/$$m | grep -c '^ok') passed"; \
	  ../../checks/spot-checks.sh .check/$$m | grep -v '^ok' || true; \
	done

# Wide tables scroll in their own box (run while make serve is running)
check-wide: ../../checks/node_modules
	node ../../checks/wide-tables.mjs 'http://localhost:3000/%m/%p' passthrough extension native

../../checks/node_modules: ../../checks/package.json
	npm --prefix ../../checks install --no-audit --no-fund
	touch $@

clean:
	rm -rf build .docusaurus vars.json .check
