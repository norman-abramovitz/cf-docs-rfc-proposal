// Writes vars.json from the book's variables file, as it is, so pages can
// `import vars from '@site/vars.json'` (passthrough) and src/vars.js can
// read the text values (native).
const fs = require('fs');
const yaml = require('js-yaml');
const src = yaml.load(fs.readFileSync('../../source/template_variables.yml', 'utf8'));
fs.writeFileSync('vars.json', JSON.stringify(src.template_variables, null, 2) + '\n');
