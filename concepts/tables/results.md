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
- **With cleanup, every table renders correctly in all three modes.** 33 of
  35 spot checks pass in each mode; the two that fail are the page
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
  headers, and captions need either HTML (passthrough) or custom code
  (extension). #1642 §5 rules out custom React; the extension here is a
  remark plugin, which is also custom code.
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
| | extension | yes | preserved; title row is a caption (provisional) | caption, row headers, no wrap on key column (26%) | list-table with nested lists: readable |
| | native | yes, lists as inline HTML in cells | preserved; title is a bold line above the table, not part of it | none; cells vertically centered | pipe table with inline `<ul>`: hard to edit |
| `troubleshooting_slow_requests` | passthrough | after cleanup: `<tbody>`, one multi-line cell, plus `<br />` outside the tables | preserved after nesting the Experiment 2 table in its list step | variant A, as written | HTML |
| | extension | yes | preserved | variant B 25/25/50 in all six; variant C by content | list-table |
| | native | yes | preserved after adding a blank line before each table | none (same as variant C) | pipe table |
| `uaa-concepts` | passthrough | after cleanup: `</td>` → `</tr>`, plus `{…}` placeholders escaped in prose | preserved | widths 30% and 25% | HTML |
| | extension | yes | preserved; `<br/><br/>` became two paragraphs (provisional) | widths, row headers, no wrap | list-table; paragraphs as in Markdown |
| | native | yes | preserved, `<br /><br />` kept | none (27/30/43, 25/74) | pipe table |

### Width variants for `troubleshooting_slow_requests`

Column widths in percent of the table, per table (Experiment 1–6). Table 2
sits inside a numbered list, so it is narrower (671 pixels).

| Variant | T1 | T2 | T3 | T4 | T5 | T6 |
|---------|----|----|----|----|----|----|
| A — as written (passthrough) | 33/25/42 | 25/36/39 | 25/31/44 | 25/23/52 | 25/25/50 | 25/25/50 |
| B — uniform 25/25/50 (extension) | 25/25/50 | 25/25/50 | 25/25/50 | 25/25/50 | 25/25/50 | 25/25/50 |
| C — roles only (extension; native is the same) | 33/25/42 | 28/35/37 | 19/33/48 | 17/24/59 | 20/23/57 | 17/25/58 |

Table 2 in each variant: [A](results/docusaurus-troubleshooting-t2-A-as-written.png),
[B](results/docusaurus-troubleshooting-t2-B-uniform.png),
[C](results/docusaurus-troubleshooting-t2-C-roles-only.png).

### Provisional changes, side by side

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
  The hints need a stated precedence; this site lets wrapping lose to the
  content and width lose to wrapping.
2. **Row headers take the header style.** With `stub-columns`, the key column
  becomes `<th scope="row">`, which the default theme draws bold and
  centered. Whether row headers look like column headers is a template
  decision.
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
  tables.

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
