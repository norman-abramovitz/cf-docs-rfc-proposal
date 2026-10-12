// Writes vars.json from the round's excerpt of the book's variables file:
// the values pages read as $vars (markdoc.config.mjs).
import fs from 'node:fs';
import {parse} from 'yaml';
const src = parse(fs.readFileSync('../../source/template_variables.yml', 'utf8'));
fs.writeFileSync('vars.json', JSON.stringify(src.template_variables, null, 2) + '\n');
