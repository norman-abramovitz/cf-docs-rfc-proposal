# Build-time values round — results

Status: draft, incomplete — covers what is known as of 2026-10-11.

What each tool did with the copyright year and the "last updated" date. A
summary across tools comes first, then one section per tool, then what
the tools share, the open question about the copyright year, and the
conventions to record. How the pages were chosen and what the terms mean:
[README](README.md). How the book sets these values today:
[survey](survey/README.md).

How to read the results:

- **Build-time value**: a value on a page that the build computes instead
  of reading it from the page's source: the copyright year and the "last
  updated" date.
- **Content date**: the date a page's content last changed. In this round
  it is the author date of the newest commit to the page's file that is
  not listed as a non-content commit, or the date the converter wrote into
  the page, whichever is later ([content-date.py](helpers/content-date.py)).
- **Candidate commits**: 72 commits from 2026 whose subject says they
  change markup only, or remove content the open-source book did not
  render ([candidates.txt](survey/candidates.txt)). The converted test
  pages' dates skip them.
- **Year modes**: *build*, the footer prints the year of the build (as the
  book does today); *site*, the year of the newest content date on the
  site; *page*, each page's own content year.
- **History variants**: a small Git repository with known dates
  ([make-history.py](helpers/make-history.py)): six commits from 2019 to
  2026, one of them the conversion. *native* is the tool's own Git-based
  date; *helper* is the date the converter wrote, updated from Git by the
  helper; *shallow* is a one-commit clone of native; *vcs* (Docusaurus) is
  a custom lookup that skips listed commits. The commits are C1 to C6
  ([docstring](helpers/make-history.py)): C2 has an author date of
  2024-12-05 and a committer date of 2025-01-10; C4 is a source-only
  change and C5 the conversion (2026-10-01), both on the ignore list; C6
  edits `access-control` after conversion (author 2026-10-05, committer
  2026-10-07).
- **Check**: [buildtime.py](checks/buildtime.py) finds the copyright notice
  and the date on a built page and compares them with
  [expectations.txt](intent/expectations.txt): "4 of 4" means every test
  page has the expected year, holder and date.

All builds ran on 2026-10-11 with the earlier rounds' tool versions
(Docusaurus 3.10.2, Zensical 0.0.69, Starlight 0.42.6, Antora 3.2.1).

## Summary

Every tool prints a copyright notice with any of the three years, and
every tool shows a "last updated" date written in the page. They differ in
how much code the footer needs and in whether the tool reads dates from
Git; where it does, the date is the conversion commit's.

| | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| **Check, build / site / page** | 4 of 4 each | 4 of 4 each | 4 of 4 each | 4 of 4 each |
| **Footer year from the build** | config (JavaScript) | not in the tool: `make` writes the year into a copy of the config | footer component override (Astro) | the default UI's `year` helper, in a replaced footer template |
| **Footer year from the site's content** | `SITE_YEAR` read by the config | the same config copy | `SITE_YEAR` in the override | `{{env.SITE_YEAR}}` in the template |
| **Year per page** | a wrapped theme component (React) | the copyright template reads `revision_date` | the same override reads the page's date | the template, plus a one-line helper |
| **Date written in the page** | `last_update.date` | `revision_date` | `lastUpdated` | `:page-last-updated:` and the template |
| **Date from Git, by the tool** | committer date; production builds only | none (the MkDocs plugin is dropped without a message) | committer date | none |
| **History, native** | 0 of 4: conversion or newest commit | 0 of 4: no date | 0 of 4: conversion or newest commit | 0 of 4: no date |
| **History, helper** | 4 of 4 | 4 of 4 | 4 of 4 | 4 of 4 |
| **Shallow clone** | every page dated by the newest commit | — | every page dated by the newest commit | — |
| **Skip listed commits** | with a custom VCS (experimental API): 1 of 4, no rename following | — | no | — |
| **Sitemap `lastmod`** | none by default | none | not tested ([build warnings](results/starlight-build-warnings.txt)) | the build time, on every page |

- **Every Git-based date after conversion is the conversion's.** The tools
  read the newest commit that touched the converted file. The conversion
  commit is the newest for every page it wrote, so three of the four test
  pages show 2026-10-01 in Docusaurus and Starlight, against 2019–2025 in
  the intent ([Docusaurus history](results/docusaurus-history.txt),
  [Starlight history](results/starlight-history.txt)).
