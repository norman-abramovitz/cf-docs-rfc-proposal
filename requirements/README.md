# Requirements

Status: draft Docs WG position, incomplete — covers what is known as of 2026-10-10.

## What this is

This document says what the Docs WG is looking for in a new documentation
stack for Cloud Foundry. The Docs WG is the Cloud Foundry working group that
edits, merges and publishes the docs at `docs.cloudfoundry.org` (its
[charter](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/docs.md);
[glossary](../glossary.md#docs-wg)).

Today the site is built by Bookbinder, a Ruby tool that collects pages
from the 12 `docs-*` content repositories listed in the book's
[`config.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml) into one site
([glossary](../glossary.md#bookbinder)). The collection is called the book,
and its settings live in
[docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry).

It is a **draft position**. Nothing here has been agreed by the Docs WG yet,
and parts of it may be wrong. Each requirement has one of two statuses:

- `proposed`: stated and ready to discuss.
- `open`: part of the requirement waits on a decision, named in its
  statement.

The requirements say what the docs need, not which tool or file format
provides it. Which tools meet them is in [Tooling](../tooling/README.md); the
side-by-side results are in [POC](../poc/README.md).

## Relation to RFC #1642

[RFC #1642](https://github.com/cloudfoundry/community/pull/1642) is a Request
for Comments: the Cloud Foundry community's process for proposing a change
that affects many teams ([glossary](../glossary.md#rfc)). It proposes moving
the docs to Markdown on a modern static site generator (a program that turns
a folder of text files into a website; [glossary](../glossary.md#static-site-generator)),
hosted on GitHub Pages (GitHub's hosting for static sites;
[glossary](../glossary.md#github-pages)). This document is a more detailed set of requirements
meant to feed that RFC.

The RFC is a draft too. Every quote from it here is exact and taken from commit
`c737539` of the pull request, file `toc/rfc/rfc-draft-new-cf-docs-stack.md`;
each quote links to its line, as in [L42]. Where this document disagrees with
the RFC, it quotes the RFC and states the position next to the quote
([below](#where-the-rfc-is-wrong-or-incomplete)).

The RFC writes MUST, SHOULD and MAY in capitals. These are RFC 2119 keywords:
a requirement, a recommendation and an option
([glossary](../glossary.md#rfc-2119-keywords)). The requirements below use a
plain "must".

## Parts

| Part | What it covers |
|---|---|
| This page | The requirement list, and where the RFC is wrong or incomplete |
| [Audiences](audiences.md) | Who changes the docs, who else is affected, and what each needs |
| [Keep and pain](keep-and-pain.md) | What works today and must stay; what causes problems |
| [Research areas](research-areas.md) | Questions that still need an answer, and what would answer them |
| [Migration](migration.md) | The steps from today's book to the new site |

## Requirements

Each requirement has an ID and a short phrase, so "[R-03](#r-03) column widths as
hints" can be cited on its own. IDs are never renumbered; new ones are added
at the end. The other documents cite these IDs.

Terms used in the table:

- **Variable:** a named value defined once and inserted into pages when the
  site is built. Today it is written `<%= vars.name %>` and defined in the
  book's [`template_variables.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml)
  ([glossary](../glossary.md#variable)).
- **Partial:** a file of content that other pages include, today with
  `<%= partial 'name' %>` ([glossary](../glossary.md#partial)).
- **Test pages:** the five pages with complex tables that the Docs WG lead
  chose for testing tools, plus one added later
  ([list](../concepts/tables/README.md#test-pages)).
- **Concept:** one documentation feature (tables, variables, notes, …) worked
  through every candidate tool at a time
  ([concepts](../concepts/README.md)).

### Content

| ID | Phrase | Statement | Source | Status |
|---|---|---|---|---|
| <a id="r-01"></a>R-01 | content and outline survive | A converted page keeps its words, code, links, heading tree and section order. Content may be restructured only where its source structure was chosen for formatting, and each such change is recorded as a deviation. | [Concepts principles](../concepts/README.md#principles) | proposed |
| <a id="r-02"></a>R-02 | rich tables | Tables can hold lists and paragraphs in cells, cells that span columns, row headers, a title above the column headers, and variables in cells, as the test pages do. A table wider than the page scrolls in its own box. | [L42]; [test pages](../concepts/tables/README.md#what-the-pages-have-in-common) | proposed |
| <a id="r-03"></a>R-03 | column widths as hints | An author can say how wide a column should be and whether it should avoid wrapping. The site honors this as intent, not as an exact value: a column's role (a short key, a value, or prose) decides most widths. | [L42]; [hints](../concepts/tables/README.md#hints-after-the-round) | proposed |
| <a id="r-04"></a>R-04 | variables everywhere | Variables work in prose, in table cells, inside HTML and in page descriptions. A variable whose value is HTML renders as markup, not as escaped text. A variable that is not defined is reported when the site builds, instead of showing as empty text. | [L43]; [variables in cells](../concepts/tables/README.md#what-the-pages-have-in-common) | proposed |
| <a id="r-05"></a>R-05 | partials and reuse | A page can include a partial, and the partial renders inside it. Today a page can also pick its partial from a variable (`scale_table: "oss_scale_table"`); whether that is still needed is an [open question](research-areas.md#are-partial-names-in-variables-still-needed). | [L179]; [`_oss_scale_table`](../concepts/tables/source/SOURCES.md) | proposed |
| <a id="r-06"></a>R-06 | typed code blocks | Code blocks show their type (shell, console, JSON, YAML) with matching highlighting, keep their text exactly, and have a copy button. | [L44]; [tables findings](../concepts/tables/README.md#what-we-learned) | proposed |
| <a id="r-07"></a>R-07 | notes and admonitions | A note, today `<p class="note">` with a `note__title` span, becomes an admonition (a boxed callout headed Note, Warning, and so on; [glossary](../glossary.md#admonition)) with the same text, including notes held in a variable. | [Concepts list](../concepts/README.md#concepts); [L100] | proposed |
| <a id="r-08"></a>R-08 | cross-repository links | Links between pages that come from different content repositories keep working after conversion, whatever the new repository layout. | [L131] | proposed |
| <a id="r-09"></a>R-09 | table styles by class | Each table names its look with a style class (a name the site's stylesheet gives a look to; [glossary](../glossary.md#style-class)). `table` is the standard style. A further style is one more class and a few stylesheet rules, maintained by the Docs WG. Which further styles to offer is open. | [Template conventions](../concepts/tables/README.md#template-conventions) | proposed |

### Authoring

| ID | Phrase | Statement | Source | Status |
|---|---|---|---|---|
| <a id="r-10"></a>R-10 | simple text plus HTML where needed | Authors write most content in a simple text format and use HTML where that format falls short, as today's pages do. The format is chosen against these requirements; Markdown is a candidate, not a given. | [Concepts principles](../concepts/README.md#principles); [L42]; [L104] | proposed |
| <a id="r-11"></a>R-11 | readable source | An author can read and edit a page's source, tables included, without knowing the build tool's programming language. | [Source readability](../concepts/tables/results.md#summary) | proposed |
| <a id="r-12"></a>R-12 | one-command local preview | A contributor previews a change with one command, without installing a language toolchain by hand; a container option is offered. | [L20]; [L38]; [L162] | proposed |
| <a id="r-13"></a>R-13 | no per-WG extensions | Working groups do not write extensions (code added to the build tool so it handles markup it lacks; [glossary](../glossary.md#extension)). The Docs WG maintains shared extensions that every page can use; another working group adds one only with Docs WG approval. | [L100]; [L104]; [tables results](../concepts/tables/results.md#summary) | proposed |
| <a id="r-22"></a>R-22 | spellcheck with a shared dictionary | Every docs pull request is spellchecked against a shared project dictionary that the Docs WG maintains, so CF and technical terms can be added. | [L96] | proposed |
| <a id="r-28"></a>R-28 | onboarding before cutover | Current maintainers get time to learn the new toolchain before the new site replaces the old one. | [L115] | proposed |

### Publishing and governance

| ID | Phrase | Statement | Source | Status |
|---|---|---|---|---|
| <a id="r-14"></a>R-14 | Docs WG approves and publishes | Only Docs WG approvers merge content and start publishing. The Docs WG reviews every pull request. | [L54]; [L82]; the [book README](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/README.md#L70) today | proposed |
| <a id="r-17"></a>R-17 | an owner for every area | Every documentation area has a named working-group owner, listed in a `CODEOWNERS` file (a GitHub file that names who must review changes to which paths; [glossary](../glossary.md#codeowners)), before its pages migrate. | [L75]; [L114] | proposed |
| <a id="r-19"></a>R-19 | open source only | Every tool in the stack is open source. Whether this also covers services, such as a hosted search index or the hosting itself, is open. | [Concepts principles](../concepts/README.md#principles) | open |
| <a id="r-27"></a>R-27 | a named owner for every task | Each task the new stack creates (migration, technical support of the build, the domain and DNS, the shared extensions, the dictionary) has a named owner before the phase that needs it. | [L172]; [L174]; [L176]; [L178] | proposed |

### Site

| ID | Phrase | Statement | Source | Status |
|---|---|---|---|---|
| <a id="r-15"></a>R-15 | URL identifies the source | From a page's URL a contributor can tell which repository and file to edit. Today `docs.cloudfoundry.org/<dir>/<file>.html` maps to `<file>.html.md.erb` in the repository that the book's `config.yml` assigns to `<dir>`. If the content moves into one repository, its directories keep that mapping. | Docs WG lead's comment on the RFC pull request; [`config.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml#L33-L37) | proposed |
| <a id="r-16"></a>R-16 | old URLs keep working | Every published URL still resolves after cutover, directly or by redirect. Heading anchors keep their ids where the conversion can keep them. | [L46]; [L58]; [L61]; [L137] | proposed |
| <a id="r-18"></a>R-18 | full-text search | The site has working full-text search across all its pages. | [L21]; [L36] | proposed |
| <a id="r-20"></a>R-20 | search-engine and AI-friendly output | The site is plain, crawlable HTML with page titles, descriptions, canonical URLs (the one address search engines should use for a page) and a sitemap, so search engines and AI-based developer tools can read it. Whether to publish an `llms.txt` file (a plain-text index of the site's pages for such tools; [glossary](../glossary.md#llmstxt)) is open. | [L22]; [L40]; [L41] | proposed |
| <a id="r-21"></a>R-21 | versioning | Version 1 publishes one version of the docs. How versions follow CF releases is decided later, from experience with Version 1. | [L37]; [L92]; [L94] | open |
| <a id="r-29"></a>R-29 | API docs in the same pipeline | The UAA API docs, and the CredHub API docs if they are in scope, are built and published by the same pipeline as the rest of the docs. | [L13]; [L177]; Docs WG lead's pre-review comment | proposed |

### Migration

| ID | Phrase | Statement | Source | Status |
|---|---|---|---|---|
| <a id="r-23"></a>R-23 | one central conversion | One central team converts all content the same way, with one set of rules, not each working group on its own. | [L131] | proposed |
| <a id="r-24"></a>R-24 | markup cleanup before conversion | Markup that browsers accept but strict parsers reject is fixed before, or as the first step of, conversion, and each fix is recorded. | [Markup that only browsers tolerate](../concepts/tables/README.md#markup-that-only-browsers-tolerate) | proposed |
| <a id="r-25"></a>R-25 | build-time values are expected differences | When a converted page is compared with the published page, values set at build time (the copyright year in the footer, "Page last updated") count as expected differences. | [Copyright concept](../concepts/README.md#concepts) | proposed |
| <a id="r-26"></a>R-26 | owner review of migrated pages | The owning working group reviews every migrated section before cutover. | [L131] | proposed |

IDs added after the first 26 so far:

- [R-27](#r-27) a named owner for every task
- [R-28](#r-28) onboarding before cutover
- [R-29](#r-29) API docs in the same pipeline

## Where the RFC is wrong or incomplete

### Extensions (L100, L104)

> Working Groups MUST NOT need custom extensions, plugins, or JavaScript code to author documentation.

([L100])

> A Docusaurus proof of concept for Stratos showed that MDX does not fully replace raw HTML. To address this, reusable MDX content (partials, snippets, and the built-in Docusaurus components) SHOULD be used instead of raw HTML, without writing custom JavaScript or React components. The PoC MUST validate that the most complex existing pages (HTML tables, CSS layouts) can be represented with MDX alone.

([L104])

**Position.** MDX is Markdown that can also hold JSX, the HTML-like syntax
of the React library ([glossary](../glossary.md#mdx)). The RFC's own evidence
at [L104] says MDX alone falls short. The tables round (the first concept,
worked by hand in four candidate tools: Docusaurus, Zensical, Starlight and
Antora; see [Tooling](../tooling/README.md)) found the same. Every tool needs
stylesheet rules for two table hints (statements of author intent, here a
column's role and "don't wrap"; [glossary](../glossary.md#hint)). Docusaurus,
Zensical and Starlight need a small extension to carry them; Antora and a
one-page Sphinx test carry them as classes with no code
([results](../concepts/tables/results.md#summary)). The rule should be about
who writes extensions, not whether any exist: working groups do not write
their own, the Docs WG maintains shared extensions that apply across all
documentation, and another working group adds one only with Docs WG approval
([R-13](#r-13) no per-WG extensions). Suggested wording for both lines was posted on the pull request on 2026-10-09 ([L100 suggestion](https://github.com/cloudfoundry/community/pull/1642#discussion_r4228197509), [L104 suggestion](https://github.com/cloudfoundry/community/pull/1642#discussion_r4228197535)); as of 2026-10-10 neither has been applied.

**History.** The rule at [L100] is recent. The RFC's first version (commit `4dbccd9`, 2025-06-30) said at [L77](https://github.com/cloudfoundry/community/blob/4dbccd9eba2cb1857f11a24b963f91ae24f56373/toc/rfc/rfc-draft-new-cf-docs-stack.md#L77):

> The chosen framework SHOULD support a plugin or extension mechanism so that Working Groups can add custom components (e.g., interactive CLI examples, version-specific callouts) without forking the core tooling. Docusaurus MDX support covers this use case. Custom extensions MUST be documented and reviewed to avoid introducing new maintenance burdens.

Commit `3dbd2c3` (2026-10-06) replaced it with the "MUST NOT" wording quoted above ([L97 at that commit](https://github.com/cloudfoundry/community/blob/3dbd2c3c3c149cae36bd059b7677a0b5295f3bda/toc/rfc/rfc-draft-new-cf-docs-stack.md#L97)). The position above is closer to the first version: extensions are allowed and reviewed, and the Docs WG owns them.

### Who does the conversion work (L160 vs L131)

> **Migration effort:** Converting ERB/HTML to Markdown at scale requires significant up-front work from Working Groups.

([L160])

> The conversion MUST be done by one central migration team to ensure consistency, not by each Working Group individually.

([L131])

**Position.** [L131] is right, and matches what the Docs WG lead asked for in
the RFC's pre-review (comments on an earlier draft, made in a shared document
before the pull request opened): all conversion done by the migration team, the same way
for every repository. [L160] should describe the central team's workload. The
working groups' share is reviewing their migrated pages ([R-23](#r-23) one
central conversion, [R-26](#r-26) owner review of migrated pages).

### Positive bullets the Docs WG lead disputed (L151, L154)

> **Lower contribution barrier:** Any developer familiar with Markdown and GitHub can contribute documentation without learning a proprietary toolchain.

([L151])

**Position.** Contributing does not need a proprietary toolchain today. Pages
are Markdown with HTML and ERB tags (ERB is Ruby's templating syntax,
`<%= … %>`; [glossary](../glossary.md#erb)) and can be edited on GitHub; the
Docs WG lead made this point in the pre-review. Bookbinder, the tool that
assembles the book, is open source: its repository's
[LICENSE](https://github.com/pivotal-cf/bookbinder/blob/83bd2a57a8ba3d04c58a5be67607b243bdea0c64/LICENSE) is Apache-2.0, while its
[gemspec](https://github.com/pivotal-cf/bookbinder/blob/83bd2a57a8ba3d04c58a5be67607b243bdea0c64/bookbinder.gemspec#L13) declares MIT. The real costs
are elsewhere: see [Keep and pain](keep-and-pain.md#what-causes-problems).

> **Community ownership:** Documentation deployment is run transparently by the Docs WG without depending on CFF staff.

([L154]; [L54] also says "removing any dependency on CFF staff")

**Position.** Nobody depends on Cloud Foundry Foundation (CFF) staff for the
docs work today: it is done in the working groups (Docs WG lead,
pre-review). What is outside the community's control is the hosting ([L24]),
which is a separate point. These two sentences should be removed or
restated as a hosting benefit.

### Also incomplete

- **Unmaintained dependencies are not in the Problem list** ([L17]–[L25]).
  The pre-review agreed this is the main reason to migrate. Bookbinder's
  repository has its
  [last commit](https://github.com/pivotal-cf/bookbinder/commit/83bd2a57a8ba3d04c58a5be67607b243bdea0c64)
  on 2024-10-17 (checked 2026-10-10).
- **Local preview exists today.** [L20] says contributors "have no easy way
  to preview generated documentation locally". The book's
  [README](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/README.md#L56-L64) describes a local preview at
  `localhost:4567`. The gap is the setup it needs
  ([R-12](#r-12) one-command local preview).
- **One repository and the URL mapping.** [L69] puts all content in "ONE
  single documentation repository". That is compatible with [R-15](#r-15) URL identifies the source only if
  its directories map to today's URL directories.
- **Plain Markdown and HTML.** [L31] says the docs "SHOULD be rewritten in
  plain Markdown", while [L42] requires the "Ability to handle HTML". The
  position is [R-10](#r-10) simple text plus HTML where needed.
- **Partials are partly answered.** [L179] asks "Are partials supported by
  Docusaurus?" Every tool in the tables round included the scale-table
  partial from a host page, Docusaurus through an MDX import
  ([sources](../concepts/tables/source/SOURCES.md)). Partials picked by a
  variable are still open ([R-05](#r-05) partials and reuse).
- **bosh.io is not mentioned.** Its docs are a separate site with 40 tables
  (counted by this evaluation at docs-bosh commit `20a4122`; the count's
  data is not yet in this repository); see [Research areas](research-areas.md#is-boshio-in-scope).

**Not yet written:** requirements that come out of the concepts not yet
worked (headings, variables, partials, notes, code blocks, cross-repository
links; [concepts](../concepts/README.md#concepts)). They will sharpen
the requirements from [R-04](#r-04) variables everywhere to [R-08](#r-08)
cross-repository links.

[L13]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L13
[L17]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L17
[L20]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L20
[L21]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L21
[L22]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L22
[L24]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L24
[L25]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L25
[L31]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L31
[L36]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L36
[L37]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L37
[L38]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L38
[L40]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L40
[L41]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L41
[L42]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L42
[L43]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L43
[L44]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L44
[L46]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L46
[L54]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L54
[L58]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L58
[L61]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L61
[L69]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L69
[L75]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L75
[L82]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L82
[L92]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L92
[L94]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L94
[L96]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L96
[L100]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L100
[L104]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L104
[L114]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L114
[L115]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L115
[L131]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L131
[L137]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L137
[L151]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L151
[L154]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L154
[L160]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L160
[L162]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L162
[L172]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L172
[L174]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L174
[L176]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L176
[L177]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L177
[L178]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L178
[L179]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L179
