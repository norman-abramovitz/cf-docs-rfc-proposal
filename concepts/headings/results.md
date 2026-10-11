# Headings round — results

Status: draft, incomplete — covers what is known as of 2026-10-10.

What each tool did with the four test pages' headings. A summary across
tools comes first, then one section per tool, then how ids are made, what
happens to skipped levels and repeated headings, and the conventions to
record. How the pages were chosen and what the modes mean:
[README](README.md). Per-page heading trees and anchors: [intent/](intent/).

How to read the results:

- **Outline:** the [outline check](checks/outline.py) compares each built
  page's headings (level and text, in order) with the published page's.
  "Same" means every heading matches.
- **Anchors:** the ids each page must keep, listed in its
  `intent/<page>.anchors` file (69 over the four pages), found anywhere on
  the built page.
- **Modes:** *passthrough* keeps the headings as written (`## <a id="x"></a> Text`,
  HTML `<h4>` tags); *native* writes each id with the tool's own heading
  syntax; *native-plain* writes no ids, so the tool makes them all.

All checks ran on 2026-10-10 against the published pages saved that day
([published/](published/)), with the tool versions the tables round
pinned.

## Summary

Every tool keeps every heading tree: all 48 pages (4 pages, 3 modes, 4
tools) pass the outline check, with the same levels and text as the
published page, skipped levels and repeated headings included. Every tool
keeps every explicit id in passthrough and in native. The tools differ in
what happens around the headings: the table of contents, the ids they make
themselves, and what the build reports.

| | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| **Outline check, all modes** | same, 12 of 12 | same, 12 of 12 | same, 12 of 12 | same, 12 of 12 |
| **Anchors, passthrough and native** | 69 of 69 | 69 of 69 | 69 of 69 | 69 of 69 with the id settings below; 65 of 69 with the defaults |
| **Anchors, native-plain** | 11 of 69 | 11 of 69 | 11 of 69 | 11 of 69 (0 with the defaults) |
| **Native id syntax** | `## Text {#id}` | `## Text {#id}` | `## Text {% #id %}` | `[[id]]` above `== Text` |
| **Headings as written (`<a id>` inside)** | builds; React hydration error in the browser; table of contents nests a link in a link | builds cleanly; anchors work | builds cleanly; anchors work | builds with `+++…+++` around the anchor; anchors work |
| **HTML `<h4>` headings as written** | render; not in the table of contents | render; not in the table of contents | render; not in the table of contents | render in a passthrough block; not sections, not in the table of contents |
| **Generated ids** | `about-metadata`; repeats `-1`, `-2` | `about-metadata`; repeats `_1`, `_2` | `about-metadata`; repeats `-1`, `-2` | `_about_metadata`, repeats `_2`; with `idprefix: ''`, `idseparator: '-'`: `about-metadata`, `-2` |
| **Variable in a heading** | heading shows the value; table of contents shows `vars.app_runtime_abbr`; generated id uses the expression | value everywhere | value everywhere | value everywhere |
| **Skipped levels** | kept, no message | kept, no message | kept, no message | kept, with a warning for each |
| **Table of contents** | `h2`–`h3` | `h2` and below | `h2`–`h3`, plus "Overview" | `h2`–`h3`, built in the browser |
| **Build checks anchors** | yes, but misses `<a id>` anchors | yes, all kinds | no | no warning for the excerpt's `<<routes,Routes>>`, whose target is missing |

- **Explicit ids are what keep links working.** With no explicit ids
  (native-plain), 58 of the 69 anchors disappear in every tool, including
  ones that other repositories link to (`metadata#types`, `#query`,
  `access-control#enable-access`). Of the 11 that survive, one now points
  at a different heading: `#example-script` was "Automate labeling
  resources" and becomes "Example script", a heading whose own id is
  `script`. Nothing warns about that.
- **A converter writes every source id with the tool's own syntax.** That
  is native mode, and it passes every check in every tool. Keeping the
  `<a id>` inside the heading works in three tools but costs the table of
  contents its link to the source's id; in Docusaurus it also breaks the
  page in the browser.
