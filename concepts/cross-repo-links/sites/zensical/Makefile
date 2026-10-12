SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build check check-other probe-broken probe-depth probe-redirects clean
# Keep the generated configs and link folders between builds
.SECONDARY:

ZENSICAL = uv run --project . zensical
# Zensical colours its messages; the logs keep the text only
NOCOLOR = perl -pe 's/\e\[[0-9;]*m//g'

# One build per variant, each a whole site in site/<variant>/ served at /.
#   mono:  docs_dir is pages/<mode>, one folder whose subfolders are the URL
#          directories (one repository with directories)
#   linked: docs_dir is linked/native, whose subfolders are symbolic links
#          to the folders of pages/native, as docs-bosh links in the docs of
#          a git submodule (a submodule checked out inside docs_dir is a
#          plain folder, so builds as mono)
#   default: Zensical's default URLs (use_directory_urls = true)
CHECKED = mono-passthrough mono-native
OTHER = linked-native default-passthrough
VARIANTS = $(CHECKED) $(OTHER)
docs.linked-native       = linked/native
docs.mono-passthrough    = pages/passthrough
docs.mono-native         = pages/native
docs.default-passthrough = pages/passthrough
dirurls.default-passthrough = true
DIRS = concepts adminguide devguide running cf-cli

install: .venv
.venv: pyproject.toml uv.lock
	uv sync --project .
	touch .venv

linked/%:
	mkdir -p $@
	ln -sfn ../../pages/$*/index.md $@/index.md
	for d in $(DIRS); do ln -sfn ../../pages/$*/$$d $@/$$d; done

.zensical-%.toml: zensical.toml
	sed -e 's|^docs_dir = .*|docs_dir = "$(docs.$*)"|' \
	    -e 's|^site_dir = .*|site_dir = "site/$*"|' \
	    -e 's|^use_directory_urls = .*|use_directory_urls = $(or $(dirurls.$*),false)|' $< > $@

# The build logs keep Zensical's link and anchor warnings
build: $(addprefix build-,$(VARIANTS))
build-%: install .zensical-%.toml linked/native
	mkdir -p .check
	$(ZENSICAL) build --clean -f .zensical-$*.toml 2>&1 | $(NOCOLOR) | tee .check/build-$*.log

check: $(addprefix build-,$(CHECKED))
	../../checks/check-site.sh site $(CHECKED)

check-other: $(addprefix build-,$(OTHER))
	../../checks/check-site.sh site $(OTHER) || true

# Links that break: a missing page and a missing anchor in another
# directory, in native and passthrough form. The probe page is copied in for
# the builds and removed again; the site is built as it is and with --strict.
probe-broken: install .zensical-mono-native.toml
	mkdir -p .check
	rm -f .check/probe-broken.log
	cp probes/broken.md pages/native/concepts/probe-broken.md
	for opt in "" --strict; do \
	  echo "## mono-native $$opt" >> .check/probe-broken.log; \
	  $(ZENSICAL) build --clean -f .zensical-mono-native.toml $$opt 2>&1 | $(NOCOLOR) >> .check/probe-broken.log; \
	  echo "exit status $${PIPESTATUS[0]}" >> .check/probe-broken.log; \
	done
	python3 -I ../../checks/links.py site/mono-native/concepts/probe-broken.html --root site/mono-native >> .check/probe-broken.log
	rm -f pages/native/concepts/probe-broken.md
	cat .check/probe-broken.log

# Links held in variables and in a partial, on a page one folder deep
# (concepts/) and one two folders deep (devguide/deploy-apps/), each link in
# three forms: the book's relative URL, a root-relative URL, and the tool's
# own form. The probe files are copied in for the build and removed again.
.zensical-probe-depth.toml: .zensical-mono-native.toml probes/depth/macros.toml
	sed -e 's|^site_dir = .*|site_dir = "site/probe-depth"|' .zensical-mono-native.toml > $@
	cat probes/depth/macros.toml >> $@

probe-depth: install .zensical-probe-depth.toml
	mkdir -p .check
	rm -f .check/probe-depth.log
	cp probes/depth/probe-depth.md pages/native/concepts/probe-depth.md
	cp probes/depth/probe-depth.md pages/native/devguide/deploy-apps/probe-depth.md
	$(ZENSICAL) build --clean -f .zensical-probe-depth.toml 2>&1 | $(NOCOLOR) >> .check/probe-depth.log; \
	  echo "exit status $${PIPESTATUS[0]}" >> .check/probe-depth.log
	for p in concepts/probe-depth devguide/deploy-apps/probe-depth; do \
	  echo "## $$p" >> .check/probe-depth.log; \
	  python3 -I ../../checks/links.py site/probe-depth/$$p.html --root site/probe-depth >> .check/probe-depth.log; \
	done
	rm -f pages/native/concepts/probe-depth.md pages/native/devguide/deploy-apps/probe-depth.md
	cat .check/probe-depth.log

# Old URLs: two that the book's redirects.rb sends to routes-domains, one in
# the same repository's folder and one in another's, built with the tool's
# redirect feature; redirects.py reports what the site serves at each.
OLD = /devguide/deploy-apps/domains-routes.html /adminguide/manage-domains-routes.html /devguide/deploy-apps/domains-routes /adminguide/manage-domains-routes
.zensical-probe-redirects.toml: .zensical-mono-native.toml probes/redirects.toml
	sed -e 's|^site_dir = .*|site_dir = "site/probe-redirects"|' .zensical-mono-native.toml > $@
	cat probes/redirects.toml >> $@

probe-redirects: install .zensical-probe-redirects.toml
	mkdir -p .check
	rm -f .check/probe-redirects.log
	$(ZENSICAL) build --clean -f .zensical-probe-redirects.toml 2>&1 | $(NOCOLOR) > .check/probe-redirects-build.log; \
	  echo "exit status $${PIPESTATUS[0]}" >> .check/probe-redirects.log
	python3 -I ../../checks/redirects.py site/probe-redirects $(OLD) >> .check/probe-redirects.log
	cat .check/probe-redirects.log

clean:
	rm -rf site linked .zensical-*.toml .check
