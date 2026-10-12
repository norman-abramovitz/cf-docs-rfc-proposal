# Tables round — results

What each tool did with the five test pages. A summary across tools comes
first, then one section per tool, newest last. Each starts with a short
summary, then the grid, then what the measurements and screenshots show. How
the pages were chosen and what the hints mean: [README](README.md). Per-table
intent and spot checks: [intent/](intent/).

How to read the grid:

- **Builds:** whether the page builds in that mode, and what had to change.
- **Content and outline:** the result of the spot checks in the intent file
  for that page, plus a check that headings, lists, and tables nest as on the
  published page.
- **Hints honored:** measured in a browser at a 1280-pixel window (the content
  column is 703 pixels wide).
- **Source readability:** a short judgment from an author's point of view.

## Summary

Every tool renders every test table correctly once the source is cleaned
up. They differ in how much cleanup the HTML needs, which hints their own
table syntax carries, and how much the rest of the page has to change.

| | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| **HTML builds as written** | no: MDX fails on all five pages | yes, all five | four of five; Markdoc changes text inside HTML silently | yes, inside passthrough blocks, but the page around it is rewritten as AsciiDoc |
| **Cleanup beyond the intent files** | close void elements, `style` as an object, `<tbody>` and `<colgroup>`, closing tags off the line start | one indent | entities and one-line cells where Markdoc would drop a dash or a space | the AsciiDoc rewrite, with four kinds of silent failure |
| **Spot checks after cleanup** (seven pages; 36 before `uaa-performance`, 42 before `_oss_roles_table`) | 49/51 in every mode (the two misses are page descriptions, not tables) | 51/51 in every mode | 51/51 in every mode | 51/51 in every mode |
| **Own table syntax carries** | a header row and each column's horizontal alignment (pipe tables) | widths on header cells, horizontal alignment | widths, horizontal alignment, lists and paragraphs in cells, spanning cells | widths, row headers, horizontal and vertical alignment, lists and paragraphs in cells, spanning cells |
| **Extension for the rest** | remark plugin | Python-Markdown block | attributes on Markdoc's table tag (85 lines) | none: roles on the table plus CSS |
| **A second style** (`table-media`) | a class on the list-table directive, `{.table-media}`; a pipe table takes one only through the table comment (2026-10-12) | the list-table block's `style` option; a pipe table takes one only through the table comment (2026-10-12) | Markdoc's class shorthand, `{% table .table-media %}`, which the native table tag takes too | a role, `[.table-media]`: plain AsciiDoc |
| **Wide tables** (wider than the column) | scroll in their own box: the theme shows every table as a block that scrolls | scroll in their own box: the theme's wrapper around Markdown tables; the site's `table.table` rule copies the theme's scrolling | scroll in their own box: the theme shows every table as a block that scrolls | the page widened; a short script in the site's UI files now puts each table in a box that scrolls |
| **Variables** | one import per page; HTML values escaped | ERB form kept as written | `{% $vars.name %}`; HTML values escaped | `{name}` attributes |

- **Two hints need CSS everywhere.** No tool's table syntax carries the
  column roles or the capped no-wrap. Antora and the Sphinx probe carry them
  as classes on the table, with no code; the other three use a small
  extension. What #1642 §5 says about extensions is quoted in the Docusaurus
  summary.
- **Migration cost outside the tables.** Antora's AsciiDoc rewrite is a
  separate cost of its own: every page changes, not only the tables, and the
  conversion failed silently in four ways (Antora finding 1). In MDX, three
  of the five first build errors are outside the tables. Markdoc changes
  terminal blocks, and MDX and Markdoc both lose the `*` in `Accept: */*`.
  Zensical shows three `*` as text where a list follows a line with no blank
  line between them.
