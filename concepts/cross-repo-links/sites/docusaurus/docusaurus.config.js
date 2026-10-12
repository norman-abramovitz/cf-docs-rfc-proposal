// Docs-only site for the cross-repository links round. One build per
// variant (make build); the environment picks the variant:
//   LAYOUT  split: one docs plugin instance per content repository, each
//                  publishing under its URL directory (concepts, adminguide, …)
//           mono:  one instance over one folder whose subfolders are the URL
//                  directories (one repository with directories)
//   PAGES   the folder under pages/ the pages come from (passthrough,
//           native-split, native-mono)
//   URLS    html:    pages are written as <path>.html (trailingSlash: false),
//                    so the book's URLs keep working on a static host
//           default: Docusaurus's default (<path>/index.html)
//   ON_BROKEN  what a broken link or anchor does: warn (here) or throw
//   REDIRECTS  1: add the client-redirects plugin with the probe's redirects
const layout = process.env.LAYOUT || 'mono';
const pages = process.env.PAGES || 'passthrough';
const urls = process.env.URLS || 'html';
const onBroken = process.env.ON_BROKEN || 'warn';

// URL directory -> repository, as the book's config.yml maps them
const repos = {
  concepts: 'docs-cloudfoundry-concepts',
  adminguide: 'docs-cf-admin',
  devguide: 'docs-dev-guide',
  running: 'docs-running-cf',
  'cf-cli': 'docs-cf-cli',
};
// The edit link names the page's source file in its own repository
const sourceFile = (p) => p.replace(/\.mdx?$/, '.html.md.erb');
const editUrlFor = (dir) => ({docPath}) =>
  `https://github.com/cloudfoundry/${repos[dir]}/blob/master/${sourceFile(docPath)}`;
const editUrlMono = ({docPath}) => {
  const [dir, ...rest] = docPath.split('/');
  if (!repos[dir]) return 'https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/master/master_middleman/source/index.html.md.erb';
  return `https://github.com/cloudfoundry/${repos[dir]}/blob/master/${sourceFile(rest.join('/'))}`;
};

const plugins = layout === 'split'
  ? Object.keys(repos).map((dir) => ['@docusaurus/plugin-content-docs', {
      id: dir,
      path: `pages/${pages}/${dir}`,
      routeBasePath: dir,
      editUrl: editUrlFor(dir),
    }])
  : [];
if (process.env.REDIRECTS === '1') {
  plugins.push(['@docusaurus/plugin-client-redirects', require('./probes/redirects.js')]);
}

module.exports = {
  title: 'Cross-repository links round — Docusaurus',
  url: 'https://docs.cloudfoundry.org',
  baseUrl: '/',
  trailingSlash: urls === 'html' ? false : undefined,
  // Report, do not stop: the build log is part of the results
  onBrokenLinks: onBroken,
  onBrokenAnchors: onBroken,
  markdown: {format: 'detect', hooks: {onBrokenMarkdownLinks: onBroken}},
  presets: [
    ['classic', {
      // mono: the home page is the docs' own page at / (slug: /); split: the
      // book repository's start page is a page of the pages plugin
      docs: layout === 'mono'
        ? {path: `pages/${pages}`, routeBasePath: '/', editUrl: editUrlMono}
        : false,
      blog: false,
      pages: layout === 'split' ? {path: `pages/${pages}/home`} : false,
    }],
  ],
  plugins,
};
