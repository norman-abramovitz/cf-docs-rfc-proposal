# Tables round — results

What each tool did with the five test pages. One section per tool, newest
last. Each starts with a short summary, then the grid, then what the
measurements and screenshots show. How the pages were chosen and what the
hints mean: [README](README.md). Per-table intent and spot checks:
[intent/](intent/).

How to read the grid:

- **Builds:** whether the page builds in that mode, and what had to change.
- **Content and outline:** the result of the spot checks in the intent file
  for that page, plus a check that headings, lists, and tables nest as on the
  published page.
- **Hints honored:** measured in a browser at a 1280-pixel window (the content
  column is 703 pixels wide).
- **Source readability:** a short judgment from an author's point of view.

## Docusaurus 3.10.2

Site: [sites/docusaurus/](sites/docusaurus/) — conventions:
[CONVENTIONS.md](sites/docusaurus/CONVENTIONS.md).

### Summary

- **The HTML does not build unchanged.** All five pages fail MDX compilation
  as they are. Three of the five first errors are outside the tables (literal
  `{…}` placeholders in prose, an unclosed `<br>`), so table cleanup alone is
  not enough to migrate a page to MDX.
- **With cleanup, every table renders correctly in all three modes.** 34 of
  36 spot checks pass in passthrough and extension; the two that fail are the
  page descriptions (finding 7). Native passes 33: it also cannot draw the
  `metadata` title as a spanning row. `make check` in the site reruns them with
  [checks/spot-checks.sh](checks/spot-checks.sh).
- **Cleanup the tables needed:** close void elements (`<col />`, `<br />`),
  fix the malformed markup the intent files list, write `style` as a JSX
  object, wrap rows in `<tbody>` and columns in `<colgroup>`, and keep a
  cell's closing tag off the start of a line. The last three only show up as
  browser errors or broken builds, not in the HTML source.
- **Variables work in MDX after one import per page.** An undefined variable
  renders empty, as on the published pages. An HTML-valued variable renders
  as escaped text unless the author uses `dangerouslySetInnerHTML`.
- **Docusaurus has no native table hints.** Widths, top alignment, row
  headers, and captions need either HTML (passthrough) or a plugin
  (extension); the extension here is a remark plugin.
  [#1642 §5](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L98-L104)
  says: "Working Groups MUST NOT need custom extensions, plugins, or
  JavaScript code to author documentation" (line 100), and "The PoC MUST
  validate that the most complex existing pages (HTML tables, CSS layouts)
  can be represented with MDX alone. Any gap found MUST be reported as a PoC
  finding" (line 104). Extension mode shows what a single extension,
  maintained once for all documentation, closes.
- **Findings outside tables** (recorded here because they block a page, to be
  worked in their own concepts): heading anchors written as
  `<a id="…"></a>` break the page's table of contents (React hydration error
  on every page that has them) and the build's anchor check; the page
  description that search engines and link previews show contains raw
  variable expressions (`{vars.appruntimeabbr}`) when the first paragraph has
  a variable.

### Grid

| Page | Mode | Builds | Content and outline | Hints honored | Source readability |
|------|------|--------|---------------------|---------------|--------------------|
| `_oss_scale_table` | passthrough | after cleanup: `<col />`, `<colgroup>` | preserved | widths 25/25/50 exactly | HTML as before |
| | extension | yes | preserved | key column does not wrap; widths 30/24/46 because "Cloud Controller Worker" does not fit in 25% without wrapping | Markdown list-table; long cells on one line |
| | native | yes | preserved | none (widths 18/15/67 by content) | pipe table, very long rows |
| `credential-types` | passthrough | after cleanup: straight quotes (class dropped), `style` object, `<tbody>` | preserved | width 20% | HTML |
| | extension | yes | preserved | width 20%, row headers, no wrap | list-table |
| | native | yes | preserved | none (18/82) | pipe table, readable |
| `metadata` | passthrough | after cleanup: two unclosed `<td>`, headers moved into `<thead>`, `style` objects, plus braces in a `<pre>` block and one `<br>` outside the tables | preserved; stray backslashes removed (decided fix) | spanning title row centered | HTML |
| | extension | yes | preserved | title row spanning all columns, row headers, no wrap on key column (26%) | list-table with nested lists: readable |
| | native | yes, lists as inline HTML in cells | preserved; title is a bold line above the table, not part of it | none; cells vertically centered | pipe table with inline `<ul>`: hard to edit |
| `troubleshooting_slow_requests` | passthrough | after cleanup: `<tbody>`, one multi-line cell, plus `<br />` outside the tables | preserved after nesting the Experiment 2 table in its list step | variant A, as written | HTML |
| | extension | yes | preserved | variant C (decided): no widths, columns sized by content | list-table |
| | native | yes | preserved after adding a blank line before each table | none (same as variant C) | pipe table |
| `uaa-concepts` | passthrough | after cleanup: `</td>` → `</tr>`, plus `{…}` placeholders escaped in prose | preserved | widths 30% and 25% | HTML |
| | extension | yes | preserved; `<br/><br/>` became two paragraphs (decided) | widths, row headers, no wrap | list-table; paragraphs as in Markdown |
| | native | yes | preserved, `<br /><br />` kept | none (27/30/43, 25/74) | pipe table |

