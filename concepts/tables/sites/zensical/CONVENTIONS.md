# Zensical conventions for tables

The patterns that worked in this round, per mode. Results and measurements:
[results.md](../../results.md#zensical-0069).

```bash
make build  # install, generate vars.yml, build the site
make serve  # serve site/ at http://localhost:8001
make check  # build, then run the spot checks for each mode
            # (MODES="passthrough-raw passthrough extension native native-plain" for all)
```

## Every mode

- **Pages are `.md`.** The source pages build with their HTML unchanged.
- **Variables keep their ERB form.** `<%= vars.name %>` works as written: the
  built-in macros support ([zensical.toml](zensical.toml)) uses ERB
  delimiters and reads `vars.yml`, generated from
  `source/template_variables.yml` with its top key renamed to `vars`. A
  variable that is not defined renders as nothing (`on_undefined = "silent"`).
  An HTML-valued variable renders as markup, as on the published pages.
- **ERB tags shown as text break the page.** The macros support reads every
  `<%= … %>` and `<% … %>` on a page, including inside code. A tag that is not
  a valid template expression is an error; `on_error_fail = true` makes it fail
  the build instead of replacing the page with an error message.
- **Partials.** A partial lives in `partials/<mode>/`, outside `docs/`, so it
  never becomes a page. The host includes it with
  `<% include "<mode>/_oss_scale_table.md" %>`, and the partial's own
  variables render. A `--8<--` snippet include does not work for partials with
  variables: snippets are inserted after variables are rendered, so their ERB
  tags stay literal.
- **Images.** Relative paths stay as written. `images/` in each mode holds a
  symbolic link to the file in `source/images/`; a link to the whole
  directory is not copied into the site.
- **Indentation matters.** A table that belongs to a list item is indented
  under it.
- **The theme styles only tables without a `class`** (`table:not([class])`).
  A table that keeps `class="table"` gets no border and no header style
  from the theme: its header cells are not bold. The site's CSS gives
  `table.table` the theme's look (see Classes on tables below).
- **Table titles.** In extension and native a table's title is a bold line
  above the table (`**Label requirements**`); the column headers stay the
  header row. Passthrough keeps the source's spanning row. The extension's
  `title` option (a spanning row) still works but the pages no longer use it.

## Passthrough

The HTML stays, with only the cleanup the intent files list. Nothing else is
forced: Python-Markdown passes HTML blocks through as written.

| Source | Passthrough |
|--------|-------------|
| `<col width="25%">` | `<col width="25%" />` (intent cleanup; browsers accept either) |
| table in a list step, not indented | indented under the step |

An HTML table indented under a list item ends up inside a paragraph in the
output (`<p>…<table>…</table></p>`); browsers close the paragraph at the
table, so the page renders and keeps its outline.

## Extension

A Markdown extension, [list_table.py](list_table.py), adds a `list-table`
block through the blocks API of the bundled pymdown-extensions. Each row is a
list item; each cell is a list item inside it, so a cell can hold lists and
paragraphs. The table sits in a `div.hinted-table`, because the theme styles
only tables without a class.

```markdown
/// list-table
    widths: 30 auto auto
    header-rows: 1
    stub-columns: 1
    roles: key prose prose

-   - Grant type
    - User
    - Details

-   - `authorization_code`
    - Developers building web apps
    - In the authorization code grant flow, …
///
```

| Option | Meaning | Hint |
|--------|---------|------|
| `widths` | percent per column, `auto` for none | column width |
| `header-rows` | number of header rows | header row |
| `stub-columns` | leading columns that are row headers | row-header column |
| `roles` | `key`, `value`, or `prose` per column | column role |
| `wrap` | `avoid` or `normal` per column; `key` defaults to `avoid` | column wrap |
| `title` | title text, shown as a header row spanning every column | title |
| `style` | a style other than the standard one; becomes the table's class | style |

The options are the same as the Docusaurus plugin's. Python-Markdown's list
rules set the layout:

- **Four-space indents.** A cell list sits four spaces in (`-   - Key`,
  `    - Value`); a list or second paragraph inside a cell, eight.
- **A blank line between rows.** Without it, a row after a cell with two
  paragraphs folds into that cell's last paragraph.
- **An empty cell is `- <!-- -->`.** Python-Markdown has no empty list item:
  a bare `-` under a cell turns that cell into a heading and the row loses a
  cell, with no error.

[docs/stylesheets/hints.css](docs/stylesheets/hints.css) sets top alignment,
the capped no-wrap, row-header style, and the centered title row. A
`wrap: avoid` cell holds a box that keeps its text on one line up to
`--table-nowrap-max` (default `16em`) and wraps between words past it. Row
headers take `--table-row-header-weight` and `--table-row-header-align`. The
theme's header rule (`.md-typeset table:not([class]) th:not([align])`) is
more specific than a plain class selector, so the row-header and title rules
are written to outrank it; without that, the variables have no effect.

## Native

Pipe tables (the `tables` extension, not on by default). A cell can hold an
inline HTML list (`<ul><li>…</li></ul>` on one line) and `<br /><br />`. A
pipe table needs a blank line before it.

The attribute lists extension works on single cells, not on a whole table:

```markdown
| Type {: style="width:20%" } | Description |
| --- | --- |
```

so native carries the source widths on the header cells. `{: .class }` on the
line after a table is not attached to the table: it becomes an extra row with
that text. Row headers, the spanning title row, and the capped no-wrap cannot
be carried; the title is a bold line above the table. Classless pipe tables
get the theme's top alignment.

`native-plain` is the same pages without the attributes: pipe tables only,
columns sized by their content.

## Classes on tables

The theme styles only tables without a `class`. A table that keeps
`class="table"` gets the theme's look from rules in `hints.css` that repeat
the theme's table rules for `table.table`, so the class is a hook the
template can format. To see the theme's own default, drop the class. Every
HTML table names its style with a class; a table without one gets
`class="table"`.

## Adding a style

A style is a class name and the CSS that gives it its look.
`table-media`, used on `uaa-performance`, is the example: a grid of charts
with no cell borders, a rule under the header, and centered cells.

- **The CSS lives in [docs/stylesheets/hints.css](docs/stylesheets/hints.css).**
  The theme styles only tables without a class, so a styled table gets its
  whole look from these rules, not only the parts that differ. Theme
  variables (`--md-typeset-table-color`, `--md-default-fg-color--lighter`)
  keep its colors in step with the theme, dark mode included.
- **Passthrough** names the style as the table's class:
  `<table class="table-media">`.
- **Extension** names it with the `style` option of the `list-table` block;
  the option becomes the table's class:

  ```markdown
  /// list-table
      header-rows: 1
      style: table-media
  ```

- **Native cannot name a style.** A pipe table takes no class: the attribute
  lists extension works on single cells, and `{: .class }` after a table
  becomes an extra row. A native table gets the standard style.
