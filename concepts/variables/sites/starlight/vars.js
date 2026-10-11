// Writes vars.json from the book's variables file, as it is: the values
// passthrough pages read as $vars (markdoc.config.mjs), and the text values
// of vars-native.mjs.
import fs from 'node:fs';
import {parse} from 'yaml';
const src = parse(fs.readFileSync('../../source/template_variables.yml', 'utf8'));
fs.writeFileSync('vars.json', JSON.stringify(src.template_variables, null, 2) + '\n');
