# Concept: Headings

Status: **In progress.** Draft, incomplete — covers what is known as of
2026-10-10. The conversions and checks are done; the conventions below
are proposals for review. Results: [results.md](results.md).

This round asks whether a page's heading tree and its heading anchors
survive conversion into each hands-on tool, and it adds the automated
check the concept list calls for: an outline check that compares the
headings of a converted page with the published page
([R-01](../../requirements/README.md#r-01) content and outline survive).

Terms used below:

- **Outline.** The page's headings in order, each with its level (`h1` to
  `h6`), its text, and the ids it carries.
- **Anchor.** An id on the page that a link can end in (`page.html#about`).
  Today's sources write one as an empty HTML anchor at the start of a
  heading: `## <a id="about"></a> About metadata`.
- **Generated id.** An id the build makes from a heading's text when the
  source gives none.
- **Modes.** *passthrough*: headings as written, `<a id>` and HTML `<h4>`
  tags included; *native*: each id written with the tool's own heading
  syntax, HTML headings written as the tool's headings; *native-plain*:
  native with no ids written, so the tool makes them all. Native-plain
  shows what a conversion that drops the ids would break.

## Progress

- [x] **Test pages chosen.** Two pages from the tables round and two new
  ones, chosen with a heading scan of the book's repositories; see
  [Test pages](#test-pages).
- [x] **Sources copied.** The new pages, verbatim at the table survey's
  commits, and the published pages as served on 2026-10-10:
  [source/SOURCES.md](source/SOURCES.md), [published/](published/).
- [x] **Intent written.** For each page, the heading tree to keep, the
  anchors to keep (an `.anchors` file the check reads), and the links from
  other pages and repositories that point at them: [intent/](intent/).
- [x] **Outline check written.** [checks/outline.py](checks/outline.py)
  (see [Outline check](#outline-check)).
- [x] **Converted and built** in all four hands-on tools, three modes
  each. Every outline survives; every explicit id survives in passthrough
  and native. Results: [results.md](results.md#summary).
- [ ] **Conventions reviewed.** The seven proposals in
  [results.md](results.md#conventions-to-record).

## Test pages

| Page | Repository | Headings | Cases |
|------|------------|----------|-------|
| [`metadata`](intent/metadata.md) | cloudfoundry/docs-cf-admin (copied in the tables round) | 32, `##`–`####` | deep tree; an explicit id on every heading; five heading texts used twice; title from front matter |
| [`troubleshooting_slow_requests`](intent/troubleshooting_slow_requests.md) | cloudfoundry/docs-cf-admin (copied in the tables round) | 12, `##`–`###` | a variable in a heading; ids that links on the page point to |
| [`access-control`](intent/access-control.md) | cloudfoundry/docs-services | 8, `##`–`####` | skipped levels (`##` then `####`, then `###`); headings with no explicit id |
| [`routes-domains`](intent/routes-domains.md), Domains section | cloudfoundry/docs-dev-guide | 17 of the page's 42, `##`–`#####` | HTML `<h4>` tags next to Markdown `####`; the deepest level in the set; ids linked from other repositories |

Every page takes its title from its front matter, not from a `#` heading.

**How they were chosen.** Decision (this round): the two tables-round pages
that qualified were reused, because their bodies were already converted
in every tool; only their heading lines change between modes. The other
cases came from a scan of the headings in the book's repositories at the
table survey's commits ([survey/shas.txt](../tables/survey/shas.txt)). The
first scan was not kept; it is redone, over all 12 of the book's
repositories, in the [heading survey](survey/README.md). It finds two pages
with skipped levels after the first heading (`access-control` and docs-bbr
`restore`; the first scan found only `access-control`) and two with HTML
heading tags (`routes-domains` has 15; `services/application-binding` has
one). No heading holds code; one page holds links in headings (see
[Not yet written](results.md#not-yet-written)).

## Outline check

[checks/outline.py](checks/outline.py) reads a built HTML page and prints
its outline, or compares two pages. It needs only Python 3.

```bash
# The outline of one page
python3 -I checks/outline.py published/metadata.html

# A built page against the published one, with the anchors it must keep
python3 -I checks/outline.py published/metadata.html BUILT.html --anchors intent/metadata.anchors

# A page built from an excerpt: only the title and one section
python3 -I checks/outline.py published/routes-domains.html BUILT.html --anchors intent/routes-domains.anchors --section domains

# Every page in every mode of one site (run from sites/<tool>, after make build)
../../checks/outline-site.sh build     # Docusaurus; site for Zensical and Antora, dist for Starlight
```

What it does:

- **Finds the content area** (the published page's `main#js-content`, or
  each tool's article), skipping navigation and tables of contents.
- **Reads each heading's text** without the permalink icons and
  screen-reader labels the tools add, and with curly quotes made straight
  (the published book curls them; the tools do not).
- **Compares** levels and text in order. Any difference fails.
- **Checks anchors**: each id in the anchors file must exist on the built
  page. Missing ids fail; ids found but not on a heading are listed.
- **Reports, without failing**, ids used more than once on the built page
  and the published page's heading ids the built page lacks.

It is written to be shared by later concepts: it knows nothing about these
four pages. `make check` in each site runs it on every page and mode. It
does not compare body text; the tables round's
[text-diff.py](../tables/checks/text-diff.py) does that.

## Method

1. **Choose pages** that hold the heading cases, preferring pages already
   converted.
2. **Write the intent**: the published heading tree, the anchors to keep,
   and who links to them (clones of the docs repositories and GitHub code
   search).
3. **Convert by hand** into each tool. Passthrough first; native and
   native-plain differ from it only in the heading lines (compare any two
   modes' files to see).
4. **Build and check** with the outline check, the tools' own link checks,
   and a browser where the table of contents is built by script.
5. **Record conventions** per tool ([sites/](sites/)`<tool>/CONVENTIONS.md`).

Each tool keeps the tables round's version and configuration, without the
table extensions and table stylesheets no page here uses. Antora adds two
attributes for generated ids
([conventions](sites/antora/CONVENTIONS.md#headings)).

## Layout

```
concepts/headings/
├── README.md          this file
├── results.md         results per tool, ids, conventions
├── broken-links.md    links to the test pages that are already broken today
├── source/            new test pages, verbatim, plus SOURCES.md
├── published/         the four published pages, as served on 2026-10-10
├── survey/            the heading survey: scan.py, headings.csv, pages.csv
├── intent/            per page: <page>.md (tree, anchors, inbound links) and <page>.anchors
├── checks/            outline.py (the shared outline check), outline-site.sh
├── sites/             docusaurus/, zensical/, starlight/, antora/: pages per mode, config, Makefile, CONVENTIONS.md
└── results/           check output, outlines, tables of contents, build warnings, browser checks
```

Each site builds with `make build` and checks with `make check`. Build
output and installed packages are ignored by git; the results in
[results/](results/) were produced from copies of the sites built outside
the repository.

Decision (2026-10-10): the saved published pages stay in the repository so
the checks can be rerun after the live site changes. They, and the rest of
this round's working files, can be removed once the conversion is
complete.
