# Concept: Copyright and build-time values

Status: **Done, with open items** (listed under
[Not yet written](results.md#not-yet-written)). The survey, the checks
and the builds are done; the year rule and the holder's name are
decided, the name to be confirmed with the Foundation. Results: [results.md](results.md).

This round asks how each hands-on tool prints the two values the book's
build computes today, the copyright year and the "Page last updated"
date, and how a comparison of converted and published pages can treat
them as expected differences
([R-25](../../requirements/README.md#r-25) build-time values are expected
differences). It also gathers evidence for the open question whether the
copyright year should follow content changes rather than the build date
([research area](../../requirements/research-areas.md#should-the-copyright-year-follow-content-changes)).

Terms used below:

- **Build-time value.** A value on a published page that the build
  computes instead of reading it from the page's source. The book has
  two: the footer's `&copy; <%= Time.now.year %>` and the "Page last
  updated" line, a Git date ([survey](survey/README.md#how-the-book-sets-build-time-values)).
- **Author date and committer date.** Git records two dates per commit:
  when the change was written (author) and when it was committed in its
  current form (committer). They differ after a rebase or cherry-pick.
- **Content date.** The date a page's content last changed. In this
  round: the author date of the newest commit to the page's file that is
  not listed as a non-content commit, or the date the converter wrote into
  the page, whichever is later.
- **Ignore list.** A file of commit ids that do not count as content
  changes, in the format of Git's `blame.ignoreRevsFile`, by convention
  named `.git-blame-ignore-revs`. **Candidate commits** are the 72 commits
  this round proposes for it ([candidates.txt](survey/candidates.txt)).
- **Shallow clone.** A Git clone with only the newest commits, often only
  one; every file then seems to have changed in that commit.
- **Year modes.** *build*: the footer prints the year of the build, as the
  book does; *site*: the year of the newest content date on the site;
  *page*: each page's own content year, beside its date.
- **History variants.** Builds in a small Git repository with known dates
  ([make-history.py](helpers/make-history.py)): *native*, the tool's own
  Git-based date; *helper*, the date written in the page and updated from
  Git by [content-date.py](helpers/content-date.py); *shallow*, a
  one-commit clone; *vcs* (Docusaurus), a custom lookup that skips listed
  commits. The repository's six commits, C1 to C6, run from 2019 to 2026;
  C5 is the conversion.

## Progress

- [x] **Survey.** Every build-time value in the book, the 15 `docs-*`
  repositories and the Bookbinder gem, with pinned lines; every copyright
  notice; and, for all 276 pages, the commit that sets "Page last updated"
  today and the one it would be with the candidates skipped. Bookbinder's
  rule matches all 17 saved published pages. [survey/](survey/README.md)
- [x] **Test pages chosen and copied**, verbatim, with the layouts and
  Bookbinder files that print the values: [source/SOURCES.md](source/SOURCES.md);
  the published pages as served on 2026-10-11 in [published/](published/).
- [x] **Intent written.** Per page, the year and date each mode must show:
  [intent/](intent/), read by the check from
  [intent/expectations.txt](intent/expectations.txt).
- [x] **Check written**: [checks/buildtime.py](checks/buildtime.py) finds
  and checks the values, and compares a converted page with the published
  page with them masked; [checks/check-site.sh](checks/check-site.sh) runs
  it over a build. All four published pages pass
  ([published check](results/published-check.txt)).
- [x] **Converted and built** in all four hands-on tools, three year modes
  each, and the history variants. Every mode passes on every page in every
  tool; every tool's own Git date fails after conversion
  ([results](results.md#summary)).
- [x] **Conventions reviewed**: the ten proposals in
  [results.md](results.md#conventions-to-record). Reviewed 2026-10-11:
  conventions 4 and 5 accepted, convention 3 amended for pages that are
  only an include.
- [x] **The copyright-year question decided** (2026-10-11: B, the
  newest content year on the site): the answers and the
  evidence are in [results.md](results.md#should-the-copyright-year-follow-content-changes).

## Test pages

| Page | Repository | Published date | Content date (candidates skipped) | Cases |
|------|------------|------|------|-------|
| [`access-control`](intent/access-control.md), whole page | cloudfoundry/docs-services | 2026-07-09 | 2026-06-26 | the newest commit is a markup fix; the page compared word by word (headings round's conversion) |
| [`architecture`](intent/architecture.md), excerpt | cloudfoundry/docs-loggregator | 2024-12-05 | 2024-12-05 | an old date set by a content edit; partials do not count |
| [`using-vol-services`](intent/using-vol-services.md), excerpt | cloudfoundry/docs-dev-guide | 2026-07-21 | 2023-05-31 | a page that is only a partial call, dated by a source-only commit |
| [`high-availability`](intent/high-availability.md), excerpt | cloudfoundry/docs-cloudfoundry-concepts | 2026-07-22 | 2026-06-29 | a source-only commit, then a borderline one; the site's newest content date |

**How they were chosen.** Decision (this round): every page carries the
same footer, so pages were chosen for their dates: four kinds of commit
that set "Page last updated" today (a markup fix, a content edit, a
source-only change on a page that is only an include, a source-only
change followed by a borderline one), from pages earlier rounds already
converted. Only `access-control` is converted whole (the headings round's
native pages), so the comparison runs on it; the other three hold the
published title and first paragraph, since the round tests the frame
around the content.

## Build-time values check

[checks/buildtime.py](checks/buildtime.py) reads a built HTML page. It
needs only Python 3.

```bash
# The build-time values on a page
python3 -I checks/buildtime.py published/architecture.html

# A built page against its intent
python3 -I checks/buildtime.py BUILT.html --expect intent/expectations.txt --page architecture --mode page

# A converted page against the published page, build-time values masked (add --no-mask to see them)
python3 -I checks/buildtime.py --compare published/access-control.html BUILT.html

# Every test page of one build (run from sites/<tool>, after make build)
../../checks/check-site.sh build-build build
```

What it does:

- **Finds the copyright notice**: a year or range after `©`, `&copy;`,
  `(c)` or "Copyright", and the holder's name after it.
- **Finds the "last updated" date** in any of the forms the book and the
  tools use: Bookbinder's `data-modified-date` attribute, a `<time
  datetime>` element (Docusaurus, Starlight, Antora here), a date in an
  element whose class names a last-updated or source-file box (Zensical),
  or a date in the text after "last updated"; and date `<meta>` tags.
- **Checks them against the intent**: one notice, with the expected year
  (`build` means the year of the build) and holder; the expected date, or
  none.
- **Compares main texts with the values masked**: the notice, the
  last-updated phrases and boxes, and heading permalinks are taken out of
  both pages and the values are listed apart; the words left are compared
  as the tables round's `text-diff.py` does.

## Content-date helper

[helpers/content-date.py](helpers/content-date.py) computes each page's
content date from the date written in the page and, with `--git`, the
author date of its newest commit not in the ignore list; `--write` writes
it back into the page's field, and `--year` prints the newest year. It
stops on a shallow clone. The sites use it for the site year and in the
history `helper` variant.

## Method

1. **Survey** where the book computes values at build time and how, and
   date every page by the book's rule.
2. **Choose pages** for the kinds of commit that date them today.
3. **Write the intent**: the year and date each mode must show.
4. **Configure each tool** for the three year modes and the date written
   in the page; build a repository with known dates to test each tool's
   own Git-based date, the helper, a shallow clone and, in Docusaurus, a
   lookup that skips commits.
5. **Check** every build with the build-time values check, and compare
   `access-control` with its published page.
6. **Record conventions** per tool ([sites/](sites/)`<tool>/CONVENTIONS.md`).

Each tool keeps the version of the earlier rounds.

## Layout

```
concepts/build-time-values/
├── README.md          this file
├── results.md         results per tool, the copyright-year question, conventions
├── survey/            survey.py, buildtime.csv, pages.csv, candidates.txt, shas.txt, README
├── source/            the four test pages, the book's layouts and Bookbinder's files, verbatim, plus SOURCES.md
├── published/         the four published pages, as served on 2026-10-11
├── intent/            per page: <page>.md; expectations.txt (what the check reads)
├── checks/            buildtime.py, check-site.sh
├── helpers/           content-date.py, make-history.py, pages.py (writes the sites' test pages)
├── sites/             docusaurus/, zensical/, starlight/, antora/: pages, config, footer overrides, Makefile, CONVENTIONS.md
└── results/           check and history output per tool, build warnings, probes, comparison, sitemaps
```

Each site builds with `make build` and checks with `make check`; `make
history` runs the history variants; Zensical has `make probe-git-plugin`
and Antora `make probe-dates`. Build output, the history repositories
(`.history/`) and installed packages are ignored by git. The results in
[results/](results/) were produced from a copy of this folder built
outside the repository; Antora's playbook reads the repository's
worktree, so its copy was a Git repository of its own.

Decision (2026-10-11): the saved published pages stay in the repository so
the checks can be rerun after the live site changes, as in earlier rounds.
