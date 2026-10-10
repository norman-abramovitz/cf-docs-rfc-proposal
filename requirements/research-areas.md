# Research areas

Status: draft Docs WG position, incomplete — covers what is known as of 2026-10-10.

Questions the requirements depend on that nobody has answered yet. For each:
why it matters, what is known, and what would answer it. Requirement IDs
refer to the [requirement list](README.md#requirements).

## Scope

### Which repositories feed the docs, and who owns each?

- **Why it matters:** every area needs an owner before it migrates (R-17),
  and the URL mapping depends on the repository list (R-15).
- **Known:** the book's
  [`config.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/master/config.yml)
  (the settings file that tells Bookbinder, today's build tool, which
  repositories to collect) lists 12 sections, each a `docs-*` repository
  mapped to a URL directory, plus sample-code repositories with no pages. A
  survey of tables covered the 15 `docs-*` repositories that are not
  archived. The book's own `CODEOWNERS` file (which names who must review
  changes) lists one team for everything.
- **What answers it:** the inventory in the RFC's first phase ([L112],
  [L167]).

### Is bosh.io in scope?

- **Why it matters:** the RFC does not mention it, yet it is Cloud Foundry
  documentation with its own tables and notes (R-07, R-09), and the book
  already sends all of `/bosh/` to `bosh.io/docs` (R-16).
- **Known:** `bosh.io/docs` is built from
  [docs-bosh](https://github.com/cloudfoundry/docs-bosh) with MkDocs and its
  Material theme ([glossary](../glossary.md#mkdocs-material)), and is owned by
  the Foundational Infrastructure working group (FI WG;
  [glossary](../glossary.md#fi-wg)). Its 40 tables are all plain Markdown pipe
  tables; it has 302 admonitions (boxed callouts headed Note, Warning, and so
  on). The rest of bosh.io (release and stemcell pages) loads the stylesheet
  and scripts that the docs build produces, so changing the docs tool affects
  the whole site.
- **What answers it:** the FI WG, with the RFC authors. Draft position:
  bosh.io follows the Docs WG table and note conventions; a tool or hosting
  change is the FI WG's decision.

### How do the UAA and CredHub API references fit?

- **Why it matters:** R-29 API docs in the same pipeline.
- **Known:** the UAA API reference is built with Slate (a generator for
  one-page API references; [glossary](../glossary.md#slate)) from examples
  that Spring REST Docs writes during the API tests
  ([glossary](../glossary.md#spring-rest-docs)). CredHub also uses Spring REST
  Docs. Book pages link to both under `docs.cloudfoundry.org/api/`, and to
  versioned UAA pages. The RFC asks who can vet the proposal for them
  ([L177]).
- **What answers it:** the UAA and CredHub maintainers: where each reference
  is built and published, and whether it must change format to join the
  pipeline.

### What do downstream consumers reuse?

- **Why it matters:** if anyone copies raw source, the source format and
  partials matter to them (R-05); if they link to the site, URLs do (R-16).
- **Known:** the RFC names SAP BTP and anynines as examples and says VMware
  Tanzu "works from its own branches and is not affected" ([L113]), but its
  open questions still name Tanzu ([L168]). In the RFC's pre-review (comments
  on an earlier draft) the Docs WG lead stated that Broadcom's docs are
  written fully in-house.
- **What answers it:** the consumer survey in the RFC's first phase ([L113]).

## Content

### Are partial names in variables still needed?

- **Why it matters:** R-05 partials and reuse. A partial is a file of content
  included in other pages. Here the partial's name comes from a variable (a
  named value defined once and inserted at build time), so the include is
  decided at build time. No tool has been tested with that yet.
- **Known:** the book's `template_variables.yml` maps
  `scale_table: "oss_scale_table"` and `roles_table: "_oss_roles_table"`,
  apparently so that another edition of the docs could swap in its own table.
  Every tool in the tables round included the scale-table partial when it was
  named directly
  ([sources](../concepts/tables/source/SOURCES.md)).
- **What answers it:** the downstream survey above, and a search of the
  content repositories for partials included through a variable.

### What should undefined variables show?

- **Why it matters:** R-04 variables everywhere asks that an undefined
  variable be reported, not shown as empty text.
- **Known:** `metadata_ref` (in `metadata`) and `bosh_cli_link` (three times
  in `troubleshooting_slow_requests`) are defined nowhere in the book; the
  published pages show nothing in their place
  ([sources](../concepts/tables/source/SOURCES.md)). Other pages may have
  more.
- **What answers it:** a scan of every page for variables missing from
  `template_variables.yml`, then the page owners say what each should be.

### Which table styles beyond the standard one?

- **Why it matters:** R-09 table styles by class. A style class is a name the
  site's stylesheet gives a look to ([glossary](../glossary.md#style-class)).
- **Known:** a survey of all 241 tables in the docs and tutorial repositories
  found one class in use, `table`. The closest thing to a second style is a
  compact one for comparison grids and long reference tables. The tables
  round added `table-media`, an image grid, as an example of how a style is
  added ([template conventions](../concepts/tables/README.md#template-conventions)).
- **What answers it:** the Docs WG choosing from the survey's table families.

### What do the concepts not yet worked require?

- **Why it matters:** R-01, R-04 to R-08 and R-25 are stated from the tables
  round and from reading the source. Each concept (one documentation feature,
  worked through every candidate tool) can change them.
- **Known:** tables are done; headings, variables, partials, notes and
  admonitions, code blocks, cross-repository links, and copyright and
  build-time values are proposed
  ([concepts](../concepts/README.md#concepts)). The tables round already
  found problems outside tables: heading anchors written as `<a id>`, terminal
  blocks, the `*` lost in `Accept: */*`, and HTML-valued variables
  ([open questions](../concepts/tables/README.md#open-questions)).
- **What answers it:** the next concept rounds.

### Should the copyright year follow content changes?

- **Why it matters:** R-25 build-time values are expected differences.
- **Known:** the footer prints the build year (`<%= Time.now.year %>`), so
  the year changes on every build. A conversion that only changes the format
  may not warrant a new year.
- **What answers it:** a Docs WG decision, with the Cloud Foundry
  Foundation if it holds a view on copyright notices.

## Site and services

### Does "open source only" cover services?

- **Why it matters:** R-19 open source only, R-18 full-text search.
- **Known:** every tool evaluated so far is open source. Algolia DocSearch
  (a hosted search service, free for open-source projects;
  [glossary](../glossary.md#algolia-docsearch)) and GitHub Pages (GitHub's
  hosting for static sites; [glossary](../glossary.md#github-pages)) are
  services that are not. The RFC names self-hosted search options such as
  [Pagefind](https://pagefind.app/), which builds its index with the site
  ([L170]).
- **What answers it:** a Docs WG decision.

### What does search do today?

- **Why it matters:** R-18 full-text search. The RFC says "Search is broken
  or disabled" ([L21]).
- **Known:** nothing recorded here yet.
- **What answers it:** a check of `docs.cloudfoundry.org` and the book's
  layout files.

### How should versions work?

- **Why it matters:** R-21 versioning.
- **Known:** the RFC starts with one version, `v1.0`, and leaves the model to
  a later Version 2 ([L92], [L94]). In the pre-review the Docs WG lead noted
  that there is one current version of Cloud Foundry and of its docs, with
  history kept in GitHub. The UAA API reference already publishes versioned
  pages.
- **What answers it:** experience with Version 1, as the RFC proposes.

### Should the site publish an `llms.txt` file?

- **Why it matters:** R-20 search-engine and AI-friendly output.
  [`llms.txt`](https://llmstxt.org/) is a plain-text index of a site's pages
  for AI-based tools.
- **Known:** the RFC lists it as optional ([L41]) and as an open question
  ([L173]).
- **What answers it:** a Docs WG decision once the tool is chosen.

### Who controls hosting and the domain today?

- **Why it matters:** R-16 old URLs keep working depends on whoever can
  change DNS at cutover; R-27 a named owner for every task.
- **Known:** the RFC says the current hosting is "managed outside the
  community GitHub organization" ([L24]) and asks who owns the domain
  ([L178]).
- **What answers it:** the Cloud Foundry Foundation and the current hosting
  owner.

## Governance

### Who maintains shared extensions, and how does a working group ask for one?

- **Why it matters:** R-13 no per-WG extensions. An extension is code added
  to the build tool so it handles markup it lacks
  ([glossary](../glossary.md#extension)).
- **Known:** in the tables round, Docusaurus, Zensical and Starlight each
  needed one small extension for column roles and "don't wrap"; Starlight's
  is 76 lines. Antora needed none
  ([results](../concepts/tables/results.md#summary)). The RFC's wording at
  [L100] and [L104] does not allow for this yet.
- **What answers it:** a Docs WG decision on ownership and a request
  process, and the RFC authors' response to the suggested wording.

### Who staffs the central migration team?

- **Why it matters:** R-23 one central conversion, R-27 a named owner for
  every task.
- **Known:** the RFC asks this itself ([L174]).
- **What answers it:** the RFC authors and the Docs WG.

[L21]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L21
[L24]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L24
[L41]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L41
[L92]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L92
[L94]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L94
[L100]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L100
[L104]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L104
[L112]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L112
[L113]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L113
[L167]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L167
[L168]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L168
[L170]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L170
[L173]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L173
[L174]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L174
[L177]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L177
[L178]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L178
