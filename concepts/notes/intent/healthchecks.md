# Intent: `healthchecks`

- Source: [`../source/healthchecks.html.md.erb`](../source/healthchecks.html.md.erb)
  (cloudfoundry/docs-dev-guide, whole page)
- Published: <https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html>
  (copy: [`../published/healthchecks.html`](../published/healthchecks.html))
- Notes file (what the check compares): [`healthchecks.notes`](healthchecks.notes)

## Cases this page covers

- **The Important kind**, the second most common (89 `<p class="note
  important">` in the book), four times.
- **A note in a table cell:** the third note sits in the last cell of the
  `http` row of an HTML table, after a `<br>`. 5 of the book's notes sit in
  table cells, 4 of them on one page
  ([survey](../survey/README.md#the-books-notes)).
- **A variable in a note:** the fourth note holds
  `<%= vars.company_name %>`. 18 of the book's notes hold a variable.
- **Code in a note**, the most common content (125 notes): `<code>` in
  three of the four.

## Notes to keep

| # | Kind | Title | Sits in | Holds | Source |
|---|------|-------|---------|-------|--------|
| 1 | important | Important | "Configure liveness health checks when creating or updating an app" (`h2`), last block | 1 paragraph, 1 code span | [L71-L75](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/healthchecks.html.md.erb#L71-L75) |
| 2 | important | Important | "Configure liveness health checks for an existing app" (`h2`), last block | 1 paragraph, 1 code span | [L99-L104](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/healthchecks.html.md.erb#L99-L104) |
| 3 | important | Important | "Health check types" (`h3`), in the table's `http` row, third cell, after the cell's text | 1 paragraph | [L146-L151](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/healthchecks.html.md.erb#L146-L151) |
| 4 | important | Important | "Health check HTTP endpoints" (`h3`), last block of the page | 1 paragraph, a variable, 1 code span | [L186-L189](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/healthchecks.html.md.erb#L186-L189) |

## What a conversion must keep

- **Kind and title**, as for every note: the reader sees "Important".
- **The note in the cell stays in the cell**, after the cell's own text.
  The notes check reads its place as `table`.
- **The variable's value** ("Cloud Foundry") in the note's text.

## Cleanup and deviations

- **The table's stray row.** The table opens its first body row twice
  (`<tr>` on lines 136 and 137). Browsers repair it. Docusaurus needs it
  removed, as the tables round found for other markup; native Zensical
  needs it removed for the note in the cell to be read as Markdown
  ([results](../results.md#notes-in-a-table-cell)). Decision (this round):
  removed wherever a mode needs it.
- **The `<br>` before the cell's note** becomes a paragraph break in native
  modes: the note is a block of its own after the cell's text. The words
  do not change.
- **No deviation** from the published text.
