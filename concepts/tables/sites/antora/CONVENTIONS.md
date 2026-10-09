# Antora conventions for tables

The patterns that worked in this round, per mode. Results and measurements:
[results.md](../../results.md#antora-321).

```bash
make build      # install, fetch the pinned UI, generate site-playbook.yml, build the site
make serve      # serve site/ at http://localhost:8002
make check      # build, then run the spot checks for each mode
                # (MODES="passthrough-raw passthrough extension native native-plain" for all)
make build-raw  # also builds the unchanged-HTML pages
```

## Every mode

- **Pages are AsciiDoc.** Antora reads AsciiDoc only, so the Markdown around
  the tables becomes AsciiDoc in every mode, passthrough included: headings,
  lists, code blocks, links, emphasis. Only the modes' tables differ.
- **One component per mode.** Each mode is a directory with an `antora.yml`
  (`name: passthrough`, `version: ~`) and `modules/ROOT/pages/`. The playbook
  reads them from this repository's worktree, so a page does not have to be
  committed to build.
- **Variables are AsciiDoc attributes.** `<%= vars.name %>` becomes `{name}`.
  [playbook.js](playbook.js) copies `source/template_variables.yml` into the
  playbook's `asciidoc.attributes` and writes `site-playbook.yml`. An
  undefined attribute renders as nothing only with `attribute-missing: drop`
  ([antora-playbook.yml](antora-playbook.yml)); by default the page shows
  `{metadata_ref}` as text. An HTML-valued attribute renders as markup.
- **Partials.** The partial lives in `modules/ROOT/partials/`; the host page
  includes it with `include::partial$_oss_scale_table.adoc[]`, and its
  attributes render.
- **Images.** `modules/ROOT/images/` holds a symbolic link to the file in
  `source/images/`; the page writes `image:request_lifecycle.png["…"]`. Alt
  text with a comma needs quotes: unquoted, the commas start the width and
  height attributes.
- **Heading anchors.** `## <a id="x"></a> Title` becomes `[[x]]` on the line
  above `== Title`. Without it Asciidoctor generates `_title`, and links to
  `#x` go nowhere. An anchor the source writes as `id="#x"` cannot be an
  AsciiDoc id; it stays HTML (`+++<a id="#x"></a>+++`), broken as on the
  published page.
- **HTML blocks** outside tables (`<pre class="terminal">`, `<ul>` lists,
  `<br><br>`) stay HTML inside a passthrough block (`++++`). A block that
  holds a variable needs `[subs=attributes+]` on the line above.
- **A list step that holds a nested list and then more blocks** wraps its
  content in an open block (`+` then `--` … `--`): AsciiDoc otherwise attaches
  the blocks after the nested list to its last bullet.

## Passthrough

Each HTML table stays as it is, inside a passthrough block:

```asciidoc
[subs=attributes+]
++++
<table class="table">
  …
  <td>The request from the load balancer did not reach {app_runtime_abbr}.</td>
  …
</table>
++++
```

The block is not parsed, so the browser gets the HTML exactly as written and
repairs it as on the published page. Only the intent files' cleanup applies.
`[subs=attributes+]` is the one addition, and only on tables with a
variable; without it `{app_runtime_abbr}` shows as text.

The default UI styles only AsciiDoc tables (`table.tableblock`). An HTML
table with `class="table"` gets the same look from
[supplemental-ui/css/hints.css](supplemental-ui/css/hints.css), so the class
is a hook the template can format. Every HTML table names its style with a
class; a table without one gets `class="table"`.

## Native

AsciiDoc's own table, with the specs AsciiDoc defines:

```asciidoc
[%header,cols=".<20%h,.<~"]
|===
|Type |Description

|`value`
|A single string value for arbitrary configurations …
|===
```

| Spec | Meaning | Hint |
|------|---------|------|
| `20%` in `cols` | column width | column width |
| `~` in `cols` | width from the content | (no width) |
| `h` in `cols` | the column's cells are header cells (`th`) | row-header column |
| `.<` in `cols` | top alignment | top alignment |
| `%header` | the first row is the header row | header row |
| `4+^\|Title` | a cell spanning four columns, centered | (title row) |
| `a\|` | an AsciiDoc cell: lists and paragraphs | block content |

A cell's lists and paragraphs are written as AsciiDoc inside an `a|` cell, so
the `<br/><br/>` in `uaa-concepts` is a paragraph break. Code spans that hold
`_`, `...`, quotes, or similar are written as literal monospace
(`` `+approvals_deleted+` ``): plain backticks would turn `...` into `…`.
AsciiDoc has one header row, so the `metadata` title is a bold line above the
table (`*Label requirements*`). The capped no-wrap and the column roles
cannot be carried.

Asciidoctor writes the alignment specs as classes (`halign-left`,
`valign-top`), and the default UI has a rule for each, so native tables need
no stylesheet for alignment. `hints.css` turns off the UI's hyphenation in
tables.

`native-plain` is the same tables with no `cols` at all. AsciiDoc then gives
every column the same width, where a Markdown pipe table sizes columns by
their content.

## Extension

No custom code: the hints are roles on the native table, and
[supplemental-ui/css/hints.css](supplemental-ui/css/hints.css) gives them
their meaning.

```asciidoc
[.hinted.col1-key.col2-prose.col3-prose.col1-nowrap%header,cols=".<30%h,.<~,.<~"]
|===
|Grant type |User |Details

|`+authorization_code+`
|Developers building web apps
|In the authorization code grant flow, …
|===
```

| Role | Meaning | Hint |
|------|---------|------|
| `hinted` | the table carries hints | — |
| `colN-key`, `colN-value`, `colN-prose` | the role of column N | column role |
| `colN-nowrap` | column N avoids wrapping (`key` columns unless `wrap: normal`) | column wrap |

Widths, header row, row headers, top alignment and block content use the
native specs above. In a `colN-nowrap` column, each body cell's paragraph or
content box keeps its text on one line up to `--table-nowrap-max` (default
`16em`) and wraps between words past it. Row headers take
`--table-row-header-weight` and `--table-row-header-align`. Every table takes
`--table-font-size` and `--table-line-height`; their defaults keep the UI's
table text (0.83 rem, smaller than the body text).

The default UI's stylesheet is built with its variables resolved, so it
exposes no variables a site can set; `hints.css` sets the look with plain
rules. The UI spaces blocks with top margins only, so cells have no extra gap
below their last paragraph or list.

## Adding a style

A style is a class name and a few rules in
[supplemental-ui/css/hints.css](supplemental-ui/css/hints.css). The example
is `table-media`, the image grid on the `uaa-performance` page.

- **Passthrough** names the style as the HTML table's class:
  `<table class="table-media">`. Its rules replace the standard look, so
  they set the borders, padding and alignment themselves.
- **Extension** names it as a role on the AsciiDoc table:
  `[.table-media%header%autowidth]`. Asciidoctor adds the role to the
  table's classes (`tableblock frame-all grid-all fit-content table-media`).
  The style's rules come after the UI's frame and grid rules and are as
  specific, so they win. `%autowidth` leaves out the equal column widths
  Asciidoctor writes by default; the style sets the table to full width and
  lets the images share it.
- **Native** has no class: a table without a role gets the standard look.
  Naming a style is what the extension adds.

The images link to themselves with `link=self` in the image macro
(`image:client-creds-threads-1.png["Threads Level 1",link=self]`). Antora
publishes module images to `_images/`, so a passthrough page links them as
`../_images/<file>`.
