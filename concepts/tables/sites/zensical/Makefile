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

clean:
	rm -rf site vars.yml .check
