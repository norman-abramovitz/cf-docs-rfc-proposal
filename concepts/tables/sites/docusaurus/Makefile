.PHONY: install build serve clean

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

clean:
	rm -rf build .docusaurus vars.json
