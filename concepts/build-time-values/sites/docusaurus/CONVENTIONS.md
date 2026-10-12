# Docusaurus conventions for build-time values

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#docusaurus-3102). The pages are the headings
round's (`access-control`) and short excerpts
([README](../../README.md#test-pages)).

```bash
make build     # install, then three builds: build-build/, build-site/, build-page/
make check     # build, then the build-time values check on every page and the access-control comparison
make history   # the tool's own "last updated" date on a repository with known dates (.history/)
make serve     # serve build-build/ at http://localhost:4301
```

## The copyright year

| Year from | How | Code |
|---|---|---|
| The build (as the book today) | `` themeConfig.footer.copyright: `… &copy; ${new Date().getFullYear()} …` `` | none: the config is JavaScript; Docusaurus's own site template does the same ([`docusaurus.config.js` L149](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/create-docusaurus/templates/classic/docusaurus.config.js#L149)) |
| The newest content date on the site | `SITE_YEAR`, computed by [`content-date.py`](../../helpers/content-date.py) `--year`, read in the config | none beyond the config |
| Each page's content date | a wrapped `@theme/DocItem/Footer` ([`src/theme/DocItem/Footer/index.js`](src/theme/DocItem/Footer/index.js)) prints the notice with the year of `lastUpdatedAt` | a React component: the site footer has no access to the page's data |

`YEAR_MODE` (`build`, `site`, `page`) picks one; the Makefile builds all
three ([docusaurus.config.js](docusaurus.config.js)). The build's year is
the build machine's local year (`new Date()`), so a build in the hours
around New Year depends on the machine's time zone.

## The "last updated" date

- **`showLastUpdateTime: true`** in the docs plugin turns it on.
- **Front matter wins**: `last_update: {date: 2024-12-05}` is used as
  written, and Git is not asked
  ([`lastUpdateUtils.ts` L64-L96](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-utils/src/lastUpdateUtils.ts#L64-L96)).
- **Without it, Git's committer date** of the newest commit that touched
  the file: `git log --format=%ct --max-count=1 -- <file>`, no rename
  following
  ([`gitUtils.ts` L148-L160](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-utils/src/vcs/gitUtils.ts#L148-L160)).
  Only in production builds: `docusaurus start` shows a fixed made-up
  date ([`vcsDefaultV1.ts` L13-L16](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-utils/src/vcs/vcsDefaultV1.ts#L13-L16)).
- **Shown in UTC**, as "Last updated on Dec 5, 2024", with a `<time
  datetime>` ([`LastUpdated/index.tsx` L25-L37](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-theme-classic/src/theme/LastUpdated/index.tsx#L25-L37)).
- **A custom VCS can skip commits.** `future.experimental_vcs` takes an
  object with three functions
  ([`configValidation.ts` L355-L360](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus/src/server/configValidation.ts#L355-L360)).
  The site's `ignoreRevsVcs` reads a `.git-blame-ignore-revs` file and
  returns the newest commit not listed. It works ([history](../../results/docusaurus-history.txt),
  `out-vcs`), but a page whose only commits before conversion are under
  its old name gets no date: the lookup does not follow the rename. The
  name says the API is experimental.
- **The sitemap has no `lastmod`** unless the sitemap plugin's `lastmod`
  option is set ([`options.ts` L33-L72](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-plugin-sitemap/src/options.ts#L33-L72); [sitemaps](../../results/sitemaps.txt)).

Decision (this round): **pages carry their content date in
`last_update.date`**, written by the converter and updated before each
build by `content-date.py --write` (the history `helper` variant). The
tool's Git lookup is not used: it dates every page by the conversion
commit, and by the newest commit in a shallow clone.
