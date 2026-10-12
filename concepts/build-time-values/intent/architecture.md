# Intent: `architecture`

- Source: [`../source/architecture.html.md.erb`](../source/architecture.html.md.erb),
  cloudfoundry/docs-loggregator
- Converted page: the title and first paragraph, as published (variables
  resolved); this round tests the frame, not the content
- Published: <https://docs.cloudfoundry.org/loggregator/architecture.html>
  (copy: [`../published/architecture.html`](../published/architecture.html))
- Expectations: [`expectations.txt`](expectations.txt)

## Cases this page covers

- **An old date that a content edit set.** The published date,
  2024-12-05, is the author date of
  [`263ee8a`](https://github.com/cloudfoundry/docs-loggregator/commit/263ee8a08955609019677eac930d83caba860058),
  "PR #94 text changes". No candidate commit touches the page, so the
  date is the same with or without the candidate list.
- **Partials do not move the date.** The page includes two partials
  (partials round, [intent](../../partials/intent/architecture.md)). Their
  newest commits are older (2023-03-23 and 2023-10-04) and would not
  change the date, but
  Bookbinder would not count them in any case: it reads the history of
  the page's own file only
  ([`bookbinder_helpers.rb` L159-L169](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/bookbinder_helpers.rb#L159-L169)).
- **A copyright year per page differs from the site's.** In page mode the
  notice says 2024.

## What a conversion must show

| Mode | Copyright year | Last updated |
|---|---|---|
| published | 2026 | 2024-12-05 |
| build | the year of the build | 2024-12-05 |
| site | 2026 | 2024-12-05 |
| page | 2024 | 2024-12-05 |
| history | the year of the build | 2024-12-05: C2's author date, written by the converter (C2's committer date is 2025-01-10) |

## Cleanup and deviations

- **Excerpt** (title and first paragraph), as stated above.
