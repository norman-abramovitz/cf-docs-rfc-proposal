# Antora conventions for build-time values

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#antora-321).

```bash
make build        # install, then three builds: site-build/, site-site/, site-page/
make check        # build, then the build-time values check and the access-control comparison
make history      # the history repository (.history/): no Git date of its own; the helper's dates
make probe-dates  # Asciidoctor's docdate and localdate, and the sitemap's lastmod, with and without SOURCE_DATE_EPOCH
make serve        # serve site-build/ at http://localhost:4304
```

The playbook reads this repository's worktree, as in the earlier rounds;
`make history` uses [history-playbook.yml](history-playbook.yml), which
reads the history repository instead.

## The copyright year

- **The default UI's footer has no notice**, but the UI ships a `year`
  helper that returns the build's year
  ([`year.js` L3](https://gitlab.com/antora/antora-ui-default/-/blob/0e38223adfd81eb74d4b1779e158f8ad05ff8923/src/helpers/year.js#L3);
  [`footer-content.hbs`](https://gitlab.com/antora/antora-ui-default/-/blob/0e38223adfd81eb74d4b1779e158f8ad05ff8923/src/partials/footer-content.hbs);
  both match the pinned UI bundle, compared with `diff`).
- **The site replaces `footer-content.hbs`** through
  `ui.supplemental_files` ([supplemental-ui/partials/footer-content.hbs](supplemental-ui/partials/footer-content.hbs)).
  Templates see the environment as `env`
  ([`build-ui-model.js` L13](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/packages/page-composer/lib/build-ui-model.js#L13)),
  so `{{env.YEAR_MODE}}` and `{{env.SITE_YEAR}}` choose the year; page
  attributes named `page-*` reach the template without the prefix
  ([L70](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/packages/page-composer/lib/build-ui-model.js#L70)).
- **Page mode needs one helper**: Handlebars cannot take the first four
  characters of a date, so [`yearOf.js`](supplemental-ui/helpers/yearOf.js)
  does. A UI helper is JavaScript (one line).

## The "last updated" date

- **No Git-based date.** Antora reads files from Git but records no commit
  date on them.
- **A page attribute carries it**: `:page-last-updated: 2024-12-05` in the
  page header, printed by the replaced footer template.
- **Asciidoctor's `docdate` is the build date**, because Antora hands it
  the file's text, not a file; with `SOURCE_DATE_EPOCH` set it is that
  date instead
  ([`document.rb` L1256-L1270](https://github.com/asciidoctor/asciidoctor/blob/2c03d22eb9fe83d04ee452939581d1b842f6d8b4/lib/asciidoctor/document.rb#L1256-L1270);
  [probe](../../results/antora-probe.txt)).
- **The sitemap's `lastmod` is the build time, the same for every page**
  ([`map-site.js` L50](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/packages/site-mapper/lib/map-site.js#L50));
  `SOURCE_DATE_EPOCH` does not change it ([probe](../../results/antora-probe.txt)).

Decision (this round): **pages carry their content date in the
`page-last-updated` attribute**, written by the converter and updated
before each build by `content-date.py --write`.
