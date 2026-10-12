# Build-time value survey

Status: draft, incomplete — covers what is known as of 2026-10-11.

A **build-time value** is a value on a published page that the build
computes instead of reading it from the page's source: today the
copyright year in the footer and the "Page last updated" date. This
survey finds every place the book and its 15 `cloudfoundry/docs-*`
repositories set or print one, records the copyright notices written in
the repositories, and finds, for every page of the book, the commit that
sets its "Page last updated" date. It was done on 2026-10-11 for the
build-time values round ([R-25](../../../requirements/README.md#r-25)
build-time values are expected differences).

| File | What it is |
|---|---|
| [buildtime.csv](buildtime.csv) | 41 rows: each place a value is set or printed at build time, and each copyright notice, with a link to the line |
| [pages.csv](pages.csv) | 276 rows, one per page of the 12 book repositories: the commit that sets "Page last updated" today, the commit it would be with the candidate commits skipped, and, for the 17 pages saved by this and earlier rounds, whether the published date matches |
| [candidates.txt](candidates.txt) | 72 commits whose subject says they change markup only, or remove content the open-source book did not render; in the format of Git's `blame.ignoreRevsFile` |
| [shas.txt](shas.txt) | The 15 repositories and the commit surveyed in each: the partial survey's list |
| [survey.py](survey.py) | Writes the three files above and prints the counts below |

## Scope

- **Repositories and files**: the partial survey's
  ([scope](../../partials/survey/README.md#scope)): the 15 repositories at
  the commits in [shas.txt](shas.txt), every text file, without `.git`,
  `node_modules` and `vendor`. `docs-bosh` (MkDocs, for bosh.io) and
  `docs-dotnet-core-tutorial` are read for notices only; the book does not
  build them.
- **Bookbinder**: the `bookbindery` 9.12.1 gem the book pins
  ([Gemfile L3](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/Gemfile#L3)),
  unpacked, cited at the repository's `v9.12.0` tag
  ([`f608a44`](https://github.com/pivotal-cf/bookbinder/commit/f608a441572def7787361842f05e42d163d78d54));
  the two differ in two files that hold no build-time value
  ([partial survey](../../partials/survey/README.md#how-the-book-resolves-a-partial)).
- **History**: full clones of the 12 book repositories, for `git log`.
  "Page last updated" dates are computed at the surveyed commits.
- **The published site**: four pages fetched on 2026-10-11
  ([../published/](../published/)) and the 17 pages earlier rounds saved.

## How the book sets build-time values

1. **The copyright year is the build's year.** The book's footer writes
   `&copy; <%= Time.now.year %> Cloud Foundry Foundation. All Rights Reserved.`
   ([`_book-footer.erb` L3](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/_book-footer.erb#L3)).
   It is the only ERB expression in the 15 repositories and the book that
   reads the clock ([buildtime.csv](buildtime.csv), kind `erb-time`).
2. **"Page last updated" is a Git date.** Before every page's content the
   book's layout prints Bookbinder's `modified_date`, unless the page's
   front matter says `modified_date: false`
   ([`_pre-content.erb` L1-L3](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/_pre-content.erb#L1-L3)).
   No page says so (no `front-matter` row in buildtime.csv).
3. **The date is the author date of the newest commit to the page's own
   file.** `modified_date` asks `page_last_modified_date`, which asks the
   Git accessor for the page's source file
   ([`bookbinder_helpers.rb` L85-L91, L159-L169](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/bookbinder_helpers.rb#L85-L169)).
   The accessor walks up to the folder that holds `.git`, lists the file's
   log, and returns the author date of the first commit whose message does
   not contain `[exclude]`
   ([`git_accessor.rb` L57-L84](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/lib/bookbinder/ingest/git_accessor.rb#L57-L84)).
   The log is ruby-git's, whose default length is 30 commits
   ([`object.rb` L62](https://github.com/ruby-git/ruby-git/blob/8425a6b6169eaeda0afe2e16b0e4210ed433caf2/lib/git/object.rb#L62)
   at v1.2.8, the same line at
   [v1.2.9.1](https://github.com/ruby-git/ruby-git/blob/cc6d6efc1b7eaf63609c4c06969b0f839dc80095/lib/git/object.rb#L62);
   Bookbinder requires `git ~> 1.2.8`,
   [gemspec L29](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/bookbinder.gemspec#L29)).
   Partials and variables the page uses do not count, and renames are not
   followed.
4. **The rule matches every saved published page.** For all 17 pages saved
   by this round and earlier ones, the published date equals the date the
   rule gives at the surveyed commits ([pages.csv](pages.csv), column
   `published_date_matches`). Two of them are dated by a merge commit,
   whose result differed from both parents: `git log -- <file>` lists such
   merges ([`542bfd4`](https://github.com/cloudfoundry/docs-cf-admin/commit/542bfd4d7a482fe0a8d3abf5284665f122c8977a)).
5. **The date is drawn in the reader's browser, in the reader's time
   zone.** The page holds milliseconds since 1970 in a `data-modified-date`
   attribute
   ([`bookbinder_helpers.rb` L90](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/bookbinder_helpers.rb#L90));
   a script writes "Dec 5, 2024" with the browser's local date
   ([`bookbinder.js` L39-L44, L89-L95](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/source/javascripts/bookbinder.js#L39-L95)).
   The static HTML says "Page last updated:" with no date, as the headings
   round's text comparison showed
   ([text diff](../../headings/results/text-diff-access-control.txt)). So
   readers in different time zones can see different dates:
   `architecture`'s 2024-12-05T22:18:28Z gives day 6 of month 12 with the
   JavaScript `Date` getters the script uses, run under `TZ=Asia/Tokyo`
   in Node (checked 2026-10-11), and day 5 under `TZ=America/Los_Angeles`.
6. **`[exclude]` exists, and was used once per repository, in 2015.** The
   nine commits whose message holds it are all "Adding last mod date
   [exclude]", 2015-12-03: the commits that added the date line
   (for example docs-buildpacks
   [`89090b9`](https://github.com/cloudfoundry/docs-buildpacks/commit/89090b9f55de728db005fa2b3745f0bf20fc6f32)).
   No commit since uses it, including the July 2026 markup commits below.

## What else on the published pages is set at build or serve time

Observed on the pages fetched on 2026-10-11 ([../published/](../published/)):

- **The HTTP `Last-Modified` header is the deployment time**, the same on
  every page: `Fri, 09 Oct 2026 09:01:28 GMT` on both
  `loggregator/architecture.html` and `adminguide/enabling-tcp-routing.html`
  (`curl -I`, 2026-10-11). It is not on the page.
- **An inline `<style>` of `@font-face` rules is added when the page is
  served**, with font paths under `/cf-fonts/`; the order of the rules
  changes from one request to the next. Two fetches of each page a few
  seconds apart differ only in that line (line 8 of each copy in
  [../published/](../published/)); the response's `server` header is
  `cloudflare`. Unverified which CDN feature adds it.
- **No sitemap and no robots file**: `https://docs.cloudfoundry.org/sitemap.xml`
  and `/robots.txt` answer 404 (2026-10-11).
- **No date in `<meta>`**: the pages' `<meta>` tags are `charset`,
  `X-UA-Compatible` and `viewport` only
  ([book layout L4-L16](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/layout.erb#L4-L16)).
- **Not build-time: version strings.** Values such as
  `routing_version: routing-release 0.166.0`
  ([`template_variables.yml` L340](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L340))
  are written by hand; they belong to the variables round.

## Copyright notices in the repositories

- **13 repositories have a `NOTICE` file**, each with "Copyright (c)
  YYYY-Present CloudFoundry.org Foundation, Inc. All Rights Reserved.": the
  first year is 2013 (docs-bbr, docs-buildpacks), 2015 (eight
  repositories and the book), 2017 (docs-credhub) or 2019
  (docs-dotnet-core-tutorial) ([buildtime.csv](buildtime.csv), kind
  `notice`). docs-running-cf and docs-services have none.
- **Earlier holders are kept**: "Copyright (c) 2012-2015 Pivotal Software,
  Inc." in four repositories, and in other words in docs-bosh; the book's own NOTICE says "2012-2105"
  ([NOTICE L3](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/NOTICE#L3),
  as written); docs-dev-guide adds "Copyright (c) 2023 VMware Inc."
  ([NOTICE L3](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/NOTICE#L3)).
- **Three names for the holder**: "CloudFoundry.org Foundation, Inc." in
  the NOTICE files, "Cloud Foundry Foundation" in the book's footer, and
  "The Linux Foundation" in the footer of cloudfoundry.org ("Copyright
  ©2026 The Linux Foundation®. All rights reserved.",
  <https://www.cloudfoundry.org/>, fetched 2026-10-11).
- **bosh.io's footer has no year**: `copyright:` in docs-bosh's MkDocs
  configuration is a "powered by" line
  ([`mkdocs.yml` L404](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/mkdocs.yml#L404)).

## The dates of today's pages

Counts from [pages.csv](pages.csv) (printed by [survey.py](survey.py)):

| Year of "Page last updated" | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|
| Today (Bookbinder's rule) | 40 | 26 | 13 | 197 |
| With the candidate commits skipped | 52 | 62 | 34 | 128 |

- **154 of the 276 pages (56%) are dated July 2026.** The commits that date
  five or more pages are bulk edits of that month:
  "Remove platform-conditional ERB blocks, keep OSS content" (20 pages in
  docs-cf-admin, 12 in docs-dev-guide, 11 in docs-cloudfoundry-concepts,
  5 in docs-credhub), "Fix inline closing </p> tags in note blocks" (18,
  docs-dev-guide), "Add note__title spans to all note blocks" (9, 6 and 5
  in three repositories), and the merge `542bfd4` (6). One older commit
  dates nine pages: "review and update topic titles to improve SEO",
  docs-buildpacks, 2023-08-30. (Subjects are quoted without the tags some
  commits carry, such as "[no-ai]".)
- **Skipping the candidates moves 133 pages' dates**: 64 stay in 2026,
  and 69 go back to 2023–2025.
- **The newest date is the same either way**: 2026-10-06. A site-wide
  "content year" is 2026 under both rules.

### The candidate list

Decision (this round): the candidates are the 2026 commits whose subject
matches markup-only or not-rendered changes (the regular expression
`CANDIDATE` in [survey.py](survey.py): closing `</p>` tags, `note__title`
spans, Redcarpet HTML blocks, "naked Markdown", `a name` to `a id`,
platform-conditional or commercial-only ERB, blank lines, trailing
newlines, notes converted to HTML). They are **candidates for the Docs WG
to review, not a decision that they changed no content**:

- One matches by its subject and also fixes typos and removes links:
  "Fix typos and exposed Markdown in rolling-deploy; remove stale links"
  (docs-dev-guide [`2dbf192`](https://github.com/cloudfoundry/docs-dev-guide/commit/2dbf192c1339ed1982f6c72a2a45654b0b49087e)).
- "Add note__title spans" adds a visible "Note" or "Important" label to
  each note: presentation, but visible.
- Merge commits are not candidates, so the merge `542bfd4`, which brought
  the ERB removal into its branch, still dates six pages.
- Commits whose subject does not say what they changed ("full edit",
  "updates") are not candidates, whatever they changed.

## How to rerun

Run from a working directory outside this repository, with `python3 -I`.
`SURVEY` stands for this folder, `concepts/build-time-values/survey`, and
`CONCEPTS` for `concepts/`.

```sh
# The 15 repositories at their commits, as in the partial survey
# (its README, "How to rerun"), into repos/

# Full histories of the 12 book repositories (blobless is enough)
mkdir -p hist
git clone -q --bare --filter=blob:none https://github.com/cloudfoundry/docs-bbr.git hist/docs-bbr.git
# … the same for each book repository in SURVEY/shas.txt

# The bookbindery 9.12.1 gem, unpacked
mkdir -p gem && curl -fsSL -o gem/bb.gem https://rubygems.org/downloads/bookbindery-9.12.1.gem
tar -xf gem/bb.gem -C gem && mkdir gem/src && tar -xzf gem/data.tar.gz -C gem/src

python3 -I SURVEY/survey.py repos hist SURVEY/shas.txt gem/src \
  CONCEPTS/headings/published CONCEPTS/notes/published CONCEPTS/partials/published \
  CONCEPTS/variables/published CONCEPTS/build-time-values/published -o out
cmp out/pages.csv SURVEY/pages.csv && cmp out/candidates.txt SURVEY/candidates.txt
```

The script reads files and runs `git log` and `git ls-tree` only; it runs
nothing from the clones or the gem.
