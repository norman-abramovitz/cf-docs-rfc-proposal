// Prints the Markdoc errors in each page, parsed the way the site's Markdoc
// integration parses it (allowHTML), with the errors the build stops on.
// Usage: node markdoc-check.mjs FILE...
import fs from 'node:fs';
import Markdoc from '@markdoc/markdoc';
import {getMarkdocTokenizer} from './node_modules/@astrojs/markdoc/dist/tokenizer.js';
import {htmlTokenTransform} from './node_modules/@astrojs/markdoc/dist/html/transform/html-token-transform.js';
import {htmlTag} from './node_modules/@astrojs/markdoc/dist/html/tagdefs/html.tag.js';

const vars = JSON.parse(fs.readFileSync(new URL('./vars.json', import.meta.url)));
const tokenizer = getMarkdocTokenizer({allowHTML: true});
for (const file of process.argv.slice(2)) {
  const text = fs.readFileSync(file, 'utf8').replace(/^---\n[\s\S]*?\n---\n/, (m) => '\n'.repeat(m.split('\n').length - 1));
  let errors;
  try {
    const ast = Markdoc.parse(htmlTokenTransform(tokenizer, tokenizer.tokenize(text)));
    errors = Markdoc.validate(ast, {variables: {vars}, tags: {'html-tag': htmlTag}})
      .filter((e) => ['error', 'critical'].includes(e.error.level) && e.error.id !== 'variable-undefined' && !/^Partial .+ not found/.test(e.error.message))
      .map((e) => `line ${e.lines[0] + 1}: ${e.error.message}`);
  } catch (e) {
    errors = [`exception: ${e.message.split('\n')[0]}`];
  }
  console.log(`${file.split('/').pop()}: ${errors.length ? errors.length + ' error(s)' : 'ok'}`);
  errors.forEach((e) => console.log('  ' + e));
}
