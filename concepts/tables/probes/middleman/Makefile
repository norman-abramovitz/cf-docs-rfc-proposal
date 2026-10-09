.PHONY: install build serve clean check

PORT ?= 8005

# Bundler as recorded in Gemfile.lock, installed into the probe. A Ruby whose
# own Bundler is shadowed by an older copy (here: Homebrew's site_ruby held
# Bundler 4.0.19 next to Ruby 4.0.7's 4.0.20) cannot install or run the
# bundle; a Bundler of the probe's own avoids that without a global change.
BUNDLER_VERSION = $(shell awk '/^BUNDLED WITH/ {getline; print $$1}' Gemfile.lock)
BUNDLE = env GEM_PATH=$(CURDIR)/vendor/bundler $(CURDIR)/vendor/bundler/bin/bundle

# sassc (a Middleman dependency) compiles C++. Where the compiler finds no
# C++ standard headers of its own, point it at the SDK's.
CXX_HEADERS = $(shell xcrun --show-sdk-path 2>/dev/null)/usr/include/c++/v1

install: vendor/bundle
vendor/bundler/bin/bundle:
	gem install bundler -v $(BUNDLER_VERSION) --install-dir vendor/bundler --no-document
vendor/bundle: Gemfile Gemfile.lock vendor/bundler/bin/bundle
	$(BUNDLE) config set --local path vendor/bundle
	CPLUS_INCLUDE_PATH=$(CXX_HEADERS) $(BUNDLE) install
	touch vendor/bundle

build: install
	$(BUNDLE) exec middleman build

serve: build
	python3 -m http.server $(PORT) -d build

PAGES = scale-table-host credential-types metadata troubleshooting_slow_requests uaa-concepts

# Spot checks from the intent files. The pages are unchanged, so the three
# checks that test the intent files' cleanup fail here as they would on the
# published page.
check: build
	@mkdir -p .check
	@for p in $(PAGES); do cp build/$$p.html .check/$$p.html; done
	@echo "== unchanged: $$(../../checks/spot-checks.sh .check | grep -c '^ok') passed"
	@../../checks/spot-checks.sh .check | grep -v '^ok' || true
	@grep -q '<span id="undefined">Undefined: </span>' build/variable-checks.html && echo "ok    undefined variable renders as nothing" || echo "FAIL  undefined variable"
	@grep -q '<div id="html-raw"><p class="note">' build/variable-checks.html && echo "ok    HTML-valued variable renders as markup" || echo "FAIL  HTML-valued variable"

clean:
	rm -rf build .check
