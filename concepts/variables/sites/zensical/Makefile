.PHONY: install build serve clean check check-raw probe

ZENSICAL = NO_COLOR=1 uv run --project . zensical
PORT ?= 8001
# The admonition type each note kind becomes: the same name
MAP = note=note,important=important,caution=caution

install: .venv
.venv: pyproject.toml uv.lock
	uv sync --locked --project .
	touch .venv

vars.yml vars-native.yml: ../../source/template_variables.yml vars.py .venv
	uv run --project . python vars.py

build: .venv vars.yml
	$(ZENSICAL) build --clean -f zensical.toml 2>&1 | tee build-passthrough.log
	$(ZENSICAL) build --clean -f zensical-native.toml 2>&1 | tee build-native.log

serve: build
	uv run --project . python -m http.server $(PORT) -d site

# Variables, outline and notes checks: every page, passthrough and native
check: build
	../../checks/check-site.sh site $(MAP)

# The raw mode: all_metrics exactly as the book writes it, with its ERB
# line that sets the title (<% current_page.data.title = ... %>), built with
# the passthrough settings, first stopping on error, then not
check-raw: .venv vars.yml
	@for f in true false; do \
	  sed -e 's#^docs_dir = .*#docs_dir = "docs/raw"#' -e 's#^site_dir = .*#site_dir = "site/raw"#' \
	      -e "s#^on_error_fail = .*#on_error_fail = $$f#" zensical.toml > .raw.toml; \
	  echo "== on_error_fail = $$f"; \
	  $(ZENSICAL) build --clean -f .raw.toml > .raw.log 2>&1; echo "exit status $$?"; \
	  grep -v '^  File \|^    ' .raw.log | grep -i 'error\|fail' | head -3; \
	  grep -o '<h1[^>]*>[^<]*<[^>]*>[^<]*' site/raw/all_metrics/index.html 2>/dev/null || echo "(no page written)"; \
	done; rm -f .raw.toml .raw.log

# What each setting of on_undefined does with a name that is not defined
# and with an empty value: probe/probe.md built once per setting
probe: .venv vars.yml
	@for u in silent keep lax strict; do \
	  sed -e 's#^docs_dir = .*#docs_dir = "probe"#' -e 's#^site_dir = .*#site_dir = "site/probe"#' \
	      -e "s#^on_undefined = .*#on_undefined = \"$$u\"#" zensical.toml > .probe.toml; \
	  echo "== on_undefined = $$u"; \
	  $(ZENSICAL) build --clean -f .probe.toml > .probe.log 2>&1; echo "exit status $$?"; \
	  grep -v '^  File \|^    ' .probe.log | grep -i 'error\|fail\|warn' | head -3; \
	  grep -o 'Undefined: [^<]*' site/probe/probe/index.html 2>/dev/null || echo "(no page written)"; \
	done; rm -f .probe.toml .probe.log

clean:
	rm -rf site vars.yml vars-native.yml build-*.log