- **A date written in the page survives conversion and shallow clones**,
  and travels with the file if it moves. In all four tools the page's own field wins over Git; with the
  helper updating it from Git (skipping a list of commits), every tool
  passes 4 of 4 in the history repository.
- **Today's "Page last updated" mostly records markup commits.** 154 of
  the book's 276 pages are dated July 2026, most by bulk commits that fix
  note markup or remove conditionals the open-source book never rendered
  ([survey](survey/README.md#the-dates-of-todays-pages)).
- **In 2026 every year rule gives 2026 for the site.** The newest content
  date is 2026-10-06 with or without the candidates. Per page, the content
  year ranges from 2023 to 2026.
- **Comparisons can mask build-time values.** `buildtime.py --compare`
  takes the notice and the dates out of both pages and lists them apart;
  what remains on `access-control` is the published page's quick links,
  its GitHub link and curly quotes, as in the headings round
  ([comparison](results/compare-access-control.txt)).

## Docusaurus 3.10.2

Site: [sites/docusaurus/](sites/docusaurus/) — conventions:
[CONVENTIONS.md](sites/docusaurus/CONVENTIONS.md).

### Summary

- **The footer year is one line of config**, as in Docusaurus's own site
  template ([template L149](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/create-docusaurus/templates/classic/docusaurus.config.js#L149)).
  A year per page needs a wrapped theme component: the site footer cannot
  read the page's data.
- **`last_update.date` in front matter wins over Git**, and Git is then
  not asked ([`lastUpdateUtils.ts` L64-L96](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-utils/src/lastUpdateUtils.ts#L64-L96)).
- **Git's date is the committer date** (`%ct`) of the newest commit to the
  file, without rename following
  ([`gitUtils.ts` L148-L160](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-utils/src/vcs/gitUtils.ts#L148-L160)):
  `access-control` shows C6's committer date, 2026-10-07, where Bookbinder
  would show its author date, 2026-10-05.
- **The development server shows a made-up date**: Git is read in
  production builds only
  ([`vcsDefaultV1.ts` L13-L16](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-utils/src/vcs/vcsDefaultV1.ts#L13-L16)).
- **A custom VCS can skip listed commits** (`future.experimental_vcs`,
  [`configValidation.ts` L355-L360](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus/src/server/configValidation.ts#L355-L360)).
  With the conversion commit listed, the three pages whose earlier
  history is under their old name get no date at all.

### Grid

| Mode | access-control | architecture | using-vol-services | high-availability |
|------|------|------|------|------|
| build, site, page | ok | ok | ok | ok |
| history, native | 2026-10-07 (C6, committer date) | 2026-10-01 (C5) | 2026-10-01 (C5) | 2026-10-01 (C5) |
| history, helper | ok | ok | ok | ok |
| history, shallow | 2026-10-07 | 2026-10-07 | 2026-10-07 | 2026-10-07 |
| history, vcs | ok | no date | no date | no date |

"ok" is the check: the year, the holder and the date as the intent says
([check](results/docusaurus-check.txt), [history](results/docusaurus-history.txt)).

## Zensical 0.0.69

Site: [sites/zensical/](sites/zensical/) — conventions:
[CONVENTIONS.md](sites/zensical/CONVENTIONS.md).

### Summary

- **The copyright line is a fixed string**, and neither the templates nor
  the configuration can compute a year
  ([`config.py` L332, L533](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/config.py#L332)).
  The build writes the year into a copy of the configuration
  (`[project.extra]`), and an overridden template prints it. Per page, the
  template reads `revision_date`: no code.
- **`revision_date` in front matter is shown as "Last update"**, as written
  ([`source-file.html` L86-L89](https://github.com/zensical/ui/blob/5d58e34f4240394d78ab89d149fdb3437151bac1/dist/partials/source-file.html#L86-L89)).
- **No date from Git.** The MkDocs plugin for it is not supported, and is
  dropped without a message
  ([`config.py` L1929-L1930](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/config.py#L1929-L1930);
  [probe](results/zensical-probe.txt)).
- **Data files for the theme render every page as a template**: the
  markdownextradata extension failed the build on the heading id
  `{#prerequisites}` ("Missing end of comment tag").

### Grid

| Mode | access-control | architecture | using-vol-services | high-availability |
|------|------|------|------|------|
| build, site, page | ok | ok | ok | ok |
| history, native | no date | no date | no date | no date |
| history, helper | ok | ok | ok | ok |

([check](results/zensical-check.txt), [history](results/zensical-history.txt))

## Starlight 0.42.6

Site: [sites/starlight/](sites/starlight/) — conventions:
[CONVENTIONS.md](sites/starlight/CONVENTIONS.md).

### Summary

- **The footer has no notice**; an override of the `Footer` component adds
  one, with any of the three years
  ([`user-config.ts` L271](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/utils/user-config.ts#L271)).
- **`lastUpdated` in front matter wins over Git**, and shows even with the
  option off
  ([`routing/data.ts` L79-L86](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/utils/routing/data.ts#L79-L86)).
- **Git's date is the committer date**, from one log of the whole content
  folder; nothing skips a commit
  ([`git.ts` L58-L68](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/utils/git.ts#L58-L68)).
  Native and shallow give the same dates as Docusaurus.
- **Dates are shown in UTC**
  ([`LastUpdated.astro` L9-L10](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/components/LastUpdated.astro#L9-L10)).

### Grid

| Mode | access-control | architecture | using-vol-services | high-availability |
|------|------|------|------|------|
| build, site, page | ok | ok | ok | ok |
| history, native | 2026-10-07 (C6, committer date) | 2026-10-01 (C5) | 2026-10-01 (C5) | 2026-10-01 (C5) |
| history, helper | ok | ok | ok | ok |
| history, shallow | 2026-10-07 | 2026-10-07 | 2026-10-07 | 2026-10-07 |

([check](results/starlight-check.txt), [history](results/starlight-history.txt))

## Antora 3.2.1

Site: [sites/antora/](sites/antora/) — conventions:
[CONVENTIONS.md](sites/antora/CONVENTIONS.md).

### Summary

- **The default UI has a build-year helper but no notice**
  ([`year.js` L3](https://gitlab.com/antora/antora-ui-default/-/blob/0e38223adfd81eb74d4b1779e158f8ad05ff8923/src/helpers/year.js#L3)).
  A replaced footer template prints the notice; it reads the environment
  (`{{env.YEAR_MODE}}`) and the page's attributes
  ([`build-ui-model.js` L13, L70](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/packages/page-composer/lib/build-ui-model.js#L13)).
  A year per page takes a one-line UI helper.
- **No date from Git**; a page attribute carries the date, and the
  template prints it.
- **Asciidoctor's `docdate` is the build date, or `SOURCE_DATE_EPOCH`'s**
  ([`document.rb` L1256-L1270](https://github.com/asciidoctor/asciidoctor/blob/2c03d22eb9fe83d04ee452939581d1b842f6d8b4/lib/asciidoctor/document.rb#L1256-L1270);
  [probe](results/antora-probe.txt)).
- **The sitemap gives every page the build time as `lastmod`**
  ([`map-site.js` L50](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/packages/site-mapper/lib/map-site.js#L50));
  `SOURCE_DATE_EPOCH` does not change it.

### Grid

| Mode | access-control | architecture | using-vol-services | high-availability |
|------|------|------|------|------|
| build, site, page | ok | ok | ok | ok |
| history, native | no date | no date | no date | no date |
| history, helper | ok | ok | ok | ok |

([check](results/antora-check.txt), [history](results/antora-history.txt))

## Across tools

### Conversion resets every Git date

The RFC moves all content into one repository
([L69]) and converts it centrally ([L131]). A Git-based date then needs
the history before the conversion, and it needs Git to connect each
converted file to its old one:

- **Docusaurus and Starlight look at the converted file only.** Neither
  follows renames for the "last updated" date, so the conversion commit
  is each page's newest commit (native grids above).
- **Git connects a converted file only when it is similar enough.**
  `git log --follow` connected `access-control`, converted whole, to its
  old file; it did not connect the three excerpts
  ([follow probe](results/follow-probe.txt)). How many real pages would
  pass Git's 50% similarity after conversion was not measured.
- **A move to a new repository loses the history** unless it is imported;
  a shallow clone loses it too. `actions/checkout`, which a GitHub Pages
  workflow ([L53]) usually runs, fetches one commit by default
  ([action.yml L74-L76](https://github.com/actions/checkout/blob/11bd71901bbe5b1630ceea73d27597364c9af683/action.yml#L74-L76)).
  In the shallow builds every page showed the newest commit's date.

So the dates that exist today can reach the converted pages in two ways:
the converter writes each page's date into the page (all four tools
show it), or the converted files keep a Git history that the build
follows. Only the first was made to work here in every tool.

### Author date and committer date

Bookbinder uses the author date
([`git_accessor.rb` L81](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/lib/bookbinder/ingest/git_accessor.rb#L81));
Docusaurus and Starlight use the committer date. They differ when a
commit is rebased or cherry-picked: C6's author date is 2026-10-05 and
its committer date 2026-10-07. Decision (this round): the helper uses the
author date, as Bookbinder does.

### Time zones

- The published date is drawn by a script in the reader's local time, so
  one page can show different days in different places
  ([survey](survey/README.md#how-the-book-sets-build-time-values), item 5).
  Docusaurus and Starlight print the date in UTC when the page is built.
- The build year is the build machine's local year in every tool tested
  (`new Date()`, `date +%Y`, the UI's `year` helper). Builds in the hours
  around New Year depend on the machine's time zone.

### Comparing converted and published pages

[R-25](../../requirements/README.md#r-25) asks that build-time values
count as expected differences. `buildtime.py --compare` lists the
copyright year and the date of both pages, then compares the main text
without them ([comparison](results/compare-access-control.txt)):

- **Masked**, `access-control` matches at 0.976–0.982 in the four tools
  (Python's `difflib` ratio over the words: 1.0 is identical).
  The differences left are not build-time values: the published quick
  links, its "Create a pull request" line and curly apostrophes; and, in
  Starlight, the title, which is outside `<main>`.
- **Unmasked**, the published "Page last updated:" (with no date in the
  static HTML) and each tool's "Last updated" line show up as
  differences.
- In page mode the per-page notice sits inside the article in Docusaurus;
  masking leaves its link text, "Cloud Foundry Documentation".

## Should the copyright year follow content changes?

The open question ([research area](../../requirements/research-areas.md#should-the-copyright-year-follow-content-changes)).
This section lays out observations for each answer. **It is not legal
advice**; the Docs WG may want the Cloud Foundry Foundation's view, as
the research area says.

### What the book does today

The footer prints the build's year, "© 2026 Cloud Foundry Foundation"
([`_book-footer.erb` L3](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/_book-footer.erb#L3)).
The repositories' NOTICE files say "YYYY-Present", with first years from
2013 to 2019 ([survey](survey/README.md#copyright-notices-in-the-repositories)).
Under the RFC, every merge rebuilds and redeploys the site
([L83]), so a build-year footer changes year with the first merge of each
year.

### The answers, with what was observed

| Answer | What the footer says | Observed elsewhere | What this round found |
|---|---|---|---|
| **A. The build's year** (today) | the year of the newest deploy | kubernetes.io: `&copy; {{ now.Year }}`, Hugo's current time ([`center.html` L1-L2](https://github.com/kubernetes/website/blob/cd14acc100ef8b0b0a54a31b8d19cc1baf7b5c77/layouts/partials/footer/center.html#L1-L2)); Docusaurus's site template ([L149](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/create-docusaurus/templates/classic/docusaurus.config.js#L149)); cloudfoundry.org's footer shows "©2026" (fetched 2026-10-11) | works in all four tools; a format-only rebuild in a new year changes the year; builds differ by date alone, so a comparison must mask it |
| **B. The newest content year on the site** | the year of the newest content date | Sphinx replaces `%Y` with the current year, or with `SOURCE_DATE_EPOCH`'s year when that is set, citing the Reproducible Builds specification ([`config.py` L694-L723](https://github.com/sphinx-doc/sphinx/blob/b04a2101295ac3fb725b16111eda0284b6da4cca/sphinx/config.py#L694-L723)) | works in all four tools with the helper; it needs a decision about which commits are content (the candidate list) and a full history or dates in the pages; in 2026 it equals A |
| **C. Each page's content year** | a year per page, with its date | not seen on the sites checked | works in all four tools; costs code in Docusaurus (a theme component) and Starlight (an override), a template in Zensical and Antora; years range 2023–2026 on the test pages |
| **D. The first year, or a range to "Present"** | for example "© 2015–Present" or "© 2001" | docs.python.org: "© Copyright 2001 Python Software Foundation", and a separate build time, "Last updated on Oct 11, 2026" (fetched 2026-10-11; [`conf.py` L74](https://github.com/python/cpython/blob/22762c0dd52bf7038cfc8a2b6ea7e8d58825160c/Doc/conf.py#L74)); the repositories' NOTICE files | a fixed string: no build-time value at all, nothing to mask |
| **E. No year** | for example "Copyright The Cloud Foundry Authors" | CNCF recommends notices without years for contributions to its projects, to avoid "years or ranges of years" ([`copyright-notices.md` L19-L38](https://github.com/cncf/foundation/blob/62fe81dea73b1267a5ad8dfa69f2632c8bafc9ea/copyright-notices.md#L19-L38)) | a fixed string |

Public statements that bear on the question:

- **US law names "the year of first publication"** as a notice's year; for
  "compilations or derivative works incorporating previously published
  material", the year of first publication of the compilation or
  derivative work "is sufficient"
  ([17 U.S.C. § 401(b)(2)](https://www.copyright.gov/title17/92chap4.html#401)).
- **A notice is optional** for works published on or after March 1, 1989,
  and "copyright owners can use any form of notice they wish"
  ([Circular 3](https://www.copyright.gov/circs/circ03.pdf), p. 2, revised
  03/2021).
- **The ASF asks its NOTICE files to name "the year(s) of distribution of
  the current and past versions"**
  ([source header policy](https://www.apache.org/legal/src-headers.html),
  fetched 2026-10-11).
- **CNCF notes that copyright notices "are rarely kept up to date as a
  file evolves"** and are not needed to keep ownership
  ([`copyright-notices.md` L78-L82](https://github.com/cncf/foundation/blob/62fe81dea73b1267a5ad8dfa69f2632c8bafc9ea/copyright-notices.md#L78-L82)).
- **The holder's name differs by place**: "CloudFoundry.org Foundation,
  Inc." (NOTICE files), "Cloud Foundry Foundation" (the book's footer),
  "The Linux Foundation" (cloudfoundry.org's footer)
  ([survey](survey/README.md#copyright-notices-in-the-repositories)).

Observations from this round's data:

- The conversion itself would be the newest commit to every page. Under
  A, B and C it moves the year only if it is counted; the helper and the
  candidate list are how B and C leave it out.
- Today's dates already count markup commits: 133 pages' dates move when
  the candidates are skipped ([survey](survey/README.md#the-dates-of-todays-pages)).
- A and D need no history; B and C need either the full history at every
  build or dates kept in the pages.

## Conventions to record

For `cf-docs-migrate convert` and the site build. Decisions of this round,
for review:

1. **Comparisons of converted and published pages mask build-time
   values**: the copyright notice, "last updated" dates (as text, as
   `<time datetime>`, as Bookbinder's `data-modified-date`), and date
   `<meta>` tags, listed apart as expected differences:
   [checks/buildtime.py](checks/buildtime.py) `--compare`
   ([R-25](../../requirements/README.md#r-25)).
2. **Every converted page carries its content date in the page**, in the
   tool's own field: `last_update.date` (Docusaurus), `revision_date`
   (Zensical), `lastUpdated` (Starlight), `:page-last-updated:` (Antora).
   The converter writes it once, from the page's history before
   conversion.
3. **The date written by the converter is Bookbinder's rule**, the author
   date of the newest commit to the page's file, except commits the Docs
   WG lists as not content (convention 4). Partials do not move a page's
   date, as today.
4. **Commits that are not content are listed in `.git-blame-ignore-revs`**
   in the docs repository: the conversion commits, and bulk markup
   commits after review of [candidates.txt](survey/candidates.txt). Git
   ([`blame.ignoreRevsFile`](https://github.com/git/git/blob/777489f9e09c8d0dd6b12f9d90de6376330577a2/Documentation/config/blame.txt#L23-L26))
   and GitHub's blame view
   ([GitHub Docs](https://github.com/github/docs/blob/be38ec5d78e24172587e61b3c6ff40ace1865c71/content/repositories/working-with-files/using-files/viewing-and-understanding-files.md#L54))
   read the same file.
5. **Before each build, the date is brought up to date from Git** by one
   shared script ([content-date.py](helpers/content-date.py) `--write`):
   the later of the written date and the newest listed-not-skipped
   commit. The tools' own Git lookups are not relied on.
6. **The build fetches the full history**, and the script stops on a
   shallow clone (`fetch-depth: 0` for `actions/checkout`).
7. **Dates and years are computed in UTC**, and dates are shown as
   calendar dates.
8. **The copyright year comes from one setting** (`YEAR_MODE`: build,
   site or page), so the decision on the open question changes one value.
   Which value is the open question ([above](#should-the-copyright-year-follow-content-changes)).
9. **A sitemap's `lastmod` is the content date or absent, never the build
   time** ([R-20](../../requirements/README.md#r-20)): Antora's default
   does not meet this; Docusaurus's sitemap plugin can take the content
   date (`lastmod` option), not tested.
10. **The build-time values check runs on every converted page**: one
    notice, with the expected year and holder, and the expected date:
    [checks/buildtime.py](checks/buildtime.py) `--expect`.

## Requirements

- [R-25](../../requirements/README.md#r-25) build-time values are expected
  differences: met by masking in the comparison helper; the copyright year
  and "last updated" date are the only build-time values on the pages,
  besides the HTTP `Last-Modified` header and a serve-time style block,
  which are not page text ([survey](survey/README.md#what-else-on-the-published-pages-is-set-at-build-or-serve-time)).
- [R-01](../../requirements/README.md#r-01) content and outline survive:
  masked, `access-control` keeps its text in every tool; the remaining
  differences are known from the headings round.
- [R-12](../../requirements/README.md#r-12) one-command local preview: a
  date written in the page shows the same in preview and production. The
  tools' Git lookups differ: Docusaurus's development server shows a
  made-up date.
- [R-16](../../requirements/README.md#r-16) old URLs keep working and
  [R-15](../../requirements/README.md#r-15) URL identifies the source:
  files keep their paths but change extension and repository, which is
  what separates them from their Git history.
- [R-20](../../requirements/README.md#r-20) search-engine and AI-friendly
  output: Docusaurus marks the date `itemprop="dateModified"`
  ([`LastUpdated/index.tsx` L37](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-theme-classic/src/theme/LastUpdated/index.tsx#L37));
  Antora's sitemap gives every page the build time.
- [R-13](../../requirements/README.md#r-13) no per-WG extensions: the year
  per page and the custom VCS are code (a React component, an Astro
  override, a Handlebars helper, a config function), maintained by the
  Docs WG if used; the build year and the site year need none beyond
  configuration, except Zensical's config copy.

## Not yet written

- **The candidate list is not reviewed.** It is chosen by commit subject;
  at least one candidate also fixes typos
  ([survey](survey/README.md#the-candidate-list)).
- **Pages that are only an include.** `using-vol-services` takes the date
  of its six-line file; whether such a page should take its partial's
  date, or the newest of both, is open.
- **The holder's name** in the notice was not decided or tested beyond
  printing today's text.
- **Sitemaps with content dates**: Docusaurus's `lastmod` option and
  Starlight's sitemap integration were not tried; Zensical lists no page
  without `site_url` ([sitemaps](results/sitemaps.txt)).
- **How authors keep the date**: the helper updates it at build; whether
  the updated date is also committed (by a bot, or by authors) was not
  tried.
- **Real conversions and rename detection**: only one whole page was
  converted; how many real pages Git would connect across the conversion
  was not measured.
- **The published site's build schedule** is not public; the
  `Last-Modified` header (2026-10-09) is the only sign of when it last
  ran (unverified as the build time).
- **Probes and on-paper tools.** Eleventy, Sphinx/MyST, Middleman, Hugo
  and VitePress were not tried; Sphinx's `%Y` and `SOURCE_DATE_EPOCH`
  handling and Hugo's `now.Year` (kubernetes.io) are cited from source
  only.

[L53]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L53
[L69]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L69
[L83]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L83
[L131]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L131
