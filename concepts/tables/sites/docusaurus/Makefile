.PHONY: install build serve clean check-raw

install: node_modules
node_modules: package.json
	npm install --no-audit --no-fund
	touch node_modules

vars.json: ../../source/template_variables.yml vars.js node_modules
	node vars.js

build: vars.json
	npm run build

serve: build
	npm run serve

# First MDX error on each unchanged-HTML page
check-raw: node_modules
	node mdx-check.mjs docs/passthrough-raw/*.mdx

clean:
	rm -rf build .docusaurus vars.json
