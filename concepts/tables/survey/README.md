# Table style survey

Status: draft, incomplete — covers what is known as of 2026-10-10.

This survey counts every table in the Cloud Foundry documentation and
tutorial repositories and groups the tables by what they hold. It was done
on 2026-10-09 to find which table styles the site template needs beyond the
standard one ([R-09](../../../requirements/README.md#r-09) table styles by
class). On the way it found markup defects that a conversion has to clean up
([R-24](../../../requirements/README.md#r-24) markup cleanup before
conversion).

Decision (evaluation, 2026-10-09): `class="table"` is the standard style,
the one most tables use. Further style classes (a style class is a name the
site's stylesheet gives a look to; [glossary](../../../glossary.md#style-class))
are chosen from what the docs repositories contain. The candidate names at
the start were compact, boxed, plain and striped.

| File | What it is |
|---|---|
| [tables.csv](tables.csv) | The data: one row per table, 238 rows, each with a GitHub link to the table at the surveyed commit |
| [shas.txt](shas.txt) | The 21 repositories and the commit surveyed in each |
| [survey.py](survey.py) | Finds and measures the tables in a set of clones |
| [families.py](families.py) | Sorts the tables into families and prints a summary |
| [bosh_tables.py](bosh_tables.py) | Extra measurements for the bosh.io tables and its Markdown |

## Scope

**Repositories.** All 15 `cloudfoundry/docs-*` repositories that are not
archived, plus the tutorial repositories, cloned from their default branch on
2026-10-09. Two `docs-*` repositories are archived and were skipped:
[docs-cfcr](https://github.com/cloudfoundry/docs-cfcr) and
[docs-routing](https://github.com/cloudfoundry/docs-routing). The
`cloudfoundry-tutorials` organization is archived as a whole; its four
repositories were cloned anyway.

| Repository | Commit (date) | Tables |
|---|---|---|
| cloudfoundry/docs-bbr | [`5146595`](https://github.com/cloudfoundry/docs-bbr/tree/51465950ce3a2196d66a9339086b94feed280c3e) (2026-07-09) | 2 |
| cloudfoundry/docs-book-cloudfoundry | [`30dfa57`](https://github.com/cloudfoundry/docs-book-cloudfoundry/tree/30dfa57692253a6ae1b3df0726444b1e32852c91) (2026-10-08) | 0 |
| cloudfoundry/docs-bosh | [`20a4122`](https://github.com/cloudfoundry/docs-bosh/tree/20a41223a7ba87700424634c42e94a22a669b45e) (2026-10-01) | 40 |
| cloudfoundry/docs-buildpacks | [`239e5c8`](https://github.com/cloudfoundry/docs-buildpacks/tree/239e5c8676200914c4d386970f9989e46de9e969) (2026-10-09) | 15 |
| cloudfoundry/docs-cf-admin | [`13826fa`](https://github.com/cloudfoundry/docs-cf-admin/tree/13826fa7d93eee66902c4a2187a96b884137b58a) (2026-07-22) | 31 |
| cloudfoundry/docs-cf-cli | [`ee9aad5`](https://github.com/cloudfoundry/docs-cf-cli/tree/ee9aad56524157ae2316c00149b75737439235dc) (2026-07-22) | 1 |
| cloudfoundry/docs-cloudfoundry-concepts | [`97e0d0b`](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/tree/97e0d0b25f059c06edd25e30355d26eb93dc560a) (2026-09-14) | 37 |
| cloudfoundry/docs-credhub | [`21b0448`](https://github.com/cloudfoundry/docs-credhub/tree/21b0448736435cec0f5a1491e0b40bda9c4307eb) (2026-07-23) | 1 |
| cloudfoundry/docs-deploying-cf | [`1113cfa`](https://github.com/cloudfoundry/docs-deploying-cf/tree/1113cfaf3626931c653c91dc8d537d7f181d6762) (2026-07-24) | 4 |
| cloudfoundry/docs-dev-guide | [`9c8df63`](https://github.com/cloudfoundry/docs-dev-guide/tree/9c8df63eb3823011e4e3aff9958c36e25d5190b7) (2026-09-28) | 42 |
| cloudfoundry/docs-dotnet-core-tutorial | [`6e83c73`](https://github.com/cloudfoundry/docs-dotnet-core-tutorial/tree/6e83c738187380d3fc02697892e0c7c9d806e01c) (2020-08-03) | 0 |
| cloudfoundry/docs-loggregator | [`8e027ba`](https://github.com/cloudfoundry/docs-loggregator/tree/8e027bac1099b737afe56afa1606b4fcf9d06c94) (2026-07-22) | 9 |
| cloudfoundry/docs-running-cf | [`956acc8`](https://github.com/cloudfoundry/docs-running-cf/tree/956acc86445d2f3cb29f031294f86f37f515b471) (2026-08-05) | 37 |
| cloudfoundry/docs-services | [`ccb0036`](https://github.com/cloudfoundry/docs-services/tree/ccb0036407e4c2eabbb61a3b3de008f821f41c5b) (2026-07-22) | 5 |
| cloudfoundry/docs-uaa | [`216c797`](https://github.com/cloudfoundry/docs-uaa/tree/216c797cfa1a971cf0f9e53eb3e4803aaf914a94) (2026-07-22) | 11 |
| cloudfoundry/tutorials | [`e41b9de`](https://github.com/cloudfoundry/tutorials/tree/e41b9de661f8bd7858f663e8d983680f1f3f8fc7) (2024-01-06) | 0 |
| cloudfoundry/what-is-cf | [`9b48cc7`](https://github.com/cloudfoundry/what-is-cf/tree/9b48cc72c8e3f0e4483087863b574e9e0526e710) (2023-10-03) | 0 |
| cloudfoundry-tutorials/cf-and-k8s | [`9df120b`](https://github.com/cloudfoundry-tutorials/cf-and-k8s/tree/9df120be20e6af6a1a6ee909186fbd79ce01067a) (2020-04-13) | 1 |
| cloudfoundry-tutorials/cf4k8s-do | [`32e6e8c`](https://github.com/cloudfoundry-tutorials/cf4k8s-do/tree/32e6e8c598328d007bbae274a3f42ff5208d7d20) (2020-11-02) | 0 |
| cloudfoundry-tutorials/cf4k8s-gke | [`b7fba34`](https://github.com/cloudfoundry-tutorials/cf4k8s-gke/tree/b7fba34fbba305f1f89a24570cc946e4922a58e8) (2020-10-20) | 0 |
| cloudfoundry-tutorials/trycf | [`7f7e44f`](https://github.com/cloudfoundry-tutorials/trycf/tree/7f7e44f9df195972bd617a7546f46ae58be6ae3b) (2020-12-15) | 2 |

The date is the commit's date. In `shas.txt` a `cft-` prefix marks a
`cloudfoundry-tutorials` repository.

- **The book.** "The book" is the set of repositories that Bookbinder, the
  tool that builds docs.cloudfoundry.org today, collects into one site
  ([glossary](../../../glossary.md#bookbinder)). `docs-book-cloudfoundry`
  holds its layout and settings and has no tables.
- **bosh.io is counted apart.** `docs-bosh` is not part of the book. It
  builds bosh.io/docs with MkDocs and the Material theme
  ([glossary](../../../glossary.md#mkdocs-material);
  [`mkdocs.yml`](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/mkdocs.yml#L319-L321)),
  a different site with a different look. Its tables are in the totals,
  but reported in their own row and in [bosh.io](#boshio) below.
- **File types.** `.md`, `.erb`, `.html`, `.haml`, `.markdown`, `.mdx` and
  `.adoc`. Folders named `.git`, `node_modules` and `vendor` are skipped.
  Markdown files at a repository's root (contributor notes, READMEs) are
  left out on purpose: no site publishes them.
- **Source, not published pages.** The survey reads the files in the
  repositories. A partial (a file included into other pages;
  [glossary](../../../glossary.md#partial)) counts once, however many pages
  include it, and a file that no page links to still counts.

## Method

[survey.py](survey.py) reads every file of those types and finds two kinds
of table:

- **HTML tables:** every `<table>` up to its closing `</table>`, with tables
  inside tables handled. Each is parsed with Python's standard HTML parser,
  which, like a browser, tolerates unclosed tags.
- **Pipe tables:** the Markdown table syntax, a header line followed by a
  delimiter line such as `---|---`, one row per line, `|` between cells
  ([glossary](../../../glossary.md#pipe-table)). Lines inside fenced code
  blocks are skipped. The script also looks next to each pipe table for a
  kramdown attribute list (`{: .class }`, the way kramdown, the book's
  Markdown parser, attaches a class to a block;
  [glossary](../../../glossary.md#kramdown)).

For each table it records, among other things: the `class` exactly as
written, column widths from `<col>`, width, style or alignment set on cells,
the number of rows and columns, whether there is a header row, row headers
(a `<th>` that starts a body row), a spanning title row (a first row with one
cell spanning every column), what the cells hold (code, lists, paragraphs,
line breaks, images, links, bold, italic), cell lengths, ERB tags (`<%`,
the template syntax the book uses for variables and partials;
[glossary](../../../glossary.md#erb)), and a `<thead>` that is never closed.
Every row of [tables.csv](tables.csv) has a link to the table's first line
at the surveyed commit.

[families.py](families.py) then puts each table in one family. The rules
are applied in this order, and the first that matches wins:

1. **media**: an image in a cell;
2. **matrix**: 4 or more columns and a median cell of 5 characters or
   fewer (the median cell is the middle value of the table's cell lengths
   in characters; HTML cells are measured as text, pipe cells as written);
3. **titled**: a spanning title row;
4. **key-value**: 2 columns;
5. **reference-3-4**: 3 or 4 columns;
6. **wide**: 5 or more columns.

The families come from the data, not from a list of style names.

## Totals

| | HTML | Pipe | All |
|---|---|---|---|
| Book repositories (docs.cloudfoundry.org) | 123 | 72 | 195 |
| bosh.io (`docs-bosh`) | 0 | 40 | 40 |
| Tutorial repositories | 0 | 3 | 3 |
| **All** | **123** | **115** | **238** |

**Classes.** Of the 123 HTML tables, 70 have `class="table"`, 8 have
`class=“table”` with typographic quotes (so the browser does not read
`table` as the class), 1 has `class="table'` with mismatched quotes, and 44
have no class. No other class appears anywhere. No pipe table has a class:
there are no kramdown attribute lists next to tables.

**Traits across all 238 tables.**

- Every table has a header row; none is used for page layout. No table sits
  inside another.
- 33 tables set a width, style or alignment on cells (`width="20%"` on
  `<th>` and similar); one `docs-cf-cli` table accounts for 31 such cells.
  One table sets widths with `<col>` (`_oss_scale_table`, a test page).
- 3 tables have row headers; 2 have a spanning title row (both on the
  `metadata` test page).
- 44 tables contain ERB tags, such as `<%= vars.name %>` variables.
- 1 table has `border="1"`, which the published site's stylesheet makes
  redundant.

**Markup defects** that browsers repair without a sign and strict tools do
not ([glossary](../../../glossary.md#well-formed-markup)):

- 5 tables never close `<thead>`, so a browser puts every row in the header:
  `_suspended_org_roles_table` and `_suspended_space_roles_table` in
  `docs-cloudfoundry-concepts`, and 3 in `_c2c_oss_overlay` in
  `docs-dev-guide`;
- 8 classes in typographic quotes and 1 with mismatched quotes (above).

Correction (2026-10-09): an earlier note listed `uaa-performance` cells
ending in `</td` without `>`. That defect does not exist; at commit
`956acc8` every one of the page's twelve tables closes its cells. The page's
real cleanup item is its headings, written `###<a id=…>` with no space
after `###`.

## Families

| Family | Count | HTML / pipe | Typical | Repositories with most |
|---|---|---|---|---|
| key-value | 126 | 51 / 75 | 2 columns, median 4 body rows (max 47), median cell 21 characters; code in 72 | dev-guide 26, running-cf 22, bosh 21, concepts 19 |
| reference-3-4 | 77 | 49 / 28 | median 4 body rows (max 59), median cell 16 characters | cf-admin 16, bosh 14, concepts 14, dev-guide 14 |
| media | 12 | 12 / 0 | 3–5 columns of chart thumbnails linked to full images | running-cf only (`uaa-performance`) |
| matrix | 11 | 5 / 6 | 4–12 columns of Yes/blank, numbers or short tokens | concepts 3, bosh 2, cf-admin 2, dev-guide 2 |
| wide | 10 | 4 / 6 | 5–6 columns of text | bosh 3, cf-admin 3, uaa 3 |
| titled | 2 | 2 / 0 | title in a spanning first row | cf-admin only (`metadata`) |

**Long reference tables** cut across the families: 14 key-value and
reference-3-4 tables have 15 or more body rows. The metrics partials in
`docs-running-cf` reach 41–59 rows; others are `docs-cf-cli` `v8` (30),
`docs-uaa` `uaa-deploy` (33) and the concepts `glossary` (16). Tables of
short cells (median 12 characters or fewer) are 29 of the key-value and 24
of the reference-3-4 tables.

Decision (evaluation, tables round): a table title is a bold line above the
table, not a row, so the titled family needs no style of its own
([template conventions](../README.md#template-conventions)).

### Examples

Links go to the table at the surveyed commit.

- **key-value:** [credhub `credential-types` L17](https://github.com/cloudfoundry/docs-credhub/blob/21b0448736435cec0f5a1491e0b40bda9c4307eb/credential-types.html.md.erb#L17),
  [dev-guide `using-tasks` L165](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/using-tasks.html.md.erb#L165),
  [dev-guide `environment-variable` L255](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/environment-variable.html.md.erb#L255) (21 body rows)
- **reference-3-4:** [cf-admin `metadata` L370](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/metadata.html.md.erb#L370),
  [loggregator `data-sources` L117](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/data-sources.html.md.erb#L117)
- **Long reference:** [running-cf `metrics/_cloud_controller` L10](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/metrics/_cloud_controller.html.md.erb#L10) (59 body rows),
  [running-cf `metrics/_diego` L35](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/metrics/_diego.html.md.erb#L35) (47),
  [cf-cli `v8` L74](https://github.com/cloudfoundry/docs-cf-cli/blob/ee9aad56524157ae2316c00149b75737439235dc/v8.html.md.erb#L74) (30)
- **matrix:** [concepts `_oss_roles_table` L1](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/_oss_roles_table.html.md.erb#L1) (12 columns × 42 body rows, Yes/blank),
  [dev-guide `environment-variable` L86](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/environment-variable.html.md.erb#L86) (variable × Running/Staging/Task),
  [cf-admin `managing-stacks` L28](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/managing-stacks.html.md.erb#L28)
- **media:** [running-cf `uaa-performance` L88](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/uaa-performance.html.md.erb#L88)
  (12 such tables on one page)
- **wide:** [uaa `uaa-metrics` L37](https://github.com/cloudfoundry/docs-uaa/blob/216c797cfa1a971cf0f9e53eb3e4803aaf914a94/uaa-metrics.html.md.erb#L37),
  [cf-admin `troubleshooting-router-error-responses` L314](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb#L314)
- **titled:** [cf-admin `metadata` L56](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/metadata.html.md.erb#L56)

### How the book renders them today

Every table on docs.cloudfoundry.org looks the same, whatever its family
or class. The site's stylesheet
([`/stylesheets/all.css`](https://docs.cloudfoundry.org/stylesheets/all.css),
as served on 2026-10-10; not pinned, as it is a built file) has one table
style and no rule for any table class: tables are full width with a 1-pixel
border, header cells are shaded (`#f8f8f8`), every cell is boxed
(`.content td, .content th, .content tr { border: solid 1px grey }`), and a
row changes color on hover. The stylesheet has a striping rule, but it
applies only under a `has-sidenav` class that no checked page carries
(`adminguide/metadata.html`), so no table is striped.

### What the families say about the candidate names

The evaluation's reading of the data, not a decision:

- **compact:** the 11 matrix tables and the 14 long reference tables are
  the ones a denser style would help. The candidate with the most evidence.
- **striped:** no source asks for it and the published site does not
  stripe. If wanted, it is for the long and matrix tables.
- **boxed:** every published table is already boxed. A trait of today's
  standard style, not a family.
- **plain:** no table lacks a header row and none is used for layout. The
  nearest case is the media family, which may want a borderless grid. The
  tables round added `table-media` for it as the example of a second style
  ([template conventions](../README.md#template-conventions)).

Which styles to offer is open; see
[Research areas](../../../requirements/research-areas.md#which-table-styles-beyond-the-standard-one).

## bosh.io

bosh.io/docs is built from `docs-bosh` with MkDocs and Material for MkDocs
(MkDocs is a Python static site generator, and Material a theme for it;
[glossary](../../../glossary.md#mkdocs-material)), in the
`squidfunk/mkdocs-material:9.7.6` image
([build task](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/ci/tasks/build.yml#L5-L12),
[`mkdocs.yml`](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/mkdocs.yml#L319-L321)).
Everything below was read at commit `20a4122`, not built.

Last checked 2026-10-10: repository `cloudfoundry/docs-bosh`, branch
`master`, commit `20a41223a7ba87700424634c42e94a22a669b45e`. The 40 tables
and their families, the absence of alignment colons and `\|` escapes, and
the 302 admonitions, 809 heading ids and 221 indented code blocks all match.
The indented code blocks are on 48 pages, not 49 as first counted: one page
closes an unindented block with an indented fence.

**The 40 tables.** All are pipe tables with a header row, in families
key-value 21, reference-3-4 14, wide 3 and matrix 2 (from
[tables.csv](tables.csv)). [bosh_tables.py](bosh_tables.py) `tables` found
no alignment colons, no `\|` escapes, no attribute lists, no images and no
title line. Nineteen are the same four small tables (concept mapping,
network type support, encryption, other features) repeated on the five
provider pages `aws`, `azure`, `google`, `openstack` and `vsphere`.

**The Markdown around them.** [bosh_tables.py](bosh_tables.py)
`constructs` counted, outside code blocks: 302 admonitions (boxed callouts
headed Note, Warning, and so on, written `!!! note`;
[glossary](../../../glossary.md#admonition)) on 128 pages, 809 heading ids
written `{: #id }` on 114 pages, and 221 fenced code blocks indented inside
a list or an admonition on 48 pages. The `content/bpm` folder is a link into
another repository and was not counted.

<details><summary>All 40 tables (T1–T40)</summary>

| # | Source | Columns | Body rows | Family | Holds | What matters for conversion |
|---|---|---|---|---|---|---|
| T1 | [resolute-release-migration.md L265](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/resolute-release-migration.md#L265) | 2 | 7 | key-value | Noble library → Resolute replacement | code spans; prose in col 2 (89 chars) |
| T2 | [networks.md L16](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/networks.md#L16) | 4 | 2 | reference-3-4 | IP assignment × network type | empty corner cell; row headers |
| T3 | [networks.md L489](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/networks.md#L489) | 4 | 4 | reference-3-4 | networks per instance, IaaS × network type | `<br>` in 2 header cells; bold col 1; `<sup>1</sup>` note marker, note as a `1:` line under the table; `-` for none |
| T4 | [networks.md L500](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/networks.md#L500) | 4 | 11 | matrix | advanced network features, IaaS × type × feature | blank col-1 cells = same IaaS as above; 3 blank spacer rows between groups; `<sup>1/2</sup>` markers with `1:`/`2:` lines below; `—` for none; 16 empty body cells |
| T5 | [init-alicloud.md L86](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/init-alicloud.md#L86) | 4 | 5 | reference-3-4 | security group rules | in a numbered-list step, after an admonition (4-space indent) |
| T6 | [vsphere.md L30](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/vsphere.md#L30) | 2 | 6 | key-value | BOSH concept → vSphere | 6 reference-style links |
| T7 | [vsphere.md L54](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/vsphere.md#L54) | 2 | 3 | key-value | vSphere network type support | — |
| T8 | [vsphere.md L70](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/vsphere.md#L70) | 2 | 3 | key-value | vSphere disk encryption | — |
| T9 | [vsphere.md L78](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/vsphere.md#L78) | 2 | 3 | key-value | vSphere misc. features | reference link |
| T10 | [init-openstack.md L103](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/init-openstack.md#L103) | 6 | 6 | wide | OpenStack security group rules | 6 columns; in a list step after an admonition; 2 empty cells; ports and CIDRs |
| T11 | [azure-compute-gallery.md L19](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/azure-compute-gallery.md#L19) | 4 | 2 | reference-3-4 | Azure roles for the CPI | every header cell bolded; bold + italic lead-ins; long code token (49 chars); 3 reference links |
| T12 | [init-aws.md L114](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/init-aws.md#L114) | 4 | 5 | reference-3-4 | AWS security group rules | in a list step after an admonition |
| T13 | [cli-ops-files.md L349](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/cli-ops-files.md#L349) | 2 | 3 | key-value | ops-file escape sequences | all cells code |
| T14 | [cpi-api-v2.md L50](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/cpi-api-v2.md#L50) | 5 | 8 | matrix | Director/CPI/stemcell version matrix | one row fully bold (the case that matters); numeric 1/2 cells; `*full agent settings**` renders as italic with a stray `*` (marker for a `\*` note under the table) |
| T15 | [prefix-delegation-networks.md L12](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/prefix-delegation-networks.md#L12) | 3 | 1 | reference-3-4 | prefix delegation support | one body row |
| T16 | [cli-v2-diff.md L27](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/cli-v2-diff.md#L27) | 2 | 14 | key-value | v1 → v2 CLI commands | commands not in code spans; `<manifest>` and `<ip>` are read as HTML tags and vanish on the live page; dangling `[3]` |
| T17 | [director-api-v1.md L46](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/director-api-v1.md#L46) | 2 | 3 | key-value | HTTP verbs | — |
| T18 | [director-tasks.md L34](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/director-tasks.md#L34) | 6 | 2 | wide | sample `bosh tasks` output | 6 columns; CLI output as a table; empty Result column |
| T19 | [git-lfs-release-blobstore.md L34](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/git-lfs-release-blobstore.md#L34) | 4 | 6 | reference-3-4 | Git LFS vs S3 decision matrix | `✓` and `-` cells; prose Rationale column |
| T20 | [links.md L527](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/links.md#L527) | 4 | 4 | reference-3-4 | link provider conflicts | 19 code spans; long Example column |
| T21 | [links.md L553](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/links.md#L553) | 3 | 4 | reference-3-4 | implicit link matching | values padded with spaces, no colons |
| T22 | [links.md L566](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/links.md#L566) | 3 | 4 | reference-3-4 | explicit link matching | as T21 |
| T23 | [google.md L13](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/google.md#L13) | 2 | 8 | key-value | BOSH concept → GCP | 8 inline links (URLs up to 67 chars in the source) |
| T24 | [google.md L33](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/google.md#L33) | 2 | 3 | key-value | GCP network type support | — |
| T25 | [google.md L41](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/google.md#L41) | 2 | 4 | key-value | GCP misc. features | reference links |
| T26 | [openstack.md L30](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/openstack.md#L30) | 2 | 9 | key-value | BOSH concept → OpenStack | 10 inline links (URLs up to 87 chars); 184-char source cell |
| T27 | [openstack.md L51](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/openstack.md#L51) | 2 | 3 | key-value | OpenStack network type support | — |
| T28 | [openstack.md L59](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/openstack.md#L59) | 2 | 4 | key-value | OpenStack misc. features | reference links |
| T29 | [pre-stop.md L53](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/pre-stop.md#L53) | 2 | 4 | key-value | pre-stop env var combinations | three code spans per cell joined by `<br>` (9 `<br>`); one `<br>` in col 2 |
| T30 | [aws.md L13](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/aws.md#L13) | 2 | 8 | key-value | BOSH concept → AWS | 7 inline links (URLs up to 96 chars) |
| T31 | [aws.md L33](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/aws.md#L33) | 2 | 3 | key-value | AWS network type support | — |
| T32 | [aws.md L46](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/aws.md#L46) | 4 | 6 | reference-3-4 | AWS disk encryption | Platform and Disk Type repeat down the rows (no blanks) |
| T33 | [aws.md L66](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/aws.md#L66) | 2 | 4 | key-value | AWS misc. features | reference links |
| T34 | [stemcell-lines.md L28](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/stemcell-lines.md#L28) | 5 | 4 | wide | stemcell lines and support dates | links to `/stemcells/#…` (bosh-io-web, outside /docs); Markdown footnote `[^windows-support]` in a cell; five stacked `<a id>` anchors above |
| T35 | [vsphere-esxi-host-failure.md L21](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/vsphere-esxi-host-failure.md#L21) | 4 | 4 | reference-3-4 | sample `bosh stemcells` output | in a nested list (6-space indent); 39-char CIDs; `1.585*` literal asterisk |
| T36 | [azure.md L16](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/azure.md#L16) | 2 | 8 | key-value | BOSH concept → Azure | 7 reference links, 1 relative link |
| T37 | [azure.md L44](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/azure.md#L44) | 2 | 3 | key-value | Azure network type support | — |
| T38 | [azure.md L60](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/azure.md#L60) | 3 | 3 | reference-3-4 | Azure managed-disk encryption | — |
| T39 | [azure.md L72](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/azure.md#L72) | 3 | 3 | reference-3-4 | Azure storage-account encryption | — |
| T40 | [azure.md L87](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/azure.md#L87) | 2 | 5 | key-value | Azure misc. features | reference links |

</details>

**Two hints the list does not have yet.** Hints are what a table asks for,
independent of any tool ([glossary](../../../glossary.md#hint);
[hints after the round](../README.md#hints-after-the-round)). The bosh.io
tables add two candidates, both open:

- **Row groups:** rows that share a first-column value, shown today as
  blank "same as above" cells and blank spacer rows (T4; T32 repeats the
  value instead).
- **Table notes:** markers in cells explained in lines under the table
  (T3, T4, T14, T34, and a `[3]` with no target in T16).

**Two defects that show on the live site** (checked 2026-10-09). In T16,
`<manifest>` and `<ip>` are read as HTML tags and disappear
([page](https://bosh.io/docs/cli-v2-diff/)). In T14, `*full agent settings**`
in a header cell renders in italics with a stray `*`
([page](https://bosh.io/docs/cpi-api-v2/)).

**The look** (checked 2026-10-09 on
[networks](https://bosh.io/docs/networks/) and
[init-openstack](https://bosh.io/docs/init-openstack/)). bosh.io uses
Material's default table: a thin outer border,
rules between rows, no rules between columns, no header shading, no
striping, text at 80% of body size, and tables sized to their content that
scroll sideways in their own box when too wide. The book boxes every cell
and shades the header (see [above](#how-the-book-renders-them-today)).

**bpm pages.** Seven more tables publish under bosh.io/docs/bpm/ from the
`bpm-release` repository, which `docs-bosh` includes as a submodule at
[`6b9988a`](https://github.com/cloudfoundry/bpm-release/tree/6b9988a0271aefc2e0cd6444ad4f8d562f46b06e/docs).
They were surveyed in a separate run and are **not in tables.csv**: six
pipe tables in
[`docs/config.md`](https://github.com/cloudfoundry/bpm-release/blob/6b9988a0271aefc2e0cd6444ad4f8d562f46b06e/docs/config.md#L31)
(one YAML schema, one table per object, columns Property / Type / Required /
Description; reference-3-4) and one in
[`docs/runtime.md`](https://github.com/cloudfoundry/bpm-release/blob/6b9988a0271aefc2e0cd6444ad4f8d562f46b06e/docs/runtime.md#L46)
(key-value). Last checked 2026-10-10: repository `cloudfoundry/bpm-release`
(the submodule URL, `cloudfoundry-incubator/bpm-release`, redirects there),
branch `master`, commit `6b9988a0271aefc2e0cd6444ad4f8d562f46b06e`, the
commit `docs-bosh` pins at `20a4122`; it is an ancestor of `master`, which
has moved on since. The seven tables and their families match. On the
[live page](https://bosh.io/docs/bpm/config/)
(checked 2026-10-09), eight Property names break in the middle of
the identifier, because Material lets code text break anywhere; this is the
strongest case so far for the "don't wrap" hint.

## How to rerun

Run everything from a working directory outside this repository, with
`python3 -I` (isolated mode: Python ignores the current directory and
environment variables when it loads modules). `SURVEY` below stands for this
folder, `concepts/tables/survey`.

**The whole survey** needs a clone of each repository in `shas.txt`, at its
commit:

```sh
mkdir -p repos
while read name sha date; do
  case $name in
    cft-*) url=https://github.com/cloudfoundry-tutorials/${name#cft-} ;;
    *)     url=https://github.com/cloudfoundry/$name ;;
  esac
  git clone --quiet "$url" "repos/$name"
  git -C "repos/$name" checkout --quiet "$sha"
done < SURVEY/shas.txt

python3 -I SURVEY/survey.py repos SURVEY/shas.txt raw
python3 -I SURVEY/families.py raw.json tables
cmp tables.csv SURVEY/tables.csv
```

`survey.py` writes `raw.json` and `raw.csv` and prints the table count;
`families.py` prints the family summary and writes `tables.json` and
`tables.csv` with the `family` column. [tables.csv](tables.csv) holds 238
tables. On 2026-10-10 `survey.py` was rerun on `docs-bbr`,
`docs-book-cloudfoundry` and `docs-bosh`, and its rows for them match the
file.

**Only the families**, from the data here, without clones:

```sh
python3 -I SURVEY/families.py SURVEY/tables.csv
```

This prints the [families](#families) and the counts behind
[traits across all 238 tables](#totals). With a second argument it writes a
copy of the data with the `family` column; on `tables.csv` that copy is
byte-identical to the input (checked 2026-10-10).

**bosh.io** needs a clone of `docs-bosh` at `20a4122`:

```sh
git clone --quiet https://github.com/cloudfoundry/docs-bosh.git docs-bosh
git -C docs-bosh checkout --quiet 20a41223a7ba87700424634c42e94a22a669b45e
python3 -I SURVEY/bosh_tables.py constructs docs-bosh
python3 -I SURVEY/bosh_tables.py tables docs-bosh SURVEY/tables.csv > bosh-tables.csv
```

`constructs` prints the Markdown counts above; `tables` writes one CSV row
per table (indent, the list or admonition it sits in, alignment, inline
HTML, code spans, links, longest URL and word, empty cells, spacer rows,
bold header, column or rows, note markers, symbols). The "Holds" and "What
matters" columns in the list of 40 were written by hand from that output
and the source.

**bpm pages** need a clone of `bpm-release` at the commit `docs-bosh` pins:

```sh
mkdir -p bpm && git clone --quiet https://github.com/cloudfoundry/bpm-release.git bpm/bpm-release
git -C bpm/bpm-release checkout --quiet 6b9988a0271aefc2e0cd6444ad4f8d562f46b06e
echo "bpm-release 6b9988a0271aefc2e0cd6444ad4f8d562f46b06e 2021-10-07" > shas-bpm.txt
python3 -I SURVEY/survey.py bpm shas-bpm.txt bpm-raw
python3 -I SURVEY/families.py bpm-raw.json bpm
python3 -I SURVEY/bosh_tables.py tables bpm/bpm-release bpm.csv bpm-release B > bpm-tables.csv
```

The scripts read files only; they run nothing from the clones.
