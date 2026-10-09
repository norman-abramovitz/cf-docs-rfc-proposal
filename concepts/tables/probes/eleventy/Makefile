.PHONY: install build serve clean check

PORT ?= 8003
ELEVENTY = npx @11ty/eleventy

install: node_modules
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

# The source pages, copied unchanged; only the file name changes, so that
# Eleventy reads them as Markdown run through EJS.
COPIES = src/uaa-concepts.md src/_includes/_oss_scale_table.md
src/uaa-concepts.md: ../../source/uaa-concepts.html.md.erb
	cp $< $@
src/_includes/_oss_scale_table.md: ../../source/_oss_scale_table.html.md.erb
	cp $< $@

build: install $(COPIES)
	$(ELEVENTY)

serve: install $(COPIES)
	$(ELEVENTY) --serve --port=$(PORT)

PAGES = scale-table-host uaa-concepts
PUBLISHED ?= ../../results/published

# Spot checks for the two pages this probe builds (the other pages' checks
# are left out), then the word-by-word comparison with the published page
# when PUBLISHED holds the saved pages.
check: build
	@mkdir -p .check
	@for p in $(PAGES); do cp _site/$$p/index.html .check/$$p.html; done
	@for p in credential-types metadata troubleshooting_slow_requests; do : > .check/$$p.html; done
	@../../checks/spot-checks.sh .check 2>/dev/null | grep -E '^(ok|FAIL) +($(subst $(eval) ,|,$(PAGES))):'
	@if [ -f $(PUBLISHED)/uaa-concepts.html ]; then echo "== text-diff uaa-concepts"; python3 ../../checks/text-diff.py $(PUBLISHED)/uaa-concepts.html _site/uaa-concepts/index.html; fi

clean:
	rm -rf _site .check $(COPIES)
