# Partial survey

Status: draft, incomplete — covers what is known as of 2026-10-11.

This survey counts every partial call and every partial file in the 15
`cloudfoundry/docs-*` repositories and in the book's own repository, and
records how each call is written, where its partial lives, and what the
partial holds. A **partial** is a file of content that is not a page of
its own and is rendered inside the pages that include it; the book names
partial files `_name.html.md.erb` and includes them with
`<%= partial 'name' %>`. The survey was done on 2026-10-11 to choose the
test pages of the partials round and to give data to the open question
whether partial names held in variables are still needed
([R-05](../../../requirements/README.md#r-05) partials and reuse;
[research area](../../../requirements/research-areas.md#are-partial-names-in-variables-still-needed)).

| File | What it is |
|---|---|
| [calls.csv](calls.csv) | One row per call, 55 rows: the call as written, its form, where it sits, and the file it resolves to, each with a GitHub link to the call at the surveyed commit |
| [partials.csv](partials.csv) | One row per partial file, 48 rows: what it holds, who includes it, how often, and whether a variable names it |
| [shas.txt](shas.txt) | The 15 repositories and the commit surveyed in each: the notes survey's list |
| [shas-2026-07.txt](shas-2026-07.txt) | The same list with eight repositories set to the commit before their July 2026 cleanup (see [History](#history)) |
| [survey.py](survey.py) | Finds the calls and partial files in a set of clones and writes both CSV files |
| [summary.py](summary.py) | Prints the counts below from the two CSV files |

## Scope

- **Repositories.** The 15 `docs-*` repositories of the
  [notes survey](../../notes/survey/README.md#scope), at the same commits.
  The book repository, docs-book-cloudfoundry, is read whole: its layouts,
  `master_middleman/source/` and subnavs. `docs-bosh` builds bosh.io with
  MkDocs, not the book; its snippet includes are counted apart.
- **Files.** The notes survey's: `.md`, `.erb`, `.html`, `.haml`,
  `.markdown`, `.mdx` and `.adoc`, without `.git`, `node_modules` and
  `vendor` folders and without Markdown files at a repository's root.
- **Variables.** The book's
  [`config/template_variables.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml)
  is read for values that name a partial file.
- **Source, not published pages.** Calls are counted where they are
  written.

## How the book resolves a partial

The book pins `bookbindery` 9.12.1 in its
[Gemfile](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/Gemfile#L3);
the repository has no `Gemfile.lock`. (Its Docker preview pins 10.1.18
instead, [`docker/files/Gemfile` L2](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/docker/files/Gemfile#L2),
which runs Middleman 4; that path was not traced.) Bookbinder's repository
is `pivotal-cf/bookbinder`; `cloudfoundry-incubator/bookbinder` redirects
to it. The 9.12.1 gem on
[RubyGems](https://rubygems.org/gems/bookbindery/versions/9.12.1) differs
from the repository's `v9.12.0` tag
([`f608a44`](https://github.com/pivotal-cf/bookbinder/commit/f608a441572def7787361842f05e42d163d78d54))
in two files that do not touch partials (`code_example_reader.rb` and
`preprocessor.rb`, a change of Ruby syntax; compared with `diff` on
2026-10-11), so the lines below are cited at that tag. It requires
Middleman `~> 3.4.0`
([gemspec](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/bookbinder.gemspec#L20)),
which uses padrino-helpers `~> 0.12.3`
([middleman-core gemspec, v3.4.1](https://github.com/middleman/middleman/blob/37845e89c0c4e84bbab9b202cf21e0c02c84d398/middleman-core/middleman-core.gemspec#L38)).
Middleman 3.4.1 and padrino-helpers 0.12.9 are the newest releases those
requirements allow; which patch release the book's build installs is not
recorded anywhere found.

1. **The site's source tree.** Bookbinder copies its own
   `master_middleman/` into the output, then the book's over it
   ([`directory_preparer.rb` L16-L17](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/lib/bookbinder/commands/components/bind/directory_preparer.rb#L16-L17),
   [`layout_preparer.rb` L21](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/lib/bookbinder/commands/components/bind/layout_preparer.rb#L21)).
   Each section's repository is then linked into `master_middleman/source/`
   under the section's `directory:` from the book's `config.yml`
   ([`link_to_site_gen_dir.rb` L17-L22](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/lib/bookbinder/preprocessing/link_to_site_gen_dir.rb#L17-L22),
   [`destination_directory.rb` L4-L12](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/lib/bookbinder/ingest/destination_directory.rb#L4-L12);
   [`config.yml` L8-L13](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml#L8-L13)).
   So docs-cf-admin is `adminguide/`, docs-dev-guide `devguide/`, and so on:
   all repositories share one source tree.
2. **`dependent_sections` bring no partials.** A dependent section is
   cloned under its parent's folder unless it is marked `no_docs`
   ([`section_repository.rb` L20-L30](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/lib/bookbinder/ingest/section_repository.rb#L20-L30)).
   All six dependent sections in the book's `config.yml` are `no_docs:
   true` (sample-app and release repositories), so none adds content or
   partials.
3. **The name.** `partial 'a/b'` asks for `a/_b`: padrino-helpers puts an
   underscore before the last path segment
   ([`render_helpers.rb` L33-L38](https://github.com/padrino/padrino-framework/blob/8b9714dfd66b2f9586d80c61c83e5abaf4e6b0c7/padrino-helpers/lib/padrino-helpers/render_helpers.rb#L33-L38),
   0.12.9). The same helper takes `locals:`.
4. **The lookup.** Middleman looks for that path first relative to the
   calling file's folder, then from the source root, and then under the
   `partials_dir` setting, which is empty by default
   ([`rendering.rb` L202-L212](https://github.com/middleman/middleman/blob/37845e89c0c4e84bbab9b202cf21e0c02c84d398/middleman-core/lib/middleman-core/core_extensions/rendering.rb#L202-L212),
   [L237-L252](https://github.com/middleman/middleman/blob/37845e89c0c4e84bbab9b202cf21e0c02c84d398/middleman-core/lib/middleman-core/core_extensions/rendering.rb#L237-L252),
   [`application.rb` L133](https://github.com/middleman/middleman/blob/37845e89c0c4e84bbab9b202cf21e0c02c84d398/middleman-core/lib/middleman-core/application.rb#L133)).
   Each try accepts any template extension and also the file name without
   its leading underscore; a leading `/` is dropped, so `/x/y` is read
   from the source root
   ([L476-L515](https://github.com/middleman/middleman/blob/37845e89c0c4e84bbab9b202cf21e0c02c84d398/middleman-core/lib/middleman-core/core_extensions/rendering.rb#L476-L515)).
   A partial in another repository is therefore reached through the other
   section's folder: `/<directory>/name` or `../<directory>/name`.
5. **Missing partials.** Middleman raises "Could not locate partial"
   ([L212](https://github.com/middleman/middleman/blob/37845e89c0c4e84bbab9b202cf21e0c02c84d398/middleman-core/lib/middleman-core/core_extensions/rendering.rb#L212));
   its build records the error, goes on, and exits with status 1
   ([`cli/build.rb` L74-L82](https://github.com/middleman/middleman/blob/37845e89c0c4e84bbab9b202cf21e0c02c84d398/middleman-core/lib/middleman-core/cli/build.rb#L74-L82)).
6. **Two passes.** A partial is rendered through all its own extensions
   (`.erb`, then `.md`) before the host page's Markdown reads the result
   ([`rendering.rb` L169-L191](https://github.com/middleman/middleman/blob/37845e89c0c4e84bbab9b202cf21e0c02c84d398/middleman-core/lib/middleman-core/core_extensions/rendering.rb#L169-L191)).
   The host's Markdown therefore sees HTML where the call was. The
   published pages show the effect: in a list item after a label, the
   partial's paragraph becomes a `<p>` inside the item's `<p>`
   ([published `architecture`](../published/architecture.html), line 586);
   and the last paragraph of `_tcp_modify_ports`, indented under its step
   in the partial, is published after the list
   ([published `enabling-tcp-routing`](../published/enabling-tcp-routing.html),
   line 628).
7. **The quick links leave partials out.** The "On this page" list is
   made from the page's own source file
   ([`bookbinder_helpers.rb` L110-L114](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/bookbinder_helpers.rb#L110-L114)),
   so headings that a partial holds are not in it: `using-vol-services`,
   whose 17 headings are all in its partial, has an empty list
   ([published copy](../../notes/published/using-vol-services.html),
   line 515; [browser check](../results/browser-checks.txt)).
8. **Bookbinder's own partials.** The layout's subnav comes from
   `partial "subnavs/#{subnav_template_name}"`, the `subnav_template` of
   the page's section
   ([`bookbinder_helpers.rb` L46-L48](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/bookbinder_helpers.rb#L46-L48)):
   the book's `_cf-subnav.erb`.

## Method

[survey.py](survey.py) reads every file and finds three forms:

| Form | What is found |
|---|---|
| `erb` | an ERB tag (`<%=`, `<%-`, `<%`) whose code starts with `partial`, `render` or `render_partial` |
| `comment` | an ERB comment (`<%# … %>`) that mentions a partial; counted, not resolved |
| `snippet` | a pymdownx.snippets line, `--8<-- "path"` (`docs-bosh` only) |

For each ERB call it records the tag, the quotes, how the name is given (a
literal, a variable such as `vars.x`, a string with `#{…}`, or another
expression), the path style (a bare name, `./`, `../`, a folder, or a
leading `/`), `locals:`, whether the call sits inside an ERB `if`,
`unless`, `case` or block, and where it sits: at the top level, in a
Markdown list item (on the item's first line, after text on that line, or
indented under it), inside an HTML `<li>` or table cell, inside other HTML,
after text, or in a fenced code block. It then resolves the name the way
Middleman does (above) in a model of the book's source tree, built from the
book's `config.yml`, and records where the partial lives: in the same
folder, another folder of the same repository, another repository, the
book repository, or the Bookbinder gem (with the gem unpacked, the fifth
argument); or that it is missing.

For each partial file (a file whose name starts with `_`, or any file a
call resolves to) it records its headings (Markdown `#` outside fences, and
HTML `<h1>`–`<h6>`), explicit ids (`<a id>`), notes, tables, code blocks,
variables, partial calls and other ERB; front matter; how often and from
which files it is included; whether it is included twice on one page or
from another repository; how deep it nests; and the variables whose value
names it, and whether any page uses them.

## Totals

| | Calls | Files with calls | Partial files |
|---|---|---|---|
| Content repositories (14) | 45 | 24 | 44 |
| Book repository | 7 (in `layouts/layout.erb`) | 1 | 4 |
| bosh.io (`docs-bosh`), snippets | 2 | 1 | — |

The 45 content calls: docs-cloudfoundry-concepts 12, docs-cf-admin 10,
docs-dev-guide 10, docs-running-cf 8, docs-loggregator 4, docs-credhub 1.
docs-bbr, docs-buildpacks, docs-cf-cli, docs-deploying-cf, docs-services,
docs-uaa and docs-dotnet-core-tutorial have none. One more ERB comment
mentions a partial
([`overview` L216](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/overview.html.md.erb#L216)).

## Findings

**Call forms.** Every call is `<%= partial '…' %>` with a literal name: 37
in single quotes, 8 in double quotes. None uses `<%-`, `render`,
`locals:`, a variable or interpolation for the name, and none sits inside
a conditional. 35 give a bare name, 9 start with `./` (the eight
`./metrics/…` calls in
[`all_metrics`](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/all_metrics.html.md.erb#L14)
and `./oss_credhub`), and one goes up through the section's own folder,
`../adminguide/tcp_modify_ports`
([`enabling-tcp-routing` L88](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/enabling-tcp-routing.html.md.erb#L88)),
which works only because the book names docs-cf-admin's folder
`adminguide`.

**Where partials live.** 37 calls find their partial in the caller's
folder and 8 in a subfolder of the same repository (`metrics/`). No call
reaches another repository, the book repository, or a missing file. The
book's layout includes 3 partials of its own and 4 that only the
Bookbinder gem provides (`layouts/header`, `local-header`, `title`,
`page-footer`).

**Where calls sit.** 41 are on a line of their own at the top level. Four
are in Markdown list items: three after a bold label,
`* **Log Cache:** <%= partial 'log_cache' %>`
([`architecture` L59](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/architecture.html.md.erb#L59),
L83, L89), and one as the whole of a step, `1. <%= partial "…" %>`
([`enabling-tcp-routing` L88](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/enabling-tcp-routing.html.md.erb#L88)).
None sits in HTML or in a table cell.

**What partials hold** (44 partial files in the content repositories):
tables 15, code blocks 14, explicit ids 11, headings 9, variables 8,
notes 3. The nine with headings are listed by
[summary.py](summary.py); the largest is `_using-vol-services`, 17
headings `h2`–`h4`, every one with an `<a id>`. No partial calls another
partial, holds other ERB, or has front matter: nesting depth is 0.

**Reuse.** 40 partial files are included from one file, one from two
(`_routing_conflict`, from
[`routes-domains` L406](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L406)
and
[`troubleshoot-app-health` L148](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/troubleshoot-app-health.html.md.erb#L148)),
and three from none:
[`_gorouter_client_cert_oss`](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/_gorouter_client_cert_oss.html.md.erb),
[`_overview`](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/_overview.html.md.erb)
and
[`_spare-cpu-and-throttling`](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/_spare-cpu-and-throttling.html.md.erb).
Two partials are included more than once on one page: `_v3-note`, three
times on
[`manifest-attributes`](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/manifest-attributes.html.md.erb#L41),
and `_log_cache`, twice on `architecture`. Neither holds a heading or an
id, so neither makes an id twice today. The book's `_cf-subnav.erb` is
included by Bookbinder's helper, not by a call.

**A page that is only a partial call.**
[`using-vol-services`](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/using-vol-services.html.md.erb#L6)
is front matter and `<%= partial 'using-vol-services' %>`; it is the only
such page.

**bosh.io.** `docs-bosh` includes two SVG diagrams with
`--8<-- "snippets/diagrams/…"`
([`changing-deployment-vm-strategy` L10](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/changing-deployment-vm-strategy.md#L10),
L14), through pymdownx.snippets, which its `mkdocs.yml` turns on
([L385](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/mkdocs.yml#L385)).
It has no other include.

## Partial names held in variables

Ten values in `template_variables.yml` name a partial file of a content
repository, and no page uses any of them:

| Variable | Value | Partial | Line |
|---|---|---|---|
| `concepts_product_model_text` | `"./overview_model"` | `_overview_model` (concepts) | [L88](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L88) |
| `roles_table` | `"_oss_roles_table"` | `_oss_roles_table` (concepts) | [L231](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L231) |
| `scale_table` | `"oss_scale_table"` | `_oss_scale_table` (concepts) | [L287](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L287) |
| `suspended_roles_table` | `"_suspended_org_roles_table"` | `_suspended_org_roles_table` (concepts) | [L301](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L301) |
| `tcp_port` | `"../adminguide/tcp_modify_ports"` | `_tcp_modify_ports` (cf-admin) | [L305](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L305) |
| `zipkin_enable` | `zipkin_oss_config` | `_zipkin_oss_config` (cf-admin) | [L314](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L314) |
| `gorouter_client_cert` | `"gorouter_client_cert_oss"` | `_gorouter_client_cert_oss` (cf-admin) | [L344](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L344) |
| `ssl_termin_gorouter` | `"ssl_termin_gorouter_oss"` | `_ssl_termin_gorouter_oss` (cf-admin) | [L345](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L345) |
| `ssl_termin_lb_only` | `"ssl_termin_lb_only_oss"` | `_ssl_termin_lb_only_oss` (cf-admin) | [L346](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L346) |
| `ssl_termin_gorouter_lb` | `"ssl_termin_gorouter_lb_oss"` | `_ssl_termin_gorouter_lb_oss` (cf-admin) | [L347](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L347) |

The pages that include these partials name them directly, for example
[`high-availability` L102](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/high-availability.html.md.erb#L102),
`<%= partial 'oss_scale_table' %>`. The only remaining mention is an ERB
comment, `<%# partials for vars.concepts_product_model_text %>`
([`overview` L216](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/overview.html.md.erb#L216)).

### History

The commits below are in the public repositories' history; their messages
are quoted.

- **2018: names moved into variables to serve two editions.**
  docs-cf-admin
  [`63d025c`](https://github.com/cloudfoundry/docs-cf-admin/commit/63d025c2dc6a84917279ad3a5abbc4e96f6b6581),
  "moving partials into variables to remove commercial refs in OSS",
  replaced pairs of calls such as `partial 'ssl_termin_gorouter_oss'` and
  `partial '../opsguide/ssl_termin_gorouter_pcf'` with one call,
  `<%= partial vars.ssl_termin_gorouter %>`, each edition's book setting
  the variable to its own partial. The same pattern appears in
  docs-cloudfoundry-concepts in 2016
  ([`c709dfd`](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/commit/c709dfdddb8086f44bc6a0ad108b530c84b5952d),
  "invoke platform-specific roles tables and add table for OSS").
- **2023–2024: the variables were replaced by literal names.** Commits
  titled "Migration" in January 2023 replaced `partial vars.x` calls with
  literal paths; for example docs-cf-admin
  [`3188129`](https://github.com/cloudfoundry/docs-cf-admin/commit/3188129288a465155058966f490942fa739f2574)
  ("replace variables in partial refs") turned
  `<%= partial vars.tcp_port %>` into
  `<%= partial "/pcf/core/4-0/tcp_port_review" %>`; also
  docs-cloudfoundry-concepts
  [`aa4d484`](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/commit/aa4d484ac850b5d9f0255b89fef8cb1bdd70f1e6)
  and docs-dev-guide
  [`faaaa22`](https://github.com/cloudfoundry/docs-dev-guide/commit/faaaa222ea6b3b6c702a7ead5387bdcadbd21221),
  which also removed the one call found that passed `:locals`. The last
  commit in any of the repositories that adds or removes a
  `partial vars.` line is docs-cf-admin
  [`45ab345`](https://github.com/cloudfoundry/docs-cf-admin/commit/45ab3458ddb3e06bd85f948c88c1f7675ee0ecba),
  2024-08-20 (found with `git log -G 'partial vars'` in each full clone;
  docs-bosh and docs-dotnet-core-tutorial were fetched without history, and
  neither is built from ERB).
- **July 2026: the conditionals were removed.** Eight repositories have a
  commit titled "Remove platform-conditional ERB block(s), keep OSS
  content"; the docs-cloudfoundry-concepts one says the repository "now
  serves only the OSS Cloud Foundry doc set"
  ([`5362f10`](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/commit/5362f104d6d911d783f0cb2de8420688f8b916c5);
  docs-cf-admin
  [`19b0c9c`](https://github.com/cloudfoundry/docs-cf-admin/commit/19b0c9c5fabd93b33ba184c6eb541f3cafd3a1b9)).
  The survey run on the commit before each of these
  ([shas-2026-07.txt](shas-2026-07.txt)) finds 70 content calls: 49 inside
  a conditional and 25 with a root path into another edition's folders
  (24 under `/pcf/core/`, one under `/core/`), none of which exists in the
  open-source book, and still no name held in a variable. Those 25 were
  the book's cross-repository partials, and none is left.

So the mechanism the variables served, one source rendering a different
partial in each edition's book, has had no user since August 2024, and the
second edition it chose for left the repositories in July 2026.

## How to rerun

Run from a working directory outside this repository, with `python3 -I`.
`SURVEY` stands for this folder, `concepts/partials/survey`. Each repository
is fetched at its commit, without history:

```sh
mkdir -p repos
git init -q repos/docs-bbr
git -C repos/docs-bbr fetch -q --depth 1 https://github.com/cloudfoundry/docs-bbr.git 51465950ce3a2196d66a9339086b94feed280c3e
git -C repos/docs-bbr checkout -q FETCH_HEAD
# … the same three lines for each repository in SURVEY/shas.txt

# The bookbindery 9.12.1 gem, unpacked (for the layout partials it provides)
mkdir -p gem && curl -fsSL -o gem/bb.gem https://rubygems.org/downloads/bookbindery-9.12.1.gem
tar -xf gem/bb.gem -C gem && mkdir gem/src && tar -xzf gem/data.tar.gz -C gem/src

python3 -I SURVEY/survey.py repos SURVEY/shas.txt calls.csv partials.csv gem/src
cmp calls.csv SURVEY/calls.csv && cmp partials.csv SURVEY/partials.csv
python3 -I SURVEY/summary.py SURVEY/calls.csv SURVEY/partials.csv
```

For the [History](#history) counts, fetch the eight repositories at the
commits in `shas-2026-07.txt` into another folder (the others as above)
and run `survey.py` and `summary.py` on it. The scripts read files only;
they run nothing from the clones or the gem.
