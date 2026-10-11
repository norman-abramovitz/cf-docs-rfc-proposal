# Intent: `using-vol-services`

- Source: [`../source/using-vol-services.html.md.erb`](../source/using-vol-services.html.md.erb)
  (the host page) and [`../source/_using-vol-services.html.md.erb`](../source/_using-vol-services.html.md.erb)
  (the partial that holds its content), cloudfoundry/docs-dev-guide
- Excerpt: the partial's lines 1–8 and 225–279, under the host's front
  matter ([SOURCES](../source/SOURCES.md#notes))
- Published: <https://docs.cloudfoundry.org/devguide/services/using-vol-services.html>
  (copy: [`../published/using-vol-services.html`](../published/using-vol-services.html))
- Notes file (what the check compares): [`using-vol-services.notes`](using-vol-services.notes)

## Cases this page covers

- **A note held in a variable.** Line 5 is `<%= vars.external_vol_win_note %>`,
  whose value in the book's variables is a whole note:
  `<p class="note"><span class="note__title"><strong>Note</strong></span> NFS and SMB volume services are available for Linux cells only. …</p>`
  ([`template_variables.yml` L176](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L176)).
  [R-07](../../../requirements/README.md#r-07) notes and admonitions names
  this case. 12 values in the book hold a note; 7 are used by pages
  ([survey](../survey/README.md#the-books-notes)).
- **Notes in a list.** In step 1 of "Create an NFS volume service" one note
  sits inside an HTML `<li>` of the step's "Where:" list, and the next sits
  in the step itself, after that list. 41 of the book's notes are in lists.
- **Markdown inside an HTML note.** The second note in the step writes a
  code span with backticks (`` `vers=3.0` ``) between `<code>` elements. The
  published page renders it as code, because inside a list item the note is
  part of a paragraph whose text is read as Markdown (published copy, line
  786). Two notes in the book do this.
- **Line breaks and `>` in a note:** two `<br>` and `<code>>= v7.1.48</code>`.
- **The partial** holds the notes; the page that publishes them only
  includes it. 10 of the book's notes are in partials.

## Notes to keep

| # | Kind | Title | Sits in | Holds | Source |
|---|------|-------|---------|-------|--------|
| 1 | note | Note | the introduction, before the first `h2` | 1 sentence pair; the whole note is the variable's value | [`_using-vol-services` L5](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/_using-vol-services.html.md.erb#L5) |
| 2 | note | Note | "Create and use NFS volume services" (`h2`), last block | 1 sentence | [L237-L240](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/_using-vol-services.html.md.erb#L237-L240) |
| 3 | important | Important | "Create an NFS volume service" (`h3`), step 1, inside the second item of the "Where:" list | 1 sentence, 1 code span | [L257-L260](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/_using-vol-services.html.md.erb#L257-L260) |
| 4 | important | Important | the same step, after the "Where:" list | 3 lines joined by `<br>`, 3 code spans (one written in Markdown) | [L266-L271](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/_using-vol-services.html.md.erb#L266-L271) |

The notes check reads the place of notes 3 and 4 as `list`.

## What a conversion must keep

- **The note held in the variable is a note on the page,** with its kind,
  title and text, wherever the variable is used.
- **Notes 3 and 4 stay inside step 1**, note 3 inside its list item.
- **All three code spans of note 4 are code**, the Markdown one included,
  and its `>=` survives.

## Cleanup and deviations

- **The "Where:" list in step 1.** Decision (this round): in native modes
  the HTML `<ul>` becomes a Markdown list (or the tool's own list), so that
  note 3, inside it, can be the tool's own admonition. The items and their
  words do not change. Passthrough keeps the HTML.
- **The variable becomes a partial in native modes.** Decision (this
  round): a note held in a variable is converted to a partial holding the
  tool's own admonition, and the page includes it where the variable was
  ([results](../results.md#a-note-held-in-a-variable)). Passthrough keeps
  the variable and renders its HTML value.
- **Excerpt.** The rest of the partial (its prerequisites, mounting, SMB
  and other NFS sections, and five more notes) is not converted.
- **No deviation** from the published text.
