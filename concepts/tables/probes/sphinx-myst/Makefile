.PHONY: install build serve clean check

SPHINX = uv run --project . sphinx-build -q
PORT ?= 8004

install: .venv
.venv: pyproject.toml uv.lock
	uv sync --project .
	touch .venv

build: .venv
	$(SPHINX) -W -b html docs _build/html

serve: build
	uv run --project . python -m http.server $(PORT) -d _build/html

# The shared spot checks; only the scale table's apply to this probe.
# Sphinx writes inline code as <code class="docutils literal notranslate">
# with each word in a <span class="pre">; CODE puts back plain <code>.
CODE = 's\#<code class="docutils literal notranslate">(.*?)</code>\#my $$c = $$1; $$c =~ s{</?span[^>]*>}{}g; "<code>$$c</code>"\#ge'
check: build
	@mkdir -p .check
	@perl -pe $(CODE) _build/html/scale-table-host.html > .check/scale-table-host.html
	@../../checks/spot-checks.sh .check 2>/dev/null | grep 'scale-table-host'

clean:
	rm -rf _build .check
