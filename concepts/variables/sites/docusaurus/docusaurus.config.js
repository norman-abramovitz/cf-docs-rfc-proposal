// Minimal docs-only site for the variables round: the notes round's site.
// DOCS_PATH builds another folder instead of docs/ (make probe).
module.exports = {
  title: 'Variables round — Docusaurus',
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
};
