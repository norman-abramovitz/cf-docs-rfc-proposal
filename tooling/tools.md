# Tools

Status: draft, incomplete — covers what is known as of 2026-10-10.

Each tool considered for the CF documentation: what it is, what it reads,
what was done with it, what was seen, and the concerns the evidence shows.
No tool has been chosen or rejected. Every tool's status is "under
evaluation", except Hugo and VitePress, which are "not yet assessed".

A static site generator is a program that turns source files (text,
templates, settings) into a folder of web pages that any web server can
host. Every tool below is one, or a documentation theme on top of one.

Requirements are cited by ID and a short phrase; the full list is in
[requirements/](../requirements/README.md). Modes (raw passthrough,
passthrough, extension, native, native-plain) are defined in the
[Tooling README](README.md#modes). Each input format, with the same table
written in it, is in [formats.md](formats.md).

## Summary

| Tool | Reads | Tier | Version tested | License | Status |
|------|-------|------|----------------|---------|--------|
| [Docusaurus](#docusaurus) | MDX, Markdown | hands-on | 3.10.2 | [MIT](https://github.com/facebook/docusaurus/blob/c245217563f6491fdb79bf5ac91bfa16536e5de9/LICENSE) | under evaluation |
| [Zensical](#zensical) | Markdown (Python-Markdown) | hands-on | 0.0.69 | [MIT](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/LICENSE.md) | under evaluation |
| [Starlight](#starlight) | Markdoc (as set up here), Markdown, MDX | hands-on | 0.42.6 on Astro 7.3.8 | [MIT](https://github.com/withastro/starlight/blob/67de74077524001c79ec233e1b113e86b2b800b0/LICENSE) | under evaluation |
| [Antora](#antora) | AsciiDoc | hands-on | 3.2.1 | [MPL-2.0](https://gitlab.com/antora/antora/-/blob/87797da7a7f337301ec9b1ad26aa291a28342d56/LICENSE) | under evaluation |
| [Eleventy](#eleventy) | Markdown run through a template language (EJS here) | probe | 3.1.6 | [MIT](https://github.com/11ty/eleventy/blob/c0bb3f4219e00629f4f58a771c1783c898b9bdab/LICENSE) | under evaluation |
| [Sphinx with MyST](#sphinx-with-myst) | MyST, reStructuredText | probe | Sphinx 9.1.0, MyST parser 5.1.0 | [BSD-2-Clause](https://github.com/sphinx-doc/sphinx/blob/b04a2101295ac3fb725b16111eda0284b6da4cca/LICENSE.rst); MyST parser [MIT](https://github.com/executablebooks/MyST-Parser/blob/723cffcf84213f0cb58695b27eec9ad72052b53a/LICENSE) | under evaluation |
| [Middleman](#middleman) | ERB, Markdown, HTML | probe (without Bookbinder) | 4.6.3 on Ruby 4.0.7 | [MIT](https://github.com/middleman/middleman/blob/ec3eab8d7540ec474a8ae187bd466fafe8e147ad/LICENSE.md) | under evaluation |
| [Hugo](#hugo) | Markdown, Go templates | on paper | — | [Apache-2.0](https://github.com/gohugoio/hugo/blob/0732eadd5aead94d4bd4674d87e9bfc79aaf10a7/LICENSE) | not yet assessed |
| [VitePress](#vitepress) | Markdown, Vue components | on paper | — | [MIT](https://github.com/vuejs/vitepress/blob/633e48af9ec25a9cc28fc3ebf1e9063b359adb2e/LICENSE) | not yet assessed |

Each license links to the project's license file at the commit checked
on 2026-10-10 ([R-19](../requirements/README.md#r-19) open source only). Tiers are explained in the [Tooling README](README.md#tiers).

Across the four hands-on tools, the round found that every test table
renders correctly in every mode once the source is cleaned up. The tools
differ in how much cleanup the HTML needs, which hints their own table
syntax carries, and how much of the rest of the page must change
([results summary](../concepts/tables/results.md#summary)).

## Today's stack

### Bookbinder

**What it is.** A Ruby tool written for the CF docs. It reads the book's
[`config.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml)
in docs-book-cloudfoundry, collects the `docs-*` content repositories it
names, and builds them into one site with Middleman (a runtime dependency
in its
[gemspec](https://github.com/pivotal-cf/bookbinder/blob/83bd2a57a8ba3d04c58a5be67607b243bdea0c64/bookbinder.gemspec#L20)).
Each repository maps to a fixed URL directory (the `directory:` of its
section in `config.yml`), so a page's URL names the repository and file to
edit ([R-15](../requirements/README.md#r-15) URL identifies the
source). Learn more: [Bookbinder](https://github.com/pivotal-cf/bookbinder);
see also the [glossary](../glossary.md#bookbinder).

**What was seen.** Its repository's
[last commit](https://github.com/pivotal-cf/bookbinder/commit/83bd2a57a8ba3d04c58a5be67607b243bdea0c64)
is dated 2024-10-17 (checked 2026-10-10). The [Middleman probe](#middleman) built all five test pages
without it, and every table matched the published page: Bookbinder adds
nothing the tables need. What else the book's build does (collecting
repositories, navigation, the "Page last updated" line) was not tested
without it.

**Status.** In use today. RFC #1642 proposes replacing the stack it is part
of ([Problem, L17–25](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L17-L25)).

## Hands-on tools

Each was built with all five test pages (and a sixth for the table-style
example) in every mode, with versions pinned, and checked with the shared
spot checks, a word-by-word comparison with the published page, and a
browser check for wide tables. Each site folder has a `CONVENTIONS.md`
with the patterns that worked.

### Docusaurus

**What it is.** A static site generator for documentation, built on
React (a JavaScript library for building pages; React and MDX are
[dependencies of its core package](https://github.com/facebook/docusaurus/blob/c245217563f6491fdb79bf5ac91bfa16536e5de9/packages/docusaurus/package.json#L92-L94)).
Pages are Markdown or MDX:
Markdown in which HTML is read as JSX, React's stricter HTML-like syntax.
Learn more: [Docusaurus](https://docusaurus.io/); see also the
[glossary](../glossary.md#docusaurus).

RFC #1642 names it
([L31](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L31)):

> The recommended engine is the current major version of Docusaurus (v3 or
> newer, maintained by Meta, MIT-licensed, widely adopted in the CNCF
> ecosystem).

**What was done.** Docusaurus 3.10.2, default theme. Site:
[sites/docusaurus/](../concepts/tables/sites/docusaurus/CONVENTIONS.md);
results: [results.md](../concepts/tables/results.md#docusaurus-3102).

**Result.** None of the five pages builds with its HTML unchanged; three of
the five first errors are outside the tables. After cleanup every table
renders correctly in all three modes. Its own table syntax is the pipe
table, which carries no widths, row headers or titles.

**Concerns, with evidence:**

- **MDX needs the HTML rewritten.** Close every tag (`<br />`), write
  `style` as a JavaScript object, add `<tbody>` and `<colgroup>`, escape
  `{…}` in prose. Some of these only show as browser errors
  ([conventions](../concepts/tables/sites/docusaurus/CONVENTIONS.md#passthrough)).
  [R-24](../requirements/README.md#r-24) markup cleanup before conversion, [R-11](../requirements/README.md#r-11) readable source.
- **No native table hints.** Widths, row headers, top alignment and titles
  need HTML or a plugin; the extension here is a remark plugin
  ([plugins/list-table.js](../concepts/tables/sites/docusaurus/plugins/list-table.js)).
  RFC [L104](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L104)
  asks the PoC to validate "that the most complex existing pages (HTML
  tables, CSS layouts) can be represented with MDX alone"; this is that
  evidence. [R-02](../requirements/README.md#r-02) rich tables, [R-03](../requirements/README.md#r-03) column widths as hints, [R-13](../requirements/README.md#r-13) no per-WG
  extensions.
- **HTML-valued variables are escaped.** They need
  `<div dangerouslySetInnerHTML={{__html: vars.name}} />` to render as
  markup ([conventions](../concepts/tables/sites/docusaurus/CONVENTIONS.md#every-mode)).
  [R-04](../requirements/README.md#r-04) variables everywhere.
- **Text in terminal blocks is read as Markdown:** `Accept: */*` shows as
  `Accept: /` ([finding 8](../concepts/tables/results.md#findings)). [R-01](../requirements/README.md#r-01)
  content and outline survive, [R-06](../requirements/README.md#r-06) typed code blocks.
- **Heading anchors written `<a id>`** cause a browser error on every page
  that has them and fail the anchor check; Docusaurus's own `{#id}` form
  avoids both ([finding 6](../concepts/tables/results.md#findings)). [R-16](../requirements/README.md#r-16)
  old URLs keep working.
- **Page descriptions** (the summary search engines show) contain raw
  variable code when the first paragraph has a variable
  ([finding 7](../concepts/tables/results.md#findings)). [R-20](../requirements/README.md#r-20) search-engine
  and AI-friendly output.
- **Links inside HTML are not link-checked**; Markdown links are
  ([finding 4](../concepts/tables/results.md#findings)). [R-08](../requirements/README.md#r-08)
  cross-repository links.

**Variables and partials.** One `import vars` line per page, then
`{vars.name}`. A partial (a file included in other pages) is imported and
used as a component, which answers RFC
[L179](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L179)
("Are partials supported by Docusaurus?") for the scale table: yes, as an
MDX import. [R-05](../requirements/README.md#r-05) partials and reuse.

**Status:** under evaluation.

### Zensical

**What it is.** A static site generator for documentation from the team
behind Material for MkDocs (the project's own description:
[README](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/README.md#L11-L12)).
Pages are Markdown read by Python-Markdown (the `markdown` package is a
[dependency](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/pyproject.toml#L58)).
Learn more: [Zensical](https://zensical.org/); see also the
[glossary](../glossary.md#zensical).

**What was done.** Zensical 0.0.69, default theme. Site:
[sites/zensical/](../concepts/tables/sites/zensical/CONVENTIONS.md);
results: [results.md](../concepts/tables/results.md#zensical-0069).

**Result.** All five pages build with their HTML unchanged, and the
variables keep their `<%= vars.name %>` form. With the intent files'
cleanup and one indent, every spot check passes in every mode. Native pipe
tables carry widths on header cells; row headers, the title row and the
capped no-wrap need HTML or the extension, a Python-Markdown block
([list_table.py](../concepts/tables/sites/zensical/list_table.py)).

**Concerns, with evidence:**

- **The default theme styles only tables without a `class`.** Tables that
  keep `class="table"` lose the theme's look until the site's CSS repeats
  it ([finding 1](../concepts/tables/results.md#findings-1)). [R-09](../requirements/README.md#r-09) table
  styles by class.
- **Every `<%= … %>` on a page is run**, including ERB shown as an example
  in prose or code. A bad one replaced the page with an error message while
  the build reported success, until `on_error_fail = true` was set
  ([finding 3](../concepts/tables/results.md#findings-1)). Pages that
  document ERB need escaping. [R-01](../requirements/README.md#r-01) content and outline survive.
- **A bare `-` for an empty list-table cell drops a cell** with no error;
  it is written `- <!-- -->`
  ([finding 5](../concepts/tables/results.md#findings-1)). [R-01](../requirements/README.md#r-01) content and
  outline survive, [R-11](../requirements/README.md#r-11) readable source.
- **A list that follows a text line with no blank line** is plain text, not
  a list: three literal `*` on one page
  ([text compared](../concepts/tables/results.md#text-compared-with-the-published-page-1)).
  [R-01](../requirements/README.md#r-01) content and outline survive.
- **Paid offerings.** Zensical is
  [MIT-licensed](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/LICENSE.md).
  The project also sells an authoring environment,
  [Zensical Studio](https://zensical.org/studio/)
  ([pricing](https://zensical.org/studio/pricing/)), and a membership,
  [Zensical Spark](https://zensical.org/spark/)
  ([pricing](https://zensical.org/spark/pricing/)), whose members get
  early-access releases (the project's own pages, read 2026-10-10). Whether features stay behind it is to be
  watched. [R-19](../requirements/README.md#r-19) open source only.

**Variables and partials.** Variables as written, through Zensical's
template engine set to ERB-style tags; HTML values render as markup.
Partials need the template engine's `include`; the `--8<--` snippet
include does not fill in the partial's variables
([finding 7](../concepts/tables/results.md#findings-1)).

**Status:** under evaluation.

### Starlight

**What it is.** A documentation theme for Astro, a JavaScript static site
generator (Astro is a
[peer dependency](https://github.com/withastro/starlight/blob/67de74077524001c79ec233e1b113e86b2b800b0/packages/starlight/package.json#L51)).
In this evaluation its pages are Markdoc (`.mdoc`): Markdown with `{% %}`
tags, with HTML allowed, read through Astro's
[Markdoc integration](https://github.com/withastro/astro/blob/9050e3819c51b0383cced278c278bc6f45c63468/packages/integrations/markdoc/package.json#L44). Learn more:
[Starlight](https://starlight.astro.build/), [Astro](https://astro.build/);
see also the [glossary](../glossary.md#starlight).

**What was done.** Starlight 0.42.6 on Astro 7.3.8, Markdoc integration
2.0.11, default theme. Site:
[sites/starlight/](../concepts/tables/sites/starlight/CONVENTIONS.md);
results: [results.md](../concepts/tables/results.md#starlight-0426).

**Result.** Four of the five pages parse with their HTML unchanged.
Markdoc's own `{% table %}` tag holds lists and paragraphs in cells and
widths on header cells without custom code; row headers, top alignment, a
title row and the capped no-wrap need the extension, which adds attributes
to that same tag
([list-table.mjs](../concepts/tables/sites/starlight/list-table.mjs)).
The theme styles every table, and the site's CSS wins over it without extra
work.

**Concerns, with evidence:**

- **Markdoc reads the text inside HTML as Markdown, and changes content
  with no error.** A lone `-` in a code span becomes an empty list; the
  space next to an inline tag disappears when the cell spans lines
  ("passwordrefers", 19 places on one page); a blank line inside `<pre>`
  in a list item stops the whole site from building
  ([findings 1–3](../concepts/tables/results.md#findings-2)). The fixes
  are character entities (`&#45;`, `&#32;`, `&#10;`) or one-line cells.
  [R-01](../requirements/README.md#r-01) content and outline survive, [R-24](../requirements/README.md#r-24) markup cleanup before conversion.
- **HTML-valued variables are escaped.** A two-line component renders them
  as markup (`{% rawhtml value=$vars.name /%}`). [R-04](../requirements/README.md#r-04) variables everywhere.
- **No link check.** Astro does not check in-page links; a scan of the
  built pages found two broken ones, also broken on the published page
  ([finding 7](../concepts/tables/results.md#findings-2)). [R-08](../requirements/README.md#r-08)
  cross-repository links.
- **Typographic quotes** can be turned on, but they then change quotes
  inside code and `<pre>` blocks too, so the option stays off
  ([finding 9](../concepts/tables/results.md#findings-2)). [R-01](../requirements/README.md#r-01) content and
  outline survive.

**Variables and partials.** `{% $vars.name %}`; partials with
`{% partial file="…" /%}`, and their variables render.

**Status:** under evaluation.

### Antora

**What it is.** A static site generator for documentation written in
AsciiDoc, a plain-text format with its own table syntax. It is designed to
build one site from content in several repositories: the playbook's
`content` key is
[a list of content sources](https://gitlab.com/antora/antora/-/blob/87797da7a7f337301ec9b1ad26aa291a28342d56/packages/content-aggregator/lib/aggregate-content.js#L84-L90),
and the project's
[README](https://gitlab.com/antora/antora/-/blob/87797da7a7f337301ec9b1ad26aa291a28342d56/README.adoc#L29)
calls it a "single or multi-repository site generator". Learn more:
[Antora](https://antora.org/); see also the
[glossary](../glossary.md#antora).

**What was done.** Antora 3.2.1, with its default UI (the theme) pinned to
one build. Site:
[sites/antora/](../concepts/tables/sites/antora/CONVENTIONS.md);
results: [results.md](../concepts/tables/results.md#antora-321).

**Result.** HTML tables build unchanged inside AsciiDoc passthrough blocks.
AsciiDoc's own table carries widths, content-sized columns, a header row,
row headers, top alignment, spanning cells, and lists and paragraphs in
cells. The extension needs no code: roles (class names) on the table and a
stylesheet. Every spot check passes in every mode.

**Concerns, with evidence:**

- **Every page is rewritten, in every mode.** Antora reads only AsciiDoc,
  so the Markdown around the tables becomes AsciiDoc even in passthrough.
  The conversion (pandoc plus a script) went wrong in four ways that each
  changed a page silently; three would not have been caught by the spot
  checks or the text comparison
  ([finding 1](../concepts/tables/results.md#findings-3)). [R-01](../requirements/README.md#r-01) content and
  outline survive, [R-23](../requirements/README.md#r-23) one central conversion.
- **The default UI styles only AsciiDoc tables, hyphenates words in cells,
  and exposes no settings** a site can change; the site's stylesheet
  overrides rules instead
  ([findings 3–5](../concepts/tables/results.md#findings-3)). [R-09](../requirements/README.md#r-09) table
  styles by class.
- **Wide tables widened the page** until an 8-line script put each table in
  a scrolling box
  ([table-scroll.js](../concepts/tables/sites/antora/supplemental-ui/js/table-scroll.js)).
  It is part of the site's UI, not of any page.
- **No link check** for links to missing anchors
  ([finding 8](../concepts/tables/results.md#findings-3)). [R-08](../requirements/README.md#r-08)
  cross-repository links.
- **The default UI is not versioned.** Its bundle is a build file at a
  moving URL; the site pins one build and checks its hash
  ([finding 10](../concepts/tables/results.md#findings-3)).
- **Multi-repository sites.** Antora builds from several repositories by
  design ([content aggregator](https://gitlab.com/antora/antora/-/blob/87797da7a7f337301ec9b1ad26aa291a28342d56/packages/content-aggregator/lib/aggregate-content.js#L84-L90)). RFC #1642 §3 proposes one docs repository
  ([L65–88](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L65-L88)).
  Read about, not tested here.

**Variables and partials.** Variables are AsciiDoc attributes, `{name}`; an
undefined one shows as text unless `attribute-missing: drop` is set. HTML
values render as markup. Partials with `include::partial$file.adoc[]`.

**Status:** under evaluation.

## Probes

Each probe built one page in one tool to answer one question.

### Eleventy

**What it is.** A JavaScript static site generator that runs pages through
a template language before Markdown. Here the template language is EJS,
whose tags look like ERB's. Learn more: [Eleventy](https://www.11ty.dev/);
see also the [glossary](../glossary.md#eleventy).

**Question.** Do `<%= vars.* %>` tags render unchanged as EJS?

**Answer.** Yes for the tables: `uaa-concepts` and the scale table come out
byte for byte as written. EJS's `<%=` escapes HTML, so HTML-valued
variables, helpers and includes need `<%-`, and an include needs the full
file name. EJS is a plugin since Eleventy 3: Eleventy 2.0.1
[depends on `ejs`](https://github.com/11ty/eleventy/blob/e71cb94003b5a94dcd40ec96f8f4b455767b9833/package.json#L109),
[3.0.0 does not](https://github.com/11ty/eleventy/blob/8675d68ec049bb683b0b09f42bd2703909eb0e53/package.json),
and the
[`@11ty/eleventy-plugin-ejs`](https://github.com/11ty/eleventy-plugin-template-languages/blob/d765d2ab8ae0328537e7b6c39a5e83742b7f5bfd/ejs/package.json#L2)
package adds it back.
Details: [probes/eleventy](../concepts/tables/probes/eleventy/README.md).

**Concerns.** The Middleman helpers other than `partial` (`image_tag`,
`link_to`) have no EJS counterpart; not covered. A literal `<%` in prose
must be written `<%%`, as in ERB. [R-04](../requirements/README.md#r-04) variables everywhere, [R-05](../requirements/README.md#r-05) partials
and reuse.

**Status:** under evaluation.

### Sphinx with MyST

**What it is.** Sphinx is a documentation generator from the Python world;
the MyST parser lets it read MyST, Markdown with directives (named blocks
with options). The parser is a Sphinx extension built on markdown-it-py
([dependencies](https://github.com/executablebooks/MyST-Parser/blob/723cffcf84213f0cb58695b27eec9ad72052b53a/pyproject.toml#L33-L39)). Learn more: [Sphinx](https://www.sphinx-doc.org/),
[MyST parser](https://myst-parser.readthedocs.io/); see also the
[glossary](../glossary.md#sphinx).

**Question.** Can a MyST `list-table`'s directive options carry the table
hints?

**Answer.** Mostly yes, with no code. Header row, row headers and widths
are options; the column roles and the capped no-wrap are classes on the
table, given meaning by a stylesheet. All five spot checks pass. A second
header row (a title above the column headers) is not carried.
Details: [probes/sphinx-myst](../concepts/tables/probes/sphinx-myst/README.md).

**Concerns.** The default theme hyphenates words in cells (turned off in
the stylesheet). Inline code is rewritten into one `<span>` per word, which
a text comparison has to undo. One page only.

**Status:** under evaluation.

### Middleman

**What it is.** A Ruby static site generator; the one Bookbinder runs
today. The book pins `bookbindery` 9.12.1
([Gemfile](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/Gemfile#L3)),
which depends on Middleman 3.4
([RubyGems](https://rubygems.org/gems/bookbindery/versions/9.12.1));
the latest Bookbinder source depends on
[Middleman 4.1.10](https://github.com/pivotal-cf/bookbinder/blob/83bd2a57a8ba3d04c58a5be67607b243bdea0c64/bookbinder.gemspec#L20). Learn more: [Middleman](https://middlemanapp.com/); see also the
[glossary](../glossary.md#middleman).

**Question.** What is the smallest change that removes Bookbinder and keeps
the pages' ERB and HTML?

**Answer.** A short config file (the book's Markdown settings and its
`vars` helper) and a small layout. All five pages build unchanged on Ruby
4.0.7 (plus the `ostruct` gem), every table matches the published page
cell for cell, and variables and the partial behave as in the book.
Details: [probes/middleman](../concepts/tables/probes/middleman/README.md).

**Concerns.** This keeps ERB and Ruby. RFC #1642 lists among the MUST
capabilities
([L39](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L39))
"A lightweight templating/component system that does not require Ruby or
ERB". Whether that line stands is a requirements question. The probe's
layout has none of the book's navigation; search, versioning and the rest
of the site were not tested.

**Status:** under evaluation, as the minimal-change baseline.

## Not yet assessed

Planned as on-paper capability checks against the requirements. Nothing
has been built.

### Hugo

**What it is.** A static site generator written in Go. Pages are Markdown,
read by the goldmark parser
([go.mod](https://github.com/gohugoio/hugo/blob/0732eadd5aead94d4bd4674d87e9bfc79aaf10a7/go.mod#L72)); shortcodes and Go templates add what Markdown
lacks. RFC #1642 names it as an alternative that "MAY be evaluated"
([L31](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L31)).
`cloudfoundry/what-is-cf` is a Hugo site today: its
[deploy script](https://github.com/cloudfoundry/what-is-cf/blob/9b48cc72c8e3f0e4483087863b574e9e0526e710/ci/deploy.sh#L7)
runs `hugo`. Learn more:
[Hugo](https://gohugo.io/); see also the [glossary](../glossary.md#hugo).

**Not yet written:** the capability check (tables and hints, variables in
cells, partials, local preview, search, versioning).

**Status:** not yet assessed.

### VitePress

**What it is.** A static site generator built on Vite and Vue (JavaScript
tools). Pages are Markdown read by markdown-it, and can use Vue
components ([dependencies](https://github.com/vuejs/vitepress/blob/633e48af9ec25a9cc28fc3ebf1e9063b359adb2e/package.json#L111-L112),
[markdown-it](https://github.com/vuejs/vitepress/blob/633e48af9ec25a9cc28fc3ebf1e9063b359adb2e/package.json#L150)). Learn more: [VitePress](https://vitepress.dev/); see also the
[glossary](../glossary.md#vitepress).

**Not yet written:** the capability check, as for Hugo.

**Status:** not yet assessed.

## Other tools in the CF docs today

- **bosh.io** (`cloudfoundry/docs-bosh`) is built with MkDocs and Material
  for MkDocs, not Bookbinder: its
  [`mkdocs.yml`](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/mkdocs.yml#L319-L321)
  sets the `material` theme, and its
  [build task](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/ci/tasks/build.yml#L5-L12)
  runs `mkdocs build` in the `squidfunk/mkdocs-material:9.7.6` image.
  MkDocs is a Python static site generator; Material for MkDocs is a
  documentation theme for it (it registers as an
  [MkDocs theme](https://github.com/squidfunk/mkdocs-material/blob/6d3dc570d51064a3f55d189bd22c2390b07d46fe/pyproject.toml#L90)).
  Its 40 tables are plain pipe tables (counted by this evaluation at
  docs-bosh commit `20a4122`;
  [table survey, bosh.io](../concepts/tables/survey/README.md#boshio)). This was read, not built. Learn more:
  [MkDocs](https://www.mkdocs.org/),
  [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/); see
  also the [glossary](../glossary.md#mkdocs-material).
- **The UAA and CredHub API references** are generated from code. UAA's is
  built with Slate (a tool for single-page API references) from Spring REST
  Docs snippets (text generated from the API's tests): its
  [Gradle build](https://github.com/cloudfoundry/uaa/blob/f09cae02367b333bc17d58997c1ba8bf336b3fae/uaa/build.gradle.kts#L150-L193)
  runs the `*Docs` tests to write the snippets, then builds the
  [vendored Slate](https://github.com/cloudfoundry/uaa/tree/f09cae02367b333bc17d58997c1ba8bf336b3fae/uaa/slate)
  with Middleman. CredHub uses Spring REST Docs with Asciidoctor, and its
  [Gradle build](https://github.com/cloudfoundry/credhub/blob/c28c27a454a259f7506498390928713c9fd7f493/backends/credhub/build.gradle#L125-L131)
  copies the result into the CredHub application's static files. RFC #1642 asks who can vet the proposal for them
  ([L177](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L177)).
  Learn more: [Slate](https://github.com/slatedocs/slate),
  [Spring REST Docs](https://spring.io/projects/spring-restdocs).

**Not yet written:** whether bosh.io and the API references are in scope
for the new stack; that is a requirements question.

## Passed over

Things set aside during the evaluation. Each entry says what was done, why
it was set aside, where the evidence is, and what would change the
decision. These are recorded because the reasons may be wrong.

### Generators not placed in a tier

**What was done:** only read about. MkDocs
([BSD-2-Clause](https://github.com/mkdocs/mkdocs/blob/2862536793b3c67d9d83c33e0dd6d50a791928f8/LICENSE);
[last commit](https://github.com/mkdocs/mkdocs/commit/2862536793b3c67d9d83c33e0dd6d50a791928f8)
dated 2025-10-20, checked 2026-10-10), mdBook
([MPL-2.0](https://github.com/rust-lang/mdBook/blob/d4658998d44112e873c90049767d7eb002169a2d/LICENSE)),
Jekyll ([MIT](https://github.com/jekyll/jekyll/blob/541d8b2ee75c8907de4744d4b87a7a6f1f997cae/LICENSE)),
Nextra ([MIT](https://github.com/shuding/nextra/blob/d6e80e1dd627b781429a6ee989b15ebba688c8ea/LICENSE))
and Docsy, a Hugo theme
([Apache-2.0](https://github.com/google/docsy/blob/3dbd63ac95988f43713a8f7b0fbb06331acc47f8/LICENSE)),
had their licenses checked. None was built.

**Why:** Decision (evaluation scope, 2026-10): the evaluation was kept to
the likely candidates, the tools already tried out by the people working
on the CF docs. These five did not come up as candidates; Jekyll, for
example, was never proposed. Leaving them out was a choice of scope, not a
finding against them; any of them could be added now. RFC #1642
[L31](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L31)
names MkDocs as an alternative that "MAY be evaluated".

**Evidence:** none in this repository yet.

**What would change it:** a requirement one of them meets better than the
tiered tools, or a question from the Docs WG.

### Width variants A and B

**What was done:** the six tables on `troubleshooting_slow_requests` were
built three ways in Docusaurus: A as written, B with uniform widths
(25/25/50), C with no widths so the column roles decide.

**Why:** C was chosen after the renderings were compared. The six tables
share one Result / Explanation / Action shape, and the template convention
that came out of the round is that widths follow the column roles (`key`,
`prose`) where a table's widths carry no other intent ([R-03](../requirements/README.md#r-03) column widths
as hints).

**Evidence:** [width variants](../concepts/tables/results.md#width-variants-for-troubleshooting_slow_requests),
with screenshots of table 2 in each.

**What would change it:** pages where roles alone size columns badly, or an
owner who needs the exact source widths.

### A table title as a caption or a spanning row

**What was done:** the `metadata` title was built as a spanning row above
the column headers, as a caption, and as a bold line above the table.

**Why:** a bold line above the table. Markdown and Markdoc tables have one
header row, so a spanning title row pushes the column headers into the body
([R-02](../requirements/README.md#r-02) rich tables). Passthrough keeps the source's spanning row.

**Evidence:** [side by side](../concepts/tables/results.md#provisional-changes-side-by-side);
[Starlight finding 4](../concepts/tables/results.md#findings-2).

**What would change it:** a format chosen for every page that has two
header rows, or owners who need the title inside the table.

### Joining HTML table cells onto one line for Markdoc

**What was done:** putting each cell on one line keeps the spaces Markdoc
otherwise drops next to inline tags; tried in Starlight passthrough.

**Why:** not adopted as a general conversion rule, because it makes the
source harder to read ([R-11](../requirements/README.md#r-11) readable source). It is used only where Markdoc
would change the text.

**Evidence:** [Starlight summary](../concepts/tables/results.md#starlight-0426).

**What would change it:** a Markdoc version that keeps those spaces, or a
decision that passthrough source readability matters less than a uniform
rule.

### Typographic quotes in Starlight

**What was done:** the Markdoc integration's `typographer` setting was
turned on.

**Why:** off. It also changes quotes inside `<pre>` blocks and HTML
`<code>`, which changes content ([R-01](../requirements/README.md#r-01) content and outline survive).

**Evidence:** [Starlight finding 9](../concepts/tables/results.md#findings-2).

**What would change it:** a setting that applies only to prose.

### Snippet includes for partials in Zensical

**What was done:** the scale-table partial was included with a `--8<--`
snippet.

**Why:** the template engine's `include` is used instead. A snippet is
inserted after variables are filled in, so the partial's
`<%= vars.recommended_by %>` showed as text ([R-05](../requirements/README.md#r-05) partials and reuse).

**Evidence:** [Zensical finding 7](../concepts/tables/results.md#findings-1).

**What would change it:** a snippet option that runs before variables are
filled in.
