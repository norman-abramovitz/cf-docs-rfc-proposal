SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build serve clean check history probe-dates

ANTORA = $(abspath node_modules/.bin/antora) --stacktrace
HELPERS = $(abspath ../../helpers)
CHECKS = $(abspath ../../checks)
KEY = :page-last-updated:
PAGES = $(filter-out pages/modules/ROOT/pages/index.adoc,$(wildcard pages/modules/ROOT/pages/*.adoc))
HISTORY ?= .history

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

# Three builds, one per footer year: the build's year, the newest content
# year on the site, and each page's own content year
build: install
	mkdir -p .check
	YEAR_MODE=build $(ANTORA) antora-playbook.yml --to-dir site-build 2>&1 | tee .check/build-build.log
	SITE_YEAR=$$(python3 -I $(HELPERS)/content-date.py --key $(KEY) --year $(PAGES)) \
	  YEAR_MODE=site $(ANTORA) antora-playbook.yml --to-dir site-site 2>&1 | tee .check/build-site.log
	YEAR_MODE=page $(ANTORA) antora-playbook.yml --to-dir site-page 2>&1 | tee .check/build-page.log

serve: build
	python3 -m http.server 4304 -d site-build

check: build
	fail=0; for m in build site page; do $(CHECKS)/check-site.sh site-$$m/cf $$m || fail=1; done; exit $$fail

# Antora has no Git-based date of its own; native shows that. helper: the
# dates the converter wrote, updated from Git by content-date.py.
history: install
	rm -rf $(HISTORY) && mkdir -p $(HISTORY)
	python3 -I $(HELPERS)/make-history.py . $(HISTORY)/native pages/modules/ROOT/pages .adoc native
	python3 -I $(HELPERS)/make-history.py . $(HISTORY)/helper pages/modules/ROOT/pages .adoc helper
	for v in native helper; do cp -R .cache $(HISTORY)/$$v/; done
	cd $(HISTORY)/native && $(ANTORA) history-playbook.yml > build.log 2>&1
	cd $(HISTORY)/helper && python3 -I $(HELPERS)/content-date.py --key $(KEY) --git \
	  --ignore-revs .git-blame-ignore-revs --write $(PAGES) && $(ANTORA) history-playbook.yml > build.log 2>&1
	@echo '## native: what the tool shows without a date in the page; expected to differ from the intent'
	-$(CHECKS)/check-site.sh $(HISTORY)/native/site/cf history
	@echo '## helper'
	$(CHECKS)/check-site.sh $(HISTORY)/helper/site/cf history

# The dates Asciidoctor sets on every page, without and with
# SOURCE_DATE_EPOCH (here the author date of the newest commit in this
# repository's history, as the Reproducible Builds specification suggests),
# and the sitemap's lastmod. The probe page is copied in for the builds and
# removed again.
probe-dates: install
	mkdir -p .check
	cp probes/dates.adoc pages/modules/ROOT/pages/probe-dates.adoc
	$(ANTORA) antora-playbook.yml --to-dir .check/probe-site > /dev/null 2>&1; \
	  grep -o '<p>[a-z]*: [^<]*</p>' .check/probe-site/cf/probe-dates/index.html > .check/probe-dates.log; \
	  echo "sitemap lastmod: $$(grep -o '<lastmod>[^<]*' .check/probe-site/sitemap.xml | sort -u | tr '\n' ' ')" >> .check/probe-dates.log
	echo '## SOURCE_DATE_EPOCH=1733437108 (2024-12-05T22:18:28Z)' >> .check/probe-dates.log
	SOURCE_DATE_EPOCH=1733437108 $(ANTORA) antora-playbook.yml --to-dir .check/probe-site > /dev/null 2>&1; \
	  grep -o '<p>[a-z]*: [^<]*</p>' .check/probe-site/cf/probe-dates/index.html >> .check/probe-dates.log; \
	  echo "sitemap lastmod: $$(grep -o '<lastmod>[^<]*' .check/probe-site/sitemap.xml | sort -u | tr '\n' ' ')" >> .check/probe-dates.log
	rm -f pages/modules/ROOT/pages/probe-dates.adoc
	cat .check/probe-dates.log

clean:
	rm -rf site site-* .check $(HISTORY)
