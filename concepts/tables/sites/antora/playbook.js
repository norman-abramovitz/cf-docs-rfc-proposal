// Writes site-playbook.yml: antora-playbook.yml plus the variables excerpt as
// AsciiDoc attributes, so <%= vars.name %> becomes {name}. RAW=1 also builds
// the unchanged-HTML pages.
const fs = require('node:fs');
const yaml = require('js-yaml');
const book = yaml.load(fs.readFileSync('antora-playbook.yml', 'utf8'));
const vars = yaml.load(fs.readFileSync('../../source/template_variables.yml', 'utf8')).template_variables;
Object.assign(book.asciidoc.attributes, vars);
if (process.env.RAW) book.content.sources[0].start_paths.push('concepts/tables/sites/antora/passthrough-raw');
fs.writeFileSync('site-playbook.yml', yaml.dump(book));
