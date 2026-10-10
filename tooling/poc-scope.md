# What the PoC must cover

Status: draft, incomplete — covers what is known as of 2026-10-10.

A PoC (proof of concept) is a small working build that tests whether an
approach works before the full migration starts. RFC #1642 plans one as
its Phase 2, in a new repository. This page quotes what the RFC asks that
PoC to do and adds what the tables round found that bears on it. The
comparisons built in this repository are described in
[poc/](../poc/README.md); the tools in [tools.md](tools.md).

Requirements are cited by ID and a short phrase; the full list is in
[requirements/](../requirements/README.md).

## What RFC #1642 asks

[Phase 2, L119–127](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L119-L127):

> A PoC SHOULD be established in a new repository (e.g.,
> `cloudfoundry/docs-next`) to:
>
> - Stand up Docusaurus (or the chosen alternative) with a representative
>   subset of CF documentation migrated to Markdown.
> - Validate local development experience, search, and versioning.
> - Test GitHub Pages deployment via GitHub Actions.
> - Validate the domain redirect strategy.
> - Gather feedback from at least three active CF documentation
>   contributors.
>
> The results of the PoC SHOULD be presented in a TOC / Docs WG meeting.

Two other lines set what the PoC compares and what it must report.
[L31](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L31):

> Other frameworks such as Hugo or MkDocs MAY be evaluated and proposed as
> alternatives during the PoC phase.

[L104](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L104):

> The PoC MUST validate that the most complex existing pages (HTML tables,
> CSS layouts) can be represented with MDX alone. Any gap found MUST be
> reported as a PoC finding.

## What the findings add, line by line

### A representative subset, migrated to Markdown

