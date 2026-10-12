# Cross-repository links round — results

Status: draft, incomplete — covers what is known as of 2026-10-11.

What each tool did with the links of the four test pages, laid out as
separate content sources and as one repository with directories. A summary
across tools comes first, then one section per tool, then the questions
across tools, the conventions to record and the requirements. How the
pages were chosen, the terms and the modes: [README](README.md). How the
book writes and resolves links today: [survey](survey/README.md). Per-page
links: [intent/](intent/).

How to read the results:

- **Links check:** the [links check](checks/links.py) reads each link in a
  built page's content area, resolves it as a browser and a static host
  would, and compares it with the page's links file ([intent/](intent/)):
  the page it reaches (as a key: its path without `.html` and without a
  final `/index`), the anchor, and whether that id exists. "39 of
  39" means every link of the four pages is as expected: 33 resolve, 1 is
  external, and 5 already broken in the book stay broken.
- **Outline check:** the headings round's
  [outline check](../headings/checks/outline.py) on every page, against
  the published page, with the ids other pages link to
  (`intent/<page>.anchors`). It passes on every page in every variant
  ([results/](results/)).
- **Variants:** one build each, a whole site served at `/`. *split* lays
  the repositories out as separate content sources, *mono* as folders of
  one repository, *linked* as folders that are symbolic links;
  *passthrough* writes links as the source does, *native* in the tool's own
  form; *default* uses the tool's default URL style instead of `.html`.

All builds ran on 2026-10-11 with the tool versions the earlier rounds
pinned: Docusaurus 3.10.2, Zensical 0.0.69, Starlight 0.42.6 (Astro 7.3.8,
`@astrojs/markdoc` 2.0.11), Antora 3.2.1.

## Summary

With each tool set to write pages as `<path>.html`, the book's URLs, every
link of the four test pages is as expected in every tool, in native form
and in every layout the tool supports: 39 of 39. The book's own relative
`.html` links also work unchanged in three tools; in Starlight two links to
folder index pages break. The tools differ in what a link across content
sources looks like in the source, whether the build checks it, and what
each tool's layout of separate repositories allows.

| | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| **Separate content sources** | one docs plugin instance per repository | folders of the one docs folder (submodules); linked folders are not built | folders of the one collection, checked out or linked | one component per repository, each a content source |
| **One repository with directories** | one docs instance | one docs folder | one collection | one `ROOT` component, a module per directory |
| **Same URLs in both layouts** | yes | yes | yes | yes |
| **`<path>.html` URLs** | `trailingSlash: false` | `use_directory_urls = false` | `build.format: 'file'`; a folder's index page becomes `<folder>.html` | `html_extension_style: default` |
| **Links check, native** | 39 of 39 (split and mono) | 39 of 39 | 39 of 39 (mono and linked) | 39 of 39 (split and mono) |
| **Links check, passthrough** | 39 of 39 | 39 of 39 | 37 of 39 | 39 of 39 |
| **Links check, default URLs** | 13 of 39 | 15 of 39 | 13 of 39 | 13 of 39 |
| **Native link to another repository** | file path in mono; root-relative URL in split | file path (`.md`) | root-relative URL | `xref:` with component (split) or module (mono) |
| **Build reports a missing page in another source** | yes, broken link | native only, warning with line | no | native only, error with page; exit 0 by default |
| **Build reports a missing anchor in another source** | native only, broken anchor | native only, warning with line | no | no |
| **Edit link names each page's repository** | yes, both layouts | no, one base | no, one base (per-page override possible) | yes, split |
| **Old URL redirects** | client-redirects plugin; not at `….html` | `redirects` plugin | Astro `redirects` | `page-aliases` |

