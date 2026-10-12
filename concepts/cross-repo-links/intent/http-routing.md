# Intent: `http-routing`

- Source: [`../source/http-routing.html.md.erb`](../source/http-routing.html.md.erb),
  cloudfoundry/docs-cloudfoundry-concepts, published under `concepts/`
  (the book's [`config.yml` L43-L46](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml#L43-L46))
- Published: <https://docs.cloudfoundry.org/concepts/http-routing.html>
  (copy: [`../published/http-routing.html`](../published/http-routing.html))
- Links file: [`http-routing.links`](http-routing.links); anchors:
  [`http-routing.anchors`](http-routing.anchors)

## Cases this page covers

- **Links out of one repository into two others**: docs-cf-admin
  (`adminguide/`) and docs-dev-guide (`devguide/`), written page-relative,
  one level up (`../adminguide/…`).
- **Links held in variables**, in three values whose text is a sentence
  with a Markdown link: `http_routing`, `zipkin_tracing_link` and
  `port_limitations_1` (relative), and `keepalive`, a root-relative link
  back to this page's own section
  ([`template_variables.yml` L185, L189, L223, L362](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L185)).
  `port_limitations_1` is the same sentence as `port_limitations`
  ([L222](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L222))
  with one `../` fewer, for pages one folder less deep.
- **An absolute link to docs.cloudfoundry.org** in an HTML `<a>`
  ([L167](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/http-routing.html.md.erb#L167)).
- **A link into a folder's index page**, `architecture/index.html#routing`,
  which the published page writes as `/concepts/architecture/#routing`
  ([published copy, line 564](../published/http-routing.html)).
- **In-page links** to three ids, and ids that the other test pages link
  to (`zipkin-headers`, `tls-to-back-end`, `round-robin`).

## What a conversion must keep

Every link resolves to its target page and anchor. Targets outside the four
test pages are stub pages ([SOURCES](../source/SOURCES.md#notes)).

| Line | Link text | As written | Kind | Target | Repository | Expect |
|---|---|---|---|---|---|---|
| 9 | Routing | `architecture/index.html#routing` | Markdown, page-relative | `concepts/architecture`#routing | docs-cloudfoundry-concepts | resolves |
| 44 | Securing Traffic into Cloud Foundry | `vars.http_routing`: `../adminguide/securing-traffic.html` | Markdown in a variable, page-relative | `adminguide/securing-traffic` | docs-cf-admin | resolves |
| 65 | Enabling Zipkin Tracing | `vars.zipkin_tracing_link`: `../adminguide/zipkin_tracing.html` | Markdown in a variable, page-relative | `adminguide/zipkin_tracing` | docs-cf-admin | resolves |
| 72 | Unique trace identification | `../adminguide/distributed-tracing.html#unique-trace-id` | Markdown, page-relative | `adminguide/distributed-tracing`#unique-trace-id | docs-cf-admin | resolves |
| 167 | multiple processes | `https://docs.cloudfoundry.org/devguide/multiple-processes.html` | HTML `<a>`, absolute | `devguide/multiple-processes` | docs-dev-guide | resolves |
| 352 | Configuring per-route options | `../devguide/custom-per-route-options.html` | Markdown, page-relative | `devguide/custom-per-route-options` | docs-dev-guide | resolves |
| 356 | Round-Robin Load Balancing | `#round-robin` | Markdown, in-page | `concepts/http-routing`#round-robin | — | resolves |
| 358 | Least-Connection Load Balancing | `#least-connection` | Markdown, in-page | `concepts/http-routing`#least-connection | — | resolves |
| 370 | Load Balancing AZ Preference | `#balancing-algorithm-az-preference` | Markdown, in-page | `concepts/http-routing`#balancing-algorithm-az-preference | — | resolves |
| 403 | Supporting WebSockets | `vars.port_limitations_1`: `../adminguide/supporting-websockets.html` | Markdown in a variable, page-relative | `adminguide/supporting-websockets` | docs-cf-admin | resolves |
| 455 | Keep alive connections | `vars.keepalive`: `/concepts/http-routing.html#keepalive` | Markdown in a variable, root-relative | `concepts/http-routing`#keepalive | — | resolves |
| 492 | Troubleshooting Router Error Responses | `../adminguide/troubleshooting-router-error-responses.html` | Markdown, page-relative | `adminguide/troubleshooting-router-error-responses` | docs-cf-admin | resolves |

"Target" is the page key the [links check](../checks/links.py) reports: the
page's path without `.html` and without a final `/index`. The page keeps
all 28 headings of the published page, two of them from the partials
`_oss_xfcc_loadbalancer` and `_oss_xfcc_router`
([outline check](../../headings/checks/outline.py)).

## Cleanup and deviations

- The two partials, which hold one heading each, are written as their
  heading ([SOURCES](../source/SOURCES.md#notes)).
- The variables are written as their values (product names as text;
  link values as written in passthrough, in the tool's link form in native).
