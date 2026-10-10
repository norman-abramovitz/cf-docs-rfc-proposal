# Tooling

Status: draft, incomplete — covers what is known as of 2026-10-10.

This document describes the tools evaluated for the Cloud Foundry
documentation, the input formats they read, how today's pages are converted
into them, the extensions each tool needs, and the problems found on the way.
It is neutral evidence: it describes what was built and seen, and makes no
choice. Every tool's status is "under evaluation"; Hugo and VitePress are
"not yet assessed".

Parts:

- [formats.md](formats.md): each input format, with one table from a real
  page written in every one of them.
- [tools.md](tools.md): each tool, what was done with it, what was seen,
  and what was passed over.
- [poc-scope.md](poc-scope.md): what RFC #1642 asks its proof of concept to
  cover, and what these findings add.

Requirements are cited by ID and a short phrase, for example "[R-03](../requirements/README.md#r-03) column
widths as hints". The IDs and their full statements are in
[requirements/](../requirements/README.md). Terms are defined where they
are first used; the [glossary](../glossary.md) has more on each.

## Why tooling first

The CF documentation today is written as `.html.md.erb` files: Markdown
(plain text with light formatting marks such as `#` for headings) mixed with
HTML (the markup language of web pages) and ERB tags (`<%= … %>`, Ruby
code that fills in variables and includes other files when the site is
built). Bookbinder, a tool written for the CF docs, collects these files
from many repositories and hands them to Middleman, a Ruby static site
generator (a program that turns source files into a set of web pages).

RFC #1642 (the draft proposal for a new CF docs stack) asks for Markdown
authoring and, in the same list, for the
[ability to handle HTML](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L42):

> Ability to handle HTML, especially HTML tables with column-width
> specification supported

