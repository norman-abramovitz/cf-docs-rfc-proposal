# Intent: `access-control`

- Source: [`../source/access-control.html.md.erb`](../source/access-control.html.md.erb),
  cloudfoundry/docs-services
- Converted page: the whole page, the headings round's native conversion
  in each tool, with its content date added
  ([`../helpers/pages.py`](../helpers/pages.py))
- Published: <https://docs.cloudfoundry.org/services/access-control.html>
  (copy: [`../published/access-control.html`](../published/access-control.html))
- Expectations (what the check reads): [`expectations.txt`](expectations.txt)

## Cases this page covers

- **The newest commit is a markup fix.** "Page last updated" on the
  published page is 2026-07-09, the author date of
  [`e7d9f46`](https://github.com/cloudfoundry/docs-services/commit/e7d9f46989d76834664b819ee2d6694e9db525c4),
  "Remove p tags that interfere with Markdown rendering". The commit
  before it,
  [`0d7756e`](https://github.com/cloudfoundry/docs-services/commit/0d7756e780c7bfd4b915a4d93c4eee4ac3a89771)
  (2026-06-26), "Remove out-of-support cf CLI v6 minimum version
  requirements", changed what the page says
  ([survey/pages.csv](../survey/pages.csv)).
- **The page compared word by word.** It is the one test page converted
  whole, so the comparison helper runs on it in every tool
  ([checks/buildtime.py](../checks/buildtime.py) `--compare`).

## What a conversion must show

| Mode | Copyright year | Last updated |
|---|---|---|
| published | 2026 | 2026-07-09 |
| build | the year of the build | 2026-06-26 |
| site | 2026, the newest content year on the test site | 2026-06-26 |
| page | 2026 | 2026-06-26 |
| history | the year of the build | 2026-10-05: the edit after conversion, by its author date |

The holder is "Cloud Foundry Foundation" in every mode, as published
([`_book-footer.erb` L3](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/_book-footer.erb#L3)).

Decision (this round): the content date in the converted modes skips the
candidate commits of [survey/candidates.txt](../survey/candidates.txt),
so it differs from the published date on purpose. The comparison helper
lists both dates as expected differences
([R-25](../../../requirements/README.md#r-25)).

## Cleanup and deviations

- None. The page text is the headings round's, unchanged.
