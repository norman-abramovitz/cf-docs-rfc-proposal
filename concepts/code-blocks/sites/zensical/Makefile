.PHONY: install build serve clean check check-browser probe

ZENSICAL = NO_COLOR=1 uv run --project . zensical
PORT ?= 4102
# The admonition type each note kind becomes: the same name
MAP = note=note,important=important,caution=caution
# What native mode requires of every code block: a type, statically; in
# the browser also a copy button that copies the block's text or commands
# (the theme adds the button with JavaScript)
REQUIRE = type
REQUIRE_BROWSER = type,copy
PAGES = routes-domains troubleshooting_slow_requests gsg-grails backup backup-clean nginx multiple-processes

install: .venv
.venv: pyproject.toml uv.lock
	uv sync --locked --project .
	touch .venv

vars.yml: ../../source/template_variables.yml vars.py .venv
	uv run --project . python vars.py

# Both modes from docs/ into site/; the log keeps Zensical's warnings
build: .venv vars.yml
	mkdir -p .check
	$(ZENSICAL) build --clean -f zensical.toml 2>&1 | tee .check/build.log

serve: build
	uv run --project . python -m http.server $(PORT) -d site

# Code-block, outline and notes checks: every page, passthrough and native
check: build
	../../checks/check-site.sh site $(MAP) $(REQUIRE)

# The same checks on the pages as the browser holds them after the theme's
# scripts ran, with each copy button clicked (../../checks/codeblocks-browser.mjs)
check-browser: build
	@python3 -m http.server $(PORT) -d site > /dev/null 2>&1 & pid=$$!; sleep 1; \
	  node ../../checks/codeblocks-browser.mjs .check/browser $(foreach m,passthrough native,$(foreach p,$(PAGES),http://localhost:$(PORT)/$(m)/$(p)/)); s=$$?; \
	  kill $$pid; ../../checks/check-site.sh .check/browser $(MAP) $(REQUIRE_BROWSER) || s=1; exit $$s

clean:
	rm -rf site vars.yml .check
