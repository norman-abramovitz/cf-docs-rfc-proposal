# Migration

Status: draft Docs WG position, incomplete — covers what is known as of 2026-10-10.

The steps that take today's docs to the new site, and what each step must
achieve. This page says **what** each step does and which requirements it
serves ([requirement list](README.md#requirements)). **How** a step is done
in a given tool, and what that costs, is in [Tooling](../tooling/README.md).

## From today's book to the new shape

**Today.** About a dozen `docs-*` content repositories hold the pages as
`.html.md.erb` files: Markdown with HTML mixed in and ERB tags (Ruby's
templating syntax, `<%= … %>`; [glossary](../glossary.md#erb)). Bookbinder, a
Ruby tool ([glossary](../glossary.md#bookbinder)), collects the repositories
listed in the book's `config.yml` and builds one site. Each repository maps
to one URL directory. Pages share variables (named values defined once in
`template_variables.yml` and inserted at build time) and partials (files of
content included in other pages). The book also holds the layout, the
footer and about 85 redirect rules.

**The new shape, as far as it is known.**

- One repository holds all content ([L69]), with directories that keep
  today's URL mapping (R-15 URL identifies the source).
- A `CODEOWNERS` file (a GitHub file naming who must review changes to which
  paths) assigns each directory to its working group (R-17 an owner for
  every area).
- Pages are in a simple text format, with HTML where it falls short (R-10).
  Which format and which tool is open.
- The Docs WG reviews and publishes (R-14).

## Steps

### 1. Inventory

List every repository, page, partial, variable and redirect that feeds the
site, with the working group that owns each area. The RFC makes this the
first phase ([L112], [L114]). The inventory also records where each page's
URL comes from, so R-15 and R-16 can be checked later.

Serves: R-17 an owner for every area, R-15 URL identifies the source, R-16
old URLs keep working.

Done so far: a survey of every table in the docs and tutorial repositories
(241 tables), used to pick table styles.

**Not yet written:** the full inventory, and whether bosh.io and the UAA and
CredHub API references are in it ([research areas](research-areas.md#scope)).

### 2. Markup cleanup

Fix the HTML that browsers accept but strict parsers reject: unclosed
elements, typographic quotes around attribute values, rows that end with the
wrong tag. Strict tools either stop the build or change the text without an
error ([details](../concepts/tables/README.md#markup-that-only-browsers-tolerate)).
Each fix is recorded, so the owner review in step 5 can see it.

Serves: R-24 markup cleanup before conversion.

**Not yet written:** whether fixes go to today's repositories first (which
also fixes the published site) or are made only during conversion.

### 3. Conversion, one concept at a time

A concept is one documentation feature: tables, headings, variables,
partials, notes, code blocks, cross-repository links
([concepts](../concepts/README.md)). Each concept is first converted by hand
in the candidate tools, and the conventions that work are recorded. Those
conventions become the rules of `cf-docs-migrate`, a migration tool still to
be written:

- `scan` finds every instance of each concept across the content;
- `convert` applies the recorded rules to every page.

One central team runs the conversion the same way for every repository
([L131]). Where the source structure was chosen only for formatting, a
conversion may restructure it, and records the change as a deviation.

Serves: R-23 one central conversion, R-01 content and outline survive, R-04
variables everywhere, R-05 partials and reuse, R-07 notes and admonitions,
R-08 cross-repository links.

Done so far: tables, for the test pages
([tables concept](../concepts/tables/README.md)).

### 4. Automated content and outline check

Compare each converted page with the published page: its text, headings,
lists, tables and links. Differences that come from build time, such as the
copyright year in the footer and "Page last updated", are expected and not
reported. Recorded deviations from step 3 are listed apart.

Serves: R-01 content and outline survive, R-25 build-time values are
expected differences.

Done so far: per-page spot checks (checks every converted page must pass,
listed for each test page) and a word-by-word text comparison, used in the
tables round ([checks](../concepts/tables/checks/)).

### 5. Owner review

The owning working group reviews each migrated section, with the report from
step 4 and the list of deviations and cleanup fixes.

Serves: R-26 owner review of migrated pages.

**Not yet written:** what the owner signs off, and what happens when an owner
does not respond.

### 6. Redirects

Every published URL keeps working: today's redirect rules are carried over,
and every page whose address changes gets a new one. Heading anchors keep
their ids where the conversion can keep them.

Serves: R-16 old URLs keep working ([L46], [L61], [L137]).

### 7. Cutover

The new site goes live at `docs.cloudfoundry.org`; the old build system is
archived, not deleted; the old hosting is shut down after a stabilization
window, which the RFC suggests is 90 days ([L135]–[L138]). Current
maintainers have had time to learn the new toolchain before this step.

Serves: R-28 onboarding before cutover, R-14 Docs WG approves and publishes,
R-16 old URLs keep working.

## Not covered yet

**Not yet written:** the timeline, which the RFC requires to be "published
and agreed upon by all affected Working Groups" ([L131]); the order in which
repositories move; and how edits made to today's repositories during the
conversion reach the new site (a freeze, or converting again).

[L46]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L46
[L61]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L61
[L69]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L69
[L112]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L112
[L114]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L114
[L131]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L131
[L135]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L135
[L137]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L137
[L138]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L138
