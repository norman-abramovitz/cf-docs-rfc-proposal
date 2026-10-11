# Intent: `cf-backup`

- Source: [`../source/cf-backup.html.md.erb`](../source/cf-backup.html.md.erb)
  (cloudfoundry/docs-bbr, whole page)
- Published: <https://docs.cloudfoundry.org/bbr/cf-backup.html>
  (copy: [`../published/cf-backup.html`](../published/cf-backup.html))
- Notes file (what the check compares): [`cf-backup.notes`](cf-backup.notes)

## Cases this page covers

- **A note that holds a list:** a `<div class="note caution">` with a
  `<ul>` of four items, each opening with a bold sentence. Lists in notes
  are always HTML and always in a `<div>` in the book
  ([survey](../survey/README.md#the-books-notes)).
- **The Caution kind**, twice, and a plain Note.
- **Two notes that are never closed** (lines 66 and 109): `<p class="note">`
  with no `</p>`. 4 of the book's 241 HTML notes are written this way, two of
  them here.
- **A note before the first heading**, in the page's introduction.

## Notes to keep

| # | Kind | Title | Sits in | Holds | Source |
|---|------|-------|---------|-------|--------|
| 1 | caution | Caution | the introduction, before "Supported Cloud Foundry configurations" (`h2`) | a list of 4 items: bold lead-ins, 2 code spans, 1 link | [L16-L29](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/cf-backup.html.md.erb#L16-L29) |
| 2 | caution | Caution | "Selective backup and restore configurations for blobstores" (`h3`), after its table and before the `h4` | 1 paragraph, 1 link to a heading on the page (`#selective-backup-restore-steps`) | [L66-L71](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/cf-backup.html.md.erb#L66-L71) |
| 3 | note | Note | "Applying ops files in the correct order" (`h3`), after the last list, before "Next steps" (`h2`) | 1 paragraph, 2 code spans | [L109-L111](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/cf-backup.html.md.erb#L109-L111) |

"Sits in" is the heading of the section the note belongs to, as the notes
check reads it: the nearest heading above the note, or the page title for
a note before the first heading.

## What a conversion must keep

- **Kind and title.** Each note stays a note of its kind, and the reader
  still sees "Caution" or "Note". The kind may become the tool's own
  admonition type, chosen by a site-wide map (see
  [results](../results.md#how-each-tool-maps-the-kinds)).
- **Contents.** The words in order, the list items as list items, code
  spans as code, the link and its target.
- **Place.** Each note stays in its section, between the same blocks.

## Cleanup and deviations

- **Close the two open notes.** Decision (this round): a conversion adds
  `</p>` at the end of each note's paragraph, where the published page ends
  it (the book's Markdown processor wraps the note in a paragraph, and the
  browser ends it at the next heading:
  `<p><p class="note caution">` … `section below.</p>`, published copy line
  603). This is the cleanup of [R-24](../../../requirements/README.md#r-24)
  markup cleanup before conversion; the text does not change. As written,
  the open notes break one tool and stop two others
  ([results](../results.md#notes-never-closed)).
- **No deviation** from the published text.
