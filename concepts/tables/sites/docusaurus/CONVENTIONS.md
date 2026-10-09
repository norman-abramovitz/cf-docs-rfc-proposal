# Docusaurus conventions for tables

The patterns that worked in this round, per mode. Results and measurements:
[results.md](../../results.md#docusaurus-3102).

```bash
make build      # install, generate vars.json, build the site
make serve      # serve build/ at http://localhost:3000
make check      # build, then run the spot checks for each mode
make check-raw  # first MDX error on each unchanged-HTML page
```

## Every mode

- **Pages are `.mdx`.** Variables need MDX expressions.
- **Variables.** `import vars from '@site/vars.json';` after the front matter,
  then `<%= vars.name %>` becomes `{vars.name}`. `vars.json` is generated from
  `source/template_variables.yml`. A variable that is not defined renders as
  nothing. An HTML-valued variable needs
  `<div dangerouslySetInnerHTML={{__html: vars.name}} />` to render as markup.
- **Partials.** A partial is a file whose name starts with `_` (no page of
  its own). The host imports it and uses it as a component:
  `import OssScaleTable from './_oss_scale_table.mdx';` … `<OssScaleTable />`.
  The partial imports `vars` itself.
- **Images.** Relative paths stay as written; `images/` links to
  `source/images/`.
- **Indentation matters.** A table that belongs to a list item is indented
  under it, with a blank line before it.
- **Braces in text** are expressions in MDX. Literal braces in prose or in
  `<pre>` are escaped: `\{OIDC provider alias\}`.

## Passthrough

The HTML stays, with the changes MDX and React need:

| Source | MDX |
|--------|-----|
| `<col width="25%">` | `<col width="25%" />` inside `<colgroup>` |
| `<br>` | `<br />` |
| `style="width:20%"` | `style={{width: '20%'}}` |
| rows directly in `<table>` | rows inside `<tbody>` |
| `<td>text` … newline … `</td>` on its own line | `</td>` at the end of the text line |

A missing `<tbody>` or `<colgroup>` builds without error but makes React
report a hydration error in the browser.

## Extension

A remark plugin, [plugins/list-table.js](plugins/list-table.js), turns a
`list-table` directive into an HTML table. Each row is a list item; each cell
is a list item inside it, so a cell can hold lists and paragraphs.

```markdown
:::list-table{widths="30 auto auto" header-rows="1" stub-columns="1" roles="key prose prose"}
- - Grant type
  - User
  - Details
- - `authorization_code`
  - Developers building web apps
  - In the authorization code grant flow, …
:::
```

| Option | Meaning | Hint |
|--------|---------|------|
| `widths` | percent per column, `auto` for none | column width |
| `header-rows` | number of header rows | header row |
| `stub-columns` | leading columns that are row headers | row-header column |
| `roles` | `key`, `value`, or `prose` per column | column role |
| `wrap` | `avoid` or `normal` per column; `key` defaults to `avoid` | column wrap |
| `caption` | caption text | caption |
| `title` | title text, shown as a header row spanning every column | title |

`widths`, `header-rows`, and `stub-columns` use MyST's `list-table` names.
[src/css/hints.css](src/css/hints.css) sets top alignment and no-wrap; the
rest of the look comes from the theme.

## Native

GFM pipe tables. In `.mdx`, a cell can hold an inline HTML list
(`<ul><li>…</li></ul>` on one line) and `<br /><br />`. No widths, alignment
other than left/center/right per column, row headers, captions, or spanning
rows. A title row becomes a bold line above the table. A pipe table needs a blank
line before it.
