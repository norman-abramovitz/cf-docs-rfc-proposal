# Starlight conventions for build-time values

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#starlight-0426).

```bash
make build     # install, then three builds: dist-build/, dist-site/, dist-page/
make check     # build, then the build-time values check and the access-control comparison
make history   # the tool's own "last updated" date on a repository with known dates (.history/)
make serve     # serve dist-build/ at http://localhost:4303
```

## The copyright year

- **Starlight's footer has no copyright notice.** The site overrides the
  `Footer` component ([`src/components/Footer.astro`](src/components/Footer.astro);
  the `components` option, [`user-config.ts` L271](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/utils/user-config.ts#L271)):
  it renders the default footer
  ([`Footer.astro`](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/components/Footer.astro#L12))
  and the notice after it. A component override is Astro code.
- **Year modes** as in the Docusaurus site: `new Date().getFullYear()`
  when the page is built, `SITE_YEAR` from the environment, or the page's
  own date (`Astro.locals.starlightRoute.lastUpdated`). All three work in
  the one component.

## The "last updated" date

- **`lastUpdated: true`** in the Starlight options turns it on (default
  false, [`user-config.ts` L261](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/utils/user-config.ts#L261)).
- **Front matter wins**: `lastUpdated: 2024-12-05` (a date, or `false`)
  ([`schema.ts` L50-L52](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/schema.ts#L50-L52);
  [`routing/data.ts` L79-L86](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/utils/routing/data.ts#L79-L86)).
  A date in front matter shows even with the option off.
- **Without it, Git's committer date**, `%ct`, of the newest commit that
  touched the file; the build reads the whole log once
  (`git log --format=t:%ct --name-status`), no rename following
  ([`git.ts` L19-L20, L58-L68](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/utils/git.ts#L19-L68)).
  No option skips commits.
- **Shown in UTC**, "Last updated: Dec 5, 2024", with a `<time datetime>`
  ([`LastUpdated.astro` L9-L10](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/components/LastUpdated.astro#L9-L10)).
- **Sitemap**: Starlight writes one only when Astro's `site` is set (the
  build says so); not tested.

Decision (this round): **pages carry their content date in
`lastUpdated`**, written by the converter and updated before each build by
`content-date.py --write`.
