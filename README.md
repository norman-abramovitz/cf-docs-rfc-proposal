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

## Contents

- [Concepts](concepts/README.md): the migration worked one documentation
  concept at a time, each converted by hand into the candidate tools.
- [Tables](concepts/tables/README.md): the first concept, done; results across
  the tools in [concepts/tables/results.md](concepts/tables/results.md#summary).

## Related

- [Docs Working Group charter](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/docs.md)
- [RFC: Cloud Foundry documentation modernization (#1642)](https://github.com/cloudfoundry/community/pull/1642)
- [docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry)
