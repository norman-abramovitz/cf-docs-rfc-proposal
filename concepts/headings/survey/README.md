# Heading survey

Status: draft, incomplete — covers what is known as of 2026-10-10.

This survey lists every heading in the source of the book's 12
repositories. It was done to choose the test pages of the Headings round
([test pages](../README.md#test-pages)): pages whose headings show a case
that a conversion could break. It reads the repositories at the commits
the table survey used ([shas.txt](../../tables/survey/shas.txt)).

The round's first scan of this kind was not kept. This survey redoes it
with a committed script and data.

| File | What it is |
|---|---|
| [headings.csv](headings.csv) | One row per heading, 2,164 rows, each with a GitHub link to the heading at the surveyed commit |
| [pages.csv](pages.csv) | One row per page, 320 rows, pages without headings included |
| [scan.py](scan.py) | Finds and measures the headings in a set of clones |

## Scope

**Repositories.** The book is the set of repositories that Bookbinder, the
tool that builds docs.cloudfoundry.org today, collects into one site
([glossary](../../../glossary.md#bookbinder)). Its sections are the 12
`cloudfoundry/docs-*` repositories named in the book's
[`config.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml#L10-L87)
at commit `30dfa57`. All 12 are scanned. The file also names sample apps
and `cf-release` as dependent sections; those are not documentation pages
and are not scanned.

| Repository | Commit (date) | Pages | With headings | Headings |
|---|---|---|---|---|
| cloudfoundry/docs-bbr | [`5146595`](https://github.com/cloudfoundry/docs-bbr/tree/51465950ce3a2196d66a9339086b94feed280c3e) (2026-07-09) | 9 | 8 | 116 |
| cloudfoundry/docs-buildpacks | [`239e5c8`](https://github.com/cloudfoundry/docs-buildpacks/tree/239e5c8676200914c4d386970f9989e46de9e969) (2026-10-09) | 62 | 50 | 434 |
| cloudfoundry/docs-cf-admin | [`13826fa`](https://github.com/cloudfoundry/docs-cf-admin/tree/13826fa7d93eee66902c4a2187a96b884137b58a) (2026-07-22) | 50 | 29 | 255 |
| cloudfoundry/docs-cf-cli | [`ee9aad5`](https://github.com/cloudfoundry/docs-cf-cli/tree/ee9aad56524157ae2316c00149b75737439235dc) (2026-07-22) | 8 | 8 | 60 |
| cloudfoundry/docs-cloudfoundry-concepts | [`97e0d0b`](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/tree/97e0d0b25f059c06edd25e30355d26eb93dc560a) (2026-09-14) | 41 | 27 | 225 |
| cloudfoundry/docs-credhub | [`21b0448`](https://github.com/cloudfoundry/docs-credhub/tree/21b0448736435cec0f5a1491e0b40bda9c4307eb) (2026-07-23) | 8 | 8 | 47 |
| cloudfoundry/docs-deploying-cf | [`1113cfa`](https://github.com/cloudfoundry/docs-deploying-cf/tree/1113cfaf3626931c653c91dc8d537d7f181d6762) (2026-07-24) | 13 | 11 | 66 |
| cloudfoundry/docs-dev-guide | [`9c8df63`](https://github.com/cloudfoundry/docs-dev-guide/tree/9c8df63eb3823011e4e3aff9958c36e25d5190b7) (2026-09-28) | 67 | 53 | 503 |
| cloudfoundry/docs-loggregator | [`8e027ba`](https://github.com/cloudfoundry/docs-loggregator/tree/8e027bac1099b737afe56afa1606b4fcf9d06c94) (2026-07-22) | 12 | 9 | 84 |
| cloudfoundry/docs-running-cf | [`956acc8`](https://github.com/cloudfoundry/docs-running-cf/tree/956acc86445d2f3cb29f031294f86f37f515b471) (2026-08-05) | 32 | 22 | 221 |
| cloudfoundry/docs-services | [`ccb0036`](https://github.com/cloudfoundry/docs-services/tree/ccb0036407e4c2eabbb61a3b3de008f821f41c5b) (2026-07-22) | 11 | 10 | 76 |
| cloudfoundry/docs-uaa | [`216c797`](https://github.com/cloudfoundry/docs-uaa/tree/216c797cfa1a971cf0f9e53eb3e4803aaf914a94) (2026-07-22) | 7 | 6 | 77 |
| **All** | | **320** | **241** | **2,164** |

The date is the commit's date. The commits are the ones in the table
survey's [shas.txt](../../tables/survey/shas.txt); this folder does not
keep its own copy.

- **Pages.** A page is a file the table survey would read
  ([survey.py](../../tables/survey/survey.py)): `.md`, `.erb`, `.html`,
  `.haml`, `.markdown`, `.mdx` and `.adoc`. Folders named `.git`,
  `node_modules` and `vendor` are skipped, and so are Markdown files at a
  repository's root (READMEs and contributor notes; no site publishes
  them). At these commits every page is an `.html.md.erb` file.
- **Partials count as pages.** A partial is a file included into other
  pages ([glossary](../../../glossary.md#partial)); its name starts with
  `_`. There are 44 partials; 9 have headings, 34 headings in all. Each is
  scanned as its own page, not inside the pages that include it.
- **Source, not published pages.** The survey reads the files in the
  repositories. It does not run ERB
  ([glossary](../../../glossary.md#erb)), so a heading's text keeps its
  `<%= vars.… %>` variables as written.

## Method

[scan.py](scan.py) reads every page and skips the parts that cannot hold a
heading:

- the front matter, the settings block between `---` lines at the top of
  the file ([glossary](../../../glossary.md#front-matter));
- fenced code blocks (from a line starting with three or more `` ` `` or
  `~`, to the next line starting with the same character);
- `<pre>` blocks and HTML comments.

In what is left it finds two kinds of heading:

- **Markdown headings:** a line that starts with one to six `#` (an ATX
  heading), at most three spaces in. The space after the `#`s may be
  missing, as the book's Markdown engine allows (see
  [No space after the `#`s](#no-space-after-the-s)). Closing `#`s are
  dropped.
- **HTML headings:** an `<h1>` to `<h6>` element, up to its closing tag.

For each heading, [headings.csv](headings.csv) records:

| Column | What it holds |
|---|---|
| `repo`, `file`, `line` | where the heading starts |
| `level` | 1 to 6 (`##` and `<h2>` are both 2) |
| `kind` | `markdown` or `html` |
| `ids`, `id_source` | the explicit id, and where it was found: `inline` (an `<a id="…">` or `<a name=…>` inside the heading), `line-before` (an anchor alone on the line just above), `attribute` (`id=` on the `<hN>` tag), or empty |
| `text` | the heading's text, HTML tags removed, ERB tags kept |
| `code` | it holds a backtick or `<code>` |
| `link` | it holds a Markdown link or an `<a href>` |
| `erb` | it holds an ERB tag (`<%`) |
| `no_space` | a Markdown heading with no space after the `#`s |
| `skipped_level` | it is more than one level deeper than the heading before it on the page |
| `url` | a link to the heading's line at the surveyed commit |

An explicit id is one the source writes; a page's other headings get an id
the build makes from their text.

For each page, [pages.csv](pages.csv) records whether it is a partial, its
heading count, the level of its first heading, the count per level, the
Markdown and HTML counts, the headings with and without an explicit id,
the number of skipped levels and the line of the first, and a link to the
file. Two more columns count lines the scan does not take as headings: `#`
lines indented four or more spaces (an indented code block in Markdown),
and setext underlines (a line of `===` or `---` under a line of text, the
other Markdown heading syntax). Both are 0 on every page.

## Totals

From [headings.csv](headings.csv) and [pages.csv](pages.csv):

- **320 pages**, 241 with headings and 79 without.
- **2,164 headings.** By level: `h1` 1, `h2` 1,027, `h3` 930, `h4` 202,
  `h5` 4, `h6` 0.
- **By kind:** 2,148 Markdown, 16 HTML.
- **Explicit ids:** 1,929 headings have one, 235 do not. Every explicit id
  is an `<a id>` inside the heading; no heading has two. The 235 without
  are on 46 pages; on 7 of those pages no heading has an id.
- **First heading:** on 235 pages it is an `h2`. Three pages start at
  `h3` and two at `h4`; all but one
  ([`managing-stacks`](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/managing-stacks.html.md.erb))
  are partials. One page starts at `h1` (below).

## Findings

### Skipped levels

A level is skipped when a heading is more than one level deeper than the
heading before it, such as `##` followed by `####`. Only headings after a
page's first are checked. Three headings on two pages skip a level:

- docs-services `access-control`, twice:
  [L61](https://github.com/cloudfoundry/docs-services/blob/ccb0036407e4c2eabbb61a3b3de008f821f41c5b/access-control.html.md.erb#L61)
  and
  [L107](https://github.com/cloudfoundry/docs-services/blob/ccb0036407e4c2eabbb61a3b3de008f821f41c5b/access-control.html.md.erb#L107),
  each a `####` after a `##`.
- docs-bbr `restore`, once:
  [L76](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/restore.html.md.erb#L76),
  a `####` after the `##` at L64.

### HTML heading tags

Two pages use HTML heading tags, both in docs-dev-guide. All 16 carry an
`<a id>` inside the tag.

- `deploy-apps/routes-domains`: 15 `<h4>` tags among Markdown headings
  (first at
  [L141](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L141)).
  The page has 42 headings, from `h2` to `h5`.
- `services/application-binding`: one `<h3>`
  ([L32](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/application-binding.html.md.erb#L32)).

### Code and links in headings

- **Code:** no heading holds a backtick or `<code>`.
- **Links:** two headings on one page, docs-buildpacks `python/index`:
  "Miniconda support (starting in buildpack version 1.5.6)"
  ([L190](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/python/index.html.md.erb#L190))
  and "Pipenv support (starting in buildpack version 1.5.19)"
  ([L194](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/python/index.html.md.erb#L194)).
  The version number is the link.

### Variables in headings

27 headings on 15 pages hold an ERB tag, all of them a variable such as
`<%= vars.app_runtime_abbr %>`
([glossary](../../../glossary.md#variable)). Example: docs-cf-admin
`troubleshooting_slow_requests`
[L422](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting_slow_requests.html.md.erb#L422).

### No space after the `#`s

97 Markdown headings on 20 pages have no space after the `#`s, as in
`##<a id='benchmark-setup'></a> Benchmarking`
([docs-running-cf `uaa-performance` L25](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/uaa-performance.html.md.erb#L25)).
By repository: running-cf 40, buildpacks 25, deploying-cf 16, dev-guide 9,
cloudfoundry-concepts 4, cf-admin 3.

The book renders them as headings: the
[published page](https://docs.cloudfoundry.org/running/uaa-performance.html)
(as served on 2026-10-10; not pinned) shows "Benchmarking" as an `<h2>`.
CommonMark ([glossary](../../../glossary.md#commonmark)) requires the
space ([spec 0.31.2, ATX headings](https://spec.commonmark.org/0.31.2/#atx-headings)),
so a tool built on it reads these lines as paragraphs. A conversion has to
add the space.

### The same id twice on a page

18 explicit ids appear on more than one heading of the same page: 40
headings on 17 pages. None of these pages uses an ERB `if`, so every copy
is published. A link to such an id reaches only the first. Examples:

- docs-running-cf `uaa-performance`: `client-credentials` four times
  ([L84](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/uaa-performance.html.md.erb#L84),
  [L169](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/uaa-performance.html.md.erb#L169),
  [L254](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/uaa-performance.html.md.erb#L254),
  [L305](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/uaa-performance.html.md.erb#L305)).
- docs-dev-guide `services/integrate-splunk`: `config` on three
  consecutive `###` headings
  ([L32](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/integrate-splunk.html.md.erb#L32),
  [L40](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/integrate-splunk.html.md.erb#L40),
  [L60](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/integrate-splunk.html.md.erb#L60)).

To list them all, group [headings.csv](headings.csv) by `repo`, `file` and
`ids`.

### An `h1` in the body

One page has a `#` heading: docs-loggregator `opentelemetry`
([L11](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/opentelemetry.html.md.erb#L11)).
The book also prints the front-matter title as an `h1`, so the
[published page](https://docs.cloudfoundry.org/loggregator/opentelemetry.html)
(as served on 2026-10-10; not pinned) has both the title and "Collector
configuration structure" as `<h1>`.

### Fences closed the book's way

docs-bbr `backup` closes a code block with `` ```<br> ``
([L76](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L76)),
and opens one with four backticks and closes it with three
([L359](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L359)).
The
[published page](https://docs.cloudfoundry.org/bbr/backup.html) (as served
on 2026-10-10; not pinned) closes both blocks there: its six headings after
L76 are all `<h2>`s. The scan closes them the same way. In CommonMark
neither line closes the block, so the rest of the page would become code.
A conversion has to repair both lines
([R-24](../../../requirements/README.md#r-24) markup cleanup before
conversion).

## Compared with the round's first scan

The round's [README](../README.md#test-pages) and
[results](../results.md#not-yet-written) describe a first scan of 11
repositories: about 1,950 headings on 225 pages with headings. Which
repository it left out is not recorded. This scan covers all 12.

- **Skipped levels:** the first scan found one page, `access-control`.
  This scan finds two; the second, `restore`, is in docs-bbr.
- **HTML heading tags:** the same two pages and counts (15 and 1).
- **Code in headings:** none, the same.
- **Links in headings:** the same one page, `python/index`, which has two
  such headings, not one.
- **Counts:** 2,164 headings on 241 pages with headings. Leaving out any
  one repository does not give the first scan's figures (without docs-bbr:
  2,048 headings on 233 pages), so the first scan also counted
  differently.

## How to rerun

Run everything from a working directory outside this repository, with
`python3 -I` (isolated mode: Python ignores the current directory and
environment variables when it loads modules). `SURVEY` below stands for
this folder, `concepts/headings/survey`.

Clone the 12 repositories at the table survey's commits, then scan them:

```sh
grep -E '^docs-(bbr|buildpacks|cf-admin|cf-cli|cloudfoundry-concepts|credhub|deploying-cf|dev-guide|loggregator|running-cf|services|uaa) ' \
  SURVEY/../../tables/survey/shas.txt > shas-book.txt
mkdir -p repos
while read name sha date; do
  git clone --quiet "https://github.com/cloudfoundry/$name" "repos/$name"
  git -C "repos/$name" checkout --quiet "$sha"
done < shas-book.txt

python3 -I SURVEY/scan.py repos shas-book.txt out
cmp out.csv SURVEY/headings.csv
cmp out-pages.csv SURVEY/pages.csv
```

`scan.py` writes `out.csv` and `out-pages.csv` and prints the totals above.
It was run twice on 2026-10-10 and both runs gave byte-identical files.
The script reads files only; it runs nothing from the clones.
