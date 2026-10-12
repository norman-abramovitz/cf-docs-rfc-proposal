SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build serve clean check history probe-git-plugin

HELPERS = $(abspath ../../helpers)
CHECKS = $(abspath ../../checks)
ZENSICAL = $(abspath .venv/bin/zensical)
KEY = revision_date
PAGES = $(filter-out docs/index.md,$(wildcard docs/*.md))
HISTORY ?= .history

install: .venv
.venv: pyproject.toml uv.lock
	uv sync --project .
	touch .venv

# Three builds, one per footer year (the build's year comes from `date`)
build: .venv
	mkdir -p .check
	{ cat zensical.toml; printf '\n[project.extra]\nyear_mode = "build"\nyear = "%s"\n' "$$(date +%Y)"; } > build.toml
	$(ZENSICAL) build --clean -f build.toml 2>&1 | tee .check/build-build.log && rm -rf site-build && mv site site-build
	{ cat zensical.toml; printf '\n[project.extra]\nyear_mode = "site"\nyear = "%s"\n' "$$(python3 -I $(HELPERS)/content-date.py --key $(KEY) --year $(PAGES))"; } > build.toml
	$(ZENSICAL) build --clean -f build.toml 2>&1 | tee .check/build-site.log && rm -rf site-site && mv site site-site
	{ cat zensical.toml; printf '\n[project.extra]\nyear_mode = "page"\nyear = ""\n'; } > build.toml
	$(ZENSICAL) build --clean -f build.toml 2>&1 | tee .check/build-page.log && rm -rf site-page && mv site site-page

serve: build
	python3 -m http.server 4302 -d site-build

check: build
	fail=0; for m in build site page; do $(CHECKS)/check-site.sh site-$$m $$m || fail=1; done; exit $$fail

# Zensical has no Git-based date of its own; native shows that. helper:
# the dates the converter wrote, updated from Git by content-date.py.
history: .venv
	rm -rf $(HISTORY) && mkdir -p $(HISTORY)
	python3 -I $(HELPERS)/make-history.py . $(HISTORY)/native docs .md native
	python3 -I $(HELPERS)/make-history.py . $(HISTORY)/helper docs .md helper
	for v in native helper; do { cat $(HISTORY)/$$v/zensical.toml; printf '\n[project.extra]\nyear_mode = "build"\nyear = "%s"\n' "$$(date +%Y)"; } > $(HISTORY)/$$v/build.toml; done
	cd $(HISTORY)/native && $(ZENSICAL) build --clean -f build.toml > build.log 2>&1
	cd $(HISTORY)/helper && python3 -I $(HELPERS)/content-date.py --key $(KEY) --git \
	  --ignore-revs .git-blame-ignore-revs --write $(PAGES) && $(ZENSICAL) build --clean -f build.toml > build.log 2>&1
	@echo '## native: what the tool shows without a date in the page; expected to differ from the intent'
	-$(CHECKS)/check-site.sh $(HISTORY)/native/site history
	@echo '## helper'
	$(CHECKS)/check-site.sh $(HISTORY)/helper/site history

# The MkDocs plugin for Git dates, configured as an MkDocs site would: what
# Zensical says about it. The config is written for one build and removed.
probe-git-plugin: .venv
	mkdir -p .check
	{ cat zensical.toml; printf '\n[project.extra]\nyear_mode = "build"\nyear = "%s"\n' "$$(date +%Y)"; } > build.toml
	{ cat build.toml; printf '\n[project.plugins.git-revision-date-localized]\nenable_creation_date = true\n'; } > probe.toml
	$(ZENSICAL) build --clean -f probe.toml > .check/probe-git-plugin.log 2>&1; echo "exit status $$?" >> .check/probe-git-plugin.log
	echo "Last update boxes on the home page (no revision_date): $$(grep -c 'md-source-file__fact' site/index.html)" >> .check/probe-git-plugin.log
	cat .check/probe-git-plugin.log

clean:
	rm -rf site site-* .check $(HISTORY) build.toml
