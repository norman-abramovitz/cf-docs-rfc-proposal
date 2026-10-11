# Concept: Partials

Status: draft, incomplete — covers what is known as of 2026-10-11. The
survey, the conversions and the checks are done; the conventions are
proposals for review. Results: [results.md](results.md).

This round asks whether a page that includes a partial renders the
partial's content in the right place, with its headings, lists, notes,
tables and variables intact, in each hands-on tool, and what each tool
needs for the ways the book uses partials
([R-05](../../requirements/README.md#r-05) partials and reuse). It also
gathers data for the open question whether a page still needs to pick its
partial from a variable
([research area](../../requirements/research-areas.md#are-partial-names-in-variables-still-needed)),
and adds a partials check beside the outline and notes checks.

Terms used below:

- **Partial.** A file of content that is not a page of its own and is
  rendered inside the pages that include it. The book names it
  `_name.html.md.erb` and includes it with `<%= partial 'name' %>`, an ERB
  call (ERB is the Ruby template language the book's pages are written
  in). The tools call the same thing a partial, a snippet, or an imported
  component.
- **Include.** A tool's way of putting a partial into a page.
- **Host page.** The page that includes a partial.
- **Content source.** A folder or repository a tool reads pages from; a
  partial "in another content source" lives outside the host page's.
- **Modes.** *passthrough*: the include closest to the ERB call the tool
  allows, the partial beside its page and named as today, its content as
  the earlier rounds' passthrough (HTML kept); *native*: the tool's own
  include and place for partials, the content in the tool's format with
  the earlier rounds' native tables, notes and heading ids; *variable*:
  the partial's name taken from a variable; *raw*: the ERB call as
  written, to show what breaks. Zensical adds *snippet*, its second kind
  of include.

## Progress

- [x] **Survey.** Every partial call and partial file in the 15 `docs-*`
  repositories and the book repository at the notes survey's commits: 45
  calls in content, 7 in the book's layout, 48 partial files, and how
  Bookbinder and Middleman resolve a name, with pinned source lines.
  History back to 2016 for the partial names held in variables.
  Script, data and write-up: [survey/](survey/README.md).
- [x] **Test pages chosen and copied**, verbatim at the survey's commits:
  [source/SOURCES.md](source/SOURCES.md), with the published pages as
  served on 2026-10-11 in [published/](published/).
- [x] **Intent written.** For each page, where each partial's content must
  appear, and a partials file the check reads: [intent/](intent/).
- [x] **Partials check written**: [checks/partials.py](checks/partials.py),
  with [checks/check-site.sh](checks/check-site.sh) and a browser check,
  [checks/partials-browser.mjs](checks/partials-browser.mjs).
- [x] **Converted and built** in all four hands-on tools, passthrough,
  native, variable and raw (Zensical also snippet), plus probes for a
  partial included twice and a missing partial. Every partial passes in
  native in every tool: [results.md](results.md#summary).
- [ ] **Conventions reviewed.** The nine proposals in
  [results.md](results.md#conventions-to-record), and the recommendation on
  [partial names in variables](results.md#are-partial-names-in-variables-still-needed).
  Accepted (2026-10-11): conventions 4, 6 and 8, the recommendation, and
  the book's two partial defects as defects the converted pages fix.

## Test pages

| Page | Repository | Partials | Cases |
|------|------------|----------|-------|
| [`high-availability`](intent/high-availability.md), one section | cloudfoundry/docs-cloudfoundry-concepts | `_oss_scale_table` | the partial whose name the book also holds in a variable (`scale_table`); a table and a variable in the partial; converted in the tables round |
| [`using-vol-services`](intent/using-vol-services.md), the notes round's excerpt | cloudfoundry/docs-dev-guide | `_using-vol-services`, and in native the note partial inside it | a page that is only a partial call; headings with ids inside a partial; a nested partial; notes in the partial |
| [`architecture`](intent/architecture.md), two sections | cloudfoundry/docs-loggregator | `_log_cache` (twice), `_syslog_agents` | a partial after text in a list item; the same partial twice on one page; variables in a partial |
| [`enabling-tcp-routing`](intent/enabling-tcp-routing.md), one section | cloudfoundry/docs-cf-admin | `_tcp_modify_ports`, and in native the note partial `mutual_tls_tcp` | a partial that is a whole list step; a path through the section's folder name; a note held in a variable |
| [`troubleshoot-app-health` and `routes-domains`](intent/troubleshoot-app-health.md), one section each | cloudfoundry/docs-dev-guide | `_routing_conflict` | the one partial included from two pages; in native, kept in another content source |

**How they were chosen.** Decision (this round): from the survey's rows,
few pages that together hold the common case (a call on a line of its own)
and every other pattern the book has: the four calls in list items, the
two partials included more than once, the one page that is only a call,
the largest partial with headings, and a partial whose name a variable
holds. Two pages come from earlier rounds (`high-availability`'s partial
from tables, `using-vol-services` from notes); `routes-domains` is the
headings round's page, in another section. Patterns the book does not have
were tested where they matter for migration: a partial's name from a
variable (variable mode), a nested partial (made by the notes round's
convention for notes held in variables), a partial in another content
source, and a partial with a heading included twice (a probe). No page
has `locals:`, a call inside a conditional or a call in a table cell; the
survey found none.

## Partials check

[checks/partials.py](checks/partials.py) reads a built HTML page and checks
each partial against a partials file. It needs only Python 3.

```bash
# The page's text blocks, with section and place, any include syntax left, and the table of contents
python3 -I checks/partials.py published/architecture.html

# A built page against its partials file
python3 -I checks/partials.py BUILT.html --expect intent/architecture.partials

# All three checks on every page in some modes of one site (run from sites/<tool>, after make build)
../../checks/check-site.sh build note=note,important=warning,caution=danger passthrough native variable
```

What it does:

- **Finds each partial** by its first and last words, in order, each
  search starting from the previous partial's first words, so a partial
  included twice is two lines and a nested one follows its parent.
- **Checks its place**: the host page's words just before and after it
  (only an admonition's title may stand between), the section it sits in,
  and whether its first and last words are in a list item, a table cell or
  the body.
- **Counts** the partial's first words on the page: as often as the file
  says.
- **Fails on include syntax left on the page**: `<%`, `{% partial`,
  `include::`, `--8<--`, an MDX `import`, "Unresolved directive".
- **Fails on an id used more than once** when one of its uses is inside an
  included span.
- **Checks the table of contents** for the ids a `toc` line names, in the
  static HTML: Docusaurus, Zensical, Starlight and the published book's
  quick links. Antora builds its table of contents in the browser;
  [partials-browser.mjs](checks/partials-browser.mjs) reads it there and
  records console errors.

It knows nothing about these pages. `make check` in each site runs it with
the outline check (with each page's anchors) and, on the two pages with
notes, the notes check. Run on the published pages, it fails twice, on the
book's own defects ([published check](results/published-check.txt)).

## Method

1. **Survey** every partial call and partial file, and how the book
   resolves a name.
2. **Choose pages** that hold the patterns, preferring pages already
   converted.
3. **Write the intent**: where each partial's content must appear.
4. **Convert by hand** into each tool, every mode; the content outside the
   includes follows the earlier rounds' conventions.
5. **Build and check** with the partials, outline and notes checks, the
   probes, and a browser.
6. **Record conventions** per tool ([sites/](sites/)`<tool>/CONVENTIONS.md`).

Each tool keeps the version and configuration of the earlier rounds;
Zensical turns on `pymdownx.snippets` for its snippet mode.

## Layout

```
concepts/partials/
├── README.md          this file
├── results.md         results per tool, cases, recommendation, conventions
├── survey/            partial survey: survey.py, summary.py, calls.csv, partials.csv, shas, README
├── source/            new test pages and partials, verbatim, plus SOURCES.md
├── published/         the four new published pages, as served on 2026-10-11
├── intent/            per page: <page>.md, <page>.partials (what the check reads), <page>.anchors; one .notes
├── checks/            partials.py, check-site.sh, partials-browser.mjs
├── sites/             docusaurus/, zensical/, starlight/, antora/: pages per mode, config, Makefile, CONVENTIONS.md
└── results/           check output per tool, build warnings, probes, browser check, published check
```

Each site builds with `make build` and checks with `make check`; `make
check-probe` and `make probe-missing` run the probes. Build output and
installed packages are ignored by git; the results in [results/](results/)
were produced from copies of the sites built outside the repository.

Decision (2026-10-11): the saved published pages stay in the repository so
the checks can be rerun after the live site changes. They, and the rest of
this round's working files, can be removed once the conversion is
complete.
