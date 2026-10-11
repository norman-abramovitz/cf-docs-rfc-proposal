# Intent: `routes-domains`

- Source: [`../../headings/source/routes-domains.html.md.erb`](../../headings/source/routes-domains.html.md.erb)
  (cloudfoundry/docs-dev-guide), the Domains section, the headings round's
  excerpt ([headings intent](../../headings/intent/routes-domains.md))
- Published: <https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html>
  (copy: [`../../headings/published/routes-domains.html`](../../headings/published/routes-domains.html))
- Notes file (what the check compares): [`routes-domains.notes`](routes-domains.notes)

## Cases this page covers

- **The common shapes:** `<p class="note">` and `<p class="note important">`
  holding one paragraph with code and a link, the most common note in the
  book ([survey](../survey/README.md#the-books-notes)).
- **`<div class="note">`** written with the same title span, twice.
- **Two notes in a row** (notes 1 and 2), with nothing between them.
- **Reuse.** The page was converted in the headings round, with its notes
  left as HTML. Decision (this round): it was reused because it qualified,
  and its converted pages became this round's passthrough pages as they
  were.

## Notes to keep

| # | Kind | Title | Sits in | Holds | Source |
|---|------|-------|---------|-------|--------|
| 1 | note | Note | "Create a shared domain" (`h4`) | 1 paragraph, 2 code spans, 1 link | [L736-L739](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L736-L739) |
| 2 | important | Important | "Create a shared domain" (`h4`), right after note 1 | 1 sentence | [L741-L744](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L741-L744) |
| 3 | note | Note | "Create a private domain" (`h4`) | 1 paragraph, 2 code spans, 1 link | [L784-L787](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L784-L787) |
| 4 | note | Note (`div`) | "Configuring DNS for your registered root domain" (`h3`) | 1 sentence | [L908-L911](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L908-L911) |
| 5 | important | Important (`div`) | the same section, after its table | 2 sentences, 1 link | [L933-L938](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L933-L938) |

## What a conversion must keep

Kind, title, words, code, links and place, as for every page; the
headings round's outline and anchors stay as that round left them (the
outline check runs with the same anchors file).

## Cleanup and deviations

None. The notes are well-formed.
