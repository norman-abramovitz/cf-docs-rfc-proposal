# Variable survey

Status: draft, incomplete — covers what is known as of 2026-10-11.

This survey counts every variable the book's pages use and every value the
book defines, and records where each use sits and what each value holds.
It was done on 2026-10-11 to choose the test pages of the variables round
and to know which cases a conversion has to handle
([R-04](../../../requirements/README.md#r-04) variables everywhere).

Terms used below:

- **Variable.** A name a page writes as an ERB tag, `<%= vars.name %>`,
  whose text comes from the book's
  [`config/template_variables.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml).
  ERB is the Ruby template language the book's build (Middleman, driven by
  Bookbinder) runs on each page before its Markdown is read. Bookbinder
  merges every YAML file in `config/` into the book's configuration
  ([`fetcher.rb` L42-L48](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/lib/bookbinder/config/fetcher.rb#L42-L48))
  and its `vars` helper wraps the `template_variables` key in a Ruby
  `OpenStruct`
  ([`bookbinder_helpers.rb` L102-L104](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/bookbinder_helpers.rb#L102-L104),
  v9.12.0; the book pins the gem at 9.12.1, for which the repository has
  no tag).
- **Key** and **value**: a line of that file, `app_domain: shared-domain.example.com`.
- **Use**: one reference to a variable in a page or layout. **Place**: where
  the use sits (text, code, a heading, a link, front matter, ...).
- **Not defined**: a name pages use that no key carries. **Empty**: a key
  with no value (`ssl:`, a YAML null). On the published pages both render
  as nothing: an `OpenStruct` returns `nil` for an unknown name, and ERB
  prints `nil` as no text.

| File | What it is |
|---|---|
| [uses.csv](uses.csv) | One row per ERB expression in the surveyed files (1,676 rows), each with a GitHub link at the surveyed commit: what it is, the variable's name, whether it is defined, what its value holds, its place and the elements around it |
| [values.csv](values.csv) | One row per key of the book's file (273), of the MkDocs tutorial's `extra:` (2), and per name pages use but no key defines (28): what the value holds, how often pages use it, and where |
| [shas.txt](shas.txt) | The 15 repositories and the commit surveyed in each, the [notes survey's list](../../notes/survey/shas.txt) |
| [survey.py](survey.py) | Finds the expressions and reads the variables file; writes the two CSV files |
| [summary.py](summary.py) | Prints the counts below from the two CSV files |

## Scope

- **Repositories.** The 15 `docs-*` repositories of the notes survey, at
  the same commits. "The book" below means the 12 content repositories the
  book's
  [`config.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml#L9-L89)
  publishes. `docs-book-cloudfoundry`'s own pages and layouts are counted
  apart. `docs-bosh` builds bosh.io with MkDocs, and
  `docs-dotnet-core-tutorial` is an MkDocs site the book does not publish;
  both are counted apart.
- **Files.** The notes survey's: `.md`, `.erb`, `.html`, `.haml`,
  `.markdown`, `.mdx` and `.adoc`, without `.git`, `node_modules` and
  `vendor` folders and without Markdown files at a repository's root.
  Files in `archive/` folders are counted and flagged.
- **Expressions.** Every ERB tag: `<%= … %>` (output), `<% … %>` (code),
  `<%# … %>` (comment); `<%%` (an escaped tag) is not one. In the MkDocs
  tutorial, every `{{ name }}`.
- **Source, not published pages.** A partial counts once however many
  pages include it.
- **Bookbinder's own layouts** (header, title) are not in these
  repositories; the variables they read are listed under
  [Variables the layouts read](#variables-the-layouts-read), from the
  Bookbinder source.

## Method

[survey.py](survey.py) reads each file and finds every ERB tag. For each
tag it records:

| Field | What is recorded |
|---|---|
| `kind` | `variable` (the tag reads `vars.name`), `partial`, `helper` (another Ruby method: `image_tag`, `mermaid_diagram`, ...), `build-time` (`Time.now`), `control` (`end`), `comment`; in docs-bosh, `bosh-template` |
| `defined`, `value_kind` | whether the book's file has the key and a value, and what the value holds (below) |
| `method` | `expression` when the tag does more than print one variable (a condition, a string built from variables); such a tag gets a row per variable it reads |
| `place` | `front-matter`; `erb-code` (a `<% %>` tag); `fenced-code` (between ```` ``` ```` or `~~~` lines); `indented-code` (four columns past the margin or the enclosing list item, after a blank line); `pre` (inside `<pre>`); `code-span` (inside backticks or `<code>`); `link-url` (in a Markdown link's target, a reference definition, or an `href` or `src`); `html-attribute` (another attribute); `heading` (a `#` line or `<h1>`–`<h6>`); `link-text` (in a Markdown link's text or inside `<a>`); `prose` otherwise. The first that applies wins |
| `table`, `note`, `list`, `html` | whether the use sits in a Markdown pipe table or an HTML cell, in an HTML note (`<p class="note">`), in a list (indented under a Markdown item, or in an open `<li>`), and the innermost HTML block element around it |
| `links_resolve` | for a value with links relative to the page: whether each link, resolved from the page's published folder, reaches a page of the book, directly or through a redirect in [`redirects.rb`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb) |

A value is `text`, `url`, `path` (a file or partial name, a relative
link target), `html` (it holds an HTML element), `markdown` (a link
`[text](url)`, backticks, `**`, emphasis, list lines, a fence, an escaped
`\_`), `html+markdown`, `empty`, or `erb` (it holds an ERB tag; none
does). HTML elements are read with a tag pattern; an HTML tag left open
inside a table cell or list item is taken to end where HTML ends it.

The places are read from the source. Two limits: an indented code block
is found by indentation alone, the way CommonMark finds it, and the book's
Markdown processor (Redcarpet) may differ at the edges; and inline HTML
left open in the source (an `<a>` never closed, a `</xth>` typo) is ended
at the next blank line or closed cell.

The YAML file is read without a YAML library. Its parse was compared with
PyYAML 6.0.2: all 273 keys and values are the same (see
[How to rerun](#how-to-rerun)).

## Totals

| | Variables | Partials | Helpers and control | Comments | Build-time | All |
|---|---|---|---|---|---|---|
| The book (12 repositories) | 1,503 | 45 | 9 | 13 | 0 | 1,570 |
| The book repository's pages and layouts | 5 | 7 | 19 | 1 | 1 | 33 |
| bosh.io (`docs-bosh`) | — | — | — | — | — | 41 ERB tags shown as code |
| MkDocs tutorial (`docs-dotnet-core-tutorial`) | 32 `{{ name }}` | — | — | — | — | 32 |

The 1,503 variable uses are in 169 files and read 180 names:
`docs-dev-guide` 496, `docs-cloudfoundry-concepts` 362, `docs-cf-admin`
265, `docs-buildpacks` 115, `docs-loggregator` 100, `docs-services` 100,
`docs-uaa` 29, `docs-deploying-cf` 15, `docs-running-cf` 9, `docs-cf-cli`
5, `docs-credhub` 4, `docs-bbr` 3. Every one is in a `.erb` file, so every
one is read by ERB. 29 are in partials, 8 in `archive/` folders.

## Where variables sit

| Place | Uses | Detail |
|---|---|---|
| Text (prose) | 1,205 | |
| Inline code | 98 | 70 in backticks, 28 in `<code>` |
| Fenced code block | 92 | |
| `<pre>` block | 44 | |
| Link text | 33 | all in Markdown links: `[<%= vars.app_runtime_abbr %> Security](security.html)` |
| Heading | 27 | on 15 pages; every one has an explicit `<a id>`, so no published id depends on a value (the hyphen-prefixed second id does, for example `-configuring-ssh-access-for-cloud-foundry`) |
| Link target | 3 | two Markdown (`[metrics](<%= vars.gorouter_metrics_link %>)`, [troubleshooting-router-error-responses L40](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb#L40); `[…](<%= vars.product_url %>)`, [notifications L15](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/notifications.html.md.erb#L15)), one HTML `href` in a table cell ([L388](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb#L388)) |
| ERB code | 1 | the page title, set from a variable (below) |
| Front matter, page description | 0 | the book's pages have no description; no front matter holds a tag |
| Another HTML attribute | 0 | |
| Indented code block | 0 | |
| Inside another variable's value | 0 | no value holds an ERB tag |

Around the uses, in every place: 96 sit in table cells (74 HTML, 22
Markdown pipe tables), 22 in HTML notes, 326 in lists (288 Markdown, 38
HTML `<li>`).

**Expressions that do more than print.** Three tags, five variable
references:

- **A page title set by code**:
  [`all_metrics` L6](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/all_metrics.html.md.erb#L6),
  `<% current_page.data.title = vars.app_runtime_abbr + " Component Metrics" %>`.
  It replaces the front matter's title ("Cloud Foundry component
  metrics"): the published page's `<title>` and heading read "Cloud Foundry
  Component Metrics" ([published copy](../published/all_metrics.html),
  lines 11 and 512). Ten pages of `docs-cloudfoundry-concepts` keep a
  comment `<%# Reset page title based on product title %>` with no code
  after it.
- **A condition with interpolation**:
  [`stacks` L11](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/stacks.html.md.erb#L11)
  and
  [`windows-stacks` L9](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/windows-stacks.html.md.erb#L9),
  `vars.current_major_version ? "#{vars.app_runtime_full} v#{vars.current_major_version}" : vars.app_runtime_full`.
  `current_major_version` is `"10-0"`, a value written "for partials"
  ([L37-L38](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L37-L38)),
  so the published page reads "supported on Cloud Foundry v10-0"
  ([published copy](../published/stacks.html), line 529).
- No page uses a variable in an `if`, and none calls a method on a value
  (`vars.x.upcase`).

**Partial names in variables.** At these commits no page picks its partial
from a variable. Eight keys hold a partial's name (`scale_table`,
`roles_table`, `suspended_roles_table`, `concepts_product_model_text`,
`gorouter_client_cert`, `ssl_termin_gorouter`, `ssl_termin_lb_only`,
`ssl_termin_gorouter_lb`) and no page reads them; `overview` names its
partial directly after a comment that mentions the variable
([L216-L217](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/overview.html.md.erb#L216-L217)).
The partials round owns this case
([R-05](../../../requirements/README.md#r-05) partials and reuse).

## What the values hold

**The 273 keys.** Text 73, HTML 60, Markdown 56, HTML and Markdown 15, a
path or partial name 14, a URL 4, empty 51.

- **HTML elements in values** (keys that hold each): `a` 42, `code` 20,
  `p` 19, `strong` 17, `span` 17, `li` 9, `ul` 7, `br` 4, `pre` 3, `h2` 3,
  `h3` 2, `em` 2, `td` 1, `tr` 1. Twelve values are whole notes
  (`<p class="note">`; the [notes survey](../../notes/survey/README.md#the-books-notes)).
  Some are fragments of a structure: a table row
  ([`r_buildpack` L343](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L343)),
  a list item (`gorouter_sni`, `setting_rate_limit_cloud_api`), a heading
  (`max_in_flight_header`, `disable_custom`).
- **Markdown in values**: links 45, code spans 23, emphasis 12, escaped
  underscores 4, bold 2, lists 2, fences 2, a pipe-table fragment 1
  ([`app_sec_group_desc` L58](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L58)).
- **Multi-line values**: 2, both YAML block scalars that hold a heading,
  paragraphs and fenced code (`default_asgs`
  [L104](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L104),
  `route_services_enabling`
  [L238](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L238)).
  No page uses either.
- **Links relative to the page** in 43 values (`../../running/config-ssh.html`).
  Every use of such a value is on a page where the link reaches a page of
  the book: 33 directly and 2 through a redirect. A value with a relative
  link is correct only at the folder depth of the pages that use it.
- **A key that is not a name**:
  [L79](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L79)
  is a sentence followed by a colon, so YAML reads it as a key with no
  value; no page can read it.
- **`title`** ([L5](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L5))
  is also AsciiDoc's attribute for the document title; passed to Antora
  as is, it renames every page ([results](../results.md#antora-321)).

**Used and unused.** Pages use 156 keys; 117 keys are used by no page (29
text, 27 HTML, 20 empty, 16 Markdown, 13 paths, 10 HTML and Markdown, 2
URLs). Some of those are read by the layouts (below).

**Product names.** 1,060 of the 1,503 uses (71%) read a variable whose
value is the product's name, "Cloud Foundry", "CF" or "cf":
`app_runtime_abbr` 809, `platform_name` 87, `app_runtime_first` 64,
`company_name` 28, `recommended_by` 20, `app_runtime_abbr_lc` 19,
`app_runtime_full` 16, `product_short` 9, and four more. They cover every
heading use and every link-text use. 174 more read an example domain
(`app_domain` 124, `private_app_domain` 36, `tcp_app_domain` 14). The
variables exist so that other books could build the same pages with other
values: a comment in `overview` says "For private/commercial books, the
partial and image files come from a private repository"
([L210-L213](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/overview.html.md.erb#L210-L213)).
Whether any other book still builds from these repositories was not
found in them.

## Variables used but not defined, or empty

**Not defined: 28 names, 38 uses.** The tables round found `metadata_ref`
and `bosh_cli_link`; both are confirmed, with 26 more:
`GSG_intro_sentence` (4 uses), `bosh_cli_link` (4), `configure_system_logging_link` (3),
`mutual_tls_ssh` (3), and one use each of `app_graceful_shutdown_config`,
`app_man_network`, `app_svc_links`, `app_traffic_logging`, `asg_note`,
`autoscaler_note_dev_guide`, `best_practices_link`, `capi_link`,
`cli_install_link`, `compliance_links`, `custom_metrics_footnote`,
`dns_warning`, `docker_auth1`, `domains_on_hosted`, `external_lb`,
`garden_runc`, `gather_routing_logs`, `gsg_app_video_link`,
`metadata_ref`, `ops_manager`, `pcf_pools`, `ssl_cert_ert`,
`tiledev_link`, `vm_note`.

**Empty: 31 keys, 44 uses**, for example `dev_console_note` (4 uses),
`gen_GSG` (4), `ssl` (1); all in text. Both kinds render as nothing on the
published pages: `app-ssh-overview` uses `mutual_tls_ssh` between two
paragraphs, and the published page has nothing there
([published copy](../published/app-ssh-overview.html), lines 528-531).
The build reports neither.

## Values that hold markup, and where they are used

ERB prints a value before Redcarpet reads the page, so a value's HTML is
markup and its Markdown is read as Markdown, as if the page held it. Two
exceptions follow from Markdown's rules, not from the variables:

- **Markdown inside an HTML block stays as written.** Of the 9 uses of an
  HTML or Markdown value inside an HTML block element (3 in `<td>`, 3 in
  `<p>`, 1 in `<li>`, 1 in `<pre>`, 1 Markdown in `<td>`), the Markdown one
  shows its backticks on the published page:
  [`configure-lb-healthcheck` L92](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/configure-lb-healthcheck.html.md.erb#L92)
  uses `healthcheck_duration`, and the published cell reads
  `` `router.requested_route_registration_interval_in_seconds` ``
  ([published copy](../published/configure-lb-healthcheck.html), line 636).
- **Links are written differently.** The book writes a Markdown link that
  reaches a page as a path from the site's root, and leaves an HTML `href`
  as written: on `app-ssh-overview` the Markdown value's link is
  `/running/config-ssh.html` and the HTML value's is
  `../../running/config-ssh.html`
  ([published copy](../published/app-ssh-overview.html), lines 549 and
  585). Which layer does this was not traced.

HTML values are used inline more often than as blocks: of the 49 uses of
an HTML value, 28 sit inside a sentence (`… (one-time). <%= vars.config_ssh_link %>`),
6 are inline values alone on a line, and 15 are block values (notes,
lists, headings) alone on a line.

## Variables the layouts read

Variables also fill the site's frame, not only pages:

- The book's layout: `book_title_short` in `<title>`
  ([`layout.erb` L14](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/layout.erb#L14)),
  `domain_name`
  ([L30](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/layout.erb#L30)),
  `ga_account_id` and `domain_name` in the analytics script
  ([`_additional-scripts.erb` L4-L5](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/_additional-scripts.erb#L4-L5)),
  `support_url` in the footer
  ([`_book-footer.erb` L6](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/_book-footer.erb#L6)).
- Bookbinder's layouts: `book_title`, `product_link`, `support_link`,
  `support_call_to_action`, `hero_text`
  ([`_header.erb` L4-L31](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/source/layouts/_header.erb#L4-L31))
  and `title`
  ([`_book-title.erb` L3](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/source/layouts/_book-title.erb#L3)).
- Other helpers in layouts: `current_page.data.title`, `quick_links`,
  `modified_date` ("Page last updated"), `production_host`,
  `yield_for_subnav`, `owners`; the footer's year is `<%= Time.now.year %>`
  ([`_book-footer.erb` L3](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/_book-footer.erb#L3)),
  the one build-time value; it belongs to the copyright concept and is
  counted, not converted
  ([R-25](../../../requirements/README.md#r-25) build-time values are expected differences).

These are site settings, not page content: they belong in each tool's
site configuration or template.

## Other expressions and other variable sources

- **Helpers in pages**: `image_tag` (2, `docs-deploying-cf`
  `common/dns_prereqs`), `mermaid_diagram` blocks (3, `docs-bbr`
  `bbr-devguide`), `partial` (45, the partials round's). 13 comments.
- **No content repository defines variables of its own.** None has a
  `config.yml` or a `template_variables` file; their READMEs point to the
  book's file (for example
  [`docs-dev-guide` README L21-L23](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/README.md#L21-L23)).
- **The MkDocs tutorial** (`docs-dotnet-core-tutorial`) uses
  `{{ product_short }}` 25 times and `{{ product_full }}` 7 times, defined
  under `extra:` in its
  [`mkdocs.yml` L42-L45](https://github.com/cloudfoundry/docs-dotnet-core-tutorial/blob/6e83c738187380d3fc02697892e0c7c9d806e01c/mkdocs.yml#L42-L45)
  and read by the `markdownextradata` plugin; all in text.
- **bosh.io** (`docs-bosh`) has no variables. Its 41 ERB tags are BOSH job
  templates shown as examples, 27 in inline code and 14 in fenced code; a
  converter must leave them as text.
- **Double braces in the book's content**: 12 lines on 2 pages hold
  `{{`, Go template examples in
  [`nginx/index` L46-L131](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/nginx/index.html.md.erb#L46-L131)
  and
  [`notifications` L111-L116](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/notifications.html.md.erb#L111-L116).
  A tool that reads `{{ }}` as its own syntax would treat them as
  variables. No page holds `{%` or `{#`.

## How to rerun

Run from a working directory outside this repository, with `python3 -I`.
`SURVEY` stands for this folder, `concepts/variables/survey`. Each
repository is fetched at its commit, without history:

```sh
mkdir -p repos
git init -q repos/docs-bbr
git -C repos/docs-bbr fetch -q --depth 1 https://github.com/cloudfoundry/docs-bbr.git 51465950ce3a2196d66a9339086b94feed280c3e
git -C repos/docs-bbr checkout -q FETCH_HEAD
# … the same three lines for each repository in SURVEY/shas.txt

python3 -I SURVEY/survey.py repos SURVEY/shas.txt uses.csv values.csv
cmp uses.csv SURVEY/uses.csv && cmp values.csv SURVEY/values.csv
python3 -I SURVEY/summary.py SURVEY/uses.csv SURVEY/values.csv
```

`survey.py` prints the totals per kind; `summary.py` prints every count on
this page. The scripts read files only; they run nothing from the clones.
To compare the YAML reading with a YAML library, load
`repos/docs-book-cloudfoundry/config/template_variables.yml` with PyYAML
(`yaml.safe_load`) and `survey.py`'s `parse_variables` function, and
compare the two mappings key by key; on 2026-10-11 they matched for all
273 keys.
