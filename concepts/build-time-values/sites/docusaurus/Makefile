SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build serve clean check history

HELPERS = $(abspath ../../helpers)
CHECKS = $(abspath ../../checks)
KEY = last_update.date
PAGES = docs/*.mdx
# The scratch history repositories (make history); outside the site by default
HISTORY ?= .history

install: node_modules
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

# Three builds, one per footer year: the build's year, the newest content
# year on the site, and each page's own content year
build: node_modules
	mkdir -p .check
	YEAR_MODE=build npx docusaurus build --out-dir build-build 2>&1 | tee .check/build-build.log
	SITE_YEAR=$$(python3 -I $(HELPERS)/content-date.py --key $(KEY) --year $(PAGES)) \
	  YEAR_MODE=site npx docusaurus build --out-dir build-site 2>&1 | tee .check/build-site.log
	YEAR_MODE=page npx docusaurus build --out-dir build-page 2>&1 | tee .check/build-page.log

serve: build
	npx docusaurus serve --dir build-build --port 4301 --no-open

check: build
	fail=0; for m in build site page; do $(CHECKS)/check-site.sh build-$$m $$m || fail=1; done; exit $$fail

# The tool's own "last updated" date, on a repository with known dates
# (helpers/make-history.py): Git as the tool reads it (native); the dates
# the converter writes, updated by the helper (helper); a shallow clone;
# and a custom VCS that skips the listed commits (vcs).
history: node_modules
	rm -rf $(HISTORY) && mkdir -p $(HISTORY) .check
	python3 -I $(HELPERS)/make-history.py . $(HISTORY)/native docs .mdx native
	python3 -I $(HELPERS)/make-history.py . $(HISTORY)/helper docs .mdx helper
	cd $(HISTORY)/native && npx docusaurus build --out-dir out > build.log 2>&1
	cd $(HISTORY)/helper && python3 -I $(HELPERS)/content-date.py --key $(KEY) --git \
	  --ignore-revs .git-blame-ignore-revs --write $(PAGES) && npx docusaurus build --out-dir out > build.log 2>&1
	git clone -q --depth 1 file://$(abspath $(HISTORY))/native $(HISTORY)/shallow
	ln -s $(abspath node_modules) $(HISTORY)/shallow/node_modules
	cd $(HISTORY)/shallow && npx docusaurus build --out-dir out > build.log 2>&1
	cd $(HISTORY)/shallow && python3 -I $(HELPERS)/content-date.py --key $(KEY) --git $(PAGES); echo "exit status $$?"
	cd $(HISTORY)/native && IGNORE_REVS=.git-blame-ignore-revs npx docusaurus build --out-dir out-vcs > build-vcs.log 2>&1
	grep -i 'warn\|error' $(HISTORY)/*/build*.log || true
	@echo '## native, shallow and vcs show what the tool reads from Git; they are expected to differ from the intent'
	-$(CHECKS)/check-site.sh $(HISTORY)/native/out history
	-$(CHECKS)/check-site.sh $(HISTORY)/shallow/out history
	-$(CHECKS)/check-site.sh $(HISTORY)/native/out-vcs history
	@echo '## helper: the dates the converter wrote, updated from Git by helpers/content-date.py'
	$(CHECKS)/check-site.sh $(HISTORY)/helper/out history

clean:
	rm -rf build-* .docusaurus .check $(HISTORY)
