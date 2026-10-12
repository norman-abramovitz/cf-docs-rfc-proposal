// How Shiki, which Expressive Code uses, splits a console line and a bash
// line into tokens: the scopes and colors of each token, with Starlight's
// default dark theme (Night Owl). Run by `make probe`.
import {codeToTokens} from 'shiki';
const line = '$ cf create-route example-space tcp-domain.example.com --port 60035';
for (const [lang, code] of [['console', line], ['shellsession', line], ['bash', line.slice(2)]]) {
  const r = await codeToTokens(code, {lang, theme: 'night-owl', includeExplanation: true});
  console.log(`== ${lang}`);
  for (const t of r.tokens[0]) {
    const scopes = (t.explanation || []).map((e) => e.scopes.map((s) => s.scopeName).at(-1)).join(', ');
    console.log(`   ${t.color}  ${JSON.stringify(t.content)}  ${scopes}`);
  }
}
