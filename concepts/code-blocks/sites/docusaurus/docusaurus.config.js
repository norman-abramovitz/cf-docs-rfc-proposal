// Minimal docs-only site for the code blocks round: the variables round's
// site, without its heading plugin (product names are text, convention 9 of
// that round), plus the Prism languages the test pages use. The classic
// theme's code block has a copy button by default.
// DOCS_PATH builds another folder instead of docs/ (make probe).
module.exports = {
  title: 'Code blocks round — Docusaurus',
  url: 'http://localhost',
  baseUrl: '/',
  // Links to pages outside the test set cannot resolve here; anchors that
  // do not resolve are reported too (onBrokenAnchors defaults to 'warn').
  onBrokenLinks: 'warn',
  markdown: {format: 'detect'}, // .md as CommonMark, .mdx as MDX
  presets: [
    ['classic', {
      docs: {routeBasePath: '/', path: process.env.DOCS_PATH || 'docs'},
      blog: false,
      pages: false,
    }],
  ],
  themeConfig: {
    // Prism grammars beyond the ones prism-react-renderer bundles. Prism has
    // no `console` grammar; its shell session grammar is `shell-session`
    // (aliases `sh-session`, `shellsession`), which the ejected
    // src/theme/prism-include-languages.js also registers as `console`.
    prism: {additionalLanguages: ['bash', 'shell-session', 'groovy', 'nginx']},
  },
  // NO_CONSOLE_ALIAS=1 builds without the `console` alias (make probe)
  customFields: {consoleAlias: !process.env.NO_CONSOLE_ALIAS},
};
