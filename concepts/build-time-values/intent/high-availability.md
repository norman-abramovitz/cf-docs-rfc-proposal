# Intent: `high-availability`

- Source: [`../source/high-availability.html.md.erb`](../source/high-availability.html.md.erb),
  cloudfoundry/docs-cloudfoundry-concepts
- Converted page: the title and first paragraph, as published
- Published: <https://docs.cloudfoundry.org/concepts/high-availability.html>
  (copy: [`../published/high-availability.html`](../published/high-availability.html))
- Expectations: [`expectations.txt`](expectations.txt)

## Cases this page covers

- **A source-only commit sets the date, and the next one is borderline.**
  The published date, 2026-07-22, is
  [`5362f10`](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/commit/5362f104d6d911d783f0cb2de8420688f8b916c5),
  which unwrapped the open-source branch of a conditional and dropped the
  commercial one: on this page, the `set_title` call and the
  `pcf_scale_table` branch. The commit before it,
  [`22bd0b6`](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/commit/22bd0b668e394c0d9bbcb664869f1e61dc4cbb49)
  (2026-06-29), "Remove commercial-only support link from
  high-availability topic", is not in the candidate list (its subject
  names no markup), so the content date with the candidates skipped is
  2026-06-29. Whether it changed the open-source page was not checked.
- **A partial that holds a presentation hint.** Its partial
  `_oss_scale_table` was last changed on 2025-05-29, "adjust column
  widths" ([`4ac2fb1`](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/commit/4ac2fb19a0a44534a8469de100af7dd91706e9b7)): a hint in this evaluation's terms
  ([principles](../../README.md#principles)), and not counted by
  Bookbinder because it is a partial.
- **The site's newest content date.** Of the four test pages this one has
  the newest content date, so it sets the site year (2026).

## What a conversion must show

| Mode | Copyright year | Last updated |
|---|---|---|
| published | 2026 | 2026-07-22 |
| build | the year of the build | 2026-06-29 |
| site | 2026 | 2026-06-29 |
| page | 2026 | 2026-06-29 |
| history | the year of the build | 2025-06-02: C3, written by the converter |

## Cleanup and deviations

- **Excerpt**, as stated above.
