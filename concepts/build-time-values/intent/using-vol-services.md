# Intent: `using-vol-services`

- Source: [`../source/using-vol-services.html.md.erb`](../source/using-vol-services.html.md.erb),
  cloudfoundry/docs-dev-guide; its content is the partial
  `_using-vol-services` (notes round's copy:
  [`../../notes/source/_using-vol-services.html.md.erb`](../../notes/source/_using-vol-services.html.md.erb))
- Converted page: the title and first paragraph, as published
- Published: <https://docs.cloudfoundry.org/devguide/services/using-vol-services.html>
  (copy: [`../published/using-vol-services.html`](../published/using-vol-services.html))
- Expectations: [`expectations.txt`](expectations.txt)

## Cases this page covers

- **A page whose file is only a partial call.** Bookbinder dates the
  page by the six-line file: 2026-07-21, the author date of
  [`689faba`](https://github.com/cloudfoundry/docs-dev-guide/commit/689faba303969899f0a18aa56f499c2956c70dc0),
  "Remove platform-conditional ERB blocks, keep OSS content". That commit
  removed a conditional the open-source book never rendered; the page's
  text did not change. With the candidates skipped the date is
  2023-05-31,
  [`a02fcd4`](https://github.com/cloudfoundry/docs-dev-guide/commit/a02fcd4ebacf60945daeaa7d0a402511bfa65a46)
  ("Update for improved SEO").
- **The content's own history is elsewhere.** The partial that holds all
  of the page's text was last changed on 2026-07-10 (a markup fix,
  [`0c89158`](https://github.com/cloudfoundry/docs-dev-guide/commit/0c891586ccdaebdad95af4f3204a06a8fbb18823));
  before the July 2026 markup commits, on 2025-03-27 ("style edits for
  recent PRs", [`92475eb`](https://github.com/cloudfoundry/docs-dev-guide/commit/92475ebeb87dbfbfbc51a7d77419561afa3827bf)). Neither date reaches the page today.
  Decision (this round): the content date follows the page's file, as
  Bookbinder does; whether a page that is only an include should take its
  partial's date is listed under [Not yet written](../results.md#not-yet-written).

## What a conversion must show

| Mode | Copyright year | Last updated |
|---|---|---|
| published | 2026 | 2026-07-21 |
| build | the year of the build | 2023-05-31 |
| site | 2026 | 2023-05-31 |
| page | 2023 | 2023-05-31 |
| history | the year of the build | 2019-03-01: C1; its only later commits (C4, C5) are listed as not content |

## Cleanup and deviations

- **Excerpt**, as stated above.
