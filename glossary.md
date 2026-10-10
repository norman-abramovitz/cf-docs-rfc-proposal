# Glossary

Status: draft, incomplete — covers what is known as of 2026-10-10.

Terms used in the [requirements](requirements/README.md),
[tooling](tooling/README.md) and [POC](poc/README.md) documents. Each of
those documents defines a term where it first uses it, so none of them needs
this page; this page is for going further. Each entry says what the term is,
where it matters in this repository, and where to learn more. Quotes from
RFC #1642 are from its text at commit `c737539` and link to the line.

## Formats

### HTML

The markup language of web pages. The CF source pages are Markdown that
switches to HTML wherever Markdown falls short, above all for tables:
column widths, lists and paragraphs in cells, a title row spanning the
columns. RFC #1642 asks for the "Ability to handle HTML, especially HTML
tables with column-width specification supported" ([RFC L42][L42]). Why
tables come first and what the test pages' HTML looks like:
[concepts/tables/README.md](concepts/tables/README.md#test-pages).

Learn more: [HTML standard](https://html.spec.whatwg.org/),
[MDN HTML reference](https://developer.mozilla.org/en-US/docs/Web/HTML).

### Markdown

A plain-text writing format: `#` for headings, `-` or `*` for lists,
backticks for code, and HTML allowed wherever Markdown has no syntax of its
own. It has many dialects (CommonMark, GFM, kramdown, Python-Markdown and
others) that agree on the basics and differ on tables, attributes and edge
cases. RFC #1642 says the docs "SHOULD be rewritten in plain Markdown"
([RFC L31][L31]); this repository treats Markdown as one candidate, not a
requirement ("The source format is open", [concepts/README.md](concepts/README.md)).

Learn more: [CommonMark](https://commonmark.org/) (includes a short
tutorial).

### CommonMark

A precise specification of Markdown's core syntax, with a test suite,
written to end the disagreements between Markdown implementations. It has
no tables; GFM adds them. MDX (Docusaurus), Markdoc (Starlight) and
markdown-it (the Eleventy probe) all parse CommonMark, while
Python-Markdown (Zensical) follows the older original Markdown rules, which
is one reason the same page can need different indentation per tool
([tooling/formats.md](tooling/formats.md)).

Learn more: [CommonMark](https://commonmark.org/).

### GFM

GitHub Flavored Markdown: CommonMark plus pipe tables, strikethrough, task
lists and automatic links. GitHub uses it to show Markdown files, including
the pages of this repository read raw. Docusaurus's native mode writes GFM
pipe tables
([sites/docusaurus/CONVENTIONS.md](concepts/tables/sites/docusaurus/CONVENTIONS.md)),
and this repository's Pages build reads its Markdown as GFM
([_config.yml](_config.yml)).

Learn more: [GFM specification](https://github.github.com/gfm/).

### Pipe table

Markdown's table syntax from GFM: one line per row, cells separated by
`|`, and a line of dashes under the header row. A cell holds one line of
inline text, so a list or a second paragraph in a cell needs inline HTML,
and there are no widths, row headers or spanning cells, only left, center or
right alignment per column. Docusaurus native, Zensical native and
native-plain, and Starlight native-plain use pipe tables; the round found
that "List-table syntaxes carry most hints; pipe tables carry few"
([concepts/tables/README.md](concepts/tables/README.md#what-we-learned)).

Learn more: [GFM specification, tables](https://github.github.com/gfm/#tables-extension-).

### kramdown

A Markdown converter written in Ruby and the default in Jekyll. It has its
own syntax for attributes and can also read GFM. Only this repository's
own GitHub Pages build uses it ([_config.yml](_config.yml)); none of the
candidate tools does, and the published CF book uses a different Ruby
Markdown engine, Redcarpet
([probes/middleman/README.md](concepts/tables/probes/middleman/README.md)).

Learn more: [kramdown](https://kramdown.gettalong.org/).

### Python-Markdown

A Markdown converter written in Python, extended through plug-ins such as
tables, attribute lists and the pymdown-extensions collection. It follows the
original Markdown rules rather than CommonMark, so nested lists need
four-space indents. Zensical (and MkDocs) read pages through it; it passes HTML
blocks through as written, which is why all five test pages build unchanged
in Zensical, and Zensical's extension mode is a Python-Markdown block
([sites/zensical/CONVENTIONS.md](concepts/tables/sites/zensical/CONVENTIONS.md)).

Learn more: [Python-Markdown](https://python-markdown.github.io/).

### MDX

Markdown with JSX: a page can import components and data and use them as
HTML-like tags, and `{…}` holds a JavaScript expression. MDX compiles the
whole page, its HTML included, as JSX, so markup that browsers tolerate stops
the build and literal braces in prose must be escaped; all five test pages
failed as written
([results.md](concepts/tables/results.md#raw-passthrough-errors)).
Docusaurus 3 uses MDX 3, which the RFC names as the replacement for ERB
([RFC L31][L31], [L39][L39]), and RFC §5 says "The PoC MUST validate that the
most complex existing pages (HTML tables, CSS layouts) can be represented
with MDX alone" ([RFC L104][L104]).

Learn more: [MDX](https://mdxjs.com/).

### JSX

An HTML-like syntax inside JavaScript, used by React to describe what a
component renders. It is stricter than HTML: every element must be closed
(`<br />`), `style` takes an object (`style={{width: '20%'}}`), and braces
start an expression. MDX reads a page's HTML as JSX, which is where most of
Docusaurus's passthrough cleanup comes from
([sites/docusaurus/CONVENTIONS.md](concepts/tables/sites/docusaurus/CONVENTIONS.md)).

Learn more: [Writing markup with JSX](https://react.dev/learn/writing-markup-with-jsx).

### Markdoc

Markdown with `{% %}` tags, made by Stripe for its own documentation. Tags
such as `{% table %}` and `{% partial %}` add structure, and `{% $name %}`
prints a variable. In this evaluation Starlight reads Markdoc pages (`.mdoc`)
with HTML allowed. Markdoc reads the text inside HTML as Markdown, which
changed content without an error in passthrough (a lone `-` became a list,
spaces next to inline tags disappeared), while its own table tag carries
widths and lists in cells
([results.md](concepts/tables/results.md#starlight-0426)).

Learn more: [Markdoc](https://markdoc.dev/).

### AsciiDoc

A plain-text markup language with a larger built-in vocabulary than
Markdown: tables with widths and row headers, admonitions, includes and
attributes (variables) are part of the language. Asciidoctor is the usual
processor. Antora reads only AsciiDoc, so every test page was rewritten from
Markdown in every mode, and that rewrite failed silently in four ways
([results.md](concepts/tables/results.md#antora-321)); its tables are written
`[%header,cols=…]` between `|===` lines
([sites/antora/CONVENTIONS.md](concepts/tables/sites/antora/CONVENTIONS.md)).

Learn more: [AsciiDoc](https://asciidoc.org/),
[Asciidoctor](https://asciidoctor.org/).

### MyST

Markedly Structured Text: a Markdown dialect that adds the directives and
roles of reStructuredText, Sphinx's original format. A directive is a fenced
block with a name and options, such as `{list-table}`. The Sphinx probe
writes the scale table as a MyST list table and takes the CF variables in as
substitutions
([probes/sphinx-myst/README.md](concepts/tables/probes/sphinx-myst/README.md)).

Learn more: [MyST](https://mystmd.org/),
[MyST parser for Sphinx](https://myst-parser.readthedocs.io/).

### List table

A table written as a nested list: each row is a list item and each cell an
item inside it, so a cell can hold lists and paragraphs. It comes from the
`list-table` directive of reStructuredText, which MyST also has; its options
name the widths, header rows and row-header columns (`widths`,
`header-rows`, `stub-columns`). The extension modes for Docusaurus and
Zensical add a list table with the same option names, and Starlight's
extension puts them on Markdoc's table tag
([sites/docusaurus/CONVENTIONS.md](concepts/tables/sites/docusaurus/CONVENTIONS.md),
[sites/zensical/CONVENTIONS.md](concepts/tables/sites/zensical/CONVENTIONS.md)).

Learn more: [MyST parser, tables](https://myst-parser.readthedocs.io/en/latest/syntax/tables.html),
[reStructuredText `list-table`](https://docutils.sourceforge.io/docs/ref/rst/directives.html#list-table).

### ERB

Embedded Ruby: Ruby code inside a text file between `<%` and `%>`, where
`<%=` prints the result. The CF source pages are `.html.md.erb` files: ERB
runs first, then Markdown. They use it for variables (`<%= vars.name %>`)
and partials (`<%= partial 'name' %>`), and in Middleman `<%=` does not
escape HTML, so an HTML-valued variable renders as markup
([probes/middleman/README.md](concepts/tables/probes/middleman/README.md)).
RFC #1642's first problem is that "Documentation is written and maintained
using ERB/Ruby templates and a custom HTML pipeline" ([RFC L19][L19]).

Learn more: [ERB](https://github.com/ruby/erb).

### EJS

Embedded JavaScript templates: the same `<% %>` tags as ERB, with JavaScript
inside. The difference that matters here is escaping: EJS's `<%=` escapes
HTML and `<%-` does not, where the CF pages' `<%=` in Middleman does not
escape. The Eleventy probe built `uaa-concepts` with its ERB variable tags
read as EJS; HTML-valued variables, helpers and includes need `<%-`
([probes/eleventy/README.md](concepts/tables/probes/eleventy/README.md)).

Learn more: [EJS](https://ejs.co/).

### Liquid

A template language from Shopify, with `{{ name }}` and `{% tag %}`
syntax, used by Jekyll and many other tools. No candidate tool in this
round uses it. This repository's Pages build turns Liquid off, because code
samples in these documents use Markdoc and other syntax that looks like
Liquid and would otherwise be run ([_config.yml](_config.yml)).

Learn more: [Liquid](https://shopify.github.io/liquid/).

### Front matter

A block at the very top of a page, between two `---` lines, that holds the
page's settings in YAML, such as its title. The CF source pages have one,
with `title` and `owner`
([source/credential-types.html.md.erb](concepts/tables/source/credential-types.html.md.erb)).
Most candidate tools read front matter, each with its own keys; AsciiDoc
(Antora) uses header attributes instead. Docusaurus takes a page's
description from the first paragraph unless the front matter sets
`description:`, which put raw variable expressions into two descriptions
([results.md](concepts/tables/results.md#docusaurus-3102)).

Learn more: [Front matter in Jekyll](https://jekyllrb.com/docs/front-matter/).

## Tools

### Static site generator

A program that turns source files (Markdown, templates, a theme) into a
folder of finished HTML pages before anyone visits the site, so the server
only hands out files. RFC #1642 proposes that the docs be "managed via a
modern static site generator" ([RFC L31][L31]) and hosted on GitHub Pages,
which serves only static files. Every tool in this evaluation is one,
today's Bookbinder and Middleman included; the tiers are in
[concepts/README.md](concepts/README.md).

Learn more: [MDN glossary: SSG](https://developer.mozilla.org/en-US/docs/Glossary/SSG).

### Bookbinder

The Ruby tool that builds today's docs.cloudfoundry.org: it collects the
`docs-*` content repositories listed in docs-book-cloudfoundry into one
"book" and builds it with Middleman. Each repository maps to a fixed URL
directory, so a page's URL tells you which repository and file to edit
([README.md](README.md#background)), and it already offers a local preview.
The Middleman probe asks what is left when Bookbinder is removed: a short
configuration and a layout
([probes/middleman/README.md](concepts/tables/probes/middleman/README.md)).

Learn more: [Bookbinder](https://github.com/pivotal-cf/bookbinder),
[docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry).

### Middleman

A Ruby static site generator; Bookbinder uses it to render the book's ERB,
Markdown and HTML into pages. The Middleman probe built all five test pages
unchanged with Middleman 4.6.3 on Ruby 4.0.7 and no Bookbinder, and every
table matched the published page cell for cell. It is the minimal-change
baseline: Bookbinder goes, the source format stays
([probes/middleman/README.md](concepts/tables/probes/middleman/README.md),
[requirements/keep-and-pain.md](requirements/keep-and-pain.md)).

Learn more: [Middleman](https://middlemanapp.com/).

### Docusaurus

A documentation site generator from Meta, built on React; pages are Markdown
or MDX. RFC #1642 says "The recommended engine is the current major version
of Docusaurus" ([RFC L31][L31]). A hands-on tool here (3.10.2): no test page
built with its HTML unchanged, every table rendered correctly after cleanup,
and its pipe tables carry no width hints
([results.md](concepts/tables/results.md#docusaurus-3102),
[sites/docusaurus/CONVENTIONS.md](concepts/tables/sites/docusaurus/CONVENTIONS.md)).

Learn more: [Docusaurus](https://docusaurus.io/).

### Zensical

A static site generator from the creators of Material for MkDocs; it reads
Markdown through Python-Markdown and is designed to build existing MkDocs
projects. A hands-on tool here (0.0.69): all five test pages built with their
HTML unchanged, and the variables kept their ERB form through its built-in
macros support
([results.md](concepts/tables/results.md#zensical-0069),
[sites/zensical/CONVENTIONS.md](concepts/tables/sites/zensical/CONVENTIONS.md)).

Learn more: [Zensical](https://zensical.org/).

### MkDocs Material

Material for MkDocs: a theme and set of extensions for MkDocs, a Python
static site generator that reads Markdown through Python-Markdown. RFC #1642
says "Other frameworks such as Hugo or MkDocs MAY be evaluated and proposed
as alternatives during the PoC phase" ([RFC L31][L31]). It is not a hands-on
tool in this round, but bosh.io's documentation (`docs-bosh`, owned by the
FI WG) is built with it, which matters for how bosh.io relates to the new
site ([requirements/audiences.md](requirements/audiences.md),
[tooling/tools.md](tooling/tools.md)).

Learn more: [MkDocs](https://www.mkdocs.org/),
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

### Starlight

A documentation framework for Astro, a JavaScript site builder. Starlight
reads Markdown and MDX by default; here it ran with Astro's Markdoc
integration, so the pages are Markdoc with HTML allowed (Starlight 0.42.6,
Astro 7.3.8). Four of five pages parsed with their HTML unchanged, but
Markdoc changed text inside HTML without an error, and Markdoc's own table
tag carries widths and lists in cells with no custom code
([results.md](concepts/tables/results.md#starlight-0426),
[sites/starlight/CONVENTIONS.md](concepts/tables/sites/starlight/CONVENTIONS.md)).

Learn more: [Starlight](https://starlight.astro.build/),
[Astro](https://astro.build/).

### Antora

A documentation site generator for AsciiDoc that builds one site from
content kept in many git repositories, organized as versioned components. A
hands-on tool here (3.2.1): every page had to be rewritten as AsciiDoc,
while the HTML tables built unchanged inside passthrough blocks. AsciiDoc's
own tables carry most hints, and the extension needs no code, only roles and
a stylesheet
([results.md](concepts/tables/results.md#antora-321),
[sites/antora/CONVENTIONS.md](concepts/tables/sites/antora/CONVENTIONS.md)).

Learn more: [Antora](https://antora.org/).

### Sphinx

A Python documentation generator that reads reStructuredText and, with the
myst-parser extension, MyST Markdown. It ran as a probe (Sphinx 9.1.0,
myst-parser 5.1.0) to see whether list-table options carry the table hints:
the header row, row headers and widths yes, and the column roles and capped
no-wrap through classes and CSS, with no code
([probes/sphinx-myst/README.md](concepts/tables/probes/sphinx-myst/README.md)).

Learn more: [Sphinx](https://www.sphinx-doc.org/).

### Eleventy

A JavaScript static site generator (also written 11ty) that accepts many
template languages; since version 3, EJS is a plugin. It ran as a probe
(3.1.6): with the CF pages' `<%= vars.* %>` tags left as they are and read as
EJS, the `uaa-concepts` tables came out byte for byte as written
([probes/eleventy/README.md](concepts/tables/probes/eleventy/README.md)).

Learn more: [Eleventy](https://www.11ty.dev/).

### Hugo

A static site generator written in Go, with templates in Go's template
syntax. RFC #1642 names it, with MkDocs, as an alternative that "MAY be
evaluated" ([RFC L31][L31]). In this evaluation it is an on-paper tool, not
yet assessed ([concepts/README.md](concepts/README.md),
[tooling/tools.md](tooling/tools.md)).

Learn more: [Hugo](https://gohugo.io/).

### VitePress

A documentation site generator built on Vite and Vue; pages are Markdown,
with Vue components allowed. In this evaluation it is an on-paper tool, not
yet assessed ([concepts/README.md](concepts/README.md),
[tooling/tools.md](tooling/tools.md)).

Learn more: [VitePress](https://vitepress.dev/).

### Jekyll

A Ruby static site generator and the engine behind GitHub Pages' built-in
builds; it reads Markdown with kramdown and templates with Liquid. It is not
a candidate tool. This repository's own Pages site is built with Jekyll 4 by
a workflow ([.github/workflows/pages.yml](.github/workflows/pages.yml)), with
Liquid turned off and the tool folders left out ([_config.yml](_config.yml)).

Learn more: [Jekyll](https://jekyllrb.com/).

### Slate

A tool, built on Middleman, that turns Markdown into a single-page API
reference with navigation, explanations and code samples side by side. The
UAA API documentation is built with Slate from snippets that Spring REST
Docs generates, outside the Bookbinder book, and RFC #1642's summary covers
"the Cloud Foundry documentation (CF, UAA API)" ([RFC L13][L13]). Who
maintains these docs and what they need is in
[requirements/audiences.md](requirements/audiences.md).

Learn more: [Slate](https://github.com/slatedocs/slate).

### Spring REST Docs

A Spring project that documents a REST API from its tests: each test that
calls the API writes request and response snippets, which the documentation
pages include. The CredHub API docs use it, and it feeds the UAA API's Slate
pages, so these docs are partly generated from code rather than written by
hand. RFC #1642 asks "Who can we involve to vet this proposal for the UAA
API docs and the CredHub API docs?" ([RFC L177][L177]); see
[requirements/audiences.md](requirements/audiences.md).

Learn more: [Spring REST Docs](https://spring.io/projects/spring-restdocs).

## Terms used in this evaluation

### Concept

One kind of documentation content, such as tables, variables, partials,
notes or code blocks, taken as the unit of work. For each concept, real
pages are converted by hand into each candidate tool and the conventions
that work are recorded; those conventions later drive the conversion tool.
Tables is the first concept and the only one done so far
([concepts/README.md](concepts/README.md)).

Learn more: [concepts/README.md](concepts/README.md).

### Test pages

The real CF pages used for the tables concept: five pages the Docs WG lead
picked because their tables are hard to express outside HTML, plus a sixth,
`uaa-performance`, added later as the example of a second table style. They
are copied verbatim with their commits and licenses
([source/SOURCES.md](concepts/tables/source/SOURCES.md)).

Learn more: [concepts/tables/README.md](concepts/tables/README.md#test-pages).

### Intent file

One file per test page that says, for each table, what the source asks for
in tool-neutral hints, what markup cleanup it needs, which deviations from
the published page are deliberate, and which spot checks every converted
version must pass. It is written before any tool is tried, so every tool is
judged against the same intent. Example:
[intent/credential-types.md](concepts/tables/intent/credential-types.md).

Learn more: [concepts/tables/README.md](concepts/tables/README.md#method).

### Hint

What a table asks for, written once and independent of any tool: a column's
role, a width, "don't wrap", row headers, a title, a style. A hint expresses
the author's intent, not an exact value, and each tool and template honors
it as well as it can ("Everything else is a hint",
[concepts/README.md](concepts/README.md)). Column widths as hints are R-03
([requirements/README.md](requirements/README.md)).

Learn more: [Hints after the round](concepts/tables/README.md#hints-after-the-round).

### Column role

A hint that says what a column holds: `key` (a short label or identifier,
often code), `value` (a short value) or `prose` (sentences). The role sets a
column's default width, wrapping and alignment, so most tables need no
explicit widths; a `key` column avoids wrapping by default. No tool's table
syntax carries roles, so they travel as classes with CSS, or through a small
extension ([results.md](concepts/tables/results.md#summary)).

Learn more: [Hints after the round](concepts/tables/README.md#hints-after-the-round).

### No-wrap

A hint (`wrap: avoid`) that keeps a column's text on one line; `key`
columns have it by default. It wins over a width, so the column grows, but
only up to a cap the template sets (`--table-nowrap-max`, 16em by default),
past which the text wraps between words: the "capped no-wrap". Like the
column roles, it needs CSS in every tool
([results.md](concepts/tables/results.md#summary)).

Learn more: [Template conventions](concepts/tables/README.md#template-conventions).

### Mode

One of the ways each test page is converted into a hands-on tool:
passthrough, extension, native and native-plain, plus raw passthrough as a
check. Comparing modes shows what each tool costs at each level of change to
the source. Each site's `CONVENTIONS.md` has a section per mode, for example
[sites/zensical/CONVENTIONS.md](concepts/tables/sites/zensical/CONVENTIONS.md).

Learn more: [Method](concepts/tables/README.md#method).

### Passthrough

The mode that keeps each table's HTML as written, translating only variables
and partials to the tool's syntax, plus the cleanup the intent files list and
whatever the tool forces. It answers how much must change if authors keep
writing HTML tables (R-10 simple text plus HTML where needed,
[requirements/README.md](requirements/README.md)). The forced changes are in
each site's `CONVENTIONS.md`; Antora keeps the HTML inside an AsciiDoc
passthrough block (`++++`), which it does not parse
([sites/antora/CONVENTIONS.md](concepts/tables/sites/antora/CONVENTIONS.md)).

Learn more: [Method](concepts/tables/README.md#method).

### Raw passthrough

Passthrough with no cleanup: the source HTML exactly as published, with
only the variables and the partial line translated. It shows which tools take
today's markup, browser-tolerated defects included: Zensical, Antora and the
Middleman probe built all five pages, MDX failed on all five, and Markdoc
parsed four while changing text inside HTML. Each tool's section in
[results.md](concepts/tables/results.md#summary) ends with its raw results.

Learn more: [Raw passthrough errors in Docusaurus](concepts/tables/results.md#raw-passthrough-errors).

### Extension

A tool's own plug-in point, used to carry the hints its table syntax cannot:
a remark plugin in Docusaurus, a Python-Markdown block in Zensical,
attributes on Markdoc's table tag in Starlight (76 lines), and in Antora and
the Sphinx probe only classes and a stylesheet, no code. RFC #1642 says
"Working Groups MUST NOT need custom extensions, plugins, or JavaScript code
to author documentation" ([RFC L100][L100]). Extension mode shows what one
extension, maintained once for all documentation, closes (R-13 no per-WG
extensions, [requirements/README.md](requirements/README.md)).

Learn more: [results.md](concepts/tables/results.md#summary),
[remark](https://github.com/remarkjs/remark).

### Native

The mode that writes each table in the tool's own table syntax, with whatever
hint mechanism that syntax offers: pipe tables in Docusaurus and Zensical
(Zensical adds widths on header cells), Markdoc's `{% table %}` tag in
Starlight, AsciiDoc tables in Antora. It shows how far an author gets with
neither HTML nor an extension. Native tables get the standard table style in
every tool, as decided
([results.md](concepts/tables/results.md#summary)).

Learn more: [Method](concepts/tables/README.md#method).

### Native-plain

Native mode with no width or alignment specs at all: pipe tables in
Zensical and Starlight, AsciiDoc tables without `cols` in Antora
(Docusaurus's native mode is already plain). It shows what a table looks like
when the author writes only the content.

Learn more: [Native with and without widths](concepts/tables/results.md#native-with-and-without-widths).

### Spot check

A specific, checkable statement about a converted page, such as "7 body
rows, each with 2 cells" for `credential-types`. Each intent file lists them
per table, and `make check` in each site runs them against the built pages
with [checks/spot-checks.sh](concepts/tables/checks/spot-checks.sh). They are
this round's content check; an automated comparison of text and headings with
the published page belongs to cf-docs-migrate (R-01 content and outline
survive, [requirements/README.md](requirements/README.md)).

Learn more: [intent/credential-types.md](concepts/tables/intent/credential-types.md).

### Template

The site-wide layout and look that every page is rendered into: header,
navigation, footer, and how elements such as tables appear. Here it means the
CF site's chosen look, as opposed to a tool's default theme, and not a
templating language such as ERB. "Template conventions" are source markup
that conversions drop because the template does it anyway, such as bold
header cells; appearance belongs to the template and is not compared
([concepts/README.md](concepts/README.md)).

Learn more: [Template conventions](concepts/tables/README.md#template-conventions).

### Theme

The package that gives a tool's site its default look: layouts, CSS,
sometimes scripts. This round used each tool's default theme, so that hints
must work under any theme. The themes disagree on which tables they style:
Docusaurus and Starlight every table, Zensical only tables without a class,
Antora only its own AsciiDoc tables, and the Antora and Sphinx themes
hyphenate words in cells
([results.md](concepts/tables/results.md#summary)).

Learn more: [results.md](concepts/tables/results.md#summary).

### Style class

A class name on a table that names its look: `class="table"` for the
standard style, `table-media` for the image-grid example. Every HTML table
names its style with a class and each site's CSS gives the class its look; a
pipe table cannot carry a class, so it gets the standard style (R-09 table
styles by class, [requirements/README.md](requirements/README.md)). Which
further styles to support is open
([concepts/tables/README.md](concepts/tables/README.md#open-questions)); how
one is added is under "Adding a style" in each site's `CONVENTIONS.md`.

Learn more: [Template conventions](concepts/tables/README.md#template-conventions).

### Probe

A one-page experiment that answers a single question about a tool, short of
a full hands-on round. There are three: Eleventy (do ERB variable tags work
as EJS?), Sphinx with MyST (can list-table options carry the hints?) and
Middleman without Bookbinder (what is the smallest change that removes
Bookbinder?). Questions and answers are in
[results.md](concepts/tables/results.md#summary); the tiers in
[concepts/README.md](concepts/README.md).

Learn more: [Probes](concepts/tables/README.md#probes).

### Partial

A fragment of a page kept in its own file and included in other pages, so
shared content is written once. The CF pages include one with
`<%= partial 'name' %>`, and some partial names are themselves stored in
variables (`scale_table: "oss_scale_table"`). RFC #1642 asks "Are partials
supported by Docusaurus? If not, the migration will have to integrate them
into their calling topics." ([RFC L179][L179]) In this round every tool
included the `_oss_scale_table` partial, Docusaurus as an imported MDX
component
([sites/docusaurus/CONVENTIONS.md](concepts/tables/sites/docusaurus/CONVENTIONS.md);
R-05 partials and reuse).

Learn more: [Importing Markdown in Docusaurus](https://docusaurus.io/docs/markdown-features/react#importing-markdown).

### Variable

A named value defined once and inserted into many pages, such as the
product name. The CF book defines them in `template_variables.yml`, pages
insert them with `<%= vars.name %>`, some values hold HTML (a note), and two
that the test pages use are not defined anywhere, so they render empty
([source/template_variables.yml](concepts/tables/source/template_variables.yml)).
RFC #1642 asks for the "Ability to handle variables in a way that's easy and
transparent for contributers" ([RFC L43][L43]); each tool's syntax and how it
handles HTML values are in
[results.md](concepts/tables/results.md#summary) (R-04 variables
everywhere).

Learn more: [concepts/README.md](concepts/README.md).

### Admonition

A highlighted block that sets a note, tip or warning apart from the text
around it. The CF pages write notes as HTML, `<p class="note">` with a
`note__title` span, and one variable (`route_services`) holds such a note.
Most candidate tools have admonition syntax of their own, such as `:::note`
in Docusaurus. RFC #1642 says customization "is handled by MDX 3 features of
the current Docusaurus version, such as admonitions" ([RFC L100][L100]). Notes and admonitions are
a proposed concept, not yet worked ([concepts/README.md](concepts/README.md);
R-07 notes and admonitions).

Learn more: [Admonitions in Docusaurus](https://docusaurus.io/docs/markdown-features/admonitions).

### Well-formed markup

HTML in which every element is closed and correctly nested and every
attribute value is properly quoted. Browsers repair markup that is not, and
say nothing; strict readers do not: MDX stops, and Markdoc changes content. A
strict parse found 5 of 12 tables, on 4 of 5 test pages, not well-formed: an
unclosed `<col>`, unclosed `<td>` cells, curly quotes around a class, a row
ended with `</td>`
([concepts/tables/README.md](concepts/tables/README.md#markup-that-only-browsers-tolerate)).
Cleaning this up before conversion is R-24 markup cleanup before conversion
([requirements/README.md](requirements/README.md)).

Learn more: [HTML standard](https://html.spec.whatwg.org/).

## Project and process

### Docs WG

The Cloud Foundry Documentation Working Group. Its charter's mission is "To
document the Cloud Foundry user experience", and its scope starts with
"Merge and edit all doc changes". RFC #1642 keeps publishing with it: "Only
Docs WG approvers can merge into the central repository and trigger
deployments." ([RFC L54][L54]) The requirements in this repository are a
draft Docs WG position (R-14 Docs WG approves and publishes,
[requirements/README.md](requirements/README.md)).

Learn more: [Docs WG charter](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/docs.md).

### FI WG

The Foundational Infrastructure Working Group, whose scope covers BOSH, UAA
and CredHub and includes "Operate https://bosh.io". It owns `docs-bosh`, the
bosh.io documentation, which is built with MkDocs Material outside the
Bookbinder book. How bosh.io's docs relate to the new site is covered in
[requirements/audiences.md](requirements/audiences.md).

Learn more: [FI WG charter](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/foundational-infrastructure.md).

### RFC

Request for Comments: in the Cloud Foundry community, a written proposal for
a change that affects the project, discussed in public as a pull request
against `cloudfoundry/community` and kept under `toc/rfc`. RFC #1642,
"Cloud Foundry Documentation Modernization", is a draft that proposes moving
the CF docs to Markdown on a modern static site generator hosted on GitHub
Pages. These documents quote it by line at commit `c737539`, because a draft
changes; where they disagree, they say so next to the quote
([requirements/README.md](requirements/README.md)).

Learn more: [CF RFC process](https://github.com/cloudfoundry/community/tree/main/toc/rfc),
[RFC #1642](https://github.com/cloudfoundry/community/pull/1642).

### RFC 2119 keywords

The capitalized words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY, read with
the meanings RFC 2119 gives them: MUST is an absolute requirement, SHOULD a
recommendation that may be set aside for a good reason, MAY truly optional.
RFC #1642 uses them throughout, for example "Key capabilities the chosen
framework MUST provide" ([RFC L33][L33]) and "Working Groups MUST NOT need
custom extensions" ([RFC L100][L100]). A requirement's strength is in these
words ([requirements/README.md](requirements/README.md)).

Learn more: [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

### PoC

Proof of concept: a small working build that shows whether an approach
works before anyone commits to it. In RFC #1642 the PoC is Phase 2: "A PoC
SHOULD be established in a new repository (e.g., `cloudfoundry/docs-next`)"
to stand up the chosen tool with a representative subset of the docs
([RFC L119–L127][L119]). The [poc/](poc/README.md) documents in this
repository compare the hand conversions of the test pages across tools:
evidence gathered ahead of that Phase 2, not the Phase 2 PoC itself
([tooling/poc-scope.md](tooling/poc-scope.md)).

Learn more: [RFC #1642](https://github.com/cloudfoundry/community/pull/1642).

### CODEOWNERS

A file in a GitHub repository that maps paths to the people or teams who own
them; GitHub then asks those owners to review every pull request that
touches their paths. RFC #1642: "The docs repository contains a `CODEOWNERS`
file that assigns each documentation area to the GitHub team of the
responsible Working Group" ([RFC L74][L74]). Today's source pages already
name an owner in their front matter (`owner: CredHub`) (R-17 an owner for
every area,
[requirements/README.md](requirements/README.md)).

Learn more: [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

### GitHub Pages

GitHub's hosting for static sites, built from a repository by a GitHub
Actions workflow or by GitHub's own Jekyll build. RFC #1642: "The
documentation site MUST be deployed to GitHub Pages under the `cloudfoundry`
GitHub organization" ([RFC L50][L50]). This repository is published there
too ([.github/workflows/pages.yml](.github/workflows/pages.yml)). Whether
the open-source-only principle covers services such as Pages is an open
question
([concepts/tables/README.md](concepts/tables/README.md#open-questions)).

Learn more: [GitHub Pages](https://docs.github.com/en/pages).

### Algolia DocSearch

A hosted search service from Algolia, free for open-source documentation:
Algolia crawls the site and answers searches from its own index. RFC #1642
names it as an example of "Built-in full-text search" ([RFC L36][L36]) and
asks whether it "is the preferred search backend, or should a self-hosted
option (e.g., Pagefind, lunr.js) be used?" ([RFC L170][L170]). Pagefind
builds the index into the site at build time and needs no service. Because
the index is a proprietary service, the choice touches the open question on
open source
([concepts/tables/README.md](concepts/tables/README.md#open-questions); R-18,
R-19).

Learn more: [Algolia DocSearch](https://docsearch.algolia.com/),
[Pagefind](https://pagefind.app/).

### llms.txt

A proposed convention: a Markdown file at a site's root, `/llms.txt`, that
lists and summarizes the site's main pages so that tools built on large
language models can find them. RFC #1642 lists "optionally an LLM-friendly
`/llms.txt` index" among the capabilities the framework must provide
([RFC L41][L41]) and asks whether one should be published ([RFC L173][L173]).
Related: R-20 search-engine and AI-friendly output
([requirements/README.md](requirements/README.md)).

Learn more: [llms.txt](https://llmstxt.org/).

### cf-docs-migrate

The planned migration tool, not yet written. Its `scan` command would find
each concept's patterns in the source and its `convert` command would apply
the conventions recorded in each site's `CONVENTIONS.md`. It would also run
the automated content and outline check against the published pages,
treating build-time values such as the copyright year as expected
differences ([concepts/tables/README.md](concepts/tables/README.md#results-grid)).
The migration steps it serves are in
[requirements/migration.md](requirements/migration.md).

Learn more: [concepts/README.md](concepts/README.md).

[L13]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L13
[L19]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L19
[L31]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L31
[L33]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L33
[L36]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L36
[L39]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L39
[L41]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L41
[L42]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L42
[L43]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L43
[L50]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L50
[L54]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L54
[L74]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L74
[L100]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L100
[L104]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L104
[L119]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L119-L127
[L170]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L170
[L173]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L173
[L177]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L177
[L179]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L179