### Width variants for `troubleshooting_slow_requests`

Column widths in percent of the table, per table (Experiment 1–6). Table 2
sits inside a numbered list, so it is narrower (671 pixels).

| Variant | T1 | T2 | T3 | T4 | T5 | T6 |
|---------|----|----|----|----|----|----|
| A — as written (passthrough) | 33/25/42 | 25/36/39 | 25/31/44 | 25/23/52 | 25/25/50 | 25/25/50 |
| B — uniform 25/25/50 (extension) | 25/25/50 | 25/25/50 | 25/25/50 | 25/25/50 | 25/25/50 | 25/25/50 |
| C — roles only (extension; native is the same) | 33/25/42 | 28/35/37 | 19/33/48 | 17/24/59 | 20/23/57 | 17/25/58 |

**Decided:** variant C. The extension page now uses it; variant B was
measured on an earlier version of that page.

Table 2 in each variant: [A](results/docusaurus-troubleshooting-t2-A-as-written.png),
[B](results/docusaurus-troubleshooting-t2-B-uniform.png),
[C](results/docusaurus-troubleshooting-t2-C-roles-only.png).

### Provisional changes, side by side

Both were decided after this comparison: the `metadata` title stays a
spanning row (the extension draws it with a `title` option), and the
`uaa-concepts` break is a paragraph break, so the extension keeps two
paragraphs.

- `metadata` title row: [spanning row](results/docusaurus-metadata-t1-passthrough-spanning-row.png),
  [caption](results/docusaurus-metadata-t1-extension-caption.png),
  [bold line above the table](results/docusaurus-metadata-t1-native-bold-title-line.png)
  (native; it reads like the level-4 heading that follows it).
- `uaa-concepts` paragraph break in a cell: [`<br/><br/>`](results/docusaurus-uaa-t2-passthrough-br.png),
  [two paragraphs](results/docusaurus-uaa-t2-extension-paragraphs.png),
  [`<br /><br />` in a pipe table](results/docusaurus-uaa-t2-native-br.png).

### Findings

1. **Hints can conflict.** `wrap: avoid` on a key column wins over its width
  when the longest key does not fit
  ([screenshot](results/docusaurus-oss-extension-nowrap-beats-width.png)).
  **Decided:** "don't wrap" wins, so a column's width varies with its
  content, but only up to a cap (`--table-nowrap-max`, 16em here); past it
  the text wraps between words. No key column on the test pages reaches the
  cap at a 1280-pixel window.
2. **Row headers take the header style.** With `stub-columns`, the key column
  becomes `<th scope="row">`, which the default theme draws bold and
  centered. **Decided:** row headers are styled on their own. The site's CSS
  gives them their own variables (weight, alignment), so a theme can change
  them without touching column headers or body cells (checked: setting them
  to left and normal weight changes only the row headers). Native pipe
  tables have no row headers to style.
3. **Placement changes the outline.** A table that follows a list item without
  indentation belongs to the item on the published page (Bookbinder's parser
  continues the item) but ends the list in Docusaurus. A pipe table also needs
  a blank line before it, where an HTML table does not.
4. **Links in HTML cells are not link-checked.** Docusaurus checks Markdown
  links at build time but not `<a href>` inside HTML.
5. **Three links point outside the test set** (`../cf-cli/v8.html`,
  `../loggregator/nozzle-tutorial.html`, `identity-providers.html`). The site
  reports them as warnings; cross-repository links are their own concept.
