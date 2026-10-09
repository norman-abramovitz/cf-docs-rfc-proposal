# Concept: Tables

Status: **In progress**.

## Progress

What has been done in this round, newest last. Each line links to the work.

- [x] **Sources copied.** The five test pages and the variables they use, verbatim
  from upstream, with commits and licenses: [source/SOURCES.md](source/SOURCES.md).
  Two variables the pages use (`metadata_ref`, `bosh_cli_link`) are not defined
  anywhere in the book, so the published pages show them as empty text.
- [x] **Intent written.** For every table, the hints that express what the
  source asks for, the markup cleanup it needs, the deviations from the
  published page, and a list of spot checks every converted version must pass:
  [intent/](intent/). Two proposed deviations await review: rendering
  `[a-z0-9A-Z]` without the stray backslashes the published `metadata` page
  shows, and giving all six `troubleshooting_slow_requests` tables the same
  column widths.
- [ ] Docusaurus site: passthrough, extension, native.
- [ ] Zensical site.
- [ ] Astro/Starlight site.
- [ ] Antora site.
- [ ] Probes: Eleventy, Sphinx/MyST, Middleman without Bookbinder.
- [ ] Results summary.

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
Exact behavior per tool is to be confirmed in this round, not assumed.

## Hints for tables

First draft, taken from what the test pages do. Hints are written once per
table, independent of any tool.

| Level | Hint | Values | Seen in |
|-------|------|--------|---------|
| Table | caption | text | `metadata`: a centered row spanning all four columns is really a caption |
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
│   ├── starlight/     │ with `make build` and `make serve`
│   └── antora/        ┘
├── probes/            eleventy/, sphinx/, middleman/
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

- Does the open-source requirement cover services (search, hosting, analytics)
  as well as code? Algolia DocSearch's index and GitHub Pages are proprietary
  services.
- Is a `pattern` hint (a named table shape) a table hint or a template
  feature?
- Should the copyright year follow content changes rather than the build date?
  A format-only conversion may not warrant a new year. See
  [Concepts](../README.md).
