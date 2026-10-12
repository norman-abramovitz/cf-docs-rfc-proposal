# The recipes set pipefail themselves: macOS ships GNU Make 3.81, which
# ignores .SHELLFLAGS, so a failed build piped into tee would pass.
SHELL := /bin/bash

.PHONY: install build serve clean check check-browser check-raw probe

PORT ?= 4101
# The admonition type each note kind becomes
MAP = note=note,important=warning,caution=danger
# What native mode requires of every code block: a type, statically; in
# the browser also a copy button that copies the block's text or commands
# (the theme renders the button in the browser)
REQUIRE = type
REQUIRE_BROWSER = type,copy
PAGES = routes-domains troubleshooting_slow_requests gsg-grails backup backup-clean nginx multiple-processes

install: node_modules
node_modules: package.json package-lock.json
	npm ci --no-audit --no-fund
	touch node_modules

vars.json: ../../source/template_variables.yml vars.js node_modules
	node vars.js

# The build log keeps Docusaurus's broken-link and broken-anchor warnings
build: vars.json
	mkdir -p .check
	set -o pipefail; npm run build 2>&1 | tee .check/build.log

serve: build
	npx docusaurus serve --no-open --port $(PORT)

# Code-block, outline and notes checks: every page, passthrough and native
check: build
	../../checks/check-site.sh build $(MAP) $(REQUIRE)

# The same checks on the pages as the browser holds them, with each copy
# button clicked (../../checks/codeblocks-browser.mjs)
check-browser: build
	@python3 -m http.server $(PORT) -d build > /dev/null 2>&1 & pid=$$!; sleep 1; \
	  node ../../checks/codeblocks-browser.mjs .check/browser $(foreach m,passthrough native,$(foreach p,$(PAGES),http://localhost:$(PORT)/$(m)/$(p)/)); s=$$?; \
	  kill $$pid; ../../checks/check-site.sh .check/browser $(MAP) $(REQUIRE_BROWSER) || s=1; exit $$s

# The raw mode: the NGINX page with its prose written as the book writes it,
# <code>{{port}}</code> (raw-mdx/). MDX compiles it (mdx-check.mjs), and the
# build stops when it renders the page.
check-raw: vars.json
	node mdx-check.mjs raw-mdx/*.mdx
	@rm -rf .check/raw-docs && mkdir -p .check/raw-docs && cp raw-mdx/*.mdx .check/raw-docs/; \
	DOCS_PATH=.check/raw-docs npx docusaurus build --out-dir .check/raw-build > .check/raw.log 2>&1; echo "build exit status $$?"; \
	grep -o "Can't render static file for pathname \"[^\"]*\"\|ReferenceError: [^)]*defined" .check/raw.log | sort -u

# Two probes, each a small site built from probe/: a console fence with and
# without the site's console alias (the token classes Prism gives its first
# line), and a passthrough page in Docusaurus's CommonMark format (.md, in
# probe/md/), where raw HTML is not rendered (the code-block check on it)
probe: vars.json
	@rm -rf .check/probe-docs && mkdir -p .check/probe-docs && cp probe/console.mdx .check/probe-docs/; \
	for a in "" 1; do \
	  NO_CONSOLE_ALIAS=$$a DOCS_PATH=.check/probe-docs npx docusaurus build --out-dir .check/probe-build > .check/probe.log 2>&1 || { tail -5 .check/probe.log; exit 1; }; \
	  echo "== console fence, NO_CONSOLE_ALIAS=$$a"; \
	  python3 -c "import re,sys; s=open(sys.argv[1]).read(); i=s.find('language-console'); print('   token classes on line 1:', sorted(set(re.findall(r'class=\"(token [^\"]+)\"', s[i:s.find('</div>', s.find('token-line', i))]))))" .check/probe-build/console/index.html; \
	done; \
	rm -rf .check/probe-docs && mkdir -p .check/probe-docs/md && cp probe/md/*.md .check/probe-docs/md/ && cp -R docs/passthrough/images .check/probe-docs/md/; \
	DOCS_PATH=.check/probe-docs npx docusaurus build --out-dir .check/probe-build > .check/probe.log 2>&1 || { tail -5 .check/probe.log; exit 1; }; \
	echo "== md/troubleshooting_slow_requests (CommonMark format)"; \
	python3 -I ../../checks/codeblocks.py .check/probe-build/md/troubleshooting_slow_requests/index.html --expect ../../intent/troubleshooting_slow_requests.code || true

clean:
	rm -rf build .docusaurus vars.json .check