- **Themes style tables differently.** Docusaurus and Starlight style every
  table; Zensical only tables without a class; Antora only its own tables;
  Sphinx's theme through its own class. Every HTML table now names its style
  with `class="table"`, and each site's CSS gives that class its standard
  look (Template conventions in the [README](README.md#template-conventions)).
  The Antora and Sphinx themes hyphenate words in cells; the template turns
  that off.
- **A second style is a class and a few CSS rules.** `table-media`, the
  example, was added to all four tools after the round. Passthrough names it
  as the HTML table's class everywhere. In Starlight and Antora the tool's
  own table syntax can name it too; in Docusaurus and Zensical a Markdown
  table cannot, so it takes the extension. The native pages keep the
  standard style in every tool, as decided. Each site's `CONVENTIONS.md`
  has an "Adding a style" section.
- **A wide table scrolls in its own box.** Checked in a browser at 1280
  and 390 pixels by giving each table an unbreakable 200-character line
  (`make check-wide`; 84 tables in Docusaurus, 112 in each of the others,
  all pass; with the roles table, 90 and 120, all pass). Antora's default UI gives a table no box, so the page
  widened until the site added a script that wraps each table. A
  `table-media` grid does not scroll: its rules make it a full-width
  table, so it shrinks its images to fit, and the check only asserts that
  it fits the column.
- **A real wide table scrolls, but at its narrowest.** The roles table
  (`_oss_roles_table`, 12 columns, added 2026-10-12) scrolls in a box of
  its own in every tool and every converted mode, as decided. Docusaurus,
  Starlight and Antora lay it out at its min-content width, every column
  as narrow as its longest word, so the activity column wraps on every
  row and the table is 4,850 to 5,500 pixels tall; Zensical gives all
  twelve columns the same 100 pixels. The published page has no box: the
  table spills 154 pixels past its 720-pixel column. No scrollbar shows
  until the reader scrolls (overlay scrollbars). In Docusaurus the box
  cuts a column through its text; in Zensical and Starlight it ends just
  after Org Billing Manager, and in Antora after Space Auditor, so
  nothing in view shows that more columns follow. The comparison pages
  show it as seen and as the full table. Since 2026-10-12 a wide table's first
  column keeps at least 24 characters' width and a shadow marks the side
  with more columns ([wide tables](#wide-tables-prose-width-and-a-continuation-cue)).

- **Widths, alignment and font size, checked after review.** Column 1 is
  sized by its content in Docusaurus passthrough and extension once the
  source's 20% is left out. Docusaurus's centered headers can be set left
  per table or for the site. Each tool's table font size is a stylesheet
  setting ([widths, alignment and font size](#widths-alignment-and-font-size)).

**Probes** (one question each; Eleventy built two test pages, Sphinx one
table, Middleman all five test pages):

| Probe | Question | Answer |
|---|---|---|
| [Eleventy 3.1.6](probes/eleventy/README.md) | Do `<%= vars.* %>` tags render unchanged as EJS? | Yes for the tables, byte for byte. EJS's `<%=` escapes HTML, so HTML-valued variables, helpers and includes need `<%-`. |
| [Sphinx 9.1.0 + MyST 5.1.0](probes/sphinx-myst/README.md) | Can `list-table` directive options carry the hints? | Header row, row headers and widths, yes; roles and the capped no-wrap through classes and CSS. No second header row. |
| [Middleman 4.6.3](probes/middleman/README.md) | Smallest change that removes Bookbinder? | A short config and a layout; all five pages build unchanged on Ruby 4.0.7 (plus the `ostruct` gem) and every table matches the published page. |

## Docusaurus 3.10.2

Site: [sites/docusaurus/](sites/docusaurus/) — conventions:
[CONVENTIONS.md](sites/docusaurus/CONVENTIONS.md).

### Summary

- **The HTML does not build unchanged.** All five pages fail MDX compilation
  as they are. Three of the five first errors are outside the tables (literal
  `{…}` placeholders in prose, an unclosed `<br>`), so table cleanup alone is
  not enough to migrate a page to MDX.
- **With cleanup, every table renders correctly in all three modes.** 34 of
  36 spot checks pass in every mode; the two that fail are the page
  descriptions (finding 7). `make check` in the site reruns them with
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
| `credential-types` | passthrough | after cleanup: straight quotes, `style` object, `<tbody>` | preserved | width 20% | HTML |
| | extension | yes | preserved | width 20%, row headers, no wrap | list-table |
| | native | yes | preserved | none (18/82) | pipe table, readable |
| `metadata` | passthrough | after cleanup: two unclosed `<td>`, headers moved into `<thead>`, `style` objects, plus braces in a `<pre>` block and one `<br>` outside the tables | preserved; stray backslashes removed (decided fix) | spanning title row centered | HTML |
| | extension | yes | preserved; title is a bold line above the table | row headers, no wrap on key column (26%) | list-table with nested lists: readable |
| | native | yes, lists as inline HTML in cells | preserved; title is a bold line above the table, not part of it | none; cells vertically centered | pipe table with inline `<ul>`: hard to edit |
| `troubleshooting_slow_requests` | passthrough | after cleanup: `<tbody>`, one multi-line cell, plus `<br />` outside the tables | preserved after nesting the Experiment 2 table in its list step | variant A, as written | HTML |
| | extension | yes | preserved | variant C (decided): no widths, columns sized by content | list-table |
| | native | yes | preserved after adding a blank line before each table | none (same as variant C) | pipe table |
| `uaa-concepts` | passthrough | after cleanup: `</td>` → `</tr>`, plus `{…}` placeholders escaped in prose | preserved | widths 30% and 25% | HTML |
| | extension | yes | preserved; `<br/><br/>` became two paragraphs (decided) | widths, row headers, no wrap | list-table; paragraphs as in Markdown |
| | native | yes | preserved, `<br /><br />` kept | none (27/30/43, 25/74) | pipe table |
| `_oss_roles_table` (added 2026-10-12) | passthrough | yes; the source compiles unchanged; only the intent cleanup (two empty markers) and `class="table"` | preserved; id kept | header row; scrolls in its own box (the theme's block table), laid out at its narrowest: 1053 pixels in 703, every activity wrapping to its longest word | HTML, one cell per line |
| | extension | yes; the list-table plugin now passes `{#id}` to the table | preserved; id kept | header row, row headers, roles, top alignment; the same narrowest layout (1060 pixels) | list-table, 12 lines per row |
| | native | yes | preserved except the id: a pipe table cannot carry one (since 2026-10-12 the table comment keeps it: [classes and ids](#classes-and-ids-on-pipe-tables)) | header row; the same narrowest layout | pipe table, rows up to 377 characters; markers as inline `<sup><strong>` |

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
paragraphs. **Changed after the Starlight round:** the title is a bold line
above the table in every converted mode of every tool, because Markdown
tables have one header row (Starlight finding 4). Passthrough keeps the
source's spanning row.

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
10. **The wide table is laid out at its narrowest** (`_oss_roles_table`,
   added 2026-10-12). The theme shows every table as a block that scrolls
   (`display: block; overflow-x: auto`), so a table wider than the column
   is drawn at its min-content width: every column as narrow as its longest
   word. The roles table is 1053 by 5518 pixels in a 703-pixel box (2087 by
   2237 at its natural width); the activity column (106 pixels) wraps on
   all 42 rows, and the prose role gives it no more room. The sticky navbar
   and the off-screen "Skip to main content" link are hidden for the
   screenshots. Relative links in the notes are rewritten root-absolute and
   reported as broken, as in finding 5; a pipe table cannot carry the
   table's id, and the list-table plugin was changed to pass it.

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
| `_oss_roles_table` (added 2026-10-12) | none: compiles unchanged | — |

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
  pass in every mode. `make check` in the site reruns them.
- **Variables work without touching the pages.** The built-in macros support
  takes ERB delimiters, so `<%= vars.name %>` renders as written. An undefined
  variable renders empty and an HTML-valued variable renders as markup, as on
  the published pages. There is no generated page description, so the
  description problem Docusaurus has (its finding 7) does not occur.
- **The default theme styles only tables without a `class`.** Eight of the
  thirteen tables kept `class="table"` in passthrough and rendered without
  the theme's table style (finding 1). **Decided:** the class stays as a hook the
  template can format; the site's CSS now gives `table.table` the theme's
  table look. Dropping the class is how to see the theme's own default.
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
| `credential-types` | passthrough | yes; class quotes made straight (intent cleanup) | preserved | width 20% | HTML |
| | extension | yes | preserved | width 20%, row headers, no wrap | list-table |
| | native | yes | preserved | width 20% through a header-cell attribute | pipe table, readable |
| `metadata` | passthrough | yes; two unclosed `<td>`, headers moved into `<thead>` (intent cleanup) | preserved; stray backslashes removed (decided fix) | spanning title row; theme look through `table.table` in the site CSS (finding 1) | HTML |
| | extension | yes | preserved; title is a bold line above the table | row headers, no wrap on key column (23%) | list-table with nested lists: readable |
| | native | yes, lists as inline HTML in cells | preserved; title is a bold line above the table | none; top alignment from the theme | pipe table with inline `<ul>`: hard to edit |
| `troubleshooting_slow_requests` | passthrough | yes | preserved after indenting the Experiment 2 table under its list step | variant A, as written; theme look through `table.table` in the site CSS (finding 1) | HTML |
| | extension | yes | preserved | variant C: no widths, columns sized by content | list-table |
| | native | yes | preserved after indenting the Experiment 2 table under its list step | variant C (same as extension) | pipe table |
| `uaa-concepts` | passthrough | yes; `</td>` → `</tr>` (intent cleanup) | preserved | widths 30% and 25% | HTML |
| | extension | yes | preserved; `<br/><br/>` became two paragraphs (decided) | widths, row headers, no wrap | list-table; paragraphs as in Markdown |
| | native | yes | preserved, `<br /><br />` kept | widths through header-cell attributes | pipe table |
| `_oss_roles_table` (added 2026-10-12) | passthrough | yes; `class="table"` and the two empty markers removed (intent cleanup) | preserved; id kept | header row; scrolls in its own box (`table.table` itself); 12 equal columns of 100 pixels | HTML |
| | extension | yes | preserved; markers `^N^`, not bold (finding 9); the id lands on the wrapper `div` | header row, row headers, roles as classes; scrolls in the theme's wrapper; equal columns | list-table, one item per cell (a 565-line block) |
| | native | yes | preserved; markers `^N^`; no id (a pipe table cannot carry one (since 2026-10-12 the table comment keeps it: [classes and ids](#classes-and-ids-on-pipe-tables))) | header row; scrolls in the theme's wrapper; equal columns | pipe table, about 140-character rows of mostly empty cells |
| | native-plain | yes (the same file as native: the source sets no widths) | as native | as native | as native |

### Column widths

Percent of the table, first body row. Table 2 of `troubleshooting_slow_requests`
sits inside a numbered list, so it is narrower (660 pixels).

| Table | Passthrough | Extension | Native |
|-------|-------------|-----------|--------|
| `_oss_scale_table` | 25/25/50 | 26/25/49 | 25/25/50 |
| `credential-types` | 20/80 | 20/80 | 20/80 |
| `metadata` T1 | 18/19/27/36 | 23/18/25/33 | 18/19/27/36 |
| `metadata` T2 | 19/19/27/35 | 23/18/26/32 | 19/19/27/35 |
| `metadata` T3 | 16/27/57 | 16/26/57 | 16/27/57 |
| `troubleshooting` T1 | 28/25/46 | 28/25/46 | 28/25/46 |
| `troubleshooting` T2 | 25/36/39 | 23/37/40 | 23/37/40 |
| `troubleshooting` T3 | 25/30/45 | 21/31/47 | 21/31/47 |
| `troubleshooting` T4 | 25/22/53 | 19/23/58 | 19/23/58 |
| `troubleshooting` T5 | 25/25/50 | 22/22/56 | 22/22/56 |
| `troubleshooting` T6 | 25/25/50 | 19/24/57 | 19/24/57 |
| `uaa-concepts` T1 | 30/26/43 | 30/26/43 | 30/26/43 |
| `uaa-concepts` T2 | 25/75 | 25/75 | 25/75 |
| `_oss_roles_table` | 8 × 12 | 8 × 12 | 8 × 12 |

Corrected 2026-10-12: four passthrough figures (`metadata` T1 and T2,
`troubleshooting` T1 and T4) were remeasured on a fresh build, at a
1280-pixel window, first body row, and replaced; the other figures
measured the same.

The scale table's key column stays on one line at 26%: "Cloud Controller
Worker" fits the 16em cap here, so the no-wrap wins over the 25% width by one
point.

### Native with and without widths

Native mode is built twice: `native` carries widths through attributes on
header cells, `native-plain` is pipe tables with no attributes, as most
Markdown tools would have them. Only the pages whose source sets widths
differ (percent of the table, first body row):

| Page | native | native-plain |
|------|--------|--------------|
| `_oss_scale_table` | 25/25/50 | 17/15/68 |
| `credential-types` | 20/80 | 15/84 |
| `uaa-concepts` table 1 | 30/26/43 | 16/31/53 |
| `uaa-concepts` table 2 | 25/75 | 16/84 |

`native-plain` passes all 36 spot checks, as `native` does.

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
  wrapper `div` so the table itself stays classless. **Decided:** keep the
  class and style it. [hints.css](sites/zensical/docs/stylesheets/hints.css)
  repeats the theme's table rules for `table.table`, so those tables now
  have borders and bold headers; a template can format them differently
  through the same class. *Later decision:* every HTML table names its
  style with a class, so the four tables without one now get
  `class="table"` too, and `credential-types` keeps it with straight quotes
  (see [Template conventions](README.md#template-conventions)).
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
9. **The wide table gets twelve equal columns** (`_oss_roles_table`,
   added 2026-10-12). The theme gives header cells `min-width: 5rem`; twelve
   of them exceed the 688-pixel column, so every column is 100 pixels and
   the table 1202 pixels, scrolling in the theme's wrapper (passthrough:
   in `table.table` itself). The activity column wraps up to eight lines.
   Note markers are `^N^` (`pymdownx.caret`); `^**N**^` next to text stays
   literal, because the delimiter follows CommonMark's flanking rules, so
   the markers are not bold outside passthrough. A pipe table cannot carry
   the id, and the list-table's `attrs` put it on the wrapper `div`. The
   sticky header is hidden for the screenshots.

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
| `_oss_roles_table` (added 2026-10-12) | the two empty note markers | intent cleanup |

The unclosed `<td>` cells in `metadata` and the stray `</td>` in
`uaa-concepts` build and render as on the published page: the browser repairs
them, as it does for the published site.

## Starlight 0.42.6

Site: [sites/starlight/](sites/starlight/) — conventions:
[CONVENTIONS.md](sites/starlight/CONVENTIONS.md). Astro 7.3.8 with the
Markdoc integration 2.0.11; pages are Markdoc (`.mdoc`) with HTML allowed.
Measured at the same 1280-pixel window; the content column is 632 pixels
wide.

### Summary

- **Four of the five pages parse with their HTML unchanged.** Only the
  variables and the partial line are translated. The fifth,
  `troubleshooting_slow_requests`, stops the build at a terminal block outside
  the tables (raw passthrough below).
- **Markdoc reads the text inside HTML as Markdown, and that changes content
  silently.** A lone `-` in a code span becomes an empty bulleted list, and
  the space next to an inline tag disappears when the text around it spans
  lines (`<code>password</code> refers` renders as "passwordrefers", 19 places
  in `uaa-concepts`). The build reports nothing (findings 1 and 2).
  **Markdoc cannot take the HTML as is.** These are the changes it needed,
  which the other tools did not:

  | In the source | Written for Markdoc | Without the change |
  |---------------|---------------------|--------------------|
  | `<li><code>-</code></li>` | `<li><code>&#45;</code></li>` | an empty bulleted list; the dash is gone |
  | `The name <code>password</code> refers to …` with the cell text over two lines | the whole cell on one line | "The name passwordrefers to …" |
  | `… creates clients with generated` at a line end, `<code>Client.client_id</code>` on the next, in a cell with a variable | `generated&#32;<code>Client.client_id</code>` | "generatedClient.client_id" |
  | a blank line inside `<pre>` in a list item | the line break written `&#10;` (`$ cf logs app1&#10;`) | the whole site fails to build |

  Joining cells onto one line is not adopted as a conversion rule: it makes
  the source harder to read.
- **With those changes every table renders correctly in every mode.** All 36
  spot checks pass in every mode.
  `make check` in the site reruns them.
- **Markdoc's own table tag is a native list-table.** Without any custom code
  its cells hold lists and paragraphs, header cells take a `width`, and a
  cell can span columns. That carries the widths, the lists in `metadata`,
  the two paragraphs in `uaa-concepts`, and a spanning title row. What it
  cannot carry: row headers, top alignment, the capped no-wrap, and a title
  row above the column headers (Markdoc has one header row, so the column
  headers become an ordinary row).
- **The extension adds the hints as attributes on that same tag.**
  [list-table.mjs](sites/starlight/list-table.mjs) declares them on Markdoc's
  table node, 85 lines, the counterpart of the Docusaurus and Zensical
  extensions; what #1642 §5 says about plugins is quoted in the Docusaurus
  summary. Authors write Markdoc's table syntax; only the attributes are new.
- **Variables need one translation.** `<%= vars.name %>` becomes
  `{% $vars.name %}`. An undefined variable renders empty. An HTML-valued
  variable renders as escaped text unless a small tag renders it as markup.
  Starlight writes no page description unless the front matter has one, so
  the description problem Docusaurus has (its finding 7) does not occur.
- **The theme styles every table, whatever its class**, so `class="table"`
  makes no difference here. Its styles sit in cascade layers, so the site's
  hint CSS wins without the specificity work Zensical needed.
- **No browser errors.** The only console message is a 404 for the default
  favicon, which this site does not provide.

### Grid

| Page | Mode | Builds | Content and outline | Hints honored | Source readability |
|------|------|--------|---------------------|---------------|--------------------|
| `_oss_scale_table` | passthrough | yes | preserved | widths 25/25/50 exactly | HTML as before |
| | extension | yes | preserved | widths, row headers, key column on one line (31/24/45) | Markdoc table; long cells on one line |
| | native | yes | preserved | widths 25/25/50 through `width` on header cells; no row headers | Markdoc table |
| | native-plain | yes | preserved | none (18/17/65) | pipe table, very long rows |
| `credential-types` | passthrough | yes; class quotes made straight (intent cleanup) | preserved | width 20% | HTML |
| | extension | yes | preserved | width 20%, row headers, no wrap | Markdoc table |
| | native | yes | preserved | width 20% through `width` on a header cell | Markdoc table, readable |
| | native-plain | yes | preserved | none (18/82) | pipe table, readable |
| `metadata` | passthrough | yes; intent cleanup, plus `&#45;` for five lone dashes and cells joined onto one line (Markdoc cannot take the HTML as is) | preserved; stray backslashes removed (decided fix) | spanning title row | HTML |
| | extension | yes | preserved; title is a bold line above the table | row headers, no wrap on key column (27%) | Markdoc table with nested lists: readable |
| | native | yes | preserved; title is a bold line above the table | lists in cells without HTML | Markdoc table with nested lists: readable |
| | native-plain | yes, lists as inline HTML in cells | preserved; title is a bold line above the table | none | pipe table with inline `<ul>`: hard to edit |
| `troubleshooting_slow_requests` | passthrough | yes; one blank line in an indented terminal block written `&#10;`, cells joined (Markdoc cannot take the HTML as is) | preserved after indenting the Experiment 2 table under its list step | variant A, as written | HTML |
| | extension | yes | preserved | variant C: no widths, columns sized by content | Markdoc table |
| | native | yes | preserved | variant C (same as extension) | Markdoc table |
| | native-plain | yes | preserved | variant C (same as extension) | pipe table |
| `uaa-concepts` | passthrough | yes; `</td>` → `</tr>` (intent cleanup), cells joined and one `&#32;` (Markdoc cannot take the HTML as is) | preserved | widths 30% and 25% | HTML |
| | extension | yes | preserved; `<br/><br/>` became two paragraphs (decided) | widths, row headers, no wrap | Markdoc table; paragraphs as in Markdown |
| | native | yes | preserved; two paragraphs (decided) | widths through `width` on header cells | Markdoc table |
| | native-plain | yes | preserved, `<br /><br />` kept | none (27/32/41, 25/75) | pipe table |
| `_oss_roles_table` (added 2026-10-12) | passthrough | yes; `class="table"` and the two empty markers removed (intent cleanup); nothing forced by Markdoc | preserved; id kept; markers as superscripts | header row; scrolls in its own box (the table itself), laid out at its narrowest: 1087 pixels in 632, 5461 tall | HTML |
| | extension | yes; `list-table.mjs` now passes the id through | preserved; id kept; markers as inline `<sup>` HTML | row headers, roles; the same narrowest layout (1092 pixels) | Markdoc table, 12 `*` lines per row, `<!-- -->` for empty cells |
| | native | yes | preserved; id kept through `{% table #… %}` | header row only; the same narrowest layout | Markdoc table, long |
| | native-plain | yes | preserved except the id: a pipe table cannot carry one (since 2026-10-12 the table comment keeps it: [classes and ids](#classes-and-ids-on-pipe-tables)) | none; the same widths | pipe table, one line per row |

### Column widths

Percent of the table, first body row. Table 2 of `troubleshooting_slow_requests`
sits inside a numbered list, so it is narrower (592 pixels).

| Table | Passthrough | Extension | Native | Native-plain |
|-------|-------------|-----------|--------|--------------|
| `_oss_scale_table` | 25/25/50 | 31/24/45 | 25/25/50 | 18/17/65 |
| `credential-types` | 20/80 | 20/80 | 20/80 | 18/82 |
| `metadata` T1 | 16/20/31/33 | 27/18/28/26 | 16/20/31/33 | 16/20/31/33 |
| `metadata` T2 | 18/21/31/30 | 27/19/29/25 | 18/21/31/30 | 18/21/31/30 |
| `metadata` T3 | 18/34/49 | 18/34/48 | 18/34/49 | 18/34/49 |
| `troubleshooting` T1 | 32/27/41 | 32/27/41 | 32/27/41 | 32/27/41 |
| `troubleshooting` T2 | 25/38/37 | 31/35/34 | 31/35/34 | 31/35/34 |
| `troubleshooting` T3 | 25/33/42 | 19/35/47 | 19/35/47 | 19/35/47 |
| `troubleshooting` T4 | 25/25/50 | 17/26/57 | 17/26/57 | 17/26/57 |
| `troubleshooting` T5 | 25/25/50 | 20/25/55 | 20/25/55 | 20/25/55 |
| `troubleshooting` T6 | 25/25/50 | 16/27/56 | 16/27/56 | 16/27/56 |
| `uaa-concepts` T1 | 30/31/39 | 30/31/39 | 30/31/39 | 27/32/41 |
| `uaa-concepts` T2 | 25/75 | 25/75 | 25/75 | 25/75 |
| `_oss_roles_table` | 9/7/7/8/9/8/9/6/9/10/8/9 | 9/7/7/8/9/8/9/6/9/10/8/9 | 9/7/7/8/9/8/9/6/9/10/8/9 | 9/7/7/8/9/8/9/6/9/10/8/9 |

Corrected 2026-10-12: the native figure for `metadata` T1 (was
16/21/31/33) were remeasured on a fresh build, at a
1280-pixel window, first body row, and replaced; the other figures
measured the same.

The scale table's key column stays on one line at 31%: "Cloud Controller
Worker" fits the 16em cap, so the no-wrap wins over the 25% width, as in
Docusaurus. In `metadata` the no-wrap key column ("(Optional) Key Prefix")
takes 27% in the extension.

### Findings

1. **Text inside HTML is Markdown.** With HTML allowed, the Markdoc
  integration parses each run of text between HTML tags as Markdown. In
  `metadata`, `<li><code>-</code></li>` renders as a code span holding an
  empty bulleted list, so the dash is gone
  ([screenshot](results/starlight-metadata-t1-passthrough-raw-dash-list.png));
  `&#45;` or `\-` keeps it. The same rule removes the `\[` escapes (here the
  decided fix), and `*`, `_`, and backticks inside HTML cells act as
  Markdown. No error is reported.
2. **Spaces next to inline tags disappear.** When the text between two tags
  spans lines or holds a variable, the space at its edge is dropped:
  `<code>password</code> refers` renders as "passwordrefers", and
  `the steps in <a …>Experiment 1 …</a>` as "the steps inExperiment 1". 19
  places in `uaa-concepts` and one in `troubleshooting_slow_requests`, all
  inside table cells ([screenshot](results/starlight-uaa-t1-passthrough-raw-spaces-lost.png)).
  Putting each cell on one line keeps the spaces (HTML renders the joined
  cell the same), and a space right after a variable is written `&#32;`.
  [checks/text-diff.py](checks/text-diff.py) found these; the spot checks
  did not.
3. **A blank line inside `<pre>` inside a list item stops the build.** The
  terminal block in step 4 of Experiment 2 has a blank line; Markdoc reports
  the list item and the `<pre>` as unclosed and the whole site fails to
  build. Writing that line break as `&#10;` lets it parse. The block also
  loses its blank line and indentation on screen. Code blocks are their own
  concept.
4. **Markdoc's table has one header row.** The first row goes in the table
  head; there is no way to put a second row there without the extension. In
  native, the spanning title row takes the head and the column headers
  become an ordinary row, written bold so they still read as headers
  ([screenshot](results/starlight-metadata-t1-native-title-row.png)).
  **Decided:** the title is a bold line above the table in every converted
  mode of every tool, so the column headers stay real header cells.
5. **The theme lets list items break inside words.** Starlight sets
  `overflow-wrap: anywhere` on list items, so in a narrow table column
  "Alphanumeric" broke as "Alphanumeri" / "c" and "[a-z0-9A-Z]" across
  lines, in every mode
  ([screenshot](results/starlight-metadata-t1-extension-word-break.png)).
  The site's CSS now limits that to words that cannot fit at all, which also
  widens those columns.
6. **Starlight has no table variables.** Its table rules use fixed padding
  (`0.5rem 1rem`), color variables for borders and header text, and the page
  text size and line height. The site's CSS adds `--table-font-size`,
  `--table-line-height`, and the row-header variables (checked: setting them
  changes only the tables, and only the row headers for the row-header
  variables). The theme spaces blocks with top margins only, so cells have no
  extra gap below their last paragraph (8 pixels above, 9 below in the
  two-paragraph `uaa-concepts` cell).
7. **No link check.** Astro does not check in-page links. A scan of the
  built pages found two broken ones in `uaa-concepts`, `#shadow` and
  `#user-groups`; both headings write their anchor as `<a id="#…">`, so the
  links are broken on the published page too. Zensical reported only
  `#shadow` because its generated heading id happens to be `user-groups`.
8. **Heading ids start with a dash.** A heading written
  `## <a id="about"></a> About metadata` gets the id `-about-metadata`; the
  `<a id="about">` inside it still works for links, and the table of
  contents shows the heading text with no browser error.
9. **Typographic quotes are an option, but not a usable one.** The Markdoc
  integration's `typographer` setting turns straight quotes into typographic
  ones in prose, as the published site does, but also inside `<pre>` blocks
  (JSON, terminal output) and inside HTML `<code>`, where they change
  content. It stays off.
10. **The wide table is laid out at its narrowest** (`_oss_roles_table`,
   added 2026-10-12). The theme shows a table as a block that scrolls, so
   it is drawn at min-content width: 1087 by 5461 pixels in a 632-pixel
   column (2113 by 1961 at its natural width). Markdoc has no superscript
   syntax; inline `<sup><strong>` works in table-tag cells, pipe cells and
   paragraphs. The table tag needed a short change in `list-table.mjs`
   to keep the id; a pipe table cannot carry one. The sticky "On this page"
   sidebar is hidden for the full-table screenshot, which runs under it.

### Text compared with the published page

[checks/text-diff.py](checks/text-diff.py), run for every mode after the
passthrough fixes above. Apart from the decided backslash fix, the main text
matches the published page except:

- **`Accept: */*` shows as `Accept: /`** in `troubleshooting_slow_requests`,
  every mode, as in Docusaurus (its finding 8): the terminal block holding it
  is HTML, and its text is read as Markdown (finding 1). The block is also
  split into paragraphs. Code blocks are their own concept.
- **Not reproduced, moved, quotes:** the same as Docusaurus — no *Page last
  updated* line or GitHub link, the section links are the theme's table of
  contents, and quotes stay straight (finding 9). The page title is in the
  page header, outside the compared text.

### Raw passthrough

`make check-raw` in the site prints the Markdoc errors per page. Four pages
parse with their HTML unchanged; `troubleshooting_slow_requests` does not
(finding 3), and one page that does not parse stops the whole build, so the
raw build leaves it out. 28 of 36 spot checks pass on the four raw pages:

| Page | Fails raw | Fixed by |
|------|-----------|----------|
| `credential-types` | class with typographic quotes | intent cleanup |
| `metadata` | the lone `-` code spans (finding 1) | `&#45;` (Markdoc cannot take the HTML as is) |
| `troubleshooting_slow_requests` | does not parse (six checks) | `&#10;` (Markdoc cannot take the HTML as is) and the indent |
| `_oss_roles_table` (added 2026-10-12) | the two empty note markers | intent cleanup |

The raw pages also lose the spaces next to inline tags (finding 2); the spot
checks do not cover that. The backslash checks pass raw, because Markdoc
reads `\[` as a Markdown escape (finding 1).

## Antora 3.2.1

Site: [sites/antora/](sites/antora/) — conventions:
[CONVENTIONS.md](sites/antora/CONVENTIONS.md). The default UI, pinned to one
build (it has no version numbers). Measured at the same 1280-pixel window;
tables are 686 pixels wide (792 on the scale table's host page, which has no
table of contents beside it).

### Summary

- **Every page is rewritten, in every mode.** Antora reads AsciiDoc, so the
  Markdown around the tables becomes AsciiDoc even in passthrough. Here that
  was done with pandoc 3.12 plus a script; the conversion itself went wrong
  in four ways that a converter has to handle (finding 1).
- **The HTML builds unchanged.** An HTML table inside a passthrough block
  (`++++`) is not parsed: the browser gets it exactly as written and repairs
  it as on the published page. Raw, 32 of 36 spot checks pass; the intent
  files' cleanup fixes the other four (raw passthrough below). The only
  addition is `[subs=attributes+]` on a table that holds a variable.
- **With that, every table renders correctly in every mode.** All 36 spot
  checks pass in passthrough, extension, native, and native-plain.
  `make check` in the site reruns them.
- **AsciiDoc's own table carries most of the hints.** Widths, content-sized
  columns, a header row, row headers, top alignment, a cell spanning columns,
  and lists and paragraphs in cells are all table specs. What it cannot
  carry: the capped no-wrap, the column roles, and a second header row (so
  the `metadata` title is a bold line above the table, as decided).
- **The extension needs no code.** Roles on the native table name the column
  roles and the no-wrap columns (`[.hinted.col1-key.col1-nowrap]`), and a
  stylesheet in a supplemental UI gives them their meaning. What #1642 §5
  says about plugins is quoted in the Docusaurus summary.
- **The default UI styles only AsciiDoc tables.** An HTML table gets no
  borders, and the UI exposes no variables (findings 3 and 4). The site's
  stylesheet styles `table.table` (every HTML table) and turns off the UI's
  hyphenation in tables (finding 5).
- **Variables become attributes.** `<%= vars.name %>` is `{name}`. An
  undefined attribute renders as nothing only with `attribute-missing: drop`;
  by default the page shows `{metadata_ref}` as text. An HTML-valued
  attribute renders as markup. Antora writes no page description unless the
  page sets one, so the description problem Docusaurus has (its finding 7)
  does not occur.
- **No browser errors** and no failed requests on any page.

### Grid

| Page | Mode | Builds | Content and outline | Hints honored | Source readability |
|------|------|--------|---------------------|---------------|--------------------|
| `_oss_scale_table` | passthrough | yes | preserved | widths 25/25/50; `class="table"` added | HTML in a passthrough block |
| | extension | yes | preserved | widths, row headers, key column on one line | AsciiDoc table |
| | native | yes | preserved | widths 25/25/50, row headers, top alignment | AsciiDoc table |
| | native-plain | yes | preserved | none; equal columns (33/33/33) | AsciiDoc table |
| `credential-types` | passthrough | yes; class quotes made straight (intent cleanup) | preserved | width 20%; `class="table"` added | HTML |
| | extension | yes | preserved | width 20%, row headers, no wrap | AsciiDoc table, readable |
| | native | yes | preserved | width 20%, row headers | AsciiDoc table, readable |
| | native-plain | yes | preserved | none; equal columns (50/50) | AsciiDoc table, readable |
| `metadata` | passthrough | yes; intent cleanup | preserved; stray backslashes removed (decided fix) | spanning title row | HTML |
| | extension | yes | preserved; title is a bold line above the table | row headers, no wrap on key column (23%) | AsciiDoc table with lists in `a\|` cells: readable |
| | native | yes | preserved; title is a bold line above the table | row headers, top alignment | AsciiDoc table with lists: readable |
| | native-plain | yes | preserved; title is a bold line above the table | none; equal columns | AsciiDoc table with lists: readable |
| `troubleshooting_slow_requests` | passthrough | yes | preserved after nesting the Experiment 2 table in its list step | variant A, as written | HTML |
| | extension | yes | preserved | variant C: no widths, columns sized by content | AsciiDoc table |
| | native | yes | preserved | variant C (same as extension) | AsciiDoc table |
| | native-plain | yes | preserved | equal columns (33/33/33), not variant C | AsciiDoc table |
| `uaa-concepts` | passthrough | yes; `</td>` → `</tr>` (intent cleanup) | preserved | widths 30% and 25%; `class="table"` added | HTML |
| | extension | yes | preserved; `<br/><br/>` became two paragraphs (decided) | widths, row headers, no wrap | AsciiDoc table |
| | native | yes | preserved; two paragraphs (decided) | widths, row headers | AsciiDoc table |
| | native-plain | yes | preserved; two paragraphs | none; equal columns | AsciiDoc table |
| `_oss_roles_table` (added 2026-10-12) | passthrough | yes; `class="table"` and the two empty markers removed (intent cleanup) | preserved; id kept; notes as AsciiDoc | header row; scrolls in its own box (882 pixels in 792), columns at their narrowest; cells centered vertically | 608 lines of HTML in a passthrough block |
| | extension | yes | preserved; markers `^N^` (not bold) | header row, row headers, top alignment, id; the same layout; the column roles are classes with no CSS, so they change nothing | AsciiDoc table, one cell per line; `cols=".<~h,11*.<~"` |
| | native | yes | preserved; markers `^N^` | header row, row headers, top alignment, id; the same layout | AsciiDoc table, as extension |
| | native-plain | yes | preserved | header row; the equal widths (8.33%) are written but give way to the table's narrowest width, so the columns match native | AsciiDoc table, as extension |

### Column widths

Percent of the table, first body row. Table 2 of `troubleshooting_slow_requests`
sits inside a numbered list, so it is narrower (650 pixels).

| Table | Passthrough | Extension | Native | Native-plain |
|-------|-------------|-----------|--------|--------------|
| `_oss_scale_table` | 25/25/50 | 25/25/50 | 25/25/50 | 33/33/33 |
| `credential-types` | 20/80 | 20/80 | 20/80 | 50/50 |
| `metadata` T1 | 16/17/29/39 | 23/16/23/38 | 17/17/25/41 | 25/25/25/25 |
| `metadata` T2 | 18/17/29/36 | 23/17/24/36 | 19/17/25/38 | 25/25/25/25 |
| `metadata` T3 | 15/33/52 | 16/33/51 | 15/33/52 | 33/33/33 |
| `troubleshooting` T1 | 34/23/43 | 34/23/43 | 34/23/43 | 33/33/33 |
| `troubleshooting` T2 | 25/36/39 | 28/34/37 | 28/34/37 | 33/33/33 |
| `troubleshooting` T3 | 25/30/45 | 18/32/49 | 18/32/49 | 33/33/33 |
| `troubleshooting` T4 | 25/21/54 | 15/23/62 | 15/23/62 | 33/33/33 |
| `troubleshooting` T5 | 25/25/50 | 19/22/59 | 19/22/59 | 33/33/33 |
| `troubleshooting` T6 | 25/25/50 | 15/24/61 | 15/24/61 | 33/33/33 |
| `uaa-concepts` T1 | 30/29/41 | 30/29/41 | 30/29/41 | 33/33/34 |
| `uaa-concepts` T2 | 26/74 | 25/75 | 25/75 | 50/50 |
| `_oss_roles_table` | 11/7/7/8/9/8/9/6/9/10/8/10 | 11/7/7/8/9/8/9/6/9/10/8/10 | 11/7/7/8/9/8/9/6/9/10/8/10 | 11/7/7/8/9/8/9/6/9/10/8/10 |

The scale table's key column fits its 25% here: tables are wider than in the
other tools, so "Cloud Controller Worker" stays on one line without the
no-wrap pushing the column wider. In `metadata` the no-wrap key column
("(Optional) Key Prefix") takes 23% in the extension. `metadata` T3 is a
Markdown table in the source, so it is an AsciiDoc table in every mode,
passthrough included.

### Findings

1. **Converting the Markdown to AsciiDoc is its own step, with its own
  failures.** pandoc 3.12 converted the prose; a script around it handled
  what pandoc got wrong, and each of these silently changes a page:
  - pandoc drops raw HTML from AsciiDoc output, tables and `<pre>` blocks
    included, so HTML blocks must be set aside and put back as passthrough
    blocks;
  - in a list step that holds a nested list and then more paragraphs, it
    attaches the later paragraphs to the nested list's last bullet (two
    places; an open block around the step's content fixes it);
  - it leaves out a heading's id when the id matches the one pandoc would
    generate, but Asciidoctor generates a different one (`_subdomains`), so
    five in-page links went nowhere until every anchor was written out;
  - an image's alt text with commas must be quoted, or the commas start the
    width and height attributes (the alt text was cut at the first comma).
  The spot checks and the text comparison would not have caught the last
  three; they were found by reading the output and by a scan of the built
  pages for in-page links without a target.
2. **The default UI applies AsciiDoc's alignment specs.** Asciidoctor writes
  each cell's alignment as a class (`halign-center`, `valign-top`), and the
  UI's stylesheet has a rule for each, so `.<` and `^` in a table's specs work
  on the bare UI. Native is measured on the bare UI (decided). *Corrected:* an
  earlier version of this finding said the UI had no such rules, and the
  site's stylesheet repeated them; they are removed, and the tables render
  the same (checked in the browser).
3. **The default UI styles only AsciiDoc tables.** Its rules are written for
  `table.tableblock`, so every HTML table in passthrough renders without
  borders, at the body text size, with centered header cells
  ([screenshot](results/antora-credential-types-t1-passthrough-unstyled.png)).
  The site's stylesheet styles `table.table` like the UI's tables, header
  cells on the left included (a `style` on a cell still wins). Every
  HTML table names its style with a class (decided), so the four tables
  that had none get `class="table"` and all twelve look like the others.
4. **The default UI exposes no variables.** It is built with its variables
  resolved, so a site cannot change table padding, borders, or text size
  through settings; it overrides rules instead. The site's stylesheet adds
  `--table-font-size`, `--table-line-height`, `--table-nowrap-max`, and the
  two row-header variables (checked in the browser: each changes only what
  it names). Table text is smaller than the page's (15 pixels against 17),
  and the font-size default keeps it so. The UI spaces blocks with top margins
  only, so cells have no extra gap below their last paragraph (10 pixels
  above and below the text in the two-paragraph `uaa-concepts` cell).
5. **The default UI hyphenates.** It sets `hyphens: auto` on the page, so
  table cells break words with a hyphen ("al-phanumeric", "certifi-cate"),
  which the published page does not
  ([screenshot](results/antora-troubleshooting-t2-native-hyphenation.png)).
  Decided: no hyphenation in tables. The site's stylesheet sets
  `hyphens: none` on tables, in every mode.
6. **An AsciiDoc table without column specs has equal columns.**
  `native-plain` shows every table at 50/50, 33/33/33, or 25/25/25/25,
  whatever the content
  ([screenshot](results/antora-credential-types-t1-native-plain-equal-widths.png)).
  A column sized by its content has to be written `~`.
7. **Code spans need the literal form.** In a table cell, plain backticks
  still apply AsciiDoc's replacements, so `KEY in (VALUE1,VALUE2...)` showed
  `…`. Code that holds `...`, `_`, quotes, and the like is written
  `` `+…+` ``.
8. **No link check.** Neither Antora nor Asciidoctor reported a link to a
  missing anchor. A scan of the built pages found `#shadow` and
  `#user-groups` broken in `uaa-concepts`, as in Starlight (its finding 7);
  both are broken on the published page too.
9. **Typography comes from AsciiDoc's replacements.** Apostrophes in prose and
  in AsciiDoc table cells become typographic (`app’s`), as on the published
  site, but not in HTML passthrough blocks, and double quotes (`"sub"`) stay
  straight everywhere.
10. **The default UI is not versioned.** Its bundle is a build artifact at a
  moving URL; the site pins one build by its job URL and checks the file's
  hash.
11. **The wide table is drawn at its narrowest** (`_oss_roles_table`,
   added 2026-10-12). The site's script puts it in a 792-pixel box; at
   auto width the columns shrink to their longest words, 882 pixels in all,
   so the box scrolls. The activity column is about 95 pixels and wraps on
   every row; the table is 4851 pixels tall. native-plain writes equal
   widths, but they give way to the table's narrowest width, unlike on the
   other pages (finding 6). Passthrough cells are centered vertically, the
   AsciiDoc modes top-aligned. Antora reports nothing for the notes' links
   to pages not in the site (finding 8).

### Text compared with the published page

[checks/text-diff.py](checks/text-diff.py), run for every mode. Apart from the
decided backslash fix, the main text matches the published page except:

- **Quotes inside tables:** in passthrough the HTML tables keep straight
  apostrophes (`organization's`), and in every mode `"sub"` keeps straight
  double quotes (finding 9).
- **`Accept: */*` is kept.** The terminal blocks stay HTML in passthrough
  blocks, so nothing in them is read as markup, unlike Docusaurus (its
  finding 8) and Starlight.
- **Not reproduced, moved:** the same as Docusaurus — no *Page last updated*
  line or GitHub link, and the section links are the UI's table of contents.

### Raw passthrough

`make build-raw` builds the five pages with their tables' HTML unchanged
(only the variables and the partial line translated, and the prose converted
to AsciiDoc as in every mode). All five build without a message, and 32 of
36 spot checks pass:

| Page | Fails raw | Fixed by |
|------|-----------|----------|
| `credential-types` | class with typographic quotes | intent cleanup |
| `metadata` | two backslash checks | intent cleanup (decided fix) |
| `troubleshooting_slow_requests` | the Experiment 2 table follows its list instead of sitting in step 4 | indenting it under the step |
| `_oss_roles_table` (added 2026-10-12) | the two empty note markers | intent cleanup |

## Widths, alignment and font size

Checked on 2026-10-11 after the Docs WG lead reviewed the
[`credential-types` sample](../../poc/tables.md#credential-types).
Method and measurements:
[widths-alignment-fonts-2026-10-11.txt](results/widths-alignment-fonts-2026-10-11.txt).

- **Column 1 sized by its content in Docusaurus passthrough and
  extension.** Both modes keep the source's 20%: passthrough as
  `style={{width: '20%'}}` on the first `<th>`, extension as
  `widths="20 auto"`. Without it, column 1 measured 18% in both, the same
  as native, which has no width. Widths are hints
  ([principles](../README.md#principles)), so either form converts the
  table.
- **Docusaurus centers header cells because its theme does not align
  them.** Infima sets the header's colour, background and weight, not its
  alignment
  ([`table.pcss` L54-L58](https://github.com/facebookincubator/infima/blob/205b8aedc62496839991b75a8bc2922350766fe4/packages/core/styles/content/table.pcss#L54-L58)),
  so the browser's default for `th`, centered, shows
  ([HTML standard, tables rendering](https://html.spec.whatwg.org/multipage/rendering.html#tables-2)).
  Two ways change it, both checked: colons in the pipe table's delimiter
  row (`| :--- | :--- |`) set each column per table; one rule in the
  site's stylesheet, `.markdown th { text-align: start; }`, sets every
  table.
- **Pipe-table alignment colons**, the GitHub Flavored Markdown form
  (`:---` left, `:---:` center, `---:` right;
  [GFM spec, tables](https://github.github.com/gfm/#tables-extension-)):
  - Docusaurus (MDX with remark-gfm 4.0.1): each cell gets
    `style="text-align: …"`.
  - Zensical (Python-Markdown 3.11 tables): each cell gets
    `style="text-align: …"`
    ([`tables.py` L141-L145](https://github.com/Python-Markdown/markdown/blob/0ffbf00cf667971d46f43aafba825e8d25098bc5/markdown/extensions/tables.py#L141-L145)).
  - Starlight (Markdoc 0.5.10): each cell gets `align="…"`
    ([`schema.ts` L139, L149](https://github.com/markdoc/markdoc/blob/16e1840c687e17c57d2b3664eac4edfbd01e7283/src/schema.ts#L139-L149)),
    and Starlight's left alignment skips cells that have it
    ([`markdown.css` L156-L158](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/style/markdown.css#L156-L158)).
  - Antora: AsciiDoc has no pipe tables. Its own form aligns by column in
    `cols`, for example `[cols="<,^,>"]`
    ([Asciidoctor, align by column](https://docs.asciidoctor.org/asciidoc/latest/tables/align-by-column/)).
    Not built.

  Horizontal alignment per column is therefore native syntax in all four
  tools. Vertical alignment and padding are not, except in Antora.
- **Table font size is a stylesheet setting in every tool**, measured on
  `credential-types`:

  | Tool | Body text | Table text | Set by |
  |---|---|---|---|
  | Docusaurus | 16px | 16px | the theme sets none; this round's `--table-font-size` ([hints.css](sites/docusaurus/src/css/hints.css)) |
  | Zensical | 15px | 12.8px | the theme: `table:not([class])` at 12.8px ([`_typeset.scss` L486-L490](https://github.com/zensical/ui/blob/5d58e34f4240394d78ab89d149fdb3437151bac1/src/assets/stylesheets/modern/main/_typeset.scss#L486-L490); its build is the stylesheet Zensical 0.0.69 ships, `main.e15858d4.min.css`) |
  | Starlight | 16px | 16px | the theme sets none ([`markdown.css` L135-L139](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/style/markdown.css#L135-L139)); this round's `--table-font-size` ([hints.css](sites/starlight/src/styles/hints.css)) |
  | Antora | 17px | 15px | the default UI: `.doc table.tableblock` at 15px ([`doc.css` L253-L255](https://gitlab.com/antora/antora-ui-default/-/blob/0e38223adfd81eb74d4b1779e158f8ad05ff8923/src/css/doc.css#L253-L255)) |

  A smaller font makes content-sized columns narrower: Docusaurus native
  at 85% text, Zensical's ratio, gave column 1 16% instead of 18%. A fixed
  width such as 20% does not change.
- **Theming.** This evaluation uses each tool's default theme. A site's
  theme, or a page's, can set table font size, padding and alignment, and
  those decide how much room a column needs. The widths and screenshots
  here show the default themes, not limits of the tools.

## Wide tables: prose width and a continuation cue

Checked on 2026-10-12, after the roles table (`_oss_roles_table`) was found
laid out at its narrowest in every tool (Summary, "A real wide table
scrolls, but at its narrowest"). Measured in Chrome 155 at a 1280-pixel
window, with the continuation cues also run in Firefox 155 and WebKit 26.6.
Method and measurements:
[wide-tables-prose-width-cue-2026-10-12.txt](results/wide-tables-prose-width-cue-2026-10-12.txt).

- **Why the table is at its narrowest.** Docusaurus and Starlight show every
  table as a block that scrolls
  ([Infima `table.pcss` L24-L28](https://github.com/facebookincubator/infima/blob/205b8aedc62496839991b75a8bc2922350766fe4/packages/core/styles/content/table.pcss#L24-L28),
  [Starlight `markdown.css` L135-L139](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/style/markdown.css#L135-L139)).
  The rows then sit in an anonymous table box
  ([CSS 2.1, anonymous table objects](https://www.w3.org/TR/CSS21/tables.html#anonymous-boxes))
  whose width is shrink-to-fit
  ([CSS 2.1 §10.3.5](https://www.w3.org/TR/CSS21/visudet.html#shrink-to-fit-float)):
  the larger of its min-content width and the column, capped at its
  max-content width. The roles table's min-content width (1,053 to 1,092
  pixels) is above the column, so that is what it gets. Antora's table is
  `width: 100%`
  ([`doc.css` L204-L206](https://gitlab.com/antora/antora-ui-default/-/blob/0e38223adfd81eb74d4b1779e158f8ad05ff8923/src/css/doc.css#L204-L206)),
  and an auto-layout table is never narrower than its columns' minimum
  ([CSS 2.1 §17.5.2.2](https://www.w3.org/TR/CSS21/tables.html#auto-table-layout)):
  882 pixels in a 792-pixel box.
- **Why Zensical's columns are equal.** Not `table-layout` (it is `auto` in
  every mode) and not a rule of this round's for the classless tables. The
  theme's script wraps every table without a class in a box that scrolls
  ([`content/_/index.ts` L162-L163](https://github.com/zensical/ui/blob/5d58e34f4240394d78ab89d149fdb3437151bac1/src/assets/javascripts/components/content/_/index.ts#L162-L163),
  [`templates/table/index.tsx` L39-L47](https://github.com/zensical/ui/blob/5d58e34f4240394d78ab89d149fdb3437151bac1/src/assets/javascripts/templates/table/index.tsx#L39-L47)),
  whose inner box is shrink-to-fit
  ([`_typeset.scss` L600-L611](https://github.com/zensical/ui/blob/5d58e34f4240394d78ab89d149fdb3437151bac1/src/assets/stylesheets/modern/main/_typeset.scss#L600-L611)),
  so the table is again at min-content width. The theme gives every header
  cell `min-width: 5rem`
  ([`_typeset.scss` L533-L534](https://github.com/zensical/ui/blob/5d58e34f4240394d78ab89d149fdb3437151bac1/src/assets/stylesheets/modern/main/_typeset.scss#L533-L534)),
  100 pixels with the theme's 20-pixel root size and border-box sizing. No
  column of the roles table needs more than 100 pixels for its longest word,
  so all twelve are 100. In passthrough, `table.table` gets the same from the
  site's [hints.css](sites/zensical/docs/stylesheets/hints.css), which copies
  the theme's rules, the 5rem included.
- **A minimum width for the first column halves the table's height.** With
  `min-width` on the Activity column, extension mode (passthrough and native
  in the evidence file; at 24ch they are within 25 pixels of these heights):

  | First column | Docusaurus | Zensical | Starlight | Antora | Activity lines per row (max / median) | Rows that wrap |
  |---|---|---|---|---|---|---|
  | none (today) | 1060 × 5518 | 1204 × 4811 | 1092 × 5442 | 883 × 4851 | 10 / 4 | 42 of 42 |
  | 16ch | 1122 × 3752 | 1240 × 3648 | 1161 × 3316 | 924 × 3555 | 6 / 2 | 29–31 |
  | 20ch | 1166 × 3198 | 1275 × 2917 | 1203 × 2924 | 958 × 2787 | 4 / 2 | 25 |
  | 24ch | 1209 × 2859 | 1309 × 2688 | 1246 × 2621 | 992 × 2595 | 3 / 1–2 | 20–24 |
  | 30ch | 1275 × 2629 | 1361 × 2443 | 1310 × 2376 | 1043 × 2331 | 3 / 1 | 12–17 |

  Width × height in pixels. The column is 263, 207, 256 and 204 pixels at
  24ch: `ch` follows each tool's table font, so the lines per row are almost
  the same in every tool. Past 24ch the gain is small (64 lines in all rows
  at 24ch, 55 at 30ch, against 165 today) and the box shows one column
  fewer. At a 390-pixel window, 24ch takes 193 to 263 of the 356 to 390
  pixels, so the box shows the Activity column and one or two role columns
  before scrolling; `min(24ch, 45vw)` keeps it to 176 pixels there (4 to 6
  lines at most, median 2).
- **A floor on every prose column changes tables that fit.** The same
  `min-width` on every `role-prose` column of the extension pages changes the
  column widths of 10 or 11 other tables per tool at 24ch, and of 20 tables
  across the four tools even at 12ch (the Result / Explanation / Action
  tables shift by up to 23 pixels): a column's minimum also changes how the
  browser shares out spare width. From 20ch
  some tables no longer fit: `metadata` (two prose columns of four) is 734
  pixels in 703 in Docusaurus and 713 in 632 in Starlight; at 24ch also
  `uaa-concepts` and, in Starlight, two of the `troubleshooting_slow_requests`
  tables. The same floor on the first column of every table changes 53 of
  the 56 native tables, since most first columns are key columns. The floor
  therefore needs a scope: tables that are wide.
- **What says a table is wide.** Passthrough and native have no role
  classes, and Docusaurus and Zensical pipe tables take no class at all
  ([Template conventions](README.md#template-conventions)). A selector on
  the number of columns needs neither:
  `table:has(> thead > tr > :nth-child(8)) tr > :first-child`. In the
  survey only three tables have more than six columns, all three role
  matrices with the label column first (11 and 12 columns). Built into each
  site's stylesheet, it gives the 24ch layout above in every mode of every
  tool, and none of the other 210 test tables changes, at 1280 or 390
  pixels; `make check-wide`'s check passes (90, 120, 120, 120). A table
  class (a `table-*` style) would say the same where a table can carry one:
  passthrough HTML, the list-table styles, Markdoc's
  `{% table .name %}` (also in Starlight native), an AsciiDoc role; not a
  Docusaurus or Zensical pipe table.
- **A scroll shadow shows that more columns follow.** Two shadows fixed to
  the box's edges, under two covers in the page colour that scroll with the
  content (`background-attachment: local`;
  [CSS Backgrounds 3](https://www.w3.org/TR/css-backgrounds-3/#background-attachment)):
  a shadow shows on each side that has more columns and disappears at that
  end. Measured at the box's edges in every mode of all four tools, light
  and dark (Antora: light only), in Chrome, Firefox and WebKit: a mean change of 24 to 40
  luminance levels at the right edge before scrolling, 0 at the end, and
  the same on the left once scrolled. It runs down the whole box, so it is
  in view wherever the reader is. It is the box's background, so an opaque
  cell background would cover it: none of the default themes has one, but
  Zensical gives a classless table the page colour, which the site makes
  transparent inside the theme's wrapper. The cover needs a solid page
  colour: Docusaurus's light `--ifm-background-color` is transparent, so the
  surface colour is used there; Antora's default UI has no dark mode and no
  colour variables, so its colour is written as white. Tables that fit show
  no shadow (no visible change on the other test pages; pixels differ only
  along text and border edges in Zensical, from antialiasing).
- **A sticky first column works, with a fix per theme, and is not a cue by
  itself.** `position: sticky; left: 0` on the first cells keeps the labels
  in view while scrolling. It needs an opaque background in the page colour
  (and, in Docusaurus, the row stripe laid over it), and a line drawn with
  an inset `box-shadow`: the collapsed borders stay behind in Antora
  (Chrome) and in Docusaurus (Firefox, WebKit), and Starlight has no
  vertical lines. In Zensical, classless tables did not stick at all: the
  theme makes the table a scroll container of its own (`overflow: auto`,
  [`_typeset.scss` L486-L489](https://github.com/zensical/ui/blob/5d58e34f4240394d78ab89d149fdb3437151bac1/src/assets/stylesheets/modern/main/_typeset.scss#L486-L489)),
  so the cells stuck to a box that never scrolls; `overflow: visible` on
  the table inside the wrapper fixes it. With the 24ch floor the sticky
  column holds 204 to 263 pixels of the box, and at 390 pixels most of it.
- **A forced scrollbar is no cue for this table.** Overlay scrollbars take
  no room in any of the four. `::-webkit-scrollbar` makes Chrome draw a
  10-pixel scrollbar in Docusaurus, Zensical and Starlight, but not in
  Antora, whose UI sets `scrollbar-width` and `scrollbar-color` on every
  element
  ([`base.css` L116-L126](https://gitlab.com/antora/antora-ui-default/-/blob/0e38223adfd81eb74d4b1779e158f8ad05ff8923/src/css/base.css#L116-L126);
  that Chrome then ignores `::-webkit-scrollbar` is unverified). In
  Firefox and WebKit, run headless, no scrollbar took room with or without
  the rule; Safari itself was not tested. Either way the scrollbar is at the
  bottom of the box: 4,000 to 4,700 pixels below the window when the top of
  the table is in view, and still 1,750 to 2,040 with the 24ch floor.
- **Compact does not make the Activity column wrap more.** With the table
  text at 85% and half the cell padding, Docusaurus and Starlight wrap
  exactly as before (165 lines, 10 at most): the table stays at min-content
  width, and the column narrows with the font. Zensical wraps less (113 to 121
  lines; the 100-pixel columns stay while the text shrinks), and Antora
  much less: the table fits its 792 pixels and stops scrolling (83 or 84
  lines), except in native-plain, where the equal widths then apply and the
  column wraps as before. With the 24ch floor, compact keeps about the
  floor's lines per row (63 to 67 in all rows, against 63 to 71) and cuts
  the height to 2,078 (Docusaurus), 1,831 (Zensical), 2,002 (Starlight) and
  1,859 pixels (Antora, where all twelve columns fit); 8, 6 and 7 columns
  are in view instead of 6, 5 and 5.

**Applied** (2026-10-12), from these measurements:

- A wide table's first column gets `min-width: 24ch`, set by a
  `--table-prose-min` variable and scoped by the number of columns (eight
  or more), so pipe tables are covered. A `table-*` class can give the
  same scope to a table that is wide for other reasons; that is not built
  yet. The `prose` role alone is not a safe carrier, because it changes
  tables that fit.
- Every scroll box gets the scroll shadow. A sticky first column is left
  as an option for a style, not the default.
- A compact style is usable on the role matrices once the floor is in
  place (compact itself is not built yet).

The change is one rule for the floor and one for the shadow in each site's
`hints.css` (Docusaurus, Zensical, Starlight, Antora); no page changes and
no script. Screenshots before and after, extension and native mode:
`results/<tool>-roles-<mode>-before.png` and `-after.png`.

## Classes and ids on pipe tables

Checked on 2026-10-12. Method and measurements:
[classes-ids-on-pipe-tables-2026-10-12.txt](results/classes-ids-on-pipe-tables-2026-10-12.txt).

No tool attaches a class or an id to a Markdown pipe table natively. One
HTML comment, written the same way in every tool, does it with a small
extension:

```markdown
<!-- table: .table-compact #label-requirements -->
**Label requirements**

| Part of Label | Length in characters | Allowed characters | Other Requirements |
| --- | --- | --- | --- |
```

`.name` adds a class (several allowed) and `#name` sets the id. The
comment sits in the block just above the table, or just above the
table's title (a paragraph that is one bold run); a blank line in
between is optional. Only one title is skipped, and any other block in
between stops it. Class and id go on the `<table>`, never on the title.
On GitHub the comment is hidden and the table renders as before; an
attribute line such as `{.table-compact}` would show as an extra row
after the table or as text before it.

- **Docusaurus** (MDX 3.1.1, remark-gfm 4.0.1). `{...}` next to a table
  is a JavaScript expression and fails to parse. HTML comments are
  accepted but dropped from the tree: Docusaurus parses them with a fork
  of remark-comment
  ([processor.ts L86-L87, L152](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-mdx-loader/src/processor.ts#L86-L87),
  on by default:
  [configValidation.ts L130-L131](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus/src/server/configValidation.ts#L130-L131)),
  which keeps a node only with an `ast` option Docusaurus does not pass
  ([index.js L35-L60](https://github.com/slorber/remark-comment/blob/426dde74a26d9d9adfe1a649d602366c46027350/index.js#L35-L60)).
  The extension, a remark plugin of 44 lines, finds the title in the tree
  and reads the comment from the page source, then sets the table's
  `hProperties`, which reach the `<table>`
  ([state.js L352-L382](https://github.com/syntax-tree/mdast-util-to-hast/blob/174795b21f7757fffb54dd8d5fb4012f4751f791/lib/state.js#L352-L382)).
- **Zensical** (Python-Markdown 3.11). A `{: }` line after a table
  becomes a row, since every line of the block is one
  ([tables.py L87-L107](https://github.com/Python-Markdown/markdown/blob/0ffbf00cf667971d46f43aafba825e8d25098bc5/markdown/extensions/tables.py#L87-L107));
  attribute lists reach cells, not the table
  ([attr_list.py L103-L154](https://github.com/Python-Markdown/markdown/blob/0ffbf00cf667971d46f43aafba825e8d25098bc5/markdown/extensions/attr_list.py#L103-L154)).
  The extension (79 lines) reads the comment from the raw-HTML stash
  after inline processing. A table given a class also gets `table`: the
  theme styles and wraps only tables without a class
  ([`_typeset.scss` L486-L490](https://github.com/zensical/ui/blob/5d58e34f4240394d78ab89d149fdb3437151bac1/src/assets/stylesheets/modern/main/_typeset.scss#L486-L490)),
  and the site's `table.table` rules give the look and the scroll box
  back. Without it, classed tables lost both (the page widened); with it,
  every wide-table check passes. The comment stays in the HTML output as
  a comment.
- **Starlight** (Markdoc 0.5.10). An annotation line beside a pipe table
  is an error, "Can't apply inline annotations to 'document'"
  ([parser.ts L118-L125](https://github.com/markdoc/markdoc/blob/16e1840c687e17c57d2b3664eac4edfbd01e7283/src/parser.ts#L118-L125));
  in a header cell it lands on that cell. Astro turns comments into
  nodes
  ([tokenizer.ts L11-L15](https://github.com/withastro/astro/blob/3571e2d2e80a66764254fa9b7750704a150ca3f6/packages/integrations/markdoc/src/tokenizer.ts#L11-L15)),
  so the comment and the title are sibling nodes of the table. The
  extension, a document transform of 45 lines, copies class and id to
  the table node, which renders the global `class` and `id`
  ([transformer.ts L17-L19](https://github.com/markdoc/markdoc/blob/16e1840c687e17c57d2b3664eac4edfbd01e7283/src/transformer.ts#L17-L19)).
- **Antora.** AsciiDoc has no pipe tables; a GFM pipe table renders as a
  paragraph. Its own table takes both in the block attributes,
  `[.table-compact#label-requirements]`
  ([html5.rb L856-L878](https://github.com/asciidoctor/asciidoctor/blob/2c03d22eb9fe83d04ee452939581d1b842f6d8b4/lib/asciidoctor/converter/html5.rb#L856-L878)),
  and the roles table already keeps its id.
- **Without an extension**, an HTML `<div>` around the pipe table can
  carry the class and id in all three tools, but on the wrapper, and
  spelled differently in each (`className` in MDX, a `markdown`
  attribute in Zensical).

With the extensions, the native roles table keeps
`id="oss-roles-permissions"` and the `metadata` Label requirements
table gets `id="label-requirements"` in Docusaurus, Zensical and
Starlight; nothing else on any page changes. Spot checks and wide-table
checks give the same results as before.
