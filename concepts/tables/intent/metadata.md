# Intent: `metadata`

- Source: [`../source/metadata.html.md.erb`](../source/metadata.html.md.erb)
- Published: <https://docs.cloudfoundry.org/adminguide/metadata.html>

The page has two HTML tables with the same shape (labels, annotations) and
one Markdown pipe table. The author used HTML only where the table needed it.

## Table 1 — Label requirements

Source: lines 56–115. Three rows: key prefix, key name, value.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | title | "Label requirements" | first row: one `<th colspan="4" style="text-align: center">` |
| Table | header row | yes | second row of `<th>` cells (outside `<thead>`) |
| Table | row-header column | yes | column 1 names the part of the label |
| Column 1 | role | key | "Part of Label" |
| Column 2 | role | value | lengths such as `0-253` |
| Column 2 | wrap | avoid | `0-253` must not break at the hyphen |
| Column 3 | role | prose | "Allowed characters" |
| Column 4 | role | prose | "Other Requirements" |
| Cell | block content | lists | column 3 in every row; column 4 in rows 1 and 3 |

No widths in the source; the role defaults apply.

**Cleanup needed:** in row 1, the column 3 `<td>` is never closed: line 77
opens the next `<td>` directly after `</ul>`. Browsers close the open cell
when they see a new `<td>`, so the published page is correct; strict parsers
fail or nest the cell. The column headers sit in a plain `<tr>` after
`</thead>`; they move into `<thead>`. `Alphanumeric ( \[a-z0-9A-Z\] )`
(lines 73 and 89): the backslashes are Markdown escapes, but Markdown is not
processed inside this HTML, so the published page shows them. They are
removed: `Alphanumeric ( [a-z0-9A-Z] )`.

**Deviations:** none. The spanning, centered first row is a title for the
table, not a column header, and stays a row spanning every column.
**Decided** after comparing renderings: a spanning row, not a caption.
**Changed after the Starlight round:** Markdown tables have one header row,
so in every converted mode of every tool the title is a bold line above the
table and the column headers stay the header row. Passthrough keeps the
source's spanning row.
Native pipe tables cannot span columns, so native shows the title as a bold
line above the table.

### Spot checks

- [ ] Title "Label requirements" shown above the column headers: a bold
      line above the table (a spanning row in passthrough).
- [ ] 3 body rows, each with 4 cells; in row 1, the "DNS subdomain format"
      list is in column 4, not nested inside column 3.
- [ ] Column 3 lists have 3, 4, and 4 items; column 4 lists have 2 and 2
      items; row 2 column 4 is a plain sentence.
- [ ] One-character code spans `-`, `.`, `_`, `/` render as visible code.
- [ ] `Alphanumeric ( [a-z0-9A-Z] )` with no backslashes.

## Table 2 — Annotation requirements

Source: lines 121–168. Same shape as Table 1, same hints.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | title | "Annotation Requirements" | first row, as in Table 1 |
| Table | header row | yes | second row of `<th>` cells |
| Table | row-header column | yes | column 1 |
| Column 1 | role | key | "Part of Annotation" |
| Column 2 | role | value | `0-253`, `1-63`, `0-5000` |
| Column 2 | wrap | avoid | |
| Column 3 | role | prose | |
| Column 4 | role | prose | |
| Cell | block content | lists | column 3 in rows 1 and 2; column 4 in row 1 |

**Cleanup needed:** the same unclosed `<td>` as Table 1, at line 142 in row 1.
Column headers move into `<thead>`. Backslashes removed from the bracket text
at lines 138 and 154, as in Table 1.

**Deviations:** the title is a bold line above the table, as in Table 1.

### Spot checks

- [ ] Title "Annotation Requirements" shown above the column headers.
- [ ] 3 body rows, each with 4 cells; row 3 is plain text in every cell
      ("Any unicode character", "n/a").
- [ ] Row 1 "DNS subdomain format" list is in column 4.

## Table 3 — Selector requirement reference (Markdown)

Source: lines 370–377. A Markdown pipe table; the baseline for "native" mode.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | header row | yes | pipe table header |
| Column 1 | role | key | requirement names |
| Column 2 | role | value | `KEY==VALUE` and similar, in code |
| Column 2 | wrap | avoid | code must not break inside `KEY in (VALUE1,VALUE2...)` if avoidable |
| Column 3 | role | prose | |

**Cleanup needed:** none.

**Deviations:** none. Every tool keeps this as its native table syntax.

### Spot checks

- [ ] 6 body rows, each with 3 cells.
- [ ] `!KEY`, `KEY==VALUE`, `KEY!=VALUE` render as code with all characters.

## Page-level checks

- [ ] `<%= vars.metadata_ref %>` (line 22) renders as nothing: no error, no
      `undefined`, no literal tag.
- [ ] `vars.app_runtime_abbr` renders as "Cloud Foundry" in the prose.
