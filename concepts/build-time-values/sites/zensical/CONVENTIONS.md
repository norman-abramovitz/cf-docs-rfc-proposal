# Zensical conventions for build-time values

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#zensical-0069).

```bash
make build             # install, then three builds: site-build/, site-site/, site-page/
make check             # build, then the build-time values check and the access-control comparison
make history           # the history repository (.history/): no Git date of its own; the helper's dates
make probe-git-plugin  # the MkDocs git-revision-date-localized plugin configured: what Zensical does
make serve             # serve site-build/ at http://localhost:4302
```

## The copyright year

- **`copyright` is a fixed string**: the theme prints `config.copyright`
  as written ([`copyright.html` L5-L7](https://github.com/zensical/ui/blob/5d58e34f4240394d78ab89d149fdb3437151bac1/dist/partials/copyright.html#L5-L7),
  the file Zensical 0.0.69 ships, compared with `cmp`; [`config.py` L533](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/config.py#L533)).
- **Templates have no build date**, and `zensical.toml` reads no
  environment variables: the code that reads `!ENV` serves MkDocs files
  only, and its comment says "We won't likely support this in Zensical"
  ([`config.py` L332](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/config.py#L332)).
  The macros extension's `now()` exists in pages, not in the theme
  ([`macros.py` L420](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/extensions/macros.py#L420)).
- **So the year comes from outside**: the Makefile appends
  `[project.extra] year_mode = …` and `year = …` to a copy of the
  configuration (`build.toml`) and builds with `-f build.toml`; the
  overridden partial ([`overrides/partials/copyright.html`](overrides/partials/copyright.html),
  `theme.custom_dir`, [`config.py` L592](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/config.py#L592))
  prints it. The build's year is `date +%Y` in the Makefile. In page mode
  the partial reads the page's own `revision_date`: no code, a Jinja
  template.
- **Not markdownextradata.** That extension gives data files to the theme,
  but it also renders every page as a Jinja template, and a heading id
  written `{#prerequisites}` opens a Jinja comment: the build failed with
  "TemplateSyntaxError: Missing end of comment tag". The earlier rounds
  set the macros extension to ERB delimiters for the same reason
  ([variables conventions](../../../variables/sites/zensical/CONVENTIONS.md)).

## The "last updated" date

- **`revision_date` in front matter** is shown as "Last update" with the
  value as written
  ([`source-file.html` L86-L89](https://github.com/zensical/ui/blob/5d58e34f4240394d78ab89d149fdb3437151bac1/dist/partials/source-file.html#L86-L89),
  included by `content.html` L10).
- **No Git-based date.** The MkDocs plugin `git-revision-date-localized`
  is not in Zensical's list of supported plugins
  ([`config.py` L123-L190](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/config.py#L123-L190));
  a plugin outside the list is dropped without a message
  ([L1929-L1930](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/config.py#L1929-L1930)).
  Configured, the build says "No issues found" and shows no date
  ([probe](../../results/zensical-probe.txt)).
- **The sitemap has no `lastmod`**, and lists no page unless `site_url` is
  set ([sitemaps](../../results/sitemaps.txt)).

Decision (this round): **pages carry their content date in
`revision_date`**, written by the converter and updated before each build
by `content-date.py --write`.
