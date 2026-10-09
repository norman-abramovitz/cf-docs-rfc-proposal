// Writes vars.json from the verbatim variables excerpt; markdoc.config.mjs
// passes it to every page as $vars.
import fs from 'node:fs';
import {parse} from 'yaml';
const src = parse(fs.readFileSync('../../source/template_variables.yml', 'utf8'));
fs.writeFileSync('vars.json', JSON.stringify(src.template_variables, null, 2) + '\n');
