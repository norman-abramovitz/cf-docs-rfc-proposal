SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build serve clean check history

HELPERS = $(abspath ../../helpers)
CHECKS = $(abspath ../../checks)
KEY = lastUpdated
PAGES = $(filter-out src/content/docs/index.mdoc,$(wildcard src/content/docs/*.mdoc))
HISTORY ?= .history

install: node_modules
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

# Three builds, one per footer year: the build's year, the newest content
# year on the site, and each page's own content year
build: node_modules
	mkdir -p .check
	YEAR_MODE=build npx astro build --outDir dist-build 2>&1 | tee .check/build-build.log
	SITE_YEAR=$$(python3 -I $(HELPERS)/content-date.py --key $(KEY) --year $(PAGES)) \
	  YEAR_MODE=site npx astro build --outDir dist-site 2>&1 | tee .check/build-site.log
	YEAR_MODE=page npx astro build --outDir dist-page 2>&1 | tee .check/build-page.log

serve: build
	npx astro preview --outDir dist-build --port 4303

check: build
	fail=0; for m in build site page; do $(CHECKS)/check-site.sh dist-$$m $$m || fail=1; done; exit $$fail

# The tool's own "last updated" date (lastUpdated: true), on a repository
# with known dates (helpers/make-history.py): native, helper and shallow,
# as in the Docusaurus site
history: node_modules
	rm -rf $(HISTORY) && mkdir -p $(HISTORY)
	python3 -I $(HELPERS)/make-history.py . $(HISTORY)/native src/content/docs .mdoc native
	python3 -I $(HELPERS)/make-history.py . $(HISTORY)/helper src/content/docs .mdoc helper
	cd $(HISTORY)/native && npx astro build --outDir out > build.log 2>&1
	cd $(HISTORY)/helper && python3 -I $(HELPERS)/content-date.py --key $(KEY) --git \
	  --ignore-revs .git-blame-ignore-revs --write $(PAGES) && npx astro build --outDir out > build.log 2>&1
	git clone -q --depth 1 file://$(abspath $(HISTORY))/native $(HISTORY)/shallow
	ln -s $(abspath node_modules) $(HISTORY)/shallow/node_modules
	cd $(HISTORY)/shallow && npx astro build --outDir out > build.log 2>&1
	grep -i 'warn\|error' $(HISTORY)/*/build.log || true
	@echo '## native and shallow show what the tool reads from Git; they are expected to differ from the intent'
	-$(CHECKS)/check-site.sh $(HISTORY)/native/out history
	-$(CHECKS)/check-site.sh $(HISTORY)/shallow/out history
	@echo '## helper: the dates the converter wrote, updated from Git by helpers/content-date.py'
	$(CHECKS)/check-site.sh $(HISTORY)/helper/out history

clean:
	rm -rf dist-* .astro .check $(HISTORY)
