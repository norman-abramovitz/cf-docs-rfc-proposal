# Intent: `enabling-tcp-routing`

- Source: the partials round's copy,
  [`../../partials/source/enabling-tcp-routing.html.md.erb`](../../partials/source/enabling-tcp-routing.html.md.erb),
  cloudfoundry/docs-cf-admin, published under `adminguide/`
  ([`config.yml` L33-L36](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml#L33-L36))
- Published: <https://docs.cloudfoundry.org/adminguide/enabling-tcp-routing.html>
  (copy: [`../../partials/published/enabling-tcp-routing.html`](../../partials/published/enabling-tcp-routing.html))
- Links file: [`enabling-tcp-routing.links`](enabling-tcp-routing.links);
  anchors: [`enabling-tcp-routing.anchors`](enabling-tcp-routing.anchors)

## Cases this page covers

- **Links into another repository with anchors**: three links to ids on
  `routes-domains` (docs-dev-guide), a test page, so the anchors are the
  converted page's own.
- **A fourth repository**: `../cf-cli/index.html`, docs-cf-cli, a folder's
  index page.
- **A link inside a list item** whose paragraph is indented under the item
  (line 55).
- **A link to a page in the same folder** written with no path
  (`quota-plans.html`), and an in-page link.

## What a conversion must keep

| Line | Link text | As written | Kind | Target | Repository | Expect |
|---|---|---|---|---|---|---|
| 25 | Create a Route | `../devguide/deploy-apps/routes-domains.html#create-route` | Markdown, page-relative | `devguide/deploy-apps/routes-domains`#create-route | docs-dev-guide | resolves |
| 55 | Configuring Apps to Listen on Custom Ports (Beta) | `../devguide/custom-ports.html` | Markdown, page-relative | `devguide/custom-ports` | docs-dev-guide | resolves |
| 72 | Domains | `../devguide/deploy-apps/routes-domains.html#domains` | Markdown, page-relative | `devguide/deploy-apps/routes-domains`#domains | docs-dev-guide | resolves |
| 120 | Using the Cloud Foundry Command Line Interface (cf CLI) | `../cf-cli/index.html` | Markdown, page-relative | `cf-cli` | docs-cf-cli | resolves |
| 126 | Prerequisites for Enabling TCP Routing | `#prerequisites` | Markdown, in-page | (this page)#prerequisites | — | resolves |
| 161 | Creating and Modifying Quota Plans | `quota-plans.html` | Markdown, page-relative | `adminguide/quota-plans` | docs-cf-admin | resolves |
| 222 | Create a TCP Route with a Port | `../devguide/deploy-apps/routes-domains.html#create-route-with-port` | Markdown, page-relative | `devguide/deploy-apps/routes-domains`#create-route-with-port | docs-dev-guide | resolves |

The link at line 120 starts on line 120 and ends on line 121; its text
runs across the line break. The page keeps all 11 headings of the
published page.

## Cleanup and deviations

- The partial `_tcp_modify_ports` and the note held in
  `vars.mutual_tls_tcp` are outside the excerpt (the partials round
  converted them).
