# Intent: `gsg-grails`

- Source: [`../source/gsg-grails.html.md.erb`](../source/gsg-grails.html.md.erb),
  cloudfoundry/docs-buildpacks
- Excerpt: Step 5, Create and bind a service instance
  ([L109-L186](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L109-L186))
- Published: <https://docs.cloudfoundry.org/buildpacks/java/getting-started-deploying-apps/gsg-grails.html>
  (copy: [`../published/gsg-grails.html`](../published/gsg-grails.html))
- Code file: [`gsg-grails.code`](gsg-grails.code); notes file:
  [`gsg-grails.notes`](gsg-grails.notes); anchors:
  [`gsg-grails.anchors`](gsg-grails.anchors) (none: the excerpt's headings
  have no explicit id)

## Cases this page covers

- **A `<pre>` inside a note**, the notes round's open item
  ([L154-L163](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L154-L163)).
- **`console` fences without a prompt** in list items (two).
- **A terminal block with blank lines in a list item**, indented four
  spaces with its list item
  ([L130-L140](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L130-L140)).
- **A terminal block that is a YAML file starting `---`**
  ([L179-L185](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L179-L185)).
- **E-mail addresses in code**, which the published HTML hides.

## What a conversion must keep

Five code blocks: two `bash`, two `console`, one `yaml` in native mode;
the block in the note stays in the note. One note, four headings.

## Cleanup and deviations

- **`console` fences without a prompt become `bash`** (proposed
  convention 3).
- **The terminal block that holds a manifest becomes `yaml`.**
- **The text of a `<pre>` in a list item is taken without the item's
  indentation**, as the published page shows it.
- **The note's address is the source's.** The published note holds a link
  reading "[email protected]"; the notes file writes the address, and the
  note holds no link.
- **Empty variables are removed** (`dev_console_1`, `dev_console_5`), as
  the variables round's convention 4 says.
