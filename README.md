# Cloud Foundry Documentation Modernization — RFC Proposal

Findings, proofs of concept, and working drafts for modernizing the Cloud
Foundry documentation stack.

## Background

The CF docs at `docs.cloudfoundry.org` are built by Bookbinder from
[docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry),
which collates the `docs-*` content repositories (`*.html.md.erb` sources)
into one site. Each repository maps to a fixed URL directory, so a page's URL
identifies the repository and file to edit.

[cloudfoundry/community#1642](https://github.com/cloudfoundry/community/pull/1642)
proposes moving this content to Markdown on a modern static site generator,
hosted on GitHub Pages. This repository holds the evidence gathered to inform
that proposal.

The RFC text is not the pull request's description; it is the one file the
pull request adds. Read it at:

- [the latest version](https://github.com/ZPascal/community/blob/cf-docs-rfc/toc/rfc/rfc-draft-new-cf-docs-stack.md)
  on the pull request's branch, or its
  [Files changed](https://github.com/cloudfoundry/community/pull/1642/files)
  tab, where comments and suggestions are made;
- [commit `c737539`](https://github.com/cloudfoundry/community/blob/c7375390fad8afff5a4c5f1b6c85749f2d649045/toc/rfc/rfc-draft-new-cf-docs-stack.md),
  the version these documents quote, line by line.

## Start here

Three draft documents, each readable on its own. They cover what is known
as of 2026-10-10 and mark what is not yet written.

1. [Requirements](requirements/README.md): what the Docs WG is looking for
   in a new documentation stack, with requirement IDs (R-01, R-02, …) that
   the other documents cite. A draft Docs WG position; it may be wrong.
2. [Tooling](tooling/README.md): the tools evaluated, the input formats they
   read, how today's pages convert into them, and the extensions each needs.
   Neutral evidence; it makes no choice.
3. [Proof-of-concept results](poc/README.md): what each tool built from real
   Cloud Foundry pages, next to the page as published today. Neutral
   evidence.

The [glossary](glossary.md) explains the terms further. Each document
defines its terms where it first uses them, so the glossary is optional.

## Contents

- [Concepts](concepts/README.md): the migration worked one documentation
  concept at a time, each converted by hand into the candidate tools.
- [Tables](concepts/tables/README.md): the first concept, done; results across
  the tools in [concepts/tables/results.md](concepts/tables/results.md#summary).

## Related

- [Docs Working Group charter](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/docs.md)
- [RFC: Cloud Foundry documentation modernization (#1642)](https://github.com/cloudfoundry/community/pull/1642)
  (pull request); [RFC text](https://github.com/ZPascal/community/blob/cf-docs-rfc/toc/rfc/rfc-draft-new-cf-docs-stack.md)
- [docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry)
