# Concept: Variables

Status: **Done, with open items** (listed under
[Not yet written](results.md#not-yet-written)). The survey, the conversions
and the checks are done; the decisions are recorded in the conventions. Results: [results.md](results.md).

This round asks whether the book's variables survive conversion into each
hands-on tool: their value, rendered as text or as markup as the book
renders it, in every place a variable appears; and whether a variable that
is not defined is reported when the site builds
([R-04](../../requirements/README.md#r-04) variables everywhere). It adds a
variables check beside the headings round's outline check and the notes
round's notes check.

Terms used below:

- **Variable.** A name a page writes as an ERB tag, `<%= vars.name %>`,
  whose text comes from the book's `config/template_variables.yml`. ERB is
  the Ruby template language the book's build runs on a page before it
  reads the page's Markdown. **Value**: the text a key holds; it can be
  plain text, a URL, HTML or Markdown. **Use**: one reference in a page.
- **Place.** Where a use sits: text, a code block, inline code, a heading,
  a link's text or target, the page title, a table cell, a note.
- **Not defined**: a name pages use that the file does not hold.
  **Empty**: a key with no value. The book renders both as nothing.
- **Modes.** *passthrough*: each `<%= vars.name %>` written as the tool's
  own variable reference, with the book's values as they are and the forms
  the earlier rounds use; *native*: the tool's own mechanism used fully,
  values prepared for the tool and every name required at build; *raw*: a
  page exactly as the book writes it, where that shows what breaks.
  Everything outside the variables is the same in both modes and follows
  the earlier rounds' conventions.

## Progress

- [x] **Survey.** Every ERB expression in the 15 `docs-*` repositories at
  the notes survey's commits, and every key of the variables file: 1,503
  variable uses of 180 names in the book, 273 keys; 28 names used but not
  defined, 31 empty keys used. Script, data and write-up:
  [survey/](survey/README.md).
- [x] **Test pages chosen and copied**, verbatim at the survey's commits:
  [source/SOURCES.md](source/SOURCES.md), with the published pages as
  served on 2026-10-11 in [published/](published/).
- [x] **Intent written.** For each page, every use, its value and where it
  renders: [intent/](intent/), with a variables file per page that the
  check reads and an anchors file for the outline check.
- [x] **Variables check written**: [checks/vars.py](checks/vars.py), with
  [checks/check-site.sh](checks/check-site.sh) and a browser check,
  [checks/vars-browser.mjs](checks/vars-browser.mjs).
- [x] **Converted and built** in all four hands-on tools, passthrough and
  native, plus raw. Every value is in place in native mode in every tool;
  passthrough keeps all of them in Zensical only:
  [results.md](results.md#summary).
- [x] **Conventions reviewed.** The eight proposals in
  [results.md](results.md#conventions-to-record), and the open questions
  below, answered 2026-10-11; a ninth convention, product names as text,
  follows from question 1.

## Test pages

| Page | Repository | Uses | Cases |
|------|------------|------|-------|
| [`app-ssh-overview`](intent/app-ssh-overview.md) | cloudfoundry/docs-dev-guide, whole page | 5 | an HTML value inside a sentence in a table cell; a Markdown value as a paragraph; a variable in a heading; a name not defined |
| [`routes-domains`](intent/routes-domains.md), Domains section | cloudfoundry/docs-dev-guide (the headings and notes rounds' page) | 50 | variables in fenced code blocks and inline code; in HTML table and header cells; two names not defined |
| [`troubleshooting-router-error-responses`](intent/troubleshooting-router-error-responses.md), four parts | cloudfoundry/docs-cf-admin | 5 | a variable as a link target, in a Markdown link and in an HTML `href`; a variable in the first sentence; a name not defined |
| [`container-security`](intent/container-security.md), four parts | cloudfoundry/docs-cloudfoundry-concepts | 16 | variables in link text; Markdown and HTML values at the end of list items; a variable in a heading |
| [`all_metrics`](intent/all_metrics.md) | cloudfoundry/docs-running-cf, without its partials | 1 | the page title set from a variable by ERB code |

**How they were chosen.** Decision (this round): from the survey's rows,
few pages that together hold every place the book puts a variable and
every kind of value: text, HTML (inline and as a note's whole text,
the latter already tested by the notes round), Markdown, a path; in
prose, code blocks, inline code, headings, link text, link targets, table
cells, lists, notes and the page title; and names that are not defined.
`routes-domains` was the one page from the earlier rounds with many
variables, and was reused. The three link-target uses in the book are on
two pages, and the title set by code on one; those pages were taken for
that reason. The pages converted in part keep every heading, so the
outline check compares whole pages; the other sections' bodies are left
out ([SOURCES](source/SOURCES.md#notes)). What no test page holds is under
[Not yet written](results.md#not-yet-written).

## Variables check

[checks/vars.py](checks/vars.py) reads a built HTML page and checks its
variables. It needs only Python 3.

```bash
# Variable syntax left on a page, and markup or Markdown shown as text
python3 -I checks/vars.py BUILT.html --names source/template_variables.yml

# The same, then every use in the page's variables file
python3 -I checks/vars.py BUILT.html --expect intent/app-ssh-overview.vars --names source/template_variables.yml

# Every check on every page and mode of one site (run from sites/<tool>, after make build)
../../checks/check-site.sh site note=note,important=important,caution=caution
```

What it does:

- **Scans the whole page**, head, navigation and table of contents
  included, text and attributes (`href`, `src`, `alt`, `title`,
  `content`, `id`), for variable syntax in each tool's form: ERB `<%`,
  MDX `{vars.`, `vars.name`, Markdoc `{%` and `$vars.`, Jinja
  `{{ name }}`, AsciiDoc `{name}` for a name in the variables file, and
  URL-encoded ERB.
- **Scans the content area**, outside code, for markup shown as text
  (`<a `, `<code>`, `<p` …, an HTML value escaped) and Markdown shown as
  text (`[text](url)`, backticks, `**`, a Markdown value not rendered).
- **Checks each use** in the page's variables file: the value's text in an
  element of the expected kind (paragraph, list item, table cell, header
  cell, link, inline code, code block, heading) within the section of the
  expected heading; a link's target; the page's `<title>` and first `h1`.
  Text is compared with white space collapsed and typographic quotes made
  straight.

It is written to be shared: it knows nothing about these pages, which the
variables files describe. It passes on the published copies of all five
pages. `make check` in each site runs it, the
[outline check](../headings/checks/outline.py) and, on `routes-domains`,
the [notes check](../notes/checks/notes.py), on every page in passthrough
and native ([checks/check-site.sh](checks/check-site.sh)). The browser
check records console errors (a React hydration error shows only there),
the table of contents after the page's scripts have run, and any variable
syntax left in the page's text.

## Method

1. **Survey** every ERB expression and every key of the variables file.
2. **Choose pages** that hold the places and kinds of value, preferring
   pages already converted.
3. **Write the intent**: each use, its value and where it renders, and the
   variables file the check reads.
4. **Convert by hand** into each tool. Passthrough first, then native,
   which differs from passthrough only in the variables (compare any two
   modes' files to see). Raw keeps a page exactly as written. The
   mechanical part, rewriting heading ids and variable references, was done
   with a scratch script; every page was then edited and reviewed by hand.
5. **Probe** what each tool does with a name that is not defined and with
   an empty value (`make probe`).
6. **Build and check** with the variables, outline and notes checks and a
   browser.
7. **Record conventions** per tool ([sites/](sites/)`<tool>/CONVENTIONS.md`).

Each tool keeps the version and configuration of the earlier rounds.

## Open questions for the Docs WG lead

1. **Keep product names as variables?** 1,060 of the 1,503 uses (71%)
   print "Cloud Foundry", "CF" or "cf"; the variables let other books build
   the same pages with other names. Recommendation: ask whether any other
   book still builds from these repositories; if none does, write the
   names as text during conversion, which removes most uses and every
   heading and title case.
   **Answer (Docs WG lead, 2026-10-11):** as recommended. No open-source
   book other than this one builds from these repositories
   (`pivotal-cf/docs-book-tiledev` is a commercial book), so the names
   are written as text.
2. **Remove the 82 references to undefined or empty names?** They render
   as nothing today; strict builds fail on them. Recommendation: remove
   them in cleanup and list them for the owners, who can add a value
   where text is missing.
   **Answer (Docs WG lead, 2026-10-11):** remove them, with the list. The
   list stays with the Docs WG, which does the conversion.
3. **Zensical's delimiters.** Decision (this round): keep `<%= %>`,
   because Jinja's `{{ }}` and `{# #}` clash with 12 lines of the book's
   content and with `{#id}` heading ids. Recommendation: accept.
   **Answer (Docs WG lead, 2026-10-11):** accepted.
4. **Docusaurus headings with a variable**: export the table of contents
   by hand on each such page (15 pages, 27 headings), or write the value
   in the heading. Recommendation: follow question 1; if the names stay
   variables, export the table of contents.
   **Answer (Docs WG lead, 2026-10-11):** question 1 leaves few such
   headings. For those, test a remark plugin that writes the value into
   the heading before Docusaurus builds the table of contents, rather
   than exporting it by hand. Tested the same day: the plugin works
   ([results](results.md#docusaurus-3102)).
5. **Where values that hold markup live.** Recommendation: one shared
   variables file, from which each site's build writes the tool's form
   (JSX, Markdoc trees, HTML); block values become partials, as the notes
   round decided for notes.
   **Answer (Docs WG lead, 2026-10-11):** decide at implementation; one
   file is fine, or one shared folder of several files, so that one
   editor's mistake reaches fewer values.
6. **Starlight's undefined-name check runs outside the build.**
   Recommendation: accept it as part of `make build` and of the pull
   request checks, since Astro's Markdoc integration will not report it.
   **Answer (Docs WG lead, 2026-10-11):** accepted, with a note. A check
   of variables outside every tool may be worth having as well.

## Layout

```
concepts/variables/
├── README.md          this file
├── results.md         results per tool, places, undefined names, conventions
├── survey/            survey.py, summary.py, uses.csv, values.csv, shas.txt, README
├── source/            new test pages and the variables file, verbatim, plus SOURCES.md
├── published/         the new published pages, and two the survey cites, as served on 2026-10-11
├── intent/            per page: <page>.md, <page>.vars (what the check compares), <page>.anchors
├── checks/            vars.py, check-site.sh, vars-browser.mjs
├── sites/             docusaurus/, zensical/, starlight/, antora/: pages per mode, config, Makefile, CONVENTIONS.md
└── results/           check output per tool, build warnings, probes, raw checks, browser check, a partials test
```

Each site builds with `make build` and checks with `make check`; `make
probe` and `make check-raw` show the undefined-name settings and the raw
mode. Build output and installed packages are ignored by git; the results
in [results/](results/) were produced from copies of the sites built
outside the repository.

Decision (2026-10-11): the saved published pages stay in the repository
so the checks can be rerun after the live site changes. They, and the rest
of this round's working files, can be removed once the conversion is
complete.
