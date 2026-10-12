# Intent: `routes-domains`

- Source: the headings round's copy,
  [`../../headings/source/routes-domains.html.md.erb`](../../headings/source/routes-domains.html.md.erb),
  and the partials round's copy of the partial it includes,
  [`_routing_conflict`](../../partials/source/_routing_conflict.html.md.erb);
  cloudfoundry/docs-dev-guide, published under `devguide/`
  ([`config.yml` L62-L65](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml#L62-L65))
- Published: <https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html>
  (copy: [`../../headings/published/routes-domains.html`](../../headings/published/routes-domains.html))
- Links file: [`routes-domains.links`](routes-domains.links); anchors:
  [`routes-domains.anchors`](routes-domains.anchors)

## Cases this page covers

- **A page two folders deep** (`devguide/deploy-apps/`), so its links into
  other repositories go up two levels (`../../concepts/…`).
- **The target of the links from `enabling-tcp-routing`**: `create-route`,
  `domains` and `create-route-with-port`. The last id is on an HTML `<h4>`
  in the source, which the headings round's convention writes as the
  tool's heading.
- **An HTML link** that goes up one level and back into its own repository
  (`<a href="../custom-ports.html">`, line 66). In the book, HTML links are
  published as written, while Markdown links that resolve are published
  root-relative ([survey](../survey/README.md#how-the-book-builds-a-link)).
- **A link inside a partial**: `_routing_conflict` links to
  `./blue-green.html`; the book resolves it against this page's folder.
- **Two links already broken in the book**, kept as written:
  `#http-vs-tcp-shared-domains` (line 62; the id became
  `http-vs-tcp-domains` in 2023,
  [headings round](../../headings/broken-links.md#routes-domains)), and
  `../deploy-apps/manifest.html#routes` (line 402; `manifest.html` has no
  `routes` id; the id is on `manifest-attributes.html`,
  [L567](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/manifest-attributes.html.md.erb#L567)).

## What a conversion must keep

| Line | Link text | As written | Kind | Target | Repository | Expect |
|---|---|---|---|---|---|---|
| 8 | HTTP routing | `../../concepts/http-routing.html` | Markdown, page-relative | `concepts/http-routing` | docs-cloudfoundry-concepts | resolves |
| 49 | round-robin | `../../concepts/http-routing.html#round-robin` | Markdown, page-relative | `concepts/http-routing`#round-robin | docs-cloudfoundry-concepts | resolves |
| 54 | Share a route with another space | `#share-route` | Markdown, in-page | (this page)#share-route | — | resolves |
| 62 | HTTP versus TCP shared domains | `#http-vs-tcp-shared-domains` | Markdown, in-page | (this page)#http-vs-tcp-shared-domains | — | no anchor |
| 66 | Configuring apps to listen on custom ports (Beta) | `../custom-ports.html` | HTML `<a>`, page-relative | `devguide/custom-ports` | docs-dev-guide | resolves |
| 402 | Deploying with app manifests | `../deploy-apps/manifest.html#routes` | Markdown, page-relative | `devguide/deploy-apps/manifest`#routes | docs-dev-guide | no anchor |
| 406 (partial, line 1) | Using blue-green deployment to reduce downtime and risk | `./blue-green.html` | Markdown in a partial, page-relative | `devguide/deploy-apps/blue-green` | docs-dev-guide | resolves |
| 408 | Routing conflict | `troubleshoot-app-health.html#routing-conflict` | Markdown, page-relative | `devguide/deploy-apps/troubleshoot-app-health`#routing-conflict | docs-dev-guide | resolves |

The page keeps all 43 headings of the published page.

## Cleanup and deviations

- The partial `_routing_conflict` is written in place
  ([SOURCES](../source/SOURCES.md#notes)).
