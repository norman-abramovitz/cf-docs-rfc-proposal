# Keep and pain

Status: draft Docs WG position, incomplete — covers what is known as of 2026-10-10.

What works in today's docs and must survive the move, and what causes
problems. Each item names the requirements it leads to, from the
[requirement list](README.md#requirements).

**How the docs are built today.** The pages live in about a dozen `docs-*`
content repositories as `.html.md.erb` files: Markdown with HTML mixed in and
ERB tags (Ruby's templating syntax, `<%= … %>`;
[glossary](../glossary.md#erb)). Bookbinder, a Ruby tool, collects the
repositories listed in the book's `config.yml` into one site
([glossary](../glossary.md#bookbinder)). It hands them to Middleman, a Ruby
static site generator (a program that turns text files into a website;
[glossary](../glossary.md#middleman)), which renders the pages. The book's
layout, styles and settings live in
[docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry),
which pins `bookbindery` 9.12.1.

## What to keep

### A page's URL tells you which file to edit

`docs.cloudfoundry.org/adminguide/metadata.html` is `metadata.html.md.erb` in
the `docs-cf-admin` repository: the book's
[`config.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/master/config.yml)
maps the `adminguide` directory to that repository, and the file name follows
the page name. The Docs WG lead asked on the RFC pull request that this
mapping be kept.

Leads to: [R-15](README.md#r-15) URL identifies the source.

### HTML where Markdown falls short

Authors use Markdown where it is enough and HTML where it is not. The
`metadata` test page shows both: a simple three-column reference table
written as a Markdown pipe table (one row per line, `|` between cells), and
two HTML tables with a spanning title row and bulleted lists in cells. Across
the book's repositories, 123 of 198 tables are HTML.

Leads to: [R-10](README.md#r-10) simple text plus HTML where needed, [R-02](README.md#r-02) rich tables.

### Variables and partials

A variable is a named value defined once and inserted into pages when the
site is built: `<%= vars.platform_name %>`, defined in the book's
`template_variables.yml` (about 290 variables). A partial is a file of
content included in other pages: `<%= partial 'oss_scale_table' %>`. Four of
the five test pages put variables inside table cells; one test page is a
partial ([test pages](../concepts/tables/README.md#what-the-pages-have-in-common)).

Leads to: [R-04](README.md#r-04) variables everywhere, [R-05](README.md#r-05) partials and reuse.

### Local preview

The book's README describes a local preview: "Bookbinder assembles the doc
set from your local copies and skips any content repositories you do not have
checked out. Point your browser at `localhost:4567` to preview your changes.
On save, your browser reloads with any additional changes." A container setup
for the same preview is in the book's `docker/` folder.

Leads to: [R-12](README.md#r-12) one-command local preview. The RFC's Problem list says the
opposite ([L20]); see the
[requirements page](README.md#also-incomplete).

### The Docs WG publishes

"Only the CFF Docs WG lead can merge pull requests, build to staging, and
publish the documentation." (book README). The RFC keeps this ([L54]).

Leads to: [R-14](README.md#r-14) Docs WG approves and publishes.

### Redirects for moved pages

The book has a redirect file, `redirects.rb`, with about 85 redirect rules for
pages that moved, including all of `/bosh/` to `bosh.io/docs`.

Leads to: [R-16](README.md#r-16) old URLs keep working. These redirects must be carried over,
not only new ones for the migration.

## What causes problems

### Bookbinder is no longer maintained

The pre-review of the RFC (comments on an earlier draft) agreed that
unmaintained dependencies are the main reason to move. Bookbinder's
[repository](https://github.com/pivotal-cf/bookbinder) was last updated in
October 2024 (checked 2026-10-10), and the book's container runs Ruby 2.6.9,
which reached its end of life in 2022.

Middleman itself still runs. A probe (a small test that answers one
question; [glossary](../glossary.md#probe)) built all five test pages with
Middleman 4.6.3 on Ruby 4.0.7 and no Bookbinder, using a short configuration
file and a small layout; every table matched the published page cell for
cell ([Middleman probe](../concepts/tables/probes/middleman/README.md)). So
the problem is Bookbinder and the old Ruby setup, not the page format.

Leads to: [R-12](README.md#r-12) one-command local preview. More broadly, this is the reason
to move at all, so it does not map to one requirement.

### Search

The RFC states "Search is broken or disabled" ([L21]).

Leads to: [R-18](README.md#r-18) full-text search.

**Not yet written:** what search does on `docs.cloudfoundry.org` today, and
since when.

### Markup that only browsers tolerate

Some HTML is malformed in ways browsers repair without a sign. A strict parse
of the test pages' tables found 5 of 12 not well-formed (well-formed: every
tag closed and nested properly, every attribute value quoted;
[glossary](../glossary.md#well-formed-markup)): an unclosed `<col>`, a
`<td>` never closed, `class=“table”` with typographic quotes, a row ending in
`</td>` instead of `</tr>`
([details](../concepts/tables/README.md#markup-that-only-browsers-tolerate)).
A survey of all 241 tables in the docs and tutorial repositories found
more: 5 tables
never close `<thead>`, 8 classes in typographic quotes, 1 class with a
mismatched quote, and cells ending in `</td` without `>`.

Strict tools fail on this markup (MDX stops the build) or change the text
without an error (Markdoc). MDX is Markdown that can also hold JSX, the
HTML-like syntax of the React library ([glossary](../glossary.md#mdx));
Markdoc is Markdown with `{% %}` tags ([glossary](../glossary.md#markdoc)).

Leads to: [R-24](README.md#r-24) markup cleanup before conversion.

### Column widths written four ways

Four of the five test pages set column widths, each a different way:
`<col width>`, `<th width>`, `<td width>` and `<th style="width:…">`. In
`troubleshooting_slow_requests` the same table shape appears six times with
widths on some rows and not others. The tables round (the first concept,
converted by hand in four candidate tools) found that a column's role (a
short key, a value, or prose) gives a better result than the written numbers.

Leads to: [R-03](README.md#r-03) column widths as hints, [R-09](README.md#r-09) table styles by class.

### HTML-valued and undefined variables

Some variables hold HTML: `route_services` is a whole
`<p class="note">` paragraph. Today it renders as markup; MDX, Markdoc and EJS
(a JavaScript templating syntax close to ERB; [glossary](../glossary.md#ejs))
escape it, so the reader would see the tags as text unless the conversion
handles it.

Two variables the test pages use, `metadata_ref` and `bosh_cli_link` (three
times), are defined nowhere in the book, so the published pages show empty
text in their place and nobody is told
([sources](../concepts/tables/source/SOURCES.md)).

Leads to: [R-04](README.md#r-04) variables everywhere.

### The copyright year changes on every build

The footer is written `&copy; <%= Time.now.year %> Cloud Foundry Foundation`
in the book's `_book-footer.erb`, so the year is the build date, whether or
not any content changed. A comparison of converted and published pages has
to allow for this. Whether the year should follow content changes instead is
an [open question](research-areas.md#should-the-copyright-year-follow-content-changes).

Leads to: [R-25](README.md#r-25) build-time values are expected differences.

### Hosting outside the community's GitHub organization

The RFC states: "The current hosting solution involves infrastructure managed
outside the community GitHub organization, leading to cost, access, and
governance concerns" ([L24]).

Leads to: [R-14](README.md#r-14) Docs WG approves and publishes, [R-27](README.md#r-27) a named owner for every
task.

**Not yet written:** where the site is hosted today, who pays for it, and who
controls the domain. The RFC asks the last one ([L178]).

[L20]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L20
[L21]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L21
[L24]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L24
[L54]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L54
[L178]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L178
