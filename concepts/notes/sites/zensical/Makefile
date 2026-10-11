.PHONY: install build serve clean check check-raw

ZENSICAL = uv run --project . zensical
PORT ?= 8001
# The admonition type each source kind becomes in native mode: the same name
MAP = note=note,important=important,caution=caution

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

# Outline and notes checks: every page in every mode
check: build
	../../checks/check-site.sh site $(MAP)

# The raw mode: notes exactly as the source writes them (only cf-backup differs)
check-raw: build
	../../checks/check-site.sh site "" raw

clean:
	rm -rf site vars.yml