6. **Heading anchors** written as `### <a id="x"></a> Title` work in the
  browser, but (a) the anchor check reports eleven of them as broken, (b) the
  table of contents copies the `<a>` into its own link, which makes React
  report a hydration error on every page with such headings, and (c) the
  generated heading ids include variable names
  (`-use-app-logs-to-locate-delays-in-varsapp_runtime_abbr`). Docusaurus's own
  form `### Title {#x}` avoids all three (checked on one page).
7. **Page descriptions** come from the first paragraph's source text, so
  `metadata` and `troubleshooting_slow_requests` publish
  `{vars.appruntimeabbr}` in their description. Setting `description:` in the
  front matter avoids it.

8. **Text inside `<pre class="terminal">` is parsed as Markdown.** A
  word-by-word comparison with the published pages
  ([checks/text-diff.py](checks/text-diff.py)) found one content change in
  every mode: `Accept: */*` in the terminal output on
  `troubleshooting_slow_requests` shows as `Accept: /`, because MDX reads
  `*/*` as emphasis. The block is also split into paragraphs inside the
  `<pre>`. Five such blocks are on the test pages; they belong to the code
  blocks concept. The spot checks did not catch it because they cover the
  tables. **Decided:** left to the code blocks concept, which has to handle
  `<pre class="terminal">` on every page anyway; the tables round keeps the
  finding.

9. **Cells are roomier than on the published page.** Measured on the
  `uaa-concepts` table at a 1280-pixel window: cell padding 12 pixels on
  every side (published: 4.8 by 8), line height 26.4 pixels (published:
  23.2), code 14.4 pixels (published: 13). The same table is about 20%
  taller. A paragraph or list at the end of a cell also kept its bottom
  margin, so cells had about 30 pixels below the text and 12 above. The
  site now removes that last margin (13 above and 13 below), and adds
  `--table-font-size` and `--table-line-height` for the template; their
  defaults keep the theme's look. Padding, borders, and header and stripe
  colors are the theme's own variables (`--ifm-table-cell-padding` and
  others). There is no theme variable for the font size of tables.

### Text compared with the published page

Apart from finding 8 and the decided backslash fix, the main text of each page
matches the published page in all three modes. The other differences:

- **Not reproduced:** the *Page last updated* line and the *Create a pull
  request or raise an issue on the source for this page in GitHub* link.
  Docusaurus offers both (`showLastUpdateTime`, `editUrl`); this site does not
  enable them.
- **Moved:** the list of section links at the top of each published page is
  Docusaurus's *On this page* list beside the article.
- **Quotes:** the published build turns straight quotes into typographic ones
  (`user’s`, `“sub”`); Docusaurus keeps them straight (ten words on two
  pages).

### Raw passthrough errors

`make check-raw` in the site prints the first MDX error per page. MDX stops at
the first error, so each page was fixed one error at a time; the full list is
in the grid above.

| Page | First error | In a table? |
|------|-------------|-------------|
| `_oss_scale_table` | `<col>` is not closed | yes |
| `credential-types` | `“` before an attribute value | yes |
| `metadata` | `{` in JSON inside `<pre>` parsed as an expression | no |
| `troubleshooting_slow_requests` | `<br>` is not closed | no |
| `uaa-concepts` | `{OIDC provider alias}` in a list parsed as an expression | no |

## Zensical 0.0.69

Site: [sites/zensical/](sites/zensical/) — conventions:
[CONVENTIONS.md](sites/zensical/CONVENTIONS.md). Measured at the same
1280-pixel window; the content column is 688 pixels wide.

### Summary

- **The HTML builds unchanged.** All five pages build as they are, with no
  change to the page source: Python-Markdown passes HTML blocks through, and
  the variables keep their ERB form. Only the host page's partial line
  changes. The intent files' cleanup and one indent (finding 4) make every
  spot check pass.
- **Every table renders correctly in all three modes.** All 36 spot checks
  pass in passthrough and extension. Native passes 35: it cannot draw the
  `metadata` title as a spanning row. `make check` in the site reruns them.
- **Variables work without touching the pages.** The built-in macros support
  takes ERB delimiters, so `<%= vars.name %>` renders as written. An undefined
  variable renders empty and an HTML-valued variable renders as markup, as on
  the published pages. There is no generated page description, so the
  description problem Docusaurus has (its finding 7) does not occur.
- **The default theme styles only tables without a `class`.** Eight of the
  thirteen tables keep `class="table"` in passthrough and render without the
  theme's table style (finding 1).
