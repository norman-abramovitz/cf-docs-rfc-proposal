# Proof-of-concept results

Status: draft, incomplete — covers what is known as of 2026-10-10.

This folder compares what the candidate documentation tools did with real
Cloud Foundry pages: the text an author writes in each tool next to the page
the tool builds from it, and next to the page as published today. It
describes; it does not recommend.

## What "POC" means here

A proof of concept (PoC, or POC) is a small working build made to show
whether an approach works (see the [glossary](../glossary.md#poc)).

RFC #1642, the draft proposal for a new CF docs stack, plans its PoC as
Phase 2:

> A PoC SHOULD be established in a new repository (e.g., `cloudfoundry/docs-next`) to:
> ([L119](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L119))

> Stand up Docusaurus (or the chosen alternative) with a representative subset of CF documentation migrated to Markdown.
> ([L121](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L121))

The work here is smaller and comes earlier. It is not that PoC. Each
candidate tool has its own small test site. The *test pages* (five pages
the Docs WG lead picked because their tables are hard to express outside
HTML, plus one added later) are converted by hand into every site, one
documentation *concept* (one kind of content, such as tables) at a time.
The question for each concept is how each tool handles that content, and at
what cost. The results can inform what the
Phase 2 PoC runs.

The RFC also says what its PoC must check for complex pages:

> The PoC MUST validate that the most complex existing pages (HTML tables, CSS layouts) can be represented with MDX alone. Any gap found MUST be reported as a PoC finding.
> ([L104](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L104))

The Docusaurus results here bear on that line. MDX is Markdown that also
accepts JSX, the HTML-like syntax of React components (see the
[glossary](../glossary.md#mdx)). Docusaurus's native and passthrough modes
(defined below) both use MDX with no plugin.

## Tools

Four tools were tried in full. Three more were *probes*: each answers one
narrow question instead of the full round.

ERB (Embedded Ruby) is the `<%= … %>` tag syntax today's pages use for
variables and partials (shared files included into a page). Middleman is the
site builder under Bookbinder, the tool that builds docs.cloudfoundry.org
today; the Middleman probe is the smallest-change baseline. Hugo and
VitePress are assessed on paper only and have no results here.

| Tool | Version | Input format | How far |
|---|---|---|---|
| Docusaurus | 3.10.2 | MDX | every test page, every mode |
| Zensical | 0.0.69 | Markdown read by Python-Markdown | every test page, every mode |
| Starlight (on Astro 7.3.8) | 0.42.6 | Markdoc: Markdown with `{% %}` tags | every test page, every mode |
| Antora | 3.2.1 | AsciiDoc | every test page, every mode |
| Eleventy | 3.1.6 | EJS: `<% %>` tags, close to today's ERB | one page ([probe](../concepts/tables/probes/eleventy/README.md)) |
| Sphinx with MyST | 9.1.0, 5.1.0 | MyST: Markdown with directives | one table ([probe](../concepts/tables/probes/sphinx-myst/README.md)) |
| Middleman without Bookbinder | 4.6.3 | today's ERB pages unchanged | the five original test pages ([probe](../concepts/tables/probes/middleman/README.md)) |

## Method

The method is described in full in the
[tables concept](../concepts/tables/README.md#method). In short, for each
test page:

1. **Intent.** An *intent file* translates what each table asks for into
   *hints*: tool-neutral statements such as "column 1 is a key column, about
   20% wide, does not wrap" (R-03 column widths as hints; requirement IDs
   are listed in [requirements](../requirements/README.md)). It also lists
   the markup cleanup the page needs (R-24 markup cleanup before conversion)
   and any deliberate change from the published page.
   Files: [intent/](../concepts/tables/intent/).
2. **Convert by hand, in each mode.** A *mode* is one way of writing the
   page for a tool:
   - *passthrough*: the page's HTML kept as written, with only the changes
     the tool forces, and variables and partials translated to the tool's
     syntax;
   - *extension*: the tool's extension point (a plugin or a custom block)
     carrying the hints;
   - *native*: the tool's own table syntax with whatever width or alignment
     settings it offers;
   - *native-plain*: native with no width or alignment settings, as most
     authors would write it.
3. **Build.** Does the page build, and what had to change first? Each site
   also builds the HTML exactly as written ("raw" passthrough) to record the
   first errors.
4. **Spot checks.** Per-table checks every converted page must pass (row
   counts, cells present, code kept, no stray characters), listed in the
   intent file and run by [spot-checks.sh](../concepts/tables/checks/spot-checks.sh)
   (R-01 content and outline survive).
5. **Text comparison.** A word-by-word comparison of each page's main text
   against the published page, in every mode
   ([text-diff.py](../concepts/tables/checks/text-diff.py)). It finds changes
   outside the tables that the spot checks do not cover.
6. **Measure and screenshot.** Column widths are measured in a browser with a
   1280-pixel window, as percent of the table, first body row. Screenshots
   use the same window. Each tool runs its default *theme* (the fonts,
   colors, borders and spacing it ships with). Appearance is not compared;
   content, structure and hints are.

Each site's `CONVENTIONS.md` records the patterns that worked, for a
conversion tool to apply later
([Docusaurus](../concepts/tables/sites/docusaurus/CONVENTIONS.md),
[Zensical](../concepts/tables/sites/zensical/CONVENTIONS.md),
[Starlight](../concepts/tables/sites/starlight/CONVENTIONS.md),
[Antora](../concepts/tables/sites/antora/CONVENTIONS.md)).

## Results by concept

### Tables

Done, with open items. Input and output side by side, page by page:
[tables.md](tables.md). Full grids, measurements and findings:
[results.md](../concepts/tables/results.md#summary).

What the round found:

- **Every tool renders every test table correctly once the HTML is cleaned
  up.** They differ in how much cleanup the HTML needs, which hints their
  own table syntax carries, and how much of the rest of the page has to
  change.
- **Width hints** survive in every tool's passthrough. In native mode they
  survive where the tool's own table syntax takes a width: Zensical (on
  header cells), Starlight and Antora. Docusaurus's pipe tables (Markdown
  tables written with `|` between cells) take none.
- **Two hints need CSS in every tool:** the column roles and the capped
  no-wrap. Antora and the Sphinx probe carry them as classes on the table;
  Docusaurus, Zensical and Starlight use a small extension.

### Other concepts

**Not yet written:** headings, variables, partials, notes and admonitions,
code blocks, cross-repository links, and build-time values such as the
copyright year. Each is listed as proposed in
[Concepts](../concepts/README.md); none has been converted yet.

## Other comparisons

These come from the tables round but are about the pages as a whole.

**Builds with the HTML as written** (five test pages):

| Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|
| none: MDX stops on all five; three of the five first errors are outside the tables | all five | four of five; Markdoc changes some text inside HTML without an error | all five, inside passthrough blocks; the page around them is rewritten as AsciiDoc |

**Spot checks after cleanup** (six pages, 42 checks): Docusaurus 40 of 42 in
every mode (the two misses are page descriptions, not tables); Zensical,
Starlight and Antora 42 of 42 in every mode.

**Text comparison, outside the tables:**

| Difference | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| `Accept: */*` in terminal output | shows as `Accept: /` | kept | shows as `Accept: /` | kept |
| Other prose | matches | three literal `*` where a list follows a text line | matches after the passthrough changes | matches after the AsciiDoc rewrite |
| Quotes | straight (published: curly) | straight | straight | curly in AsciiDoc text, straight in HTML blocks |

Details: [results.md](../concepts/tables/results.md), section "Text compared
with the published page" under each tool.

**Not yet written:** the RFC's Phase 2 items (local preview, search,
versioning, GitHub Pages deployment, redirects, contributor feedback) were
not compared across these sites.

## Files

- [tables.md](tables.md): the tables concept, one section per test page.
- [img/](img/): screenshots used in these files, 1280-pixel window.
