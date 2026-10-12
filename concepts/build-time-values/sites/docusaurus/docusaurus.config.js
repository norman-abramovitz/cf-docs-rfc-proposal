// Build-time values round: the copyright year and "last updated" date.
// YEAR_MODE picks where the footer's year comes from:
//   build  the year of the build (the book's footer today: Time.now.year)
//   site   SITE_YEAR, the year of the newest content date on the site,
//          which `make` computes with helpers/content-date.py
//   page   each page's own content year, shown with its "last updated"
//          date (src/theme/DocItem/Footer); the site footer has no year
// IGNORE_REVS, if set, names a file of commit ids that the "last updated"
// date skips (a custom VCS, below); used by `make history` only.
const fs = require('node:fs');
const path = require('node:path');
const {execFileSync} = require('node:child_process');

const mode = process.env.YEAR_MODE || 'build';
const year = {build: String(new Date().getFullYear()), site: process.env.SITE_YEAR, page: null}[mode];
if (mode === 'site' && !/^\d{4}$/.test(year || '')) {
  throw new Error('YEAR_MODE=site needs SITE_YEAR (four digits)');
}
const notice = (y) =>
  `<a href="/">Cloud Foundry Documentation</a> &copy; ${y} ` +
  `<a href="https://cloudfoundry.org">Cloud Foundry Foundation</a>. All Rights Reserved.`;

// The tool's Git lookup (git log -1 --format=%ct) with listed commits skipped
function ignoreRevsVcs(file) {
  const ignore = new Set(
    fs.readFileSync(file, 'utf8').split('\n').map((l) => l.replace(/#.*/, '').trim()).filter(Boolean),
  );
  return {
    initialize: () => {},
    getFileCreationInfo: async (filePath) => null,
    getFileLastUpdateInfo: async (filePath) => {
      const out = execFileSync('git', ['log', '--format=%H %at %an', '--', path.basename(filePath)], {
        cwd: path.dirname(filePath),
        encoding: 'utf8',
      });
      for (const line of out.split('\n')) {
        const [h, at, ...author] = line.split(' ');
        if (h && !ignore.has(h)) return {timestamp: Number(at) * 1000, author: author.join(' ')};
      }
      return null;
    },
  };
}

module.exports = {
  title: 'Build-time values round — Docusaurus',
  url: 'http://localhost',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  markdown: {format: 'detect'},
  customFields: {yearMode: mode},
  future: process.env.IGNORE_REVS ? {experimental_vcs: ignoreRevsVcs(process.env.IGNORE_REVS)} : {},
  presets: [
    ['classic', {
      // Front matter last_update.date wins; without it, production builds
      // read the date of the newest commit that touched the file.
      docs: {routeBasePath: '/', showLastUpdateTime: true},
      blog: false,
      pages: false,
    }],
  ],
  themeConfig: {
    footer: year ? {copyright: notice(year)} : undefined,
  },
};
