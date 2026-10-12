# Concept: Cross-repository links

Status: **draft, incomplete — covers what is known as of 2026-10-11.** The
survey, the conversions, the checks and the probes are done; the
conventions are proposals for review. Results: [results.md](results.md).

This round asks whether links between pages that come from different
content repositories keep working after conversion, in each hands-on tool,
whether the content stays in separate repositories or moves into one
([R-08](../../requirements/README.md#r-08) cross-repository links). The RFC
allows bulk conversion "as long as cross-repository links are preserved"
([L131]) and puts all content into one repository ([L69]);
[R-15](../../requirements/README.md#r-15) asks that a URL still name its
source, and [R-16](../../requirements/README.md#r-16) that old URLs keep
working. The round adds a links check beside the outline, notes, variables
and partials checks, and answers the two open items the variables and
partials rounds left on relative links.

Terms used below:

- **Content repository.** One of the `cloudfoundry/docs-*` repositories the
  book collects. The book's `config.yml` publishes each under a URL
  **directory**: docs-cf-admin under `adminguide/`, docs-dev-guide under
  `devguide/`, and so on
  ([`config.yml` L9-L90](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml#L9-L90)).
  A link **crosses a repository boundary** when the page it renders on and
  the page it reaches come from different repositories.
- **Link forms.** *Page-relative* (`../adminguide/x.html`, resolved
  against the page's address), *root-relative* (`/adminguide/x.html`),
  *absolute* (with a host), *in-page* (`#id`). The **anchor** or fragment
  is the id after `#`.
- **Content source.** A folder or repository a tool reads pages from:
  a docs plugin instance (Docusaurus), the docs folder (Zensical), the docs
  collection (Starlight), a component's content source (Antora).
- **Layouts.** *split*: one content source per repository, as separate
  repositories would be read; *mono*: one repository whose top-level
  folders are the URL directories; *linked*: one folder whose subfolders
  are symbolic links to the repositories' folders.
- **Modes.** *passthrough*: every link as the source writes it;
  *native*: every internal link in the tool's own form (a file path,
  `xref:`, or the tool's URL). Everything outside the links follows the
  earlier rounds' native conventions in both modes.
- **URL style.** *`.html`*: pages published as `<path>.html`, the book's
  URLs; *default*: the tool's default, `<path>/index.html`, used in one
  extra variant per tool to show what breaks.
- **Stub page.** A page standing for a link target outside the test pages:
  its title and the ids the test pages link to.

## Progress

- [x] **Survey.** Every link in the 15 `docs-*` repositories and the book
  repository at the partials survey's commits: 3,210 rows in the book
  (2,892 in pages, partials and variable values), 1,693 in the two MkDocs
  sites, and the book's 85 redirect rules; 594 rows cross a repository
  boundary; 55 already fail. The model is checked against 18 published
  pages: 233 of 233 heading ids, 250 of 251 links. Script, data and
  write-up: [survey/](survey/README.md).
- [x] **Test pages chosen and copied**, verbatim at the survey's commits:
  [source/SOURCES.md](source/SOURCES.md), with `http-routing` as served on
  2026-10-11 in [published/](published/); the other three published pages
  are the earlier rounds' copies.
- [x] **Intent written.** For each page, every link with its target page
  and anchor, and a links file the check reads: [intent/](intent/).
- [x] **Links check written**: [checks/links.py](checks/links.py), with
  [checks/check-site.sh](checks/check-site.sh),
  [checks/check-published.sh](checks/check-published.sh) and
  [checks/redirects.py](checks/redirects.py).
- [x] **Converted and built** in all four hands-on tools, in every layout
  each tool supports, passthrough and native, plus each tool's default URL
  style. Every native variant passes 39 of 39 links:
  [results.md](results.md#summary).
- [x] **Probes**: broken links into another source, links held in
  variables and partials at two depths, and redirects for old URLs, in
  every tool.
- [ ] **Conventions reviewed.** The nine proposals in
  [results.md](results.md#conventions-to-record).

## Test pages

| Page | Repository | Links | Cases |
|------|------------|-------|-------|
| [`http-routing`](intent/http-routing.md) | cloudfoundry/docs-cloudfoundry-concepts (new) | 12 | links into two other repositories; four links held in variables, one written for its page's depth; an absolute link to docs.cloudfoundry.org; a folder index page |
| [`troubleshooting-router-error-responses`](intent/troubleshooting-router-error-responses.md) | cloudfoundry/docs-cf-admin (variables round) | 12 | the other end of a two-way pair with `http-routing`; a link whose target is a variable, into a third repository; three links already broken; an external link |
| [`enabling-tcp-routing`](intent/enabling-tcp-routing.md) | cloudfoundry/docs-cf-admin (partials round) | 7 | three links to ids on `routes-domains`; a fourth repository (docs-cf-cli) and its index page; a link in an indented list paragraph |
| [`routes-domains`](intent/routes-domains.md) | cloudfoundry/docs-dev-guide (headings round) | 8 | a page two folders deep; the target of the links above, one id on an HTML heading; an HTML link; a link inside a partial; two links already broken |

**How they were chosen.** Decision (this round): from the survey's rows,
pages that link to each other across repositories, taken from the earlier
rounds where possible, with together every link form the book's content
uses (page-relative at one and two levels, root-relative, absolute, in-page,
a variable as target, links held in variable values and in a partial, an
HTML link, a folder index page) and links already broken. `http-routing` is
new: the earlier rounds' test pages link to it more than to any other page
(seven links from three of them), it links back, and it holds one of the
two root-relative links in the book's variable values. The four pages
come from three repositories; their 15 stub targets add docs-running-cf
and docs-cf-cli. Each page keeps every heading and the lines holding the
links ([SOURCES](source/SOURCES.md#notes)).

## Links check

[checks/links.py](checks/links.py) reads a built page and checks its links.
It needs only Python 3.

```bash
# Every link in the page's content area: href, form, target page and anchor, status
python3 -I checks/links.py SITE/concepts/http-routing.html --root SITE

# The same, against the page's links file
python3 -I checks/links.py SITE/concepts/http-routing.html --root SITE --expect intent/http-routing.links

# Links and outline checks on every test page in some variants of one site (run from sites/<tool>)
../../checks/check-site.sh build split-native mono-native

# The links check on the four published pages, at their paths
checks/check-published.sh

# What a built site serves at old URLs
python3 -I checks/redirects.py SITE /devguide/deploy-apps/domains-routes.html
```

What it does:

- **Finds the content area** (each tool's article, or the published page's
  `main#js-content`), leaving out navigation, tables of contents, the
  published page's quick links, permalink icons and edit buttons.
- **Resolves each link as a browser and a static host do**: joined to the
  page's own URL, then the file in the built site, a folder's
  `index.html`, or `PATH.html` for a path with no extension (as GitHub
  Pages serves it). A target that only redirects is reported as a redirect
  page, not as resolving.
- **Checks the anchor** against every `id` and `<a name>` of the target
  page.
- **Reports each link's form after conversion**: in-page, page-relative or
  root-relative with `.html`, a folder or no extension, absolute, external.
- **With a links file**, matches the page's links by their text, in order,
  and fails on a link that is missing, resolves elsewhere, or is not listed.
  Links already broken in the book are listed as `no anchor` and must stay
  so.

It knows nothing about these pages. `make check` in each site runs it and
the outline check on every test page; `make check-other` on the variants
that show what breaks.

## Method

1. **Survey** every link and resolve it against a model of the book's site
   and server; check the model on published pages and live.
2. **Choose pages** that link to each other across repositories and hold
   the book's link forms, preferring pages already converted.
3. **Write the intent**: each link's target page and anchor.
4. **Convert** into each tool, in each layout and mode. The mechanical part
   (headings in each tool's syntax, links rewritten for native mode,
   AsciiDoc lists) was done with a scratch script; every page was then
   reviewed by hand.
5. **Build and check** each variant with the links and outline checks, and
   run the probes.
6. **Record conventions** per tool ([sites/](sites/)`<tool>/CONVENTIONS.md`).

Each tool keeps the version of the earlier rounds and their settings for
headings; the URL settings are this round's.

## Layout

```
concepts/cross-repo-links/
├── README.md          this file
├── results.md         results per tool, across tools, conventions, requirements
├── survey/            survey.py, summary.py, ids.py, published.py, links.csv, redirects.csv, shas, checks of the model, README
├── source/            the new test page and redirects.rb, verbatim, plus SOURCES.md
├── published/         http-routing as served on 2026-10-11
├── intent/            per page: <page>.md, <page>.links (what the check compares), <page>.anchors
├── checks/            links.py, check-site.sh, check-published.sh, redirects.py
├── sites/             docusaurus/, zensical/, starlight/, antora/: pages per mode and layout, config, Makefile, probes, CONVENTIONS.md
└── results/           check output per tool, build warnings, probes, edit links, published check
```

Each site builds with `make build` and checks with `make check`; `make
check-other`, `make probe-broken`, `make probe-depth` and `make
probe-redirects` run the rest. Build output and installed packages are
ignored by git (each site's `.gitignore`); the results in
[results/](results/) were produced from copies of the sites built outside
the repository, with the copies' paths removed.

Decision (this round): the saved published page stays in the repository so
the checks can be rerun after the live site changes, as in the earlier
rounds.

[L69]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L69
[L131]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L131