The working framing for this evaluation is that the input needs **simple
text formatting and HTML injection**: plain text for most of a page, and
HTML where plain text cannot say what the page needs ([R-10](../requirements/README.md#r-10) simple text plus
HTML where needed). Whether a tool can do that is a property of the tool and
of the format it reads, so the tools have to be looked at before the
content can be planned. The format is open: Markdown is one candidate, not
a requirement.

The first test was tables, because complex HTML tables are the main reason
the content is not plain Markdown today. The Docs WG lead picked five pages
whose tables are hard to express outside HTML; they are listed in
[concepts/tables/README.md](../concepts/tables/README.md#test-pages). The
full record of that round is under [concepts/tables/](../concepts/tables/README.md);
this document summarises it and links to it.

## Tiers

Not every tool got the same amount of work. The tiers come from
[concepts/README.md](../concepts/README.md#candidate-tools):

| Tier | Tools | What was done | Status |
|------|-------|---------------|--------|
| Hands-on | Docusaurus, Zensical, Starlight (on Astro), Antora | All five test pages converted by hand in every mode (below), built, measured in a browser, and checked | under evaluation |
| Probe | Eleventy, Sphinx with MyST, Middleman without Bookbinder | One page each, to answer one question | under evaluation |
| On paper | Hugo, VitePress | A capability check against the requirements is planned | not yet assessed |

A probe is a small, single-question test: one page in one tool. Each
tool's entry, with its findings, is in [tools.md](tools.md).

## Modes

Each test page was converted into each hands-on tool in several ways,
called modes. A mode is a choice of how much of the source's HTML to keep:

- **Raw passthrough:** the HTML exactly as written, defects included. Only
  the variables and the include line change. It shows what a tool does with
  today's markup before any cleanup.
- **Passthrough:** the HTML kept, after the cleanup the page needs (below)
  and whatever the tool forces.
- **Extension:** the table written in a form the tool does not have by
  default, added through the tool's own extension point (a plugin, a
  Markdown extension, or roles and CSS). The extension carries the table's
  hints.
- **Native:** the tool's own table syntax, plus whatever hint mechanism the
  tool offers on its own.
- **Native-plain:** native without any width or alignment settings, as most
  Markdown tables are written. Built only where it differs from native.

A hint is what a table asks for, written once and independent of any tool:
a column's role (`key` for a short label, `value`, or `prose` for
sentences), a width, whether a column avoids wrapping, whether the first
column holds row headers, a title. Hints express intent, not exact values;
each tool honors them as well as it can ([R-03](../requirements/README.md#r-03) column widths as hints). The
full list: [Hints after the round](../concepts/tables/README.md#hints-after-the-round).

What every mode looks like for one table: [formats.md](formats.md).

## Conversion process

How a page gets from today's source into a tool's input. What the migration
as a whole involves (inventory, owners, redirects, cutover) is in
[requirements/migration.md](../requirements/migration.md); this section is
the "how".

RFC #1642 asks for one conversion done centrally
([L131](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L131)):

> The conversion MUST be done by one central migration team to ensure
> consistency, not by each Working Group individually.

The plan is to record, concept by concept, the conversion rules that worked
when pages were converted by hand, and later build them into a migration
tool, `cf-docs-migrate`, with a `scan` command (find every instance of a
concept across the docs) and a `convert` command (apply the rules) ([R-23](../requirements/README.md#r-23)
one central conversion). The tool is not yet written. A concept is one kind
of thing the pages contain, such as tables, variables or code blocks; the
list is in [concepts/README.md](../concepts/README.md#concepts).

The steps seen in the tables round, in order:

1. **Clean up the markup.** Five of the twelve HTML tables on the test pages
   are not well-formed (an unclosed cell, a class written with typographic
   quotes, a row closed with `</td>`). Browsers repair this silently;
   tools that read HTML strictly do not ([R-24](../requirements/README.md#r-24) markup cleanup before
   conversion). The defects are listed in
   [Markup that only browsers tolerate](../concepts/tables/README.md#markup-that-only-browsers-tolerate).
2. **Translate variables and includes.** `<%= vars.name %>` and
   `<%= partial '…' %>` become each tool's syntax ([R-04](../requirements/README.md#r-04) variables everywhere,
   [R-05](../requirements/README.md#r-05) partials and reuse). The forms are listed per tool in
   [tools.md](tools.md).
3. **Write each table in the chosen mode,** keeping the hints the intent
   file for the page records. The intent files are in
   [concepts/tables/intent/](../concepts/tables/intent/) (for example,
   [credential-types](../concepts/tables/intent/credential-types.md));
   each one translates the source's exact values into hints and lists the
   checks the converted table must pass.
4. **Convert the rest of the page** if the tool does not read Markdown.
   Antora reads AsciiDoc, so every page is rewritten. In the tables round
   this was done with pandoc (a general document converter) plus a script,
   and the conversion failed silently in four ways
   ([Antora finding 1](../concepts/tables/results.md#findings-3)).
5. **Build and check.** Three checks are shared by every site, in
   [concepts/tables/checks/](../concepts/tables/checks/): spot
   checks per table (row and cell counts, code spans, characters that must
   not appear), a word-by-word comparison with the published page, and a
   browser check that a wide table scrolls in its own box. The text
   comparison found content changes the spot checks missed. Build-time
   values such as the copyright year are expected differences ([R-25](../requirements/README.md#r-25)
   build-time values are expected differences).
6. **Owner review.** Each converted area is reviewed by its owner ([R-26](../requirements/README.md#r-26)
   owner review of migrated pages). Not part of the tables round.

**Not yet written:** the conversion steps for the other concepts (headings,
variables, partials, notes, code blocks, cross-repository links), and how
`scan` and `convert` are built.

## Extensions needed per tool

No tool's own table syntax carries every hint. The column roles and the
capped no-wrap (a column that stays on one line up to a limit the template
sets, then wraps between words) need CSS in every tool. What else each tool
needed, as built in the tables round:

| Tool | What its own syntax lacks | What closes the gap | Code written |
|------|---------------------------|---------------------|--------------|
| Docusaurus | widths, row headers, top alignment, title row, roles, no-wrap | a remark plugin (code that changes the Markdown before it becomes HTML): [plugins/list-table.js](../concepts/tables/sites/docusaurus/plugins/list-table.js) | JavaScript, 94 lines today, plus CSS |
| Zensical | row headers, title row, roles, no-wrap (widths go on header cells) | a Python-Markdown block: [list_table.py](../concepts/tables/sites/zensical/list_table.py) | Python, 120 lines today, plus CSS |
| Starlight | row headers, top alignment, title row, roles, no-wrap | attributes added to Markdoc's own table tag: [list-table.mjs](../concepts/tables/sites/starlight/list-table.mjs) | JavaScript, 83 lines today, plus CSS |
| Antora | roles, no-wrap | roles (class names) on the AsciiDoc table, given meaning by a stylesheet: [hints.css](../concepts/tables/sites/antora/supplemental-ui/css/hints.css) | CSS only for the hints; an 8-line script puts wide tables in a scrolling box |
| Sphinx with MyST (probe) | roles, no-wrap | classes on the `list-table`, given meaning by a stylesheet | CSS only |
| Eleventy (probe) | nothing: the HTML is used as written | the official EJS plugin | none |
| Middleman (probe) | nothing: the pages build unchanged | a short config file and a layout | none |

Variables that hold HTML need care in three tools. MDX (Docusaurus),
Markdoc (Starlight) and EJS (Eleventy) escape a variable's value, so a value
such as `<p class="note">…</p>` shows as text unless the page uses a
special form for it. Zensical, Antora and Middleman insert the value as
markup, as the published site does.

RFC #1642
[L100](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L100)
says:

> Working Groups MUST NOT need custom extensions, plugins, or JavaScript
> code to author documentation.

Whether one shared extension, maintained once for all documentation,
meets that line is a requirements question ([R-13](../requirements/README.md#r-13) no per-WG extensions),
not a tooling one. The table above shows what each tool needed for the
test pages.

## Problem areas

Problems found in the tables round that a conversion must handle. Most sit
outside the tables and belong to concepts not yet worked; they are listed
here because they stop a page from building or change its content.

| Problem | Tools affected | Requirement | Evidence |
|---------|----------------|-------------|----------|
| Markup that only browsers tolerate breaks the build or changes content | Docusaurus (MDX), Starlight (Markdoc) | [R-24](../requirements/README.md#r-24) markup cleanup before conversion | [summary](../concepts/tables/results.md#summary) |
| Text inside HTML is read as Markdown: a lone `-` becomes a list, spaces next to tags disappear, `*/*` loses its `*` — with no error | Starlight (Markdoc); Docusaurus (MDX) for `*/*` | [R-01](../requirements/README.md#r-01) content and outline survive | [Starlight findings](../concepts/tables/results.md#findings-2) |
| Braces `{…}` in prose are code in MDX | Docusaurus | [R-01](../requirements/README.md#r-01) content and outline survive | [raw passthrough errors](../concepts/tables/results.md#raw-passthrough-errors) |
| HTML-valued variables are escaped | Docusaurus, Starlight, Eleventy | [R-04](../requirements/README.md#r-04) variables everywhere | [Eleventy probe](../concepts/tables/probes/eleventy/README.md) |
| Every page rewritten in another format, with silent failures | Antora | [R-01](../requirements/README.md#r-01) content and outline survive | [Antora finding 1](../concepts/tables/results.md#findings-3) |
| Themes style different tables: all, only classless ones, only their own | all four | [R-09](../requirements/README.md#r-09) table styles by class | [summary](../concepts/tables/results.md#summary) |
| Heading anchors written `<a id>` break the table of contents | Docusaurus | [R-16](../requirements/README.md#r-16) old URLs keep working | [Docusaurus finding 6](../concepts/tables/results.md#findings) |
| A page description shows raw variable code | Docusaurus | [R-20](../requirements/README.md#r-20) search-engine and AI-friendly output | [Docusaurus finding 7](../concepts/tables/results.md#findings) |
| No check for links to missing anchors | Starlight, Antora | [R-08](../requirements/README.md#r-08) cross-repository links (a link checker is how broken links are found) | [Starlight finding 7](../concepts/tables/results.md#findings-2) |
| ERB tags shown as examples in prose are run as code | Zensical (its template engine reads every `<%= … %>`) | [R-01](../requirements/README.md#r-01) content and outline survive | [Zensical finding 3](../concepts/tables/results.md#findings-1) |
| A table after a list step leaves the list unless indented | Docusaurus, Zensical, Starlight | [R-01](../requirements/README.md#r-01) content and outline survive | [Docusaurus finding 3](../concepts/tables/results.md#findings) |
| Default themes hyphenate words in cells | Antora, Sphinx | none yet (a template choice) | [Antora finding 5](../concepts/tables/results.md#findings-3) |

**Not yet written:** problem areas for the concepts not yet worked (code
blocks, notes, cross-repository links), and for the two tools not yet
assessed.
