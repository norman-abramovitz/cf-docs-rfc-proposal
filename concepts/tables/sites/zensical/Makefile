.PHONY: install build serve clean check

ZENSICAL = uv run --project . zensical
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

PAGES = scale-table-host credential-types metadata troubleshooting_slow_requests uaa-concepts
MODES ?= passthrough extension native

# Spot checks from the intent files, per mode; prints only failures
check: build
	@for m in $(MODES); do \
	  mkdir -p .check/$$m; \
	  for p in $(PAGES); do cp site/$$m/$$p/index.html .check/$$m/$$p.html; done; \
	  echo "== $$m: $$(../../checks/spot-checks.sh .check/$$m | grep -c '^ok') passed"; \
	  ../../checks/spot-checks.sh .check/$$m | grep -v '^ok' || true; \
	done

clean:
	rm -rf site vars.yml .check
