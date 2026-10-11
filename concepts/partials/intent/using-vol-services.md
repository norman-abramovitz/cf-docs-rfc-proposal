# Intent: `using-vol-services`

- Source: [`../../notes/source/using-vol-services.html.md.erb`](../../notes/source/using-vol-services.html.md.erb)
  (the page) and [`../../notes/source/_using-vol-services.html.md.erb`](../../notes/source/_using-vol-services.html.md.erb)
  (its partial), cloudfoundry/docs-dev-guide, copied in the notes round
- Excerpt: the notes round's, the partial's lines 1–8 and 225–279
  ([notes SOURCES](../../notes/source/SOURCES.md#notes)); here the page
  stays a page that only includes the partial, as the source is
- Published: <https://docs.cloudfoundry.org/devguide/services/using-vol-services.html>
  (the notes round's copy: [`../../notes/published/using-vol-services.html`](../../notes/published/using-vol-services.html))
- Partials file: [`using-vol-services.partials`](using-vol-services.partials);
  notes file: the notes round's [`using-vol-services.notes`](../../notes/intent/using-vol-services.notes);
  anchors: [`using-vol-services.anchors`](using-vol-services.anchors)

## Cases this page covers

- **A page that is only a partial call**: front matter and
  `<%= partial 'using-vol-services' %>`
  ([L6](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/using-vol-services.html.md.erb#L6)),
  the only such page in the book.
- **Headings inside a partial**, with explicit ids (`nfs`, `create-nfs` in
  the excerpt; 17 in the whole partial), and whether they reach the table
  of contents.
- **A nested partial** in native modes: the note held in the variable
  `external_vol_win_note` is a partial of its own (the notes round's
  accepted convention), included from inside `_using-vol-services`. The
  book has no nested partial; this is the one case where conversion makes
  one.
- **Notes in a list** inside the partial (the notes round's cases).

## What a conversion must keep

| Partial | Section | Place | Opens with | Ends with |
|---|---|---|---|---|
| `_using-vol-services` | the page title | body, ending in a list step | "Here are instructions to help you read and write" | "cf services" |
| `external_vol_win_note` (variable; partial in native) | the page title | body | "NFS and SMB volume services are available for Linux cells only." | "These services are not available for Windows cells." |

- **The partial's headings are in the table of contents** with the source's
  ids: `#nfs` and `#create-nfs` (the partials file's `toc` line).
- **The four notes** with kind, title, text and place (the notes file).

## Cleanup and deviations

- **The published page has no table of contents.** The book's quick links
  read only the page's own file, which holds no heading
  ([survey](../survey/README.md#how-the-book-resolves-a-partial)); the
  published page fails the `toc` line. Decision (this round): the intent
  is the headings in the table of contents, as on every other page.
