# Starlight conventions for tables

The patterns that worked in this round, per mode. Results and measurements:
[results.md](../../results.md#starlight-0426).

```bash
make build      # install, generate vars.json, build the site
make serve      # serve dist/ at http://localhost:4321
make check      # build, then run the spot checks for each mode
                # (MODES="passthrough-raw passthrough extension native native-plain" for all)
make check-raw  # Markdoc errors on each unchanged-HTML page
```

## Every mode

- **Pages are Markdoc (`.mdoc`).** The Markdoc integration runs with
  `allowHTML`, so HTML in a page is kept
  ([astro.config.mjs](astro.config.mjs)).
- **Variables.** `<%= vars.name %>` becomes `{% $vars.name %}`.
  [markdoc.config.mjs](markdoc.config.mjs) passes `vars.json`, generated from
  `source/template_variables.yml`, to every page as `$vars`. A variable that
  is not defined renders as nothing. An HTML-valued variable renders as
  escaped text; `{% rawhtml value=$vars.name /%}` renders it as markup
  through a two-line component ([src/components/RawHtml.astro](src/components/RawHtml.astro)).
- **Partials.** A partial is a file whose name starts with `_` (no page of
  its own). The host includes it with
  `{% partial file="./_oss_scale_table.mdoc" /%}`, and the partial's
  variables render. Markdoc wraps the partial in its own `<article>`.
- **Images.** Relative paths stay as written; `images/` in each mode holds a
  symbolic link to the file in `source/images/`.
- **Indentation matters.** A table that belongs to a list item is indented
  under it.
- **The theme styles every table**, whatever its class, and its styles sit in
  cascade layers: any rule in the site's own CSS wins without extra
  specificity. `class="table"` changes nothing; a template can still use it
  as a hook.

## Passthrough

The HTML stays, with the cleanup the intent files list and what Markdoc
forces. Markdoc reads the text between HTML tags as Markdown, which causes
three of the changes:

| Source | Passthrough | Why |
|--------|-------------|-----|
| `<li><code>-</code></li>` | `<li><code>&#45;</code></li>` | a lone `-` is read as a list item; the code span holds an empty list |
| a table cell over several lines | the cell on one line | the space next to an inline tag is dropped (`password</code>refers`) |
| a variable followed by a space and a tag | `{% $vars.x %} … generated&#32;<code>` | the same dropped space |
| a blank line inside `<pre>` inside a list item | the line break written `&#10;` | the block does not parse |

The text between tags is still Markdown, so `*`, `_`, and `\` inside HTML
cells act as Markdown (the `\[` escapes in `metadata` disappear without any
change). Joining cell lines changes nothing on screen: HTML collapses the
whitespace anyway.

## Extension

The hints are attributes on Markdoc's own `{% table %}` tag.
[list-table.mjs](list-table.mjs) declares them on Markdoc's table node and
turns them into a `colgroup`, row headers, a title row, and classes; a table
without them renders as Markdoc renders it.

```markdown
{% table widths="30 auto auto" header-rows=1 stub-columns=1 roles="key prose prose" %}
* Grant type
* User
* Details
---
* `authorization_code`
* Developers building web apps
* In the authorization code grant flow, …
{% /table %}
```

| Option | Meaning | Hint |
|--------|---------|------|
| `widths` | percent per column, `auto` for none | column width |
| `header-rows` | number of header rows | header row |
| `stub-columns` | leading columns that are row headers | row-header column |
| `roles` | `key`, `value`, or `prose` per column | column role |
| `wrap` | `avoid` or `normal` per column; `key` defaults to `avoid` | column wrap |
| `title` | title text, shown as a header row spanning every column | title |

The options are the same as the Docusaurus and Zensical extensions'. Rows are
separated by `---`; each cell is a `*` item, so a cell can hold a list or
several paragraphs (indent them two spaces under the `*`). Markdoc's own
table syntax is unchanged; the extension only adds attributes.

[src/styles/hints.css](src/styles/hints.css) gives the classes their meaning:
top alignment, the capped no-wrap (`--table-nowrap-max`, default `16em`),
row-header style (`--table-row-header-weight`, `--table-row-header-align`),
the centered title row, and `--table-font-size` and `--table-line-height` for
every table (defaults: the body text). It also keeps list items in tables from
breaking inside words, which the theme allows everywhere else.

Starlight has no table variables of its own. Its table rules use fixed
padding (`0.5rem 1rem`) and its color variables (`--sl-color-gray-5` for
borders, `--sl-color-white` for header text); its text variables
(`--sl-text-body`, `--sl-line-height`, `--sl-font`) apply to the whole page.

## Native

Markdoc's own table tag, with only the attributes Markdoc defines: `width`
on header cells, `colspan` and `align` on any cell, and `class` and `id` on
anything.

```markdown
{% table %}
* Type {% width="20%" %}
* Description
---
* `value`
* A single string value …
{% /table %}
```

Cells hold lists and paragraphs without inline HTML. Markdoc puts only the
first row in the table head, so a spanning title row takes the head and the
column headers become an ordinary row (written bold). Row headers, top
alignment, and the capped no-wrap cannot be carried; a class on each cell
would carry a role, but only cell by cell.

`native-plain` is the same pages as pipe tables: lists in cells as inline
HTML (`<ul><li>…</li></ul>` on one line), `<br /><br />` for the paragraph
break, the title as a bold line above the table, and no widths.