**What is known.** The Docs WG lead named five pages whose tables are hard
to express outside HTML; they are the test pages of the tables round
([list](../concepts/tables/README.md#test-pages)). All five were built in
four tools and three probes. Every table renders correctly in every tool
once the source is cleaned up; the tools differ in the cost of getting
there ([results summary](../concepts/tables/results.md#summary)).

**What it adds:**

- **The subset needs the hard pages, not only typical ones.** Three of the
  five first MDX errors are outside the tables (`{…}` in prose, an unclosed
  `<br>`), so a subset of simple pages would not show them
  ([raw passthrough errors](../concepts/tables/results.md#raw-passthrough-errors)).
  [R-02](../requirements/README.md#r-02) rich tables.
- **"Migrated to Markdown" depends on the tool.** Markdoc and MDX are
  Markdown dialects that read HTML differently, and Antora reads AsciiDoc,
  not Markdown. The source format is open in this evaluation
  ([principles](../concepts/README.md#principles)). [R-10](../requirements/README.md#r-10) simple text plus
  HTML where needed.
- **The source needs cleanup first.** Five of the twelve HTML tables on the
  test pages are not well-formed; strict readers fail or change content
  ([defects](../concepts/tables/README.md#markup-that-only-browsers-tolerate)).
  A PoC that starts from cleaned pages should say so. [R-24](../requirements/README.md#r-24) markup cleanup
  before conversion.

### MDX alone (L104)

**What is known.** In Docusaurus the test tables render correctly as
HTML in MDX after cleanup (passthrough), and as a list table through a
remark plugin (extension). With Docusaurus's own Markdown table (native),
the content survives but widths, row headers, top alignment and titles do
not: the `credential-types` table comes out 18/82 where the source asks for
20% ([grid](../concepts/tables/results.md#grid)). These are the gaps L104
asks to be reported. [R-03](../requirements/README.md#r-03) column widths as hints, [R-13](../requirements/README.md#r-13) no per-WG
extensions.

How the same table looks in every tool and mode:
[formats.md](formats.md#what-each-format-carried) and
[poc/tables.md](../poc/tables.md#credential-types).

### Local development, search and versioning

- **Local development.** Every site in this repository builds and serves
  with one command (`make build`, `make serve`), with tool versions pinned.
  The Middleman probe shows today's pages previewed without Bookbinder.
  What a contributor has to install differs: Node.js for Docusaurus,
  Starlight, Antora and Eleventy; Python (through `uv`) for Zensical and
  Sphinx; Ruby for Middleman. [R-12](../requirements/README.md#r-12) one-command local preview.
- **Search.** **Not yet tested** in any tool. RFC
  [L170](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L170)
  asks whether Algolia DocSearch or a self-hosted option such as Pagefind
  is preferred. Algolia DocSearch's search client is open source
  ([MIT](https://github.com/algolia/docsearch/blob/e387920e842c1f2fdb69bbdfff4c2d4d7754ce29/LICENSE)),
  but it queries an index hosted by Algolia and needs an Algolia
  application ID and API key
  ([code](https://github.com/algolia/docsearch/blob/e387920e842c1f2fdb69bbdfff4c2d4d7754ce29/packages/docsearch-react/src/DocSearch.tsx#L57-L59)).
  Pagefind builds its index from the built site
  ([options](https://github.com/Pagefind/pagefind/blob/b6185b2ec6f43c198299eccde2c4b05ffc0ec1e5/pagefind/src/options.rs#L34-L37)).
  The hosted index bears on [R-19](../requirements/README.md#r-19) open source only (an open question:
  [tables README](../concepts/tables/README.md#open-questions)). [R-18](../requirements/README.md#r-18)
  full-text search.
- **Versioning.** **Not yet tested** in any tool. [R-21](../requirements/README.md#r-21) versioning.

### GitHub Pages deployment

**Not yet tested** for any candidate tool. (This repository's own pages are
published to GitHub Pages with Jekyll; that is not a candidate build.)
[R-14](../requirements/README.md#r-14) Docs WG approves and publishes.

### The domain redirect strategy

**Not yet tested.** One finding bears on it: links to a section of a page
(`page.html#section`) depend on heading anchors, and the tools treat
today's `<a id="…">` anchors differently. Docusaurus reports them as broken
and shows a browser error; Antora needs each one rewritten as `[[id]]`;
Starlight generates ids that start with a dash but keeps the `<a id>`
working ([Docusaurus finding 6](../concepts/tables/results.md#findings),
[Antora conventions](../concepts/tables/sites/antora/CONVENTIONS.md#every-mode),
[Starlight finding 8](../concepts/tables/results.md#findings-2)). [R-16](../requirements/README.md#r-16) old
URLs keep working.

### Feedback from contributors

**Not yet done.** The "source readability" judgments in the results are the
evaluators' own, not contributors'
([how to read the grid](../concepts/tables/results.md)). One table written
in every format is in [formats.md](formats.md). [R-11](../requirements/README.md#r-11) readable source.

## What else the PoC needs to cover

Found in the tables round and not in the RFC's list:

| Area | Why | Requirement | Evidence |
|------|-----|-------------|----------|
| A word-by-word comparison with the published page | It found content changes the per-table checks missed (`*/*`, dropped spaces) | [R-01](../requirements/README.md#r-01) content and outline survive | [checks/](../concepts/tables/checks/), [Starlight finding 2](../concepts/tables/results.md#findings-2) |
| HTML-valued and undefined variables | MDX, Markdoc and EJS escape HTML values; two variables the pages use are defined nowhere and show as empty text today | [R-04](../requirements/README.md#r-04) variables everywhere | [progress](../concepts/tables/README.md#progress), [Eleventy probe](../concepts/tables/probes/eleventy/README.md) |
| Partials | Each tool includes files differently; RFC L179 asks whether Docusaurus supports them | [R-05](../requirements/README.md#r-05) partials and reuse | [tools.md](tools.md#docusaurus) |
| Code blocks in HTML (`<pre class="terminal">`) | MDX and Markdoc read their text as Markdown | [R-06](../requirements/README.md#r-06) typed code blocks | [Docusaurus finding 8](../concepts/tables/results.md#findings) |
| Table styles named by a class | Themes disagree on which tables they style | [R-09](../requirements/README.md#r-09) table styles by class | [template conventions](../concepts/tables/README.md#template-conventions) |
| Wide tables | A table wider than the column must scroll in its own box, not widen the page | [R-02](../requirements/README.md#r-02) rich tables | [results summary](../concepts/tables/results.md#summary) |
| Link checking | Two tools do not check links to missing anchors; one does not check links inside HTML | [R-08](../requirements/README.md#r-08) cross-repository links | [Starlight finding 7](../concepts/tables/results.md#findings-2), [Docusaurus finding 4](../concepts/tables/results.md#findings) |
| Page descriptions | Docusaurus publishes raw variable code in the description search engines show | [R-20](../requirements/README.md#r-20) search-engine and AI-friendly output | [Docusaurus finding 7](../concepts/tables/results.md#findings) |
| Build-time values | The copyright year changes on every build; comparisons must expect it | [R-25](../requirements/README.md#r-25) build-time values are expected differences | [concepts README](../concepts/README.md#concepts) |

**Not yet written:** PoC scope for the concepts not yet worked (headings,
notes and admonitions, code blocks, cross-repository links), and for Hugo
and VitePress, which have not been assessed.
