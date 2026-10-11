// Reports every variable a page uses that the variables do not define, as
// Markdoc's validator finds it (error id "variable-undefined"). The site's
// Markdoc integration drops that error, so the build alone says nothing.
// Usage: MODE=native node vars-check.mjs FILE...   (exit status 1 on any)
import fs from 'node:fs';
import Markdoc from '@markdoc/markdoc';
import vars from './vars.json' with {type: 'json'};
import nativeVars from './vars-native.mjs';

const variables = {vars: process.env.MODE === 'native' ? nativeVars : vars};
let found = 0;
for (const file of process.argv.slice(2)) {
  const text = fs.readFileSync(file, 'utf8').replace(/^---\n[\s\S]*?\n---\n/, (m) => '\n'.repeat(m.split('\n').length - 1));
  for (const e of Markdoc.validate(Markdoc.parse(text), {variables})) {
    if (e.error.id !== 'variable-undefined') continue;
    found++;
    console.log(`${file.split('/').pop()}:${e.lines[0] + 1}: ${e.error.message}`);
  }
}
console.log(found ? `${found} variable(s) not defined` : 'ok    every variable defined');
process.exit(found ? 1 : 0);