- **The published page's second ids are not kept.** The book gives every
  Markdown heading an id made from its text in addition to the `<a id>`,
  with a leading hyphen when a space follows the anchor (`-about-metadata`).
  Repeated headings get the same id twice. Two kinds of these ids are
  already linked from other repositories and already broken: 72 links in
  28 files to `metadata.html#-view-metadata-for-an-object` (a heading since
  reworded) and two to `routes-domains` headings that are now HTML `<h4>`
  tags, which get no generated id. Details under
  [Links from other pages](#links-from-other-pages).

## Docusaurus 3.10.2

Site: [sites/docusaurus/](sites/docusaurus/) — conventions:
[CONVENTIONS.md](sites/docusaurus/CONVENTIONS.md).

### Summary

- **Every outline survives in every mode**, and every explicit id in
  passthrough and native ([check](results/docusaurus-check.txt),
  [outlines](results/docusaurus-outlines.txt)).
- **Headings as written break the page in the browser.** The table of
  contents copies the heading's content, so `## <a id="about"></a> About metadata`
  becomes a table-of-contents link that holds another link:
  `<a href="#-about-metadata" class="table-of-contents__link toc-highlight"><a></a> About metadata</a>`.
  The browser's parser splits it, and React reports error #418, a
  hydration mismatch, on load; the native page has no error
  ([browser check](results/browser-checks.txt)). The tables round found the
  same error on pages with `<a id>` headings.
- **The build's anchor check misses `<a id>` anchors.** In passthrough it
  reports 14 in-page links as broken (`#total-latency`, `#shared-domains`,
  …) whose targets are on the page as `<a id>`, plus `#routes`, which is
  outside the `routes-domains` excerpt; in native it reports only
  `#routes`
  ([build warnings](results/docusaurus-build-warnings.txt)).
- **A variable in a heading shows its source in the table of contents.**
  "Use app logs to locate delays in vars.app_runtime_abbr" in all three
  modes ([toc](results/docusaurus-toc.txt)); the heading itself shows
  "Cloud Foundry". With no explicit id, the generated id is
  `use-app-logs-to-locate-delays-in-varsapp_runtime_abbr`.

### Grid

| Mode | metadata | troubleshooting | access-control | routes-domains |
|------|----------|-----------------|----------------|----------------|
| passthrough | same; 32/32 | same; 12/12 | same; 8/8 | same; 17/17 |
| native | same; 32/32 | same; 12/12 | same; 8/8 | same; 17/17 |
| native-plain | same; 3/32 | same; 0/12 | same; 5/8 | same; 3/17 |

"same" is the outline check; the fraction is anchors kept.

### Other findings

- **Generated ids keep a leading hyphen** when a space follows the
  `<a id>` (`-about-metadata`), as the published page does; with `:` the
  two differ (`-experiment-1-measure-…` against the published
  `-experiment-1:-measure-…`).
- **Body changes outside headings** on the two new pages, recorded for the
  variables and code blocks concepts: variables in fenced and inline code
  need JSX (`<CodeBlock>`, `<code>{…}</code>`); `*.` in two cells of a row
  is read as emphasis and fails the build until escaped; terminal blocks
  lose their blank lines and indentation unless written as one JavaScript
  string ([conventions](sites/docusaurus/CONVENTIONS.md#body-changes-the-new-pages-needed)).
- **Source readability.** `## About metadata {#about}` is shorter than the
  source's form and puts the id where a reader expects it, at the end.

## Zensical 0.0.69

Site: [sites/zensical/](sites/zensical/) — conventions:
[CONVENTIONS.md](sites/zensical/CONVENTIONS.md).

### Summary

- **The source headings build unchanged.** The two new pages are the
  source files with their ERB as written (the excerpt keeps only the
  Domains section); the two carried pages are the tables round's.
- **Every outline survives in every mode**, and every explicit id in
  passthrough and native ([check](results/zensical-check.txt),
  [outlines](results/zensical-outlines.txt)).
- **The build's anchor check understands every kind of anchor.** It flags
  only the excerpt's `#routes` in passthrough and native, and every link
  whose target id is gone in native-plain (13, one of them `#routes`),
  with file, line and column
  ([build warnings](results/zensical-build-warnings.txt)).
- **Variables in headings work everywhere**: heading text, generated id
  and table of contents, because the ERB is rendered before the Markdown is
  read.

### Grid

| Mode | metadata | troubleshooting | access-control | routes-domains |
|------|----------|-----------------|----------------|----------------|
| passthrough | same; 32/32 | same; 12/12 | same; 8/8 | same; 17/17 |
| native | same; 32/32 | same; 12/12 | same; 8/8 | same; 17/17 |
| native-plain | same; 3/32 | same; 0/12 | same; 5/8 | same; 3/17 |

### Other findings

- **The table of contents lists every level**, `h2` to `h5` on
  `routes-domains`, where the published quick links stop at `h3`
  ([toc](results/zensical-toc.txt)). In passthrough it links to the
  generated ids (`#list-domains-for-an-org`), not the source's
  (`#list-domains`), and it leaves out the HTML `<h4>` headings, so the
  Private domains section lists "Delete a private domain" but not the two
  `<h4>` headings above it.
- **Repeated headings get `_1`**, where the other tools use a hyphen.
- **Code line anchors.** On pages with code blocks the outline check
  reports code line ids (`#__codelineno-0-1` and others) more than once
  per page. This is outside headings and was not looked into.

## Starlight 0.42.6

Site: [sites/starlight/](sites/starlight/) — conventions:
[CONVENTIONS.md](sites/starlight/CONVENTIONS.md).

### Summary

- **Every outline survives in every mode**, and every explicit id in
  passthrough and native ([check](results/starlight-check.txt),
  [outlines](results/starlight-outlines.txt)).
- **Markdoc's id annotation, `{% #id %}`, is the native form.** It puts the
  id on the heading and in the table of contents.
- **The source headings build unchanged** and their anchors work; the
  table of contents links to the generated ids, which keep a leading
  hyphen.
- **No anchor or link check at build time.**

### Grid

| Mode | metadata | troubleshooting | access-control | routes-domains |
|------|----------|-----------------|----------------|----------------|
| passthrough | same; 32/32 | same; 12/12 | same; 8/8 | same; 17/17 |
| native | same; 32/32 | same; 12/12 | same; 8/8 | same; 17/17 |
| native-plain | same; 3/32 | same; 0/12 | same; 5/8 | same; 3/17 |

### Other findings

- **The title's id is `_top`**, and the table of contents adds an
  "Overview" entry for it ([toc](results/starlight-toc.txt)).
- **Body changes outside headings** on the two new pages: a variable in
  inline code renders as the literal tag (`{% $vars.app_domain %}`); in
  `<code>` it renders. Correction (2026-10-11): this said the same of a
  fenced code block, but a fence renders the variable, rebuilt with this
  site's configuration
  ([variables round](../variables/results.md#starlight-0426)). A
  `<pre>` block keeps its lines only with each line break written
  `&#10;`; otherwise Markdoc joins the lines and turns blank lines into
  paragraphs, as the tables round found
  ([conventions](sites/starlight/CONVENTIONS.md#body-changes-the-new-pages-needed)).

## Antora 3.2.1

Site: [sites/antora/](sites/antora/) — conventions:
[CONVENTIONS.md](sites/antora/CONVENTIONS.md).

### Summary

- **Every outline survives in every mode**
  ([check](results/antora-check.txt),
  [outlines](results/antora-outlines.txt)). The pages are AsciiDoc in every
  mode; the two carried pages are the tables round's native AsciiDoc, and
  the two new ones were written by hand.
- **Asciidoctor's default ids lose the published ids of headings without
  an `<a id>`.** It makes `_limitations` and
  `_enabling_access_to_a_subset_of_users`, so 4 of `access-control`'s 8
  anchors were missing in passthrough and native
  ([check with defaults](results/antora-default-ids-check.txt),
  [outlines with defaults](results/antora-default-ids-outlines.txt)).
  Setting `idprefix: ''` and `idseparator: '-'` in the playbook makes the
  same ids as the published page and the other tools; all 69 anchors then
  pass in passthrough and native.
- **Skipped levels warn.** Each `====` under a `==` logs "section title
  out of sequence: expected level 2, got level 3", three per page and mode,
  nine in all; the build finishes and the heading stays an `h4`
  ([build warnings](results/antora-build-warnings.txt)).
- **An HTML heading in a passthrough block is not a section**: it renders,
  but AsciiDoc's structure puts the blocks after it in the section above,
  and the table of contents leaves it out. Native writes it as a section.

### Grid (with `idprefix: ''`, `idseparator: '-'`)

| Mode | metadata | troubleshooting | access-control | routes-domains |
|------|----------|-----------------|----------------|----------------|
| passthrough | same; 32/32 | same; 12/12 | same; 8/8 | same; 17/17 |
| native | same; 32/32 | same; 12/12 | same; 8/8 | same; 17/17 |
| native-plain | same; 3/32 | same; 0/12 | same; 5/8 | same; 3/17 |

### Other findings

- **The table of contents is built in the browser**, `h2` and `h3`; the
  static HTML holds none of it ([browser check](results/browser-checks.txt)).
- **Repeated headings are numbered from 2** (`add-metadata-to-a-resource-2`).

## Anchors and ids

### How each tool makes an id

For a heading with no explicit id. From the outlines in
[results/](results/).

| Heading | Published | Docusaurus | Zensical | Starlight | Antora (settings above) |
|---------|-----------|------------|----------|-----------|--------|
| `### Limitations` | `limitations` | `limitations` | `limitations` | `limitations` | `limitations` (default `_limitations`) |
| `## <a id="about"></a> About metadata` (passthrough) | `-about-metadata` | `-about-metadata` | `about-metadata` | `-about-metadata` | `about-metadata` |
| `## Example: Label resources with a git commit` (native-plain) | `-example:-label-resources-with-a-git-commit` (passthrough form) | `example-label-resources-with-a-git-commit` | same | same | same |
| second "Add metadata to a resource" (native-plain) | `-add-metadata-to-a-resource`, the same id again | `…-1` | `…_1` | `…-1` | `…-2` |
| "Use app logs to locate delays in *variable*" (native-plain) | `-use-app-logs-to-locate-delays-in-cloud-foundry` (passthrough form) | `…-in-varsapp_runtime_abbr` | `…-in-cloud-foundry` | `…-in-cloud-foundry` | `…-in-cloud-foundry` |

On the published page every Markdown heading carries two ids, the one made
from its text and the `<a id>` inside it; an HTML heading carries only the
`<a id>`. The published ids are made from the heading's text including
the space after the `<a id>`, and keep `:` and `.` (the Markdown
processor's own rule; this round did not trace which setting of the book
turns it on).

### Links from other pages

Found in the clones of the docs repositories and by GitHub code search on
2026-10-10 (code search covers default branches only, so counts are lower
bounds). Full lists with pinned links are in each [intent file](intent/).

| Page | Anchors linked from elsewhere | Kept: passthrough, native | Kept: native-plain |
|------|-------------------------------|---------------------------|--------------------|
| metadata | `#types` (docs-dev-guide), `#query` (cloud_controller_ng v3 API docs), `#reqs`, `#requirements-reference` | all, every tool | none |
| troubleshooting_slow_requests | none outside the page; five links on the page | all | none |
| access-control | `#enable-access` (docs-services, at least 16 other files), `#disable-access` | all | none |
| routes-domains (Domains section) | `#domains`, `#private-domains`, `#shared-domains`, `#domains-dns` | all | the first three (their text gives the same id); `#domains-dns` breaks |

**Already broken today**, before any conversion: 81 links in 35 files
and 8 repositories, to 7 ids that are not on the pages. They are
`metadata#-view-metadata-for-an-object` (72 links in 28 files, in the
Terraform provider's and a Crossplane provider's docs, all from four
hand-written source lines), `access-control#make-plans-public` (two
repositories), and seven links to five `routes-domains` ids. Two of the
`routes-domains` links are on the page itself, written in its source:
`#create-route-w-port` (the id is `create-route-with-port`) and
`#http-vs-tcp-shared-domains` (the id became `http-vs-tcp-domains` in
2023). Some point at ids generated from older heading text, which
disappeared when the heading changed or became an HTML `<h4>`; others at
explicit ids that were renamed. A migration cannot repair these by keeping
ids, but fixing the link, a redirect or an added anchor could
([R-16](../../requirements/README.md#r-16) old URLs keep working). The
full list, with each source line pinned, the cause and the id each link
was most likely meant for: [broken-links.md](broken-links.md).

## Skipped levels and repeated headings

- **Skipped levels** (`access-control`: `##` then `####`, then `###`) are
  kept as written by every tool: the `h4` stays an `h4`, and the outline
  check passes. Antora alone reports them, with one warning per heading.
  In the tables of contents: Docusaurus, Starlight and Antora list `h2`
  and `h3`, so the `h4` headings are left out and "Limitations" appears
  under "Deactivating access"; Zensical lists every level.
- **Repeated headings** (`metadata`: five texts, twice each) are kept
  apart by their explicit ids in passthrough and native. With no ids, every
  tool numbers the second one, each its own way (`-1`, `_1`, `-2`); the
  published page gives both the same generated id, which is not valid HTML
  and makes the second one unreachable by that id.

## Conventions to record

For `cf-docs-migrate convert`. Decisions of this round, for review:

1. **Write every id the source writes, in the tool's own heading syntax**
   (native mode): `{#id}` (Docusaurus, Zensical), `{% #id %}` (Starlight),
   `[[id]]` (Antora). Do not keep the `<a id>` inside the heading.
2. **Write HTML headings as the tool's headings.** `<h4><a id="x"></a>Text</h4>`
   becomes `#### Text {#x}` (or the tool's form): it then joins the table of
   contents and, in Antora, the section structure.
3. **Keep the published generated id of a heading that has no `<a id>`,**
   by matching the tool's id rule to it (Antora: `idprefix: ''`,
   `idseparator: '-'`) or by writing the id explicitly. Do not keep the
   published second ids of headings that have an `<a id>`. **Accepted**
   (Docs WG lead, 2026-10-10), with the links already broken today listed
   for fixing ([Links from other pages](#links-from-other-pages)).
4. **Keep skipped levels.** Renumbering is the owner's decision, recorded
   as a deviation, not a converter rule.
5. **Give a heading that holds a variable an explicit id** (needed in
   Docusaurus, harmless elsewhere).
6. **The page title stays in the front matter** (Docusaurus, Zensical,
   Starlight) or the document title (Antora); no tool needed an `# H1`.
7. **The outline check runs on every converted page**:
   [checks/outline.py](checks/outline.py), with the page's anchors file.

## Requirements

- [R-01](../../requirements/README.md#r-01) content and outline survive:
  the outline check is the automated part of this requirement for
  headings; all four tools pass it in every mode. Text was compared only
  for `access-control`
  ([text diff](results/text-diff-access-control.txt): the differences are
  the site's quick links, "Page last updated", the GitHub link, and curly
  quotes).
- [R-16](../../requirements/README.md#r-16) old URLs keep working: explicit
  ids keep heading anchors in every tool; leaving ids to the tool breaks
  58 of 69 and silently moves one.
- [R-08](../../requirements/README.md#r-08) cross-repository links: the
  linked anchors listed above come from other CF repositories as well as
  from outside the project.
- [R-11](../../requirements/README.md#r-11) readable source: the native
  forms are shorter than `<a id>` and need no HTML.
- [R-25](../../requirements/README.md#r-25) build-time values are expected
  differences: no heading holds one; "Page last updated" shows up in the
  text comparison as expected.
- [R-04](../../requirements/README.md#r-04) variables everywhere and
  [R-06](../../requirements/README.md#r-06) typed code blocks: variables
  inside code blocks needed tool-specific markup in Docusaurus and
  Starlight (findings above), and the Starlight workaround drops the code
  block's type.

## Not yet written

- **Headings with code or links.** No test page has one. The
  [heading survey](survey/README.md) (12 book repositories, 241 pages with
  headings, 2,164 headings) found no heading with code and one page with
  links in headings: `docs-buildpacks` `python/index.html.md.erb`, where
  the version number in two headings is a link
  ([L190](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/python/index.html.md.erb#L190),
  [L194](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/python/index.html.md.erb#L194)).
- **What the survey found that no test page covers.** Headings with no
  space after the `#`s (97), the same explicit id on two headings of one
  page (40 headings), an `h1` in a page body, and code fences that only the
  book's Markdown engine closes
  ([survey findings](survey/README.md#findings)).
- **Where the published generated ids come from.** The book's Markdown
  settings do not set heading ids in Bookbinder's `config.rb`; which layer
  turns them on was not traced.
- **The table-of-contents text for a heading with a variable in
  Docusaurus.** No fix was tried.
- **Text comparison for every page.** Only `access-control` was compared
  word by word, and not for Starlight (the comparison script reads the
  page's `<article>`, which Starlight pages lack).
- **Probes and on-paper tools.** Eleventy, Sphinx/MyST, Middleman, Hugo
  and VitePress were not part of this round.
- **Screenshots.** None were taken; nothing in this round depends on
  appearance.
