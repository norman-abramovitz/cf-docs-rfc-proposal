// Minimal docs-only site for the tables round. Default theme, no blog.
module.exports = {
  title: 'Tables round — Docusaurus',
  url: 'http://localhost',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  markdown: {format: 'detect'}, // .md as CommonMark, .mdx as MDX
  presets: [
    ['classic', {
      docs: {routeBasePath: '/'},
      blog: false,
      pages: false,
    }],
  ],
};
