.PHONY: screenshots install build serve clean check check-wide

# PYTHONPATH lets the build import list_table.py from this directory
ZENSICAL = PYTHONPATH=. uv run --project . zensical
PORT ?= 8001

install: .venv
.venv: pyproject.toml uv.lock
	uv sync --project .
	touch .venv

# The variables excerpt, with its top key renamed so pages read vars.name
vars.yml: ../../source/template_variables.yml
	sed 's/^template_variables:/vars:/' $< > $@

build: .venv vars.yml
	$(ZENSICAL) build --clean

serve: build
	uv run --project . python -m http.server $(PORT) -d site

PAGES = scale-table-host credential-types metadata troubleshooting_slow_requests uaa-concepts uaa-performance roles-table-host bosh-networks bosh-cpi-api-v2 bosh-director-tasks bpm-config
MODES ?= passthrough extension native native-plain

# Spot checks from the intent files, per mode; prints only failures. The
# build puts a cell's no-wrap box on its own line; JOIN puts it back.
JOIN = 's\#(<t[dh][^>]*>)\s*(<div class="wrap-avoid-box">)\#$$1$$2\#g; s\#(</div>)\s*(</t[dh]>)\#$$1$$2\#g'
check: build
	@for m in $(MODES); do \
	  mkdir -p .check/$$m; \
	  for p in $(PAGES); do perl -0pe $(JOIN) site/$$m/$$p/index.html > .check/$$m/$$p.html; done; \
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
HIDE = header.md-header
POC = ../../../../poc
screenshots: ../../checks/node_modules
	@for m in $(MODES); do for p in $(PAGES); do \
	  node ../../checks/screenshots.mjs "http://localhost:$(PORT)/$$m/$$p/" $(POC)/compare/img/zensical-$$m-$$p --hide '$(HIDE)' || echo "skipped $$m/$$p"; \
	done; done
	@for f in $(POC)/compare/img/zensical-*; do [ ! -f $(POC)/img/$${f##*/} ] || cp $$f $(POC)/img/; done
	python3 -I $(POC)/pair/build.py

../../checks/node_modules: ../../checks/package.json
	npm --prefix ../../checks install --no-audit --no-fund
	touch $@

clean:
	rm -rf site vars.yml .check
