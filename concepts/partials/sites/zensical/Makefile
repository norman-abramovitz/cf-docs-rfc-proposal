.PHONY: install build serve clean check check-probe probe-missing probe-raw

ZENSICAL = uv run --project . zensical
PORT ?= 8001
# The admonition type each source kind becomes in native mode: the same name
MAP = note=note,important=important,caution=caution

install: .venv
.venv: pyproject.toml uv.lock
	uv sync --project .
	touch .venv

# The variables excerpt, with its top key renamed so pages read vars.name.
# A variable with no value is written as an empty string: YAML reads it as
# null, which the template engine prints as "None"; ERB prints nothing.
vars.yml: ../../source/template_variables.yml
	sed -e 's/^template_variables:/vars:/' -e 's/^\(  [A-Za-z0-9_]*:\)$$/\1 ""/' $< > $@

build: .venv vars.yml
	mkdir -p .check
	$(ZENSICAL) build --clean 2>&1 | tee .check/build.log

serve: build
	uv run --project . python -m http.server $(PORT) -d site

# Partials, outline and notes checks: every page in passthrough, native,
# snippet and variable
check: build
	../../checks/check-site.sh site $(MAP) passthrough native snippet variable

# One partial with a heading included twice: the ids and the table of contents
check-probe: build
	python3 -I ../../../headings/checks/outline.py site/probe/twice/index.html
	python3 -I ../../checks/partials.py site/probe/twice/index.html | grep '^toc'

# Pages that stop the build, each copied in for one build and removed again:
# a missing partial (include and snippet), a partial outside include_dir,
# and the ERB call as written (raw)
PROBES = missing-include missing-snippet updir raw-high-availability
probe-missing: .venv vars.yml
	mkdir -p .check
	for p in $(PROBES); do \
	  cp probes/$$p.md docs/probe/$$p.md; \
	  echo "## $$p" >> .check/probe-missing.log; \
	  $(ZENSICAL) build --clean >> .check/probe-missing.log 2>&1; echo "exit status $$?" >> .check/probe-missing.log; \
	  rm -f docs/probe/$$p.md; \
	done
	cat .check/probe-missing.log

clean:
	rm -rf site vars.yml .check
