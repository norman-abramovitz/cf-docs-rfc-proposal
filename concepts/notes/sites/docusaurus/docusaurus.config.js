// Minimal docs-only site for the notes round: the headings round's site
// (the tables round's without its table plugin and table CSS).
module.exports = {
  title: 'Notes round — Docusaurus',
  url: 'http://localhost',
  baseUrl: '/',
  // Links to pages outside the test set cannot resolve here; anchors that
  // do not resolve are reported too (onBrokenAnchors defaults to 'warn').
  onBrokenLinks: 'warn',
  markdown: {format: 'detect'}, // .md as CommonMark, .mdx as MDX
  presets: [
    ['classic', {
      docs: {routeBasePath: '/'},
      blog: false,
      pages: false,
    }],
  ],
};
