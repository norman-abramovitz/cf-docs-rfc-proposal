SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

.PHONY: install build check check-other probe-broken probe-depth probe-redirects clean
.SECONDARY:

# CI=true: the default UI then uses each source's edit_url, not a file://
# link, for content read from a worktree (Antora's content-edit-url docs)
ANTORA = CI=true npx antora --stacktrace
# Antora colours its messages; the logs keep the text only
NOCOLOR = perl -pe 's/\e\[[0-9;]*m//g'

# The default UI, pinned to the same build as the earlier rounds
UI_URL = https://gitlab.com/antora/antora-ui-default/-/jobs/15385706035/artifacts/raw/build/ui-bundle.zip
UI_SHA256 = e0ac81aad26961a9cd3cf9bce692a598eff4a1bd2822ce73c9cdc13a15a1e70d

# One build per variant, each a whole site in site/<variant>/ served at /.
#   split:   antora-split.yml, one component per content repository
#   mono:    antora-mono.yml, one ROOT component with one module per directory
#   default: the mono passthrough pages with Antora's indexify URL style
#            (<path>/index.html), the folder URLs the other tools default to
CHECKED = split-passthrough split-native mono-passthrough mono-native
OTHER = default-passthrough
VARIANTS = $(CHECKED) $(OTHER)
book.default-passthrough = mono-passthrough
opts.default-passthrough = --html-url-extension-style=indexify --to-dir site/default-passthrough

install: node_modules .cache/ui-bundle.zip
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

.cache/ui-bundle.zip:
	mkdir -p .cache
	curl -fsSL -o $@.tmp '$(UI_URL)'
	echo '$(UI_SHA256)  $@.tmp' | shasum -a 256 -c -
	mv $@.tmp $@

.playbook-split-%.yml: antora-split.yml
	sed 's/MODE/$*/g' $< > $@
.playbook-mono-%.yml: antora-mono.yml
	sed 's/MODE/$*/g' $< > $@

# The build logs keep Antora's messages (xref targets not found, …).
# A variant's playbook is named by book.<variant>, else by the variant.
.SECONDEXPANSION:
build: $(addprefix build-,$(VARIANTS))
build-%: install .playbook-$$(or $$(book.$$*),$$*).yml
	mkdir -p .check
	$(ANTORA) .playbook-$(or $(book.$*),$*).yml $(opts.$*) 2>&1 | $(NOCOLOR) | tee .check/build-$*.log

check: $(addprefix build-,$(CHECKED))
	../../checks/check-site.sh site $(CHECKED)

check-other: $(addprefix build-,$(OTHER))
	../../checks/check-site.sh site $(OTHER) || true

# Links that break: a missing page and a missing anchor in another content
# source (split) or module (mono), in native and passthrough form. The probe
# page is copied in for the builds and removed again. Each layout is built
# with Antora's default failure level, and with --log-failure-level=error
# and --log-level=info (Asciidoctor reports an in-page reference it cannot
# find at the info level).
probe-broken: install .playbook-split-native.yml .playbook-mono-native.yml
	mkdir -p .check
	rm -f .check/probe-broken.log
	cp probes/broken-split.adoc native/split/concepts/modules/ROOT/pages/probe-broken.adoc
	cp probes/broken-mono.adoc native/mono/modules/concepts/pages/probe-broken.adoc
	for v in split-native mono-native; do \
	  for opt in "" "--log-failure-level=error --log-level=info"; do \
	    echo "## $$v $$opt" >> .check/probe-broken.log; \
	    $(ANTORA) .playbook-$$v.yml --to-dir .check/probe-$$v $$opt 2>&1 | $(NOCOLOR) >> .check/probe-broken.log; \
	    echo "exit status $${PIPESTATUS[0]}" >> .check/probe-broken.log; \
	  done; \
	  python3 -I ../../checks/links.py .check/probe-$$v/concepts/probe-broken.html --root .check/probe-$$v >> .check/probe-broken.log; \
	done
	rm -f native/split/concepts/modules/ROOT/pages/probe-broken.adoc native/mono/modules/concepts/pages/probe-broken.adoc
	cat .check/probe-broken.log

