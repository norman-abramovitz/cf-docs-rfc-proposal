# Concept: Notes and admonitions

Status: **Done, with open items** (listed under
[Not yet written](results.md#not-yet-written)). The survey, the conversions
and the checks are done; the map from kinds to types stays open. Results: [results.md](results.md).

This round asks whether the book's notes survive conversion into each
hands-on tool: their kind, their title, their words and what they hold, and
where they sit on the page
([R-07](../../requirements/README.md#r-07) notes and admonitions). It adds a
notes check beside the headings round's outline check.

Terms used below:

- **Note.** A passage set apart from the text around it and headed Note,
  Important or Caution. The book writes it as HTML:
  `<p class="note important">`, then `<span class="note__title"><strong>Important</strong></span>`,
  then the text. The tools call the same thing an **admonition**
  ([glossary](../../glossary.md#admonition)) and give it a syntax of their
  own.
- **Kind.** The class after `note`: `note`, `important` or `caution` (and
  `warning` on two archived pages). **Title:** the word the reader sees.
- **Modes.** *passthrough*: the HTML notes kept, with the changes the tool
  forces; *native*: each note written with the tool's own admonition;
  *raw*: the notes exactly as the source writes them, kept only on the
  pages where that differs from passthrough, to show what breaks.
  Everything outside the notes is the same in all modes and follows the
  earlier rounds' conventions.

## Progress

- [x] **Survey.** Every note in the 15 `docs-*` repositories at the table
  survey's commits: 241 HTML notes in the book, 12 in variables, 302
  Python-Markdown admonitions on bosh.io. Script, data and write-up:
  [survey/](survey/README.md).
- [x] **Test pages chosen and copied**, verbatim at the survey's commits:
  [source/SOURCES.md](source/SOURCES.md), with the published pages as
  served on 2026-10-10 in [published/](published/).
- [x] **Intent written.** For each page, every note's kind, title,
  contents and place, and the cleanup it needs: [intent/](intent/), with a
  notes file per page that the check reads.
- [x] **Notes check written**: [checks/notes.py](checks/notes.py); the
  outline check gained `--until` for an excerpt that ends inside a section.
- [x] **Converted and built** in all four hands-on tools, passthrough and
  native, plus raw. Every note passes in passthrough and native in every
  tool: [results.md](results.md#summary).
- [ ] **Conventions reviewed.** The eight proposals in
  [results.md](results.md#conventions-to-record). Convention 6, a note held
  in a variable becomes a partial, is accepted; convention 3, the map from
  kind to type, waits on a test of extensions and CSS
  ([how each tool maps the kinds](results.md#how-each-tool-maps-the-kinds)).

## Test pages

| Page | Repository | Notes | Cases |
|------|------------|-------|-------|
| [`cf-backup`](intent/cf-backup.md) | cloudfoundry/docs-bbr, whole page | 3 | a `<div>` note holding a list; the Caution kind; two notes never closed |
| [`using-vol-services`](intent/using-vol-services.md) | cloudfoundry/docs-dev-guide, the opening and the NFS section of its partial | 4 | a note held in a variable; notes in a list step and inside an HTML list item; a Markdown code span, `<br>` and `>=` inside an HTML note |
| [`healthchecks`](intent/healthchecks.md) | cloudfoundry/docs-dev-guide, whole page | 4 | the Important kind; a note in a table cell; a variable in a note |
| [`routes-domains`](intent/routes-domains.md), Domains section | cloudfoundry/docs-dev-guide (copied in the headings round) | 5 | the common shapes: `<p>` and `<div>` notes with code and links; two notes in a row |

**How they were chosen.** Decision (this round): from the survey's rows,
few pages that together hold the common shapes and the hard cases: notes
holding lists, code, links and variables; notes in lists, table cells and
variables; Markdown inside HTML; notes never closed.
`routes-domains` was the only page from the earlier rounds with notes, and
was reused. Two patterns are on no test page: a code block inside a note
(2 notes in the book) and the `warning` kind (2 notes, archived); see
[Not yet written](results.md#not-yet-written).

## Notes check

[checks/notes.py](checks/notes.py) reads a built HTML page and lists its
notes, or compares them with a notes file. It needs only Python 3.

```bash
# The notes on a page
python3 -I checks/notes.py published/healthchecks.html

# A notes file from a page (the intent files were made this way)
python3 -I checks/notes.py published/healthchecks.html --emit

# A built page against the notes file, with the site's map from kind to type
python3 -I checks/notes.py BUILT.html --expect intent/healthchecks.notes --map note=note,important=warning,caution=danger

# Both checks on every page and mode of one site (run from sites/<tool>, after make build)
../../checks/check-site.sh build note=note,important=warning,caution=danger
```

What it does:

- **Finds the notes** in the content area: the book's `p.note` and
  `div.note`, Docusaurus's `div.theme-admonition`, Zensical's
  `div.admonition`, Starlight's `aside.starlight-aside`, Antora's
  `div.admonitionblock`.
- **Reads each note's kind** from its class, **its title** from the title
  element (in Antora, from the label its icon carries), **its words**
  without the title, **what it holds** (list items, code, code blocks,
  links), **the section** it sits in (the nearest heading above it) and
  **its place** (in a list item, a table cell, or the body).
- **Compares** them in order with the notes file: the kind through the
  site's map, the title without regard to case, the words, the contents,
  the section and the place. Any difference fails.

It is written to be shared: it knows nothing about these pages. `make
check` in each site runs it and the outline check on every page in
passthrough and native ([checks/check-site.sh](checks/check-site.sh));
`make check-raw` runs them on the raw mode. A browser check,
[checks/notes-browser.mjs](checks/notes-browser.mjs), records console errors
and each note's label and colours; appearance is not compared, but it shows
whether the kinds look different and whether a note has a box at all.

**The outline check** ([../headings/checks/outline.py](../headings/checks/outline.py))
gained one option, `--until ID`, which ends a `--section` before the
heading that carries `ID`, for `using-vol-services`, an excerpt that stops
inside a section. Without it the check behaves as before.

## Method

1. **Survey** the notes of every `docs-*` repository.
2. **Choose pages** that hold the patterns, preferring pages already
   converted.
3. **Write the intent**: each note's kind, title, contents and place, and
   the notes file the check compares against.
4. **Convert by hand** into each tool. Passthrough first, then native,
   which differs from passthrough only in the notes (compare any two modes'
   files to see). Raw keeps the notes exactly as written, where that
   differs.
5. **Build and check** with the notes check, the outline check and a
   browser.
6. **Record conventions** per tool ([sites/](sites/)`<tool>/CONVENTIONS.md`).

Each tool keeps the version and configuration of the earlier rounds.
Starlight adds its own Markdoc preset (`@astrojs/starlight-markdoc` 0.7.0)
for the aside tag, and takes only that tag from it.

## Layout

```
concepts/notes/
├── README.md          this file
├── results.md         results per tool, kinds, conventions
├── survey/            note survey: survey.py, summary.py, notes.csv, shas.txt, README
├── source/            new test pages, verbatim, plus SOURCES.md
├── published/         the three new published pages, as served on 2026-10-10
├── intent/            per page: <page>.md (notes, cases, cleanup) and <page>.notes (what the check compares)
├── checks/            notes.py, check-site.sh, notes-browser.mjs
├── sites/             docusaurus/, zensical/, starlight/, antora/: pages per mode, config, Makefile, CONVENTIONS.md
└── results/           check output per tool and mode, build warnings, browser checks, built HTML excerpts
```

Each site builds with `make build` and checks with `make check` and `make
check-raw`. Build output and installed packages are ignored by git; the
results in [results/](results/) were produced from copies of the sites
built outside the repository.

Decision (2026-10-10): the saved published pages stay in the repository so
the checks can be rerun after the live site changes. They, and the rest of
this round's working files, can be removed once the conversion is
complete.
