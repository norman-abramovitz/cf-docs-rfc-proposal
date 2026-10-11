// Minimal docs-only site for the partials round: the notes round's site.
module.exports = {
  title: 'Partials round — Docusaurus',
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