# Links held in variables and in a partial, on a page one folder deep
# (concepts/) and one two folders deep (devguide/deploy-apps/), each link in
# three forms: the book's relative URL, a root-relative URL, and the tool's
# own form. The probe files are copied in for the build and removed again.
.playbook-probe-depth.yml: .playbook-mono-native.yml probes/depth/attributes.yml
	awk '{print} /idseparator:/ {while ((getline l < "probes/depth/attributes.yml") > 0) print l}' $< \
	  | sed -e 's|dir: ./site/mono-native|dir: ./.check/probe-depth|' > $@

probe-depth: install .playbook-probe-depth.yml
	mkdir -p .check native/mono/modules/concepts/partials
	rm -f .check/probe-depth.log
	cp probes/depth/probe-partial.adoc native/mono/modules/concepts/partials/probe-partial.adoc
	cp probes/depth/probe-depth-1.adoc native/mono/modules/concepts/pages/probe-depth.adoc
	cp probes/depth/probe-depth-2.adoc native/mono/modules/devguide/pages/deploy-apps/probe-depth.adoc
	$(ANTORA) .playbook-probe-depth.yml 2>&1 | $(NOCOLOR) >> .check/probe-depth.log; \
	  echo "exit status $${PIPESTATUS[0]}" >> .check/probe-depth.log
	for p in concepts/probe-depth devguide/deploy-apps/probe-depth; do \
	  echo "## $$p" >> .check/probe-depth.log; \
	  python3 -I ../../checks/links.py .check/probe-depth/$$p.html --root .check/probe-depth >> .check/probe-depth.log; \
	done
	rm -rf native/mono/modules/concepts/partials native/mono/modules/concepts/pages/probe-depth.adoc \
	  native/mono/modules/devguide/pages/deploy-apps/probe-depth.adoc
	cat .check/probe-depth.log

# Old URLs: two that the book's redirects.rb sends to routes-domains, one in
# the same repository's folder and one in another's, built with the tool's
# redirect feature; redirects.py reports what the site serves at each.
OLD = /devguide/deploy-apps/domains-routes.html /adminguide/manage-domains-routes.html /devguide/deploy-apps/domains-routes /adminguide/manage-domains-routes
# The aliases are added to routes-domains for the builds and removed again.
ALIAS.split-native = :page-aliases: deploy-apps/domains-routes.adoc, adminguide::manage-domains-routes.adoc
ALIAS.mono-native = :page-aliases: deploy-apps/domains-routes.adoc, adminguide:manage-domains-routes.adoc
PAGE.split-native = native/split/devguide/modules/ROOT/pages/deploy-apps/routes-domains.adoc
PAGE.mono-native = native/mono/modules/devguide/pages/deploy-apps/routes-domains.adoc
probe-redirects: install
	mkdir -p .check
	rm -f .check/probe-redirects.log
	$(MAKE) --no-print-directory probe-redirects-split-native probe-redirects-mono-native
	cat .check/probe-redirects.log
probe-redirects-%: .playbook-%.yml
	cp $(PAGE.$*) $(PAGE.$*).orig
	ALIAS='$(ALIAS.$*)' perl -pi -e 'print "$$ENV{ALIAS}\n" if $$. == 2' $(PAGE.$*)
	echo "## $*" >> .check/probe-redirects.log
	$(ANTORA) .playbook-$*.yml --to-dir .check/probe-redirects-$* 2>&1 | $(NOCOLOR) > .check/probe-redirects-$*.log; \
	  echo "exit status $${PIPESTATUS[0]}" >> .check/probe-redirects.log
	mv $(PAGE.$*).orig $(PAGE.$*)
	python3 -I ../../checks/redirects.py .check/probe-redirects-$* $(OLD) >> .check/probe-redirects.log

clean:
	rm -rf site .playbook-*.yml .check