- **The book already rewrites its links.** Markdown links that find their
  page are published root-relative (`/adminguide/x.html`); HTML links are
  published as written ([survey](survey/README.md#how-the-book-builds-a-link)).
  Docusaurus does the same with relative URL links; Zensical and Antora
  publish page-relative URLs; Starlight publishes what the page says.
- **`<path>.html` URLs are the setting that matters most.** With each
  tool's default folder URLs, 24 to 26 of the 39 links break in passthrough,
  in every tool, since `../x.html` then reaches neither the right folder
  nor an existing file ([check-other results](results/)).
- **Some forms do not depend on the page's depth.** Root-relative URLs,
  Antora xrefs and Docusaurus file links in a partial resolve on pages at
  any depth; relative URLs held in variables or partials work only at one
  depth in every tool, as in the book ([depth probe](#links-in-variables-and-partials)).
- **The book has 55 links that already fail**, and its own link checker
  reports none of them, since it checks neither fragments nor absolute URLs
  ([survey](survey/README.md#findings)). Three tools can report the
  equivalent problems at build time in native form; Starlight cannot
  without a plugin.

## Docusaurus 3.10.2

Site: [sites/docusaurus/](sites/docusaurus/) — conventions:
[CONVENTIONS.md](sites/docusaurus/CONVENTIONS.md).

### Summary

- **Separate repositories are separate docs plugin instances**, each under
  its URL directory; one repository is one instance. Both give the same
  URLs and pass every check ([check](results/docusaurus-check.txt)).
- **File links work only within one instance.** In split, the 19 file
  links to other instances stay `….mdx` URLs that reach nothing
  (`split-filelinks`, 20 of 39); the native split pages link to other
  instances by root-relative URL instead.
- **Passthrough works in the output and fails the build's check**: every
  `.html` link resolves, while Docusaurus reports 24 of them as broken
  ([build warnings](results/docusaurus-build-warnings.txt)).
- **The build reports links across sources**: a missing page and a missing
  anchor in another instance are both reported, and `throw` stops the
  build ([probe](results/docusaurus-probe-broken.txt)).
- **One edit link per repository** in both layouts, through an `editUrl`
  function ([edit links](results/edit-links.txt)).
- **A folder's index page needs `slug: index`** to keep `…/index.html`.

### Grid

| Variant | http-routing | troubleshooting | enabling-tcp-routing | routes-domains |
|---|---|---|---|---|
| split-passthrough | 12/12 | 12/12 | 7/7 | 8/8 |
| split-native | 12/12 | 12/12 | 7/7 | 8/8 |
| mono-passthrough | 12/12 | 12/12 | 7/7 | 8/8 |
| mono-native | 12/12 | 12/12 | 7/7 | 8/8 |
| split-filelinks | 5/12 | 7/12 | 2/7 | 6/8 |
| default-passthrough | 3/12 | 7/12 | 1/7 | 2/8 |

Links as expected; every outline is the same as the published page's.

## Zensical 0.0.69

Site: [sites/zensical/](sites/zensical/) — conventions:
[CONVENTIONS.md](sites/zensical/CONVENTIONS.md).

### Summary

- **One docs folder.** Separate repositories can only be folders inside it.
  A submodule checked out there builds like any folder; a folder that is a
  symbolic link is not built at all (`linked-native`: no test page), so
  docs-bosh's way of mounting the bpm-release docs would not carry over.
- **`.md` file links are native and checked**: a missing page or anchor is
  a warning with file, line and column, and `--strict` stops the build
  ([probe](results/zensical-probe-broken.txt)). `.html` links are neither
  rewritten nor checked.
- **Passthrough builds unchanged**, 39 of 39, with `use_directory_urls =
  false`. With the default, Zensical moves relative URLs one folder
  deeper and 15 of 39 links are as expected.
- **Template variables and includes are text**: a file link held in a
  variable or a partial is read from the including page, so it works at
  one depth only ([probe](results/zensical-probe-depth.txt)).
- **One edit link base** for the site.

### Grid

| Variant | http-routing | troubleshooting | enabling-tcp-routing | routes-domains |
|---|---|---|---|---|
| mono-passthrough | 12/12 | 12/12 | 7/7 | 8/8 |
| mono-native | 12/12 | 12/12 | 7/7 | 8/8 |
| linked-native | not built | not built | not built | not built |
| default-passthrough | 4/12 | 7/12 | 2/7 | 2/8 |

## Starlight 0.42.6

Site: [sites/starlight/](sites/starlight/) — conventions:
[CONVENTIONS.md](sites/starlight/CONVENTIONS.md).

### Summary

- **One collection; folders checked out or linked into it both build.**
  `linked-native` passes every check ([check](results/starlight-check.txt)).
- **Links are URLs only.** The native form is the root-relative URL
  Starlight writes itself, `/adminguide/x.html`, which works at any depth.
- **A folder's index page is `<folder>.html`**, with `format: 'file'` and
  `'preserve'` alike, so passthrough's two links to `…/index.html` break
  (37 of 39) and the old URLs need redirects.
- **No link checking at build time**: missing pages and anchors build
  silently ([probe](results/starlight-probe-broken.txt)).
- **One edit link base**, with a per-page `editUrl` override.

### Grid

| Variant | http-routing | troubleshooting | enabling-tcp-routing | routes-domains |
|---|---|---|---|---|
| mono-passthrough | 11/12 | 12/12 | 6/7 | 8/8 |
| mono-native | 12/12 | 12/12 | 7/7 | 8/8 |
| linked-native | 12/12 | 12/12 | 7/7 | 8/8 |
| default-passthrough | 3/12 | 7/12 | 1/7 | 2/8 |

## Antora 3.2.1

Site: [sites/antora/](sites/antora/) — conventions:
[CONVENTIONS.md](sites/antora/CONVENTIONS.md).

### Summary

- **Both layouts are Antora's own concepts.** Separate repositories are components,
  one per URL directory; one repository is the `ROOT` component with a
  module per directory. The URLs are the same, and the xrefs differ only in
  `::` against `:` ([check](results/antora-check.txt)).
- **`xref:` is the cross-source reference**: named by component or module
  and path, resolved by Antora on whatever page renders it, attributes and
  partials included ([depth probe](results/antora-probe-depth.txt)).
- **A missing xref target is an error with the page**, but the build exits
  0 unless a failure level is set; fragments of xrefs are never checked
  ([probe](results/antora-probe-broken.txt)).
- **Each content source has its own edit link**
  ([edit links](results/edit-links.txt)).
- **`page-aliases` makes old URLs, across components too**, as static
  redirect pages or server rules
  ([probe](results/antora-probe-redirects.txt)).

### Grid

| Variant | http-routing | troubleshooting | enabling-tcp-routing | routes-domains |
|---|---|---|---|---|
| split-passthrough | 12/12 | 12/12 | 7/7 | 8/8 |
| split-native | 12/12 | 12/12 | 7/7 | 8/8 |
| mono-passthrough | 12/12 | 12/12 | 7/7 | 8/8 |
| mono-native | 12/12 | 12/12 | 7/7 | 8/8 |
| default-passthrough | 3/12 | 7/12 | 1/7 | 2/8 |

## Across tools

### Separate sources or one repository

The RFC puts all content into "ONE single documentation repository"
([L69]); under [R-15](../../requirements/README.md#r-15) URL identifies the
source, its directories keep the book's `config.yml` mapping. Both layouts were built
in every tool:

- **Every tool gives the same URLs in both layouts**, so the choice does
  not change any published link.
- **What a layout of separate repositories means differs.** Antora reads
  each repository as a content source, at its own branch, with its own edit
  link. Docusaurus needs each repository's files in the site's folder (a
  submodule or a checkout by the build), one plugin instance each.
  Zensical and Starlight read one folder: other repositories are folders
  checked out into it; Starlight also builds linked folders, Zensical does
  not.
- **The native link changes with the layout only in Docusaurus and
  Antora.** Docusaurus's file links stop at an instance's edge, so links to
  other repositories become URLs; Antora's xrefs name a component instead
  of a module. In Zensical and Starlight nothing changes.
- **One repository gives every tool a single edit base, which is then the
  right one**; separate repositories need per-source edit links, which
  Docusaurus and Antora give and Zensical cannot (Starlight only per page).

Decision (Docs WG lead, 2026-10-11): **keep separate content
repositories**, which differs from the RFC's [L69]. Access in the
`cloudfoundry` organization is granted per repository: each Working
Group area's approvers get "Write access for all repos in the area"
([RFC-0014 L39](https://github.com/cloudfoundry/community/blob/9f189bfa613bb7a9c2da6616666661790d4410eb/toc/rfc/rfc-0014-github-teams-and-access.md#L39)).
In one repository every team named in `CODEOWNERS` needs write access to
all of it, so merge and push rights are no longer per area, and a
`CODEOWNERS` line is satisfied by any one of its owners, so it cannot
require both the area's Working Group and the Docs WG. Review by path
does still work: the generated branch protection sets
`require_code_owner_reviews: true`
([orgs/readme.md L59](https://github.com/cloudfoundry/community/blob/9f189bfa613bb7a9c2da6616666661790d4410eb/orgs/readme.md#L59)).
Today all 15 docs repositories are one area of the Docs WG
([docs.md L38-L60](https://github.com/cloudfoundry/community/blob/9f189bfa613bb7a9c2da6616666661790d4410eb/toc/working-groups/docs.md#L38-L60)).
How the site collects the repositories, Git submodules pinned by the
site's repository or a checkout at build as Bookbinder does today, is
decided later. Submodules are real folders, so each tool reads them as it
reads one repository.

### URLs and old URLs

- **Every tool can publish the book's `<path>.html` URLs**, so no page
  needs a redirect for that. Docusaurus links to its pages without the
  extension, and GitHub Pages serves `/x` from `x.html`
  ([spot check of this repository's site](survey/spot-check.txt)).
- **Folder index pages are the exception.** The book has 135 internal links
  to them ([survey](survey/README.md#findings)). Zensical and Antora keep
  `<folder>/index.html`; Docusaurus does with `slug: index`; Starlight
  publishes `<folder>.html`. The book also publishes the folder form
  (`/concepts/architecture/`), which a static host serves from
  `<folder>/index.html` where that file exists.
- **Redirects on a static host are pages.** Every tool writes an HTML page
  with a meta refresh at the old path; no setting for HTTP redirects on
  GitHub Pages was found (unverified). Docusaurus's and Zensical's pages also run a script that keeps
  the old URL's fragment; Antora's script drops it; Starlight's page has no
  script ([redirect probes](results/)). Docusaurus writes its redirect at
  `<old>/index.html`, so an old `….html` URL is not covered.
- **The book's 85 redirect rules** need moving too: 40 lead to a page, 30
  to a page that no longer exists, 3 to another redirect, 12 off the site,
  and one can never match ([survey](survey/README.md#findings)).
  The live ones fall under [R-16](../../requirements/README.md#r-16) old URLs
  keep working.

### What a link looks like after conversion

The same link, from `enabling-tcp-routing` (docs-cf-admin) to an id on
`routes-domains` (docs-dev-guide), in each tool's native form:

```erb
[Create a Route](../devguide/deploy-apps/routes-domains.html#create-route)
```

```mdx
[Create a Route](../devguide/deploy-apps/routes-domains.mdx#create-route)   (mono)
[Create a Route](/devguide/deploy-apps/routes-domains#create-route)         (split)
```

```markdown
[Create a Route](../devguide/deploy-apps/routes-domains.md#create-route)
```

```markdown
[Create a Route](/devguide/deploy-apps/routes-domains.html#create-route)
```

```asciidoc
xref:devguide::deploy-apps/routes-domains.adoc#create-route[Create a Route]   (split)
xref:devguide:deploy-apps/routes-domains.adoc#create-route[Create a Route]    (mono)
```

Docusaurus (mono), Zensical and Antora name the target's source file, so
the build can find it and report it when it is gone
([R-11](../../requirements/README.md#r-11) readable source). Starlight and
Docusaurus (split) name a URL.

### What the build reports

| | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| missing page, native | broken link | warning, file:line | — | ERROR, page |
| missing anchor, native | broken anchor | warning, file:line | — | — |
| missing page, passthrough | broken link | — | — | — |
| missing anchor, passthrough | broken link | — | — | — |
| in-page id missing | broken anchor | warning, file:line | — | INFO, at `--log-level=info` |
| the build fails | `onBrokenLinks: 'throw'` (default) | `--strict` | — | `--log-failure-level` (exit 2) |

From the [broken-link probes](results/). Of the five links already broken
in the test pages, native builds report all five in Docusaurus and
Zensical, and the three in-page ones in Antora at the info level.

### Links in variables and partials

Two earlier rounds left this open: values with page-relative links work only
at their page's depth ([variables round](../variables/results.md#not-yet-written)),
and relative links inside a partial resolve against the including page
([partials round](../partials/results.md#not-yet-written)). The depth probe
put each link form in a variable and in a partial, on a page one folder
deep and on one two folders deep:

| Form | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| relative URL, in a variable | one depth | one depth | one depth | one depth |
| relative URL, in a partial | one depth | one depth | one depth | one depth |
| root-relative URL, either | any depth | any depth | any depth | any depth |
| the tool's own form, in a variable | `<Link to>`: any depth | file path: one depth | root URL: any depth | `xref:`: any depth |
| the tool's own form, in a partial | file path: any depth | file path: one depth | root URL: any depth | `xref:`: any depth |

So the book's behaviour carries over to every tool for relative links, and
the book's two variables for one link (`port_limitations`,
`port_limitations_1`) exist for that reason. Root-relative links, Antora
xrefs, and Docusaurus file links in a partial remove the dependence on
depth ([probes](results/)).

### The published pages

The links check on the four published pages, placed at their paths, finds
the same five broken ids the book's source has, plus one outside the
excerpt (`#create-route-w-port`), and shows the book's forms: of the links
between site pages, 26 are root-relative, 5 page-relative (all HTML links)
and 3 absolute ([published check](results/published-check.txt)). The 4
links to `/cdn-cgi/l/email-protection` on `routes-domains` are Cloudflare's
([survey](survey/README.md#method)).

## Conventions to record

For `cf-docs-migrate convert`. Decisions of this round, for review:

1. **Pages are published at the book's URLs, `<directory>/<path>.html`**:
   `trailingSlash: false` (Docusaurus), `use_directory_urls = false`
   (Zensical), `build.format: 'file'` (Starlight), `html_extension_style:
   default` (Antora). A folder's `index` page keeps `<folder>/index.html`
   where the tool allows (Docusaurus `slug: index`); in Starlight its old
   URL gets a redirect. **Accepted** (Docs WG lead, 2026-10-11).
2. **Each content repository keeps its URL directory as a top-level
   folder** (one repository) or as its component, instance or folder name
   (separate repositories), as the book's `config.yml` maps it
   ([R-15](../../requirements/README.md#r-15) URL identifies the source).
   **Accepted** (Docs WG lead, 2026-10-11), with separate repositories
   ([decision](#separate-sources-or-one-repository)).
3. **Internal links are converted to the tool's own form**: file paths
   (Docusaurus within one instance, Zensical), `xref:` (Antora), the
   root-relative URL the tool writes (Starlight, and Docusaurus across
   instances). This applies to page-relative, root-relative and absolute
   `docs.cloudfoundry.org` links alike, and to HTML `<a>` links to site
   pages.
4. **A link inside a variable's value or a partial uses a form that does
   not depend on the including page**: root-relative URL, `xref:`, or (in a
   Docusaurus partial) a file path. Values written for one depth, such as
   `port_limitations` and `port_limitations_1`, become one.
5. **Links already broken in the book are listed and fixed at the source**,
   not changed silently by the converter; the list starts with the 55 in
   the [survey](survey/links.csv) (status `broken`). **Accepted**
   (Docs WG lead, 2026-10-11): fixed at the source before conversion
   ([R-24](../../requirements/README.md#r-24) markup cleanup before
   conversion), and merged into the headings round's
   [broken-links.md](../headings/broken-links.md#found-by-the-cross-repository-links-survey-2026-10-11) list.
6. **The build checks internal links and anchors and fails on them in pull
   requests**: `onBrokenLinks` and `onBrokenAnchors: 'throw'` (Docusaurus),
   `--strict` (Zensical), `--log-failure-level=error` (Antora, which still
   does not check anchors in xrefs), and a link checker such as this
   round's [links.py](checks/links.py) run over the built site for what a
   tool does not check (Starlight entirely; anchors in Antora).
   **Accepted** (Docs WG lead, 2026-10-11).
7. **Every old URL that `redirects.rb` still serves gets the tool's redirect
   page**, and old URLs whose target is gone are listed for a decision
   ([R-16](../../requirements/README.md#r-16) old URLs keep working).
   Decided (Docs WG lead,
   2026-10-11): the 30 rules whose target is gone are dropped or
   retargeted in the cleanup before conversion; they are listed in
   [broken-links.md](../headings/broken-links.md#found-by-the-cross-repository-links-survey-2026-10-11).
8. **Each page's edit link names its own repository and file**: an
   `editUrl` function (Docusaurus), `edit_url` per content source
   (Antora), `editUrl` front matter written by the converter (Starlight).
   **Accepted** (Docs WG lead, 2026-10-11), with separate repositories.
   Zensical cannot meet it as tested: `repo_url` and `edit_uri` are site
   settings, so every edit link points into one repository
   ([Zensical conventions](sites/zensical/CONVENTIONS.md)).
9. **The links check runs on every converted page**, beside the outline
   check: [checks/links.py](checks/links.py).

## Requirements

- [R-08](../../requirements/README.md#r-08) cross-repository links: every
  tool keeps every link of the test pages working across repositories, in
  both layouts it supports, once pages are published at the book's URLs.
  The forms that keep working when content moves between depths are
  root-relative URLs and each tool's own reference.
- [R-15](../../requirements/README.md#r-15) URL identifies the source: in
  every tool and layout the URL directory can stay the repository's
  `config.yml` directory. An edit link per repository is possible in
  Docusaurus and Antora; in Starlight only per page; in Zensical not with
  separate repositories.
- [R-16](../../requirements/README.md#r-16) old URLs keep working: every
  tool can keep the `.html` URLs, so redirects are needed only for the
  book's existing rules and, in Starlight, for folder index pages. On a
  static host a redirect is a page; anchors survive it only through
  Docusaurus's and Zensical's scripts.
- [R-01](../../requirements/README.md#r-01) content and outline survive:
  every outline passes; each link's target and anchor is checked.
- [R-23](../../requirements/README.md#r-23) one central conversion: the
  conversion of links is mechanical once the target of each link is known,
  which needs the whole book's model at once (as the survey builds it),
  not one repository at a time. The RFC's condition, "as long as
  cross-repository links are preserved" ([L131]), is checkable with the
  links check.

## Not yet written

- **The whole book.** Four pages and stubs were converted; the survey
  covers every link, but the conversion was not run on all 2,892.
- **Links in the subnav and the book's home page** (264 and 221
  root-relative links) were counted, not converted; navigation is another
  concept.
- **Images** (153 relative image links) were counted, not converted.
- **bosh.io's links into the bpm-release submodule** (13) were not
  resolved; the submodule was not fetched.
- **Git submodules and a checkout at build**, the two ways to collect
  separate repositories ([decision](#separate-sources-or-one-repository)),
  were not built; the split layout read local folders.
- **Starlight's `starlight-links-validator`** and Docusaurus's file links
  to another instance by `@site/` path were not tried.
- **A browser check** of the redirect pages (that a reader lands on the
  target, with or without the fragment) was not run; the probes read the
  pages' HTML.
- **The publishing pipeline's handling of Bookbinder's link-check status**
  was not found in public sources.
- **Probes and on-paper tools.** Eleventy, Sphinx/MyST, Middleman, Hugo
  and VitePress were not part of this round.

[L69]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L69
[L131]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L131
