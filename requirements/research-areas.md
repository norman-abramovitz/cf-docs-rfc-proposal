# Research areas

Status: draft Docs WG position, incomplete — covers what is known as of 2026-10-10.

Questions the requirements depend on that nobody has answered yet. For each:
why it matters, what is known, and what would answer it. Requirement IDs
refer to the [requirement list](README.md#requirements).

## Scope

### Which repositories feed the docs, and who owns each?

- **Why it matters:** every area needs an owner before it migrates
  ([R-17](README.md#r-17) an owner for every area), and the URL mapping
  depends on the repository list ([R-15](README.md#r-15) URL identifies the source).
- **Known:** the book's
  [`config.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml)
  (the settings file that tells Bookbinder, today's build tool, which
  repositories to collect) lists 12 sections, each a `docs-*` repository
  mapped to a URL directory, plus sample-code repositories with no pages. A
  survey of tables covered the 15 `docs-*` repositories that are not
  archived (this evaluation's [table survey](../concepts/tables/survey/README.md#scope), 2026-10-09). The book's own [`CODEOWNERS`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/CODEOWNERS) file
  (which names who must review changes) lists one team for everything.
- **What answers it:** the inventory in the RFC's first phase ([L112],
  [L167]).

### Is bosh.io in scope?

- **Why it matters:** the RFC does not mention it, yet it is Cloud Foundry
  documentation with its own tables and notes ([R-07](README.md#r-07) notes
  and admonitions, [R-09](README.md#r-09) table styles by class), and the
  book already [sends all of `/bosh/`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L6) to
  `bosh.io/docs` ([R-16](README.md#r-16) old URLs keep working).
- **Known:** `bosh.io/docs` is built from
  [docs-bosh](https://github.com/cloudfoundry/docs-bosh) with MkDocs and its
  Material theme ([glossary](../glossary.md#mkdocs-material);
  [`mkdocs.yml`](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/mkdocs.yml#L319-L321),
  [build task](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/ci/tasks/build.yml#L5-L12)), and is owned by
  the Foundational Infrastructure working group (FI WG;
  [glossary](../glossary.md#fi-wg); its
  [charter lists docs-bosh](https://github.com/cloudfoundry/community/blob/9f189bfa613bb7a9c2da6616666661790d4410eb/toc/working-groups/foundational-infrastructure.md#L352)).
  Its 40 tables are all plain Markdown pipe tables; it has 302 admonitions
  (boxed callouts headed Note, Warning, and so on); both counted by this
  evaluation at docs-bosh commit `20a4122`
  ([table survey, bosh.io](../concepts/tables/survey/README.md#boshio)). The rest of bosh.io (release and stemcell pages) loads
  the stylesheet and scripts that the docs build produces
  ([`bosh-io-web` `main.go`](https://github.com/cloudfoundry/bosh-io-web/blob/951ec131ce4218a2a259603390d70e259ebeb691/main/main.go#L120-L205),
  [layout](https://github.com/cloudfoundry/bosh-io-web/blob/951ec131ce4218a2a259603390d70e259ebeb691/templates/layout.tmpl#L43)), so changing the docs tool
  affects the whole site.
- **What answers it:** the FI WG, with the RFC authors. Draft position:
  bosh.io follows the Docs WG table and note conventions; a tool or hosting
  change is the FI WG's decision.

### How do the UAA and CredHub API references fit?

- **Why it matters:** [R-29](README.md#r-29) API docs in the same pipeline.
- **Known:** the UAA API reference is built with Slate (a generator for
  one-page API references; [glossary](../glossary.md#slate)) from examples
  that Spring REST Docs writes during the API tests
  ([glossary](../glossary.md#spring-rest-docs);
  [UAA Gradle build](https://github.com/cloudfoundry/uaa/blob/f09cae02367b333bc17d58997c1ba8bf336b3fae/uaa/build.gradle.kts#L150-L193)). CredHub also
  uses Spring REST Docs
  ([CredHub Gradle build](https://github.com/cloudfoundry/credhub/blob/c28c27a454a259f7506498390928713c9fd7f493/backends/credhub/build.gradle#L87-L88)).
  Book pages link to both under `docs.cloudfoundry.org/api/`
  ([book navigation](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/subnavs/_cf-subnav.erb#L425-L431)),
  and to versioned UAA pages
  ([`uaa-concepts`](https://github.com/cloudfoundry/docs-uaa/blob/216c797cfa1a971cf0f9e53eb3e4803aaf914a94/uaa-concepts.html.md.erb#L126-L127)). The RFC asks who can vet the proposal for them
  ([L177]).
- **What answers it:** the UAA and CredHub maintainers: where each reference
  is built and published, and whether it must change format to join the
  pipeline.

### What do downstream consumers reuse?

- **Why it matters:** if anyone copies raw source, the source format and
  partials matter to them ([R-05](README.md#r-05) partials and reuse); if
  they link to the site, URLs do ([R-16](README.md#r-16) old URLs keep working).
- **Known:** the RFC names SAP BTP and anynines as examples and says VMware
  Tanzu "works from its own branches and is not affected" ([L113]), but its
  open questions still name Tanzu ([L168]). In the RFC's pre-review (comments
  on an earlier draft) the Docs WG lead stated that Broadcom's docs are
  written fully in-house (see commits
  [docs-book-cloudfoundry `bdb9de7`](https://github.com/cloudfoundry/docs-book-cloudfoundry/commit/bdb9de7cca8bda0c1ed2e8930090019cc4927269)
  and
  [docs-dev-guide `689faba`](https://github.com/cloudfoundry/docs-dev-guide/commit/689faba303969899f0a18aa56f499c2956c70dc0)).
- **What answers it:** the consumer survey in the RFC's first phase ([L113]).

## Content

### Are partial names in variables still needed?

- **Why it matters:** [R-05](README.md#r-05) partials and reuse. A partial is a file of content
  included in other pages. Here the partial's name comes from a variable (a
  named value defined once and inserted at build time), so the include is
  decided at build time. No tool has been tested with that yet.
- **Known:** the book's `template_variables.yml` maps
  [`scale_table: "oss_scale_table"`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L287)
  and [`roles_table: "_oss_roles_table"`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L231),
  apparently so that another edition of the docs could swap in its own table.
  Every tool in the tables round included the scale-table partial when it was
  named directly
  ([sources](../concepts/tables/source/SOURCES.md)).
- **What answers it:** the downstream survey above, and a search of the
  content repositories for partials included through a variable.

### What should undefined variables show?

- **Why it matters:** [R-04](README.md#r-04) variables everywhere asks that an undefined
  variable be reported, not shown as empty text.
- **Known:** `metadata_ref` (in `metadata`) and `bosh_cli_link` (three times
  in `troubleshooting_slow_requests`) are defined nowhere in the book; the
  published pages show nothing in their place
  ([sources](../concepts/tables/source/SOURCES.md)). Other pages may have
  more.
- **What answers it:** a scan of every page for variables missing from
  `template_variables.yml`, then the page owners say what each should be.

### Which table styles beyond the standard one?

- **Why it matters:** [R-09](README.md#r-09) table styles by class. A style class is a name the
  site's stylesheet gives a look to ([glossary](../glossary.md#style-class)).
- **Known:** a survey of all 238 tables in the docs and tutorial repositories
  found one class in use, `table` (this evaluation's
  [table survey](../concepts/tables/survey/README.md#totals), 2026-10-09). The closest thing to a second style is a
  compact one for comparison grids and long reference tables. The tables
  round added `table-media`, an image grid, as an example of how a style is
  added ([template conventions](../concepts/tables/README.md#template-conventions)).
- **What answers it:** the Docs WG choosing from the survey's
  [table families](../concepts/tables/survey/README.md#families).

### What do the concepts not yet worked require?

- **Why it matters:** these requirements are stated from the tables round
  and from reading the source:
  - [R-01](README.md#r-01) content and outline survive
  - [R-04](README.md#r-04) variables everywhere
  - [R-05](README.md#r-05) partials and reuse
  - [R-06](README.md#r-06) typed code blocks
  - [R-07](README.md#r-07) notes and admonitions
  - [R-08](README.md#r-08) cross-repository links
  - [R-25](README.md#r-25) build-time values are expected differences

  Each concept (one documentation feature, worked through every candidate
  tool) can change them.
- **Known:** tables are done; headings, variables, partials, notes and
  admonitions, code blocks, cross-repository links, and copyright and
  build-time values are proposed
  ([concepts](../concepts/README.md#concepts)). The tables round already
  found problems outside tables: heading anchors written as `<a id>`, terminal
  blocks, the `*` lost in `Accept: */*`, and HTML-valued variables
  ([open questions](../concepts/tables/README.md#open-questions)).
- **What answers it:** the next concept rounds.

### Should the copyright year follow content changes?

- **Why it matters:** [R-25](README.md#r-25) build-time values are expected differences.
- **Known:** the footer prints the build year
  ([`<%= Time.now.year %>`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/_book-footer.erb#L3)), so
  the year changes on every build. A conversion that only changes the format
  may not warrant a new year.
- **What answers it:** a Docs WG decision, with the Cloud Foundry
  Foundation if it holds a view on copyright notices.

## Site and services

### Does "open source only" cover services?

- **Why it matters:** [R-19](README.md#r-19) open source only, [R-18](README.md#r-18) full-text search.
- **Known:** every tool evaluated so far is open source (licenses in
  [Tools](../tooling/tools.md#summary)). Algolia DocSearch (a hosted search
  service, free for public technical documentation per Algolia's
  [own page](https://docsearch.algolia.com/docs/who-can-apply/);
  [glossary](../glossary.md#algolia-docsearch)) and GitHub Pages (GitHub's
  hosting for static sites; [glossary](../glossary.md#github-pages)) are
  services that are not. DocSearch's search client is
  [MIT-licensed](https://github.com/algolia/docsearch/blob/e387920e842c1f2fdb69bbdfff4c2d4d7754ce29/LICENSE),
  but it needs an Algolia application ID and API key
  ([code](https://github.com/algolia/docsearch/blob/e387920e842c1f2fdb69bbdfff4c2d4d7754ce29/packages/docsearch-react/src/DocSearch.tsx#L57-L59)).
  The RFC names self-hosted search options such as
  [Pagefind](https://pagefind.app/), which builds its index from the built
  site ([options](https://github.com/Pagefind/pagefind/blob/b6185b2ec6f43c198299eccde2c4b05ffc0ec1e5/pagefind/src/options.rs#L34-L37))
  ([L170]).
- **What answers it:** a Docs WG decision.

### What does search do today?

- **Why it matters:** [R-18](README.md#r-18) full-text search. The RFC says "Search is broken
  or disabled" ([L21]).
- **Known:** nothing recorded here yet.
- **What answers it:** a check of `docs.cloudfoundry.org` and the book's
  layout files.

### How should versions work?

- **Why it matters:** [R-21](README.md#r-21) versioning.
- **Known:** the RFC starts with one version, `v1.0`, and leaves the model to
  a later Version 2 ([L92], [L94]). In the pre-review the Docs WG lead noted
  that there is one current version of Cloud Foundry and of its docs, with
  history kept in GitHub. The UAA API reference already publishes versioned
  pages ([build](https://github.com/cloudfoundry/uaa/blob/f09cae02367b333bc17d58997c1ba8bf336b3fae/uaa/build.gradle.kts#L189)).
- **What answers it:** experience with Version 1, as the RFC proposes.

### Should the site publish an `llms.txt` file?

- **Why it matters:** [R-20](README.md#r-20) search-engine and AI-friendly output.
  [`llms.txt`](https://llmstxt.org/) is a plain-text index of a site's pages
  for AI-based tools.
- **Known:** the RFC lists it as optional ([L41]) and as an open question
  ([L173]).
- **What answers it:** a Docs WG decision once the tool is chosen.

### Who controls hosting and the domain today?

- **Why it matters:** [R-16](README.md#r-16) old URLs keep working depends on whoever can
  change DNS at cutover; [R-27](README.md#r-27) a named owner for every task.
- **Known:** the RFC says the current hosting is "managed outside the
  community GitHub organization" ([L24]) and asks who owns the domain
  ([L178]).
- **What answers it:** the Cloud Foundry Foundation and the current hosting
  owner.

## Governance

### Who maintains shared extensions, and how does a working group ask for one?

- **Why it matters:** [R-13](README.md#r-13) no per-WG extensions. An extension is code added
  to the build tool so it handles markup it lacks
  ([glossary](../glossary.md#extension)).
- **Known:** in the tables round, Docusaurus, Zensical and Starlight each
  needed one small extension for column roles and "don't wrap"
  ([list-table.mjs](../concepts/tables/sites/starlight/list-table.mjs)). Antora needed none
  ([results](../concepts/tables/results.md#summary)). The RFC's wording at
  [L100] and [L104] does not allow for this yet.
- **What answers it:** a Docs WG decision on ownership and a request
  process, and the RFC authors' response to the suggested wording.

### Who staffs the central migration team?

- **Why it matters:** [R-23](README.md#r-23) one central conversion, [R-27](README.md#r-27) a named owner for
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
