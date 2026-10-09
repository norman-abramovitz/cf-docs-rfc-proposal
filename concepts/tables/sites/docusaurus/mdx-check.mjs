// Compiles each MDX file with the site's own @mdx-js/mdx and prints the first
// error per file. MDX stops at the first error, so a page can hide more.
import {compile} from '@mdx-js/mdx';
import fs from 'node:fs';
for (const f of process.argv.slice(2)) {
  try { await compile(fs.readFileSync(f, 'utf8')); console.log(`OK    ${f.split('/').pop()}`); }
  catch (e) {
    const line = e.place?.start?.line ?? e.line ?? e.place?.line; const src = fs.readFileSync(f,'utf8').split('\n')[line-1] ?? '';
    console.log(`FAIL  ${f.split('/').pop()}:${line}: ${e.reason ?? e.message}\n      > ${src.trim().slice(0,110)}`);
  }
}
