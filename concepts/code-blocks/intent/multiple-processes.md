# Intent: `multiple-processes`

- Source: [`../source/multiple-processes.html.md.erb`](../source/multiple-processes.html.md.erb),
  cloudfoundry/docs-dev-guide
- Excerpt: the whole page
- Published: <https://docs.cloudfoundry.org/devguide/multiple-processes.html>
  (copy: [`../published/multiple-processes.html`](../published/multiple-processes.html))
- Code file: [`multiple-processes.code`](multiple-processes.code); notes
  file: [`multiple-processes.notes`](multiple-processes.notes); anchors:
  [`multiple-processes.anchors`](multiple-processes.anchors)

## Cases this page covers

- **A fence the published page shows as text**: the YAML fence in step 1
  is indented four spaces under a paragraph indented three
  ([L18-L31](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/multiple-processes.html.md.erb#L18-L31)),
  so Redcarpet reads an indented code block and shows ```` ```yaml ````
  and ```` ``` ```` in it.
- **A terminal block with blank lines and `&#35;`** in a list item, with a
  note after it in the same item
  ([L98-L124](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/multiple-processes.html.md.erb#L98-L124)).
- **A Procfile** in an unlabelled fence.

## What a conversion must keep

Seven code blocks: one `yaml`, four `bash`, two `text` in native mode;
the note in its list item; five headings, four ids.

## Cleanup and deviations

- **Block 1 is the YAML without the fence lines**, in the list item.
  Decision (this round): the CommonMark reading, which is what the author
  wrote; the published page fails here.
- **Block 7 is the source's whole block**, which the published page breaks
  into paragraphs after its first line.
- **The paragraph before block 1 is indented four spaces** in Zensical's
  native page: Python-Markdown needs four for a list item's continuation.