- **Zensical has no table hints of its own.** Native pipe tables can carry
  widths through attributes on header cells; row headers, the title row and
  the capped no-wrap need HTML (passthrough) or a plugin (extension). The
  extension is a Python-Markdown block, the counterpart of the Docusaurus
  remark plugin; what #1642 §5 says about plugins is quoted in the
  Docusaurus summary.
- **No browser errors** on any page in any mode.

### Grid

| Page | Mode | Builds | Content and outline | Hints honored | Source readability |
|------|------|--------|---------------------|---------------|--------------------|
| `_oss_scale_table` | passthrough | yes; `<col />` closed (intent cleanup, not forced) | preserved | widths 25/25/50 exactly | HTML as before |
| | extension | yes | preserved; the empty Notes cell is written `- <!-- -->` (finding 5) | widths, row headers, key column on one line (26/25/49) | list-table, four-space indents; long cells on one line |
| | native | yes | preserved | widths 25/25/50 through header-cell attributes; no row headers | pipe table, very long rows |
| `credential-types` | passthrough | yes; class with typographic quotes dropped (intent cleanup) | preserved | width 20% | HTML |
| | extension | yes | preserved | width 20%, row headers, no wrap | list-table |
| | native | yes | preserved | width 20% through a header-cell attribute | pipe table, readable |
| `metadata` | passthrough | yes; two unclosed `<td>`, headers moved into `<thead>` (intent cleanup) | preserved; stray backslashes removed (decided fix) | spanning title row; no theme table style (finding 1) | HTML |
| | extension | yes | preserved | title row spanning all columns, row headers, no wrap on key column (23%) | list-table with nested lists: readable |
| | native | yes, lists as inline HTML in cells | preserved; title is a bold line above the table | none; top alignment from the theme | pipe table with inline `<ul>`: hard to edit |
| `troubleshooting_slow_requests` | passthrough | yes | preserved after indenting the Experiment 2 table under its list step | variant A, as written; no theme table style (finding 1) | HTML |
| | extension | yes | preserved | variant C: no widths, columns sized by content | list-table |
| | native | yes | preserved after indenting the Experiment 2 table under its list step | variant C (same as extension) | pipe table |
| `uaa-concepts` | passthrough | yes; `</td>` → `</tr>` (intent cleanup) | preserved | widths 30% and 25% | HTML |
| | extension | yes | preserved; `<br/><br/>` became two paragraphs (decided) | widths, row headers, no wrap | list-table; paragraphs as in Markdown |
| | native | yes | preserved, `<br /><br />` kept | widths through header-cell attributes | pipe table |

### Column widths

Percent of the table, first body row. Table 2 of `troubleshooting_slow_requests`
sits inside a numbered list, so it is narrower (660 pixels).

| Table | Passthrough | Extension | Native |
|-------|-------------|-----------|--------|
| `_oss_scale_table` | 25/25/50 | 26/25/49 | 25/25/50 |
| `credential-types` | 20/80 | 20/80 | 20/80 |
| `metadata` T1 | 16/17/27/40 | 23/18/25/33 | 18/19/27/36 |
| `metadata` T2 | 17/17/28/38 | 23/18/26/32 | 19/19/27/35 |
| `metadata` T3 | 16/27/57 | 16/26/57 | 16/27/57 |
| `troubleshooting` T1 | 26/25/49 | 28/25/46 | 28/25/46 |
| `troubleshooting` T2 | 25/36/39 | 23/37/40 | 23/37/40 |
| `troubleshooting` T3 | 25/30/45 | 21/31/47 | 21/31/47 |
| `troubleshooting` T4 | 25/20/55 | 19/23/58 | 19/23/58 |
| `troubleshooting` T5 | 25/25/50 | 22/22/56 | 22/22/56 |
| `troubleshooting` T6 | 25/25/50 | 19/24/57 | 19/24/57 |
| `uaa-concepts` T1 | 30/26/43 | 30/26/43 | 30/26/43 |
| `uaa-concepts` T2 | 25/75 | 25/75 | 25/75 |

The scale table's key column stays on one line at 26%: "Cloud Controller
Worker" fits the 16em cap here, so the no-wrap wins over the 25% width by one
point.

### Findings

