# Concept: Tables

Status: **Done, with open items** (listed under
[Open questions](#open-questions)). Results: [results.md](results.md).

Terms used below:

- **Modes.** Each page is converted three ways: *passthrough* (the HTML as
  written), *extension* (the tool's extension point carrying the hints), and
  *native* (the tool's own table syntax). *native-plain* is native without
  width or alignment specs. See [Method](#method).
- **Hints.** What a table asks for, independent of any tool: a column's
  *role* (`key`, `value`, `prose`), its width, whether it avoids wrapping
  (*no-wrap*, up to a *cap*), row headers, a title. See
  [Hints for tables](#hints-for-tables).
- **Spot checks.** Per-table checks every converted page must pass, listed
  in each [intent](intent/) file and run by [checks/](checks/).
- **Variants A, B, C.** Three ways of setting widths on the
  `troubleshooting_slow_requests` tables: as written, uniform, roles only.

## Progress

What has been done in this round, newest last. Each line links to the work.

- [x] **Sources copied.** The five test pages and the variables they use, verbatim
  from upstream, with commits and licenses: [source/SOURCES.md](source/SOURCES.md).
  Two variables the pages use (`metadata_ref`, `bosh_cli_link`) are not defined
  anywhere in the book, so the published pages show them as empty text.
- [x] **Intent written.** For every table, the hints that express what the
  source asks for, the markup cleanup it needs, the deviations from the
  published page, and a list of spot checks every converted version must pass:
  [intent/](intent/).
- [x] **Intent reviewed.** The stray backslashes the published `metadata`
  page shows (`\[a-z0-9A-Z\]`) are treated as a source defect and removed.
  The six `troubleshooting_slow_requests` tables are rendered with three width
  variants (as written, uniform, roles only) to compare. Two changes stay
  provisional until the renderings are compared: a caption instead of the
  spanning title row in `metadata`, and real paragraphs instead of
  `<br/><br/>` in `uaa-concepts`.
- [x] **Docusaurus done.** None of the five pages builds with its HTML
  unchanged; three of the five first errors are outside the tables. After
  cleanup every table renders correctly in all three modes. Docusaurus has no
  native table hints: widths and captions need HTML or a custom plugin. Results,
  width variants, and side-by-side screenshots: [results.md](results.md#docusaurus-3102).
- [x] **Renderings reviewed.** The `metadata` title stays a spanning row, not a
  caption. The `<br/><br/>` in `uaa-concepts` is a paragraph break, so the
  cell holds two paragraphs. The `troubleshooting_slow_requests` tables use
  variant C, no widths: the column roles decide. These are now
  [template conventions](#template-conventions).
- [x] **Hint rules decided.** "Don't wrap" wins over a width, up to a cap
  past which the text wraps between words. Row headers get their own
  styling. The `*/*` lost in terminal output (results finding 8) is left to
  the code blocks concept.
- [x] **Zensical done.** All five pages build with their HTML unchanged, and
  the variables keep their `<%= vars.name %>` form. With the intent files'
  cleanup every table renders correctly in all three modes. The default theme
  styles only tables without a `class`, so tables that keep `class="table"`
  lose the theme's table style (later styled through the class; see
  [Template conventions](#template-conventions)). Native pipe tables can
  carry widths on header cells; row headers and the title row need HTML or
  a custom extension.
  Results and findings: [results.md](results.md#zensical-0069).
- [x] **Starlight done.** Pages are Markdoc with HTML allowed. Four of the
  five pages parse with their HTML unchanged, but Markdoc reads the text inside
  HTML as Markdown: a lone `-` in code becomes a list and spaces next to
  inline tags disappear, with no error, so passthrough needs a few forced
  changes. Markdoc's own table tag holds lists and paragraphs in cells and
  widths on header cells without custom code; row headers and a title row
  above the column headers need the extension. Results and findings:
  [results.md](results.md#starlight-0426).
- [x] **Starlight reviewed.** The `metadata` title moves to a bold line above
  the table in every converted mode of every tool, because Markdown tables
  have one header row. Markdoc's changes to passthrough HTML are recorded as
  "Markdoc cannot take the HTML as is", with examples. Joining table cells
  onto one line is not adopted as a conversion rule, for source readability.
- [x] **Antora done.** Antora reads AsciiDoc, so every page is rewritten
  from Markdown in every mode; that conversion has failures of its own, which
  a converter must handle. HTML tables build unchanged inside passthrough
  blocks. AsciiDoc's own table carries widths, row headers, top alignment and
  lists in cells; the extension needs no code, only roles and a stylesheet.
  The default UI styles only AsciiDoc tables and hyphenates words in cells,
  so the site's stylesheet styles HTML tables with `class="table"` and turns
  hyphenation off. Results and findings:
  [results.md](results.md#antora-321).
- [x] **Sphinx/MyST probe done.** The scale table is a MyST `list-table`.
  Its directive options carry the header row, row headers and widths;
  classes on the table carry the column roles, the capped no-wrap and
  `class="table"`, given meaning by a small stylesheet, with no code.
  Variables come from the shared file as substitutions. The default theme
  hyphenates words in cells, so the stylesheet turns that off. All five spot
  checks pass. Details: [probes/sphinx-myst](probes/sphinx-myst/README.md).
- [x] **Eleventy probe done.** `uaa-concepts` builds with its
  `<%= vars.name %>` tags left as they are and read as EJS, and its tables
  come out exactly as written. EJS is a plugin since Eleventy 3. EJS's `<%=`
  escapes HTML, where Middleman's ERB does not, so a conversion must write
  `<%-` for any HTML-valued variable or helper, and for includes. An include
  needs the full file name where ERB's `partial` does not. Details:
  [probes/eleventy](probes/eleventy/README.md).
- [x] **Middleman probe done.** Middleman 4.6.3 without Bookbinder builds
  all five pages unchanged on Ruby 4.0.7, with a short config file (the
  book's Markdown settings and its `vars` helper) and a small layout. Every
  table matches the published page cell for cell, and variables and the
  partial behave as in the book. Ruby 4.0 needs one extra gem (`ostruct`).
  Details: [probes/middleman](probes/middleman/README.md).
- [x] **Results summarized.** [results.md](results.md#summary) opens with
  a summary across the four tools and the three probes; what the round
  taught is under [What we learned](#what-we-learned) below.
- [x] **Table styles surveyed.** Every table in the docs repos and the
  tutorial repos (241) was counted to find which table styles the template
  needs beyond the standard one. The only class any source uses is
  `table`; the closest thing to a second style is a compact one for
  comparison grids and long reference tables. Which styles to support is
  still open (see [Open questions](#open-questions)).
- [x] **Example style: `table-media`.** To show how a style beyond `table`
  is added, the survey's image-grid family got one: no cell borders, a rule
  under the header, centered cells, images filling their cells. The first
  section of `uaa-performance` is the test page, in every mode of all four
  tools; all spot checks pass. Each site's `CONVENTIONS.md` has an "Adding
  a style" section: where the CSS lives and how a table names its style.

## What we learned

- **Every tool can render these tables.** After cleanup, every test table
  renders correctly in every tool and every mode. The tools differ in the
  cost of getting there, not in the result.
- **The HTML needs cleanup before any strict tool reads it.** The defects
  browsers tolerate ([below](#markup-that-only-browsers-tolerate)) break MDX
  and change content in Markdoc. Zensical, Eleventy and Middleman take the
  HTML as written; Antora takes it inside passthrough blocks but needs every
  page rewritten as AsciiDoc around it.
- **List-table syntaxes carry most hints; pipe tables carry few.** Markdoc's
  table tag, AsciiDoc tables and MyST's `list-table` hold lists, paragraphs,
  widths and spans. Markdown pipe tables hold one line per cell and no
  widths (Zensical adds widths on header cells), so lists stay inline HTML.
- **Two hints need CSS in every tool:** the column roles and the capped
  no-wrap. Where a table takes classes (Antora, Sphinx), that is CSS only;
  Docusaurus, Zensical and Starlight need a small extension.
- **The template sets the look, through a class.** Themes disagree on which
  tables they style, so every HTML table names its style with a class;
  `table` is the standard style. Themes that hyphenate get it turned off in
  tables. A further style is one more class and a few CSS rules
  (`table-media`); Starlight's and Antora's own table syntax can name it,
  while a Markdown pipe table needs the extension.
- **Some changes sit outside the tables and still block a page:** heading
  anchors written as `<a id>` (MDX), terminal blocks (MDX, Markdoc), the `*`
  in `Accept: */*` (MDX, Markdoc), and variable escaping (MDX, Markdoc,
  EJS). They belong to their own concepts.

## Why tables first

The Docs WG lead identified five pages whose tables are hard to express outside
HTML. They are the core of the concern that the current content cannot simply
be rewritten in Markdown. Headings would be an easier first concept, but would
not address that concern.

## Test pages

| Page | Repository | Tables |
|------|------------|--------|
| `_oss_scale_table.html.md.erb` (partial) | cloudfoundry/docs-cloudfoundry-concepts | 1 |
| `metadata.html.md.erb` | cloudfoundry/docs-cf-admin | 2 HTML, 1 Markdown |
| `troubleshooting_slow_requests.html.md.erb` | cloudfoundry/docs-cf-admin | 6 |
| `uaa-concepts.html.md.erb` | cloudfoundry/docs-uaa | 2 |
| `credential-types.html.md.erb` | cloudfoundry/docs-credhub | 1 |
| `uaa-performance.html.md.erb` (first section) | cloudfoundry/docs-running-cf | 1 of 12 |

`uaa-performance` was added after the round, as the example for a second
table style (see [Template conventions](#template-conventions)). The traits
below are the first five pages'.

### What the pages have in common

- **Key-to-prose shape.** Each table has a short first column (a component,
  label part, result, grant type, or credential type, often in `<code>`) and a
  last column of sentences or paragraphs.
- **Column widths.** Four of the five pages set widths, in four different ways:
  `<col width>`, `<th width>`, `<td width>`, and `<th style="width:…">`.
- **Variables inside cells.** Four of the five use `<%= vars.* %>` inside
  `<td>`.
- **Block content in cells.** Lists (`metadata`) and paragraph breaks
  (`uaa-concepts`).
- **Reuse.** `_oss_scale_table` is a partial included from
  `high-availability.html.md.erb`.

### Markup that only browsers tolerate

A strict parse of each table (ERB replaced, entities numeric) shows 5 of 12
tables, on 4 of 5 pages, are not well-formed:

| Page | Defect |
|------|--------|
| `_oss_scale_table` | `<col width="25%">` is not self-closed |
| `metadata` (both HTML tables) | A `<td>` containing a `<ul>` is never closed before the next `<td>` |
| `credential-types` | `class=“table”` uses typographic quotes |
| `uaa-concepts` | The `implicit` row ends with `</td>` instead of `</tr>` |

Browsers repair these silently. Tools that parse HTML as JSX (MDX) or as XML
need well-formed markup, so cleanup is a likely first step of any conversion.
What each tool did with them: [results.md](results.md#summary).

## Hints for tables

First draft, taken from what the test pages do. Hints are written once per
table, independent of any tool. *Superseded* by
[Hints after the round](#hints-after-the-round); kept as the record.

| Level | Hint | Values | Seen in |
|-------|------|--------|---------|
| Table | title | text | `metadata`: a centered row spanning all four columns, above the column headers |
| Table | header row | yes / no | all |
| Table | row-header column | yes / no | first column acting as row labels |
| Table | pattern | name | `troubleshooting_slow_requests`: Result / Explanation / Action, six times |
| Column | role | `key`, `value`, `prose` | first and last columns everywhere |
| Column | width | range or relative weight (e.g. 10–15%, 40%) | four of five pages |
| Column | wrap | `avoid`, `normal` | key columns |
| Column | align | horizontal `left` / `center` / `right`; vertical `top` / `middle` | — |
| Cell | block content | lists, paragraphs | `metadata`, `uaa-concepts` |

Default: `role: key` implies a narrow column, `wrap: avoid`, and top alignment,
so most tables need only one or two hints.

Example: a five-column table with widths 10–15% / 10–15% / 40% / 10–15% /
10–15%, where column 1 avoids wrapping and is top-aligned, and column 4 is
centered vertically and horizontally.

### Hints after the round

| Level | Hint | Values | Change from the first draft |
|-------|------|--------|-----------------------------|
| Table | title | text | Shown as a bold line above the table, not a row or caption: Markdown tables have one header row |
| Table | header row | yes / no | Unchanged; every table in the docs repos has one |
| Table | row-header column | yes / no | Unchanged; row headers are styled apart from column headers and body cells |
| Table | style | `table` (standard), `table-media` (example); further names to be picked | New. HTML tables carry it as a class; a Markdown table gets the standard style |
| Table | pattern | — | Dropped: the Result / Explanation / Action tables set no widths, and the roles decide |
| Column | role | `key`, `value`, `prose` | Unchanged; carried as classes |
| Column | width | relative weight | Kept where the source sets one; roles decide otherwise |
| Column | wrap | `avoid`, `normal` | `avoid` wins over a width, up to a cap the template sets |
| Column | align | horizontal, vertical | Defaults differ by theme (Docusaurus pipe tables center cells vertically); Antora's specs carry top alignment natively; elsewhere the extensions set it |
| Cell | block content | lists, paragraphs | `<br/><br/>` between two blocks of text is a paragraph break |

### Template conventions

Some source markup only restates what the site template should do anyway.
Conversions drop that markup and rely on the template instead:

- **Header cells are bold.** `<th><strong>…</strong></th>` becomes `<th>…</th>`.
- **A table title is a line above the table.** It is a bold line before the
  table, not a caption and not a row: Markdown tables have one header row,
  which stays for the column headers. (Decided first as a spanning row;
  changed after the Starlight round.)
- **A paragraph break in a cell is a paragraph.** `<br/><br/>` between two
  blocks of text becomes two paragraphs.
- **Widths follow the column roles.** A table with the Result / Explanation /
  Action pattern sets no widths; `key` and `prose` decide.
- **"Don't wrap" beats a width.** A `wrap: avoid` column grows past its width
  to keep its text on one line, so column widths vary with the content. Past
  a cap the template sets, the text wraps between words after all.
- **Row headers are styled on their own.** The template can set their look
  apart from column headers and body cells.
- **Every HTML table names its style with a class.** `class="table"` is the
  standard style, the one most tables use; a conversion adds it to a table
  that has no class. A Markdown table cannot carry a class, so it gets the
  standard style; another style needs the extension. `table-media`, an
  image grid, is the example of a second style; each site's
  `CONVENTIONS.md` shows how it is added. Which further styles to
  support (candidates: compact, boxed, plain, striped) is decided from the
  survey of every table in the docs and tutorial repos; it is still open.
- **A wide table scrolls in its own box.** A table wider than the content
  column scrolls sideways inside a box of its own; the page never scrolls
  sideways because of a table. A `table-media` grid shrinks its images to
  fit instead. Each site's `make check-wide` checks this in a browser
  ([results](results.md)).

## Method

For each table on each test page:

1. **Read the intent.** Translate the source's exact values into hints (for
   example, `width="25%"` on a `<code>` column becomes `role: key`). Record any
   deviation from the source and the reason. Output: `intent/<page>.md`.
2. **Convert by hand into each hands-on tool, three ways:**
   - **passthrough** — the HTML unchanged, translating only variables and
     partials to the tool's syntax;
   - **extension** — the tool's own extension mechanism carrying the hints;
   - **native** — the tool's native table syntax plus whatever hint mechanism
     it offers.
3. **Build and judge.** Does it build? Are content and outline preserved
   ideally? Which hints are honored? How readable is the source for an author?
4. **Record the convention** for each tool and mode that works. These become
   the rules `cf-docs-migrate convert` implements.

The pages use variables and one partial, so each site needs minimal variable
and include support to build. That support is part of this concept, not a
separate one. Each tool's default theme is used; hints must work under any
theme.

### Probes

| Tool | Question |
|------|----------|
| Eleventy | Do `<%= vars.* %>` tags render unchanged as EJS? |
| Sphinx/MyST | Can `list-table` directive options carry the hints? |
| Middleman without Bookbinder | What is the smallest change that removes Bookbinder and keeps ERB and HTML? |

## Layout

```
concepts/tables/
├── README.md          this file
├── source/            test pages, verbatim, plus SOURCES.md
├── intent/<page>.md   hints per table and recorded deviations
├── sites/
│   ├── zensical/      ┐ one minimal site per hands-on tool, versions pinned,
│   ├── docusaurus/    │ each page in passthrough/, extension/, native/,
│   ├── starlight/     │ and native-plain/ where it differs, with
│   └── antora/        ┘ `make build`, `make serve` and `make check`
├── checks/            spot checks and text comparison shared by every site
├── probes/            eleventy/, sphinx-myst/, middleman/
└── results.md         comparison grid; screenshots in results/
```

`source/SOURCES.md` records, for each page, the repository, path, commit, and
license. The content repositories are Apache-2.0 licensed (docs-uaa via its
NOTICE file). Source copies stay verbatim; all changes live in `sites/` and
`probes/`.

## Results grid

`results.md` has one row per page × tool × mode:

| Column | Values |
|--------|--------|
| Builds | yes / no (error) |
| Content and outline | preserved / changed (note) / lost (note) |
| Hints honored | list of hints, with screenshots |
| Source readability | short judgment from an author's point of view |
| Convention | the pattern used, linked from the tool's conventions |

The content and outline check is manual in this round. An automated check
(text and heading extraction compared against the published page) belongs to
`cf-docs-migrate`, and must treat build-time values such as the copyright year
as expected differences.

## Toolchains

Node for Docusaurus, Starlight, and Antora; `uv` for Zensical and Sphinx. Each
site pins its tool versions so results can be reproduced. Nothing is installed
globally.

## Open questions

Left open by this round:

- **Table styles.** Which styles beyond `table` the template supports. The
  survey found only `table` in use; a compact style has the most evidence.
  `table-media` exists as the example of how a style is added.
- **Deferred to other concepts:** the `*` lost in `Accept: */*` (MDX,
  Markdoc), terminal blocks (MDX, Markdoc), heading anchors written as
  `<a id>` (MDX), page descriptions that contain variables (Docusaurus), a
  list right after a text line (Zensical), and HTML-valued variables that
  are escaped (MDX, Markdoc, EJS).
- **On-paper tools.** Hugo and VitePress (see [Concepts](../README.md)) were
  not part of this round.

From before the round:

- Does the open-source requirement cover services (search, hosting, analytics)
  as well as code? Algolia DocSearch's index and GitHub Pages are proprietary
  services.
- Is a `pattern` hint (a named table shape) a table hint or a template
  feature? *Answered by this round:* neither is needed for the test pages.
  The Result / Explanation / Action tables set no widths, and the column
  roles decide.
- Should the copyright year follow content changes rather than the build date?
  A format-only conversion may not warrant a new year. See
  [Concepts](../README.md).
