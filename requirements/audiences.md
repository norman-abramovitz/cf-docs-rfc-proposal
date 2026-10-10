# Audiences

Status: draft Docs WG position, incomplete — covers what is known as of 2026-10-10.

Who changes the Cloud Foundry docs, who else depends on them, and what each
group needs. Needs are given as requirement IDs from the
[requirement list](README.md#requirements), such as "R-15 URL identifies the
source".

This page does not say which working group owns which part of the docs. A
working group is one of the Cloud Foundry community's standing teams, each
with a charter. Mapping areas to owners is the inventory the RFC asks for in
its first phase ([L112], [L114]), and is not done yet.

## Summary

| Audience | Changes the docs? | Main needs |
|---|---|---|
| [Docs WG lead and approvers](#docs-wg-lead-and-approvers) | yes, and publishes them | R-14, R-09, R-11, R-12, R-22, R-27, R-28 |
| [Working-group content owners](#working-group-content-owners) | yes, in their areas | R-17, R-26, R-13, R-11, R-12 |
| [Occasional contributors](#occasional-contributors) | yes, small fixes | R-15, R-12, R-10, R-11 |
| [UAA and CredHub API doc maintainers](#uaa-and-credhub-api-doc-maintainers) | yes, from code | R-29, R-08, R-16 |
| [bosh.io maintainers](#boshio-maintainers) | yes, on a separate site | R-09, R-07 (scope open) |
| [Central migration team](#central-migration-team) | once, all of it | R-23, R-24, R-01, R-25, R-04, R-05, R-08 |
| [Downstream consumers](#downstream-consumers) | no, they reuse it | R-16, R-15 |
| [Readers](#readers) | no | R-18, R-16, R-02, R-06, R-07 |
| [Search engines and AI-based tools](#search-engines-and-ai-based-tools) | no | R-20, R-16 |

## Who changes the docs

### Docs WG lead and approvers

The Docs WG is the working group for the Cloud Foundry docs. Its
[charter](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/docs.md)
lists in its scope "Merge and edit all doc changes" and "Maintain internal
consistency of doc style, including Notes and tables". The book's
[README](https://github.com/cloudfoundry/docs-book-cloudfoundry) states how
it works today: "Only the CFF Docs WG lead can merge pull requests, build to
staging, and publish the documentation." (CFF is the Cloud Foundry
Foundation; the book is the configuration that collects the content
repositories into one site.)

Needs:

- R-14 Docs WG approves and publishes: merging and publishing stay with the
  Docs WG ([L54]).
- R-09 table styles by class, R-07 notes and admonitions: the consistent
  style the charter asks for has to be something the site's template
  (the shared layout and stylesheet every page uses) can apply.
- R-11 readable source and R-12 one-command local preview: the lead reviews
  every pull request ([L82]) and needs to read the source and see the result.
- R-22 spellcheck with a shared dictionary: the Docs WG maintains the
  dictionary ([L96]).
- R-28 onboarding before cutover: current maintainers learn the new
  toolchain before it replaces the old one ([L115]).
- R-27 a named owner for every task: the Docs WG lead asked in the RFC's
  pre-review (comments on an earlier draft) that every task and maintenance
  aspect have a specific assignment. The RFC still lists these as open
  questions ([L172], [L174], [L176]).

The RFC's proof of concept is to "Gather feedback from at least three active
CF documentation contributors" ([L125]). The Docs WG lead asked to be one of
them.

### Working-group content owners

Working groups that own documentation areas review changes to them. The RFC
assigns each area to a working group's GitHub team through a `CODEOWNERS`
file, a GitHub file that names who must review changes to which paths
([L75]). The Docs WG charter excludes one kind of content from its own
responsibility: "Be responsible for component level documentation (e.g.
Cloud Controller v3 docs)" is listed under Non-Goals, so that content belongs
to the teams that build the components.

Needs:

- R-17 an owner for every area, before the area migrates ([L114]).
- R-26 owner review of migrated pages ([L131]).
- R-13 no per-WG extensions: a working group can author its pages with the
  shared extensions (code the Docs WG adds to the build tool so it handles
  markup it lacks), and asks the Docs WG for a new one rather than writing
  its own.
- R-11 readable source and R-12 one-command local preview.

### Occasional contributors

Anyone who opens a pull request to fix a page: a typo, a changed command, an
outdated step.

Needs:

- R-15 URL identifies the source: today `docs.cloudfoundry.org/adminguide/metadata.html`
  is `metadata.html.md.erb` in `docs-cf-admin`, because the book's
  `config.yml` maps the `adminguide` directory to that repository. A
  contributor finds the file from the address bar.
- R-12 one-command local preview, without installing a language toolchain
  by hand.
- R-10 simple text plus HTML where needed, and R-11 readable source: the
  page source should look like the page.

### UAA and CredHub API doc maintainers

UAA (the Cloud Foundry login and token service) and CredHub (the credential
store used by Cloud Foundry and BOSH) publish API reference docs built from their code, not from the book.
The UAA API docs live in the `cloudfoundry/uaa` repository and are built with
Slate, a generator for one-page API references
([glossary](../glossary.md#slate)), from examples that Spring REST Docs
writes while the API tests run ([glossary](../glossary.md#spring-rest-docs)).
CredHub also uses Spring REST Docs. CredHub's prose pages in its own `docs/`
folder are separate from the book's `docs-credhub` repository.

Book pages link to both references under `docs.cloudfoundry.org/api/uaa/`
and `docs.cloudfoundry.org/api/credhub/`, and to versioned UAA pages such as
`api/uaa/version/73.7.0/`, so the UAA reference already publishes
versions.

The RFC covers "CF, UAA API" ([L13]) and asks "Who can we involve to vet this
proposal for the UAA API docs and the CredHub API docs?" ([L177]).

Needs:

- R-29 API docs in the same pipeline: the Docs WG lead asked in the
  pre-review that the UAA API docs go through the same pipeline as the CF
  docs.
- R-08 cross-repository links and R-16 old URLs keep working: book pages
  link into the API references, including versioned UAA addresses.

**Not yet written:** where the CredHub API docs are built and published
today, and whether either API reference must change format to join the
pipeline.

### bosh.io maintainers

The BOSH docs at `bosh.io/docs` are a separate site built from
[docs-bosh](https://github.com/cloudfoundry/docs-bosh) with MkDocs and its
Material theme ([glossary](../glossary.md#mkdocs-material)), not by the book.
They are owned by the Foundational Infrastructure working group (FI WG;
[charter](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/foundational-infrastructure.md)).
The site has 40 tables, all plain Markdown pipe tables (rows written on one
line each, with `|` between cells), and 302 admonitions (boxed callouts
headed Note, Warning, and so on). The RFC does
not mention bosh.io.

Draft position: bosh.io follows the Docs WG's table and note conventions
(R-09, R-07). Whether bosh.io moves to a new tool or into the new site is the
FI WG's decision; the Docs WG can advise. See
[Research areas](research-areas.md#is-boshio-in-scope).

### Central migration team

The RFC requires that "The conversion MUST be done by one central migration
team to ensure consistency, not by each Working Group individually" ([L131]).
Who staffs it is an open question in the RFC ([L174]).

Needs:

- R-23 one central conversion: one set of rules, applied the same way to
  every repository.
- R-24 markup cleanup before conversion: the source has HTML that browsers
  accept and strict parsers reject.
- R-01 content and outline survive, checked automatically against the
  published pages, with R-25 build-time values are expected differences.
- R-04 variables everywhere, R-05 partials and reuse, R-08 cross-repository
  links: the parts of a page that a conversion most often breaks.

How the team converts: [Migration](migration.md).

### Downstream consumers

The RFC asks that "Working Group leads and known downstream consumers (e.g.,
SAP BTP, anynines, …; VMware Tanzu works from its own branches and is not
affected) SHOULD be asked whether they consume the CF docs as-is or maintain
their own derivative documentation" ([L113]). In the pre-review the Docs WG
lead added that Broadcom's docs are written fully in-house and do not rely on
the CF doc repositories. The RFC's open questions still name VMware Tanzu as
a downstream distribution ([L168]), which does not match [L113].

Needs:

- R-16 old URLs keep working, for anyone who links to the docs.
- R-15 URL identifies the source, for anyone who copies pages.

**Not yet written:** what each downstream consumer reuses (raw source or
published HTML). That comes from the survey at [L113].

## Also affected: people and programs that read the docs

### Readers

People who use Cloud Foundry and read the docs to do so.

Needs: R-18 full-text search, R-16 old URLs keep working (bookmarks and links
from other sites), R-02 rich tables, R-06 typed code blocks, R-07 notes and
admonitions.

### Search engines and AI-based tools

Search engines, and what the RFC calls "AI-based developer tools" ([L22]):
programs that read the published docs to answer developers' questions.

Needs: R-20 search-engine and AI-friendly output, R-16 old URLs keep working.

[L13]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L13
[L22]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L22
[L54]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L54
[L75]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L75
[L82]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L82
[L96]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L96
[L112]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L112
[L113]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L113
[L114]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L114
[L115]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L115
[L125]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L125
[L131]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L131
[L168]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L168
[L172]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L172
[L174]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L174
[L176]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L176
[L177]: https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md#L177
