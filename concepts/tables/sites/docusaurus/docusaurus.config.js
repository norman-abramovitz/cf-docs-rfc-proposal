// Minimal docs-only site for the tables round. Default theme, no blog.
module.exports = {
  title: 'Tables round — Docusaurus',
  url: 'http://localhost',
  baseUrl: '/',
  // Links to pages outside the test set (other repositories) cannot resolve
  // here; cross-repository links are a separate concept.
  onBrokenLinks: 'warn',
  markdown: {format: 'detect'}, // .md as CommonMark, .mdx as MDX
  presets: [
    ['classic', {
      docs: {
        routeBasePath: '/',
        // Raw passthrough pages are kept as evidence; build them with RAW=1.
        exclude: [
          '**/_*.{js,jsx,ts,tsx,md,mdx}', '**/_*/**', '**/*.test.{js,jsx,ts,tsx}', '**/__tests__/**',
          ...(process.env.RAW ? [] : ['passthrough-raw/**']),
        ],
      },
      blog: false,
      pages: false,
    }],
  ],
};