1. **The default theme styles only tables without a `class`.** Its rules are
  written for `table:not([class])`. Passthrough keeps `class="table"` on the
  two `metadata` tables and the six `troubleshooting_slow_requests` tables, so
  they render with no border, and their header cells are in normal weight,
  not bold as the template convention says
  ([passthrough](results/zensical-metadata-t1-passthrough-class-unstyled.png),
  [extension](results/zensical-metadata-t1-extension-theme-styled.png)). The
  class only restates what the template should do; `credential-types` already
  drops it (its quotes were broken). The extension puts its hook on a
  wrapper `div` so the table itself stays classless.
2. **The theme's header rule outranks plain hint CSS.** The theme sets header
  cells with `.md-typeset table:not([class]) th:not([align])`. A rule such as
  `.hinted-table th[scope='row']` loses to it, so the title row was not
  centered and the row-header variables had no effect. Written to outrank it,
  both work (checked: setting the row-header variables to right and normal
  weight changes only the row headers).
3. **Template errors replace the page unless the build is told to fail.**
  Every `<%= … %>` on a page goes through the template engine, including ERB
  tags shown as examples in prose or code. A tag that is not a valid
  expression (the host page's first draft mentioned `partial 'oss_scale_table'`
  inside one) produced a page that said "Macro Syntax Error", and the build
  still reported success. `on_error_fail = true` makes it fail. Pages that
  document ERB will need escaping.
4. **Placement changes the outline, as in Docusaurus.** A table that follows
  a list item without indentation ends the list (Docusaurus finding 3).
  Indented, an HTML table becomes inline HTML inside the item's paragraph
  (`<p>…<table>…</table></p>`); browsers close the paragraph at the table,
  so the table stays in the step.
5. **Python-Markdown's list rules can drop a cell silently.** In a
  list-table, a bare `-` for an empty cell turns the cell above it into a
  heading (Markdown reads `-` under a line as a heading underline), so the
  row loses a cell and the build reports nothing. The spot checks caught it
  as missing `≥` cells. An empty cell is written `- <!-- -->`. Rows also need
  a blank line between them, and nesting needs four-space indents.
6. **Attribute lists work on cells, not on tables.** `{: .class }` on the
  line after a pipe table becomes an extra row showing that text. On a single
  cell it works, which is how native carries widths
  (`| Type {: style="width:20%" } |`). Per-column hints such as no-wrap would
  need an attribute on every body cell.
7. **Partials need the template engine's include, not snippets.** A
  `--8<--` snippet is inserted after variables are rendered, so a partial
  included that way shows `<%= vars.recommended_by %>` literally. The
  template engine's `include` renders the partial's variables. Partials sit
  outside `docs/` so they do not become pages.
8. **The anchor check found a real broken link and no false ones.**
  `uaa-concepts` links to `#shadow`, but the heading's anchor is
  `<a id="#shadow">` (with the `#`), so the link is broken on the published
  page too. The `<a id>` heading anchors that Docusaurus reported as broken
  are recognized here, and they cause no browser errors.

### Text compared with the published page

[checks/text-diff.py](checks/text-diff.py), run for every mode. Apart from the
decided backslash fix, the main text matches the published page except:

- **Three literal asterisks** in `troubleshooting_slow_requests`, every mode:
  a bulleted list that follows a paragraph line with no blank line between is
  a list on the published page and plain text here. Lists are their own
  concept.
- **Terminal output inside a list item** (`<pre class="terminal">`) is split
  into paragraphs inside the `<pre>` when it contains a blank line (one block,
  in `troubleshooting_slow_requests`); no characters are lost. `Accept: */*`
  comes through intact: the block that holds it is not in a list. Code blocks
  are their own concept.
- **Not reproduced, moved, quotes:** the same as Docusaurus — no *Page last
  updated* line or GitHub link, the section links are the theme's table of
  contents, and quotes stay straight (Python-Markdown's `smarty` extension
  would make them typographic; it is not on).

### Raw passthrough

The five pages built unchanged (only the host page's include line is
translated). 32 of 36 spot checks pass; the four that fail are exactly what
the intent files' cleanup and the indent fix:

| Page | Fails raw | Fixed by |
|------|-----------|----------|
| `credential-types` | class with typographic quotes | intent cleanup |
| `metadata` | backslashes in `\[a-z0-9A-Z\]` (two checks) | decided fix |
| `troubleshooting_slow_requests` | Experiment 2 table outside its list step | indent |

The unclosed `<td>` cells in `metadata` and the stray `</td>` in
`uaa-concepts` build and render as on the published page: the browser repairs
them, as it does for the published site.
