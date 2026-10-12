# Intent: `troubleshooting-router-error-responses`

- Source: the variables round's copy,
  [`../../variables/source/troubleshooting-router-error-responses.html.md.erb`](../../variables/source/troubleshooting-router-error-responses.html.md.erb),
  cloudfoundry/docs-cf-admin, published under `adminguide/`
  ([`config.yml` L33-L36](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml#L33-L36))
- Published: <https://docs.cloudfoundry.org/adminguide/troubleshooting-router-error-responses.html>
  (copy: [`../../variables/published/troubleshooting-router-error-responses.html`](../../variables/published/troubleshooting-router-error-responses.html))
- Links file: [`troubleshooting-router-error-responses.links`](troubleshooting-router-error-responses.links);
  anchors: [`troubleshooting-router-error-responses.anchors`](troubleshooting-router-error-responses.anchors)

## Cases this page covers

- **The other end of a two-way pair**: this page links to `http-routing`
  three times, and `http-routing` links back.
- **A link whose target is a variable**,
  `[metrics](<%= vars.gorouter_metrics_link %>)`, whose value is
  `../running/all_metrics.html#routing`
  ([L341](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L341)),
  into a third repository, docs-running-cf. It is one of three variable
  link targets in the book's pages
  ([variables survey](../../variables/survey/README.md)).
- **Three links already broken in the book**, kept as written:
  - `#gorouter-errors` (line 17): no such id; the section "Diagnose Gorouter
    errors" has the id `gorouter`.
  - `#tls-to-back-end` (line 204): an in-page link to an id this page does
    not have; `http-routing` has it, and line 234 links there.
  - `../concepts/http-routing.html#with-tls` (line 291): `http-routing` has
    no `with-tls` id (its ids are listed in the [intent](http-routing.md)).
  The live pages lack these ids as well
  ([spot check](../survey/spot-check.txt)). Which id each link was meant for
  is this round's reading, not recorded history.
- **An external link** to GitHub, which no check follows.

## What a conversion must keep

| Line | Link text | As written | Kind | Target | Repository | Expect |
|---|---|---|---|---|---|---|
| 17 | Diagnose Gorouter Errors | `#gorouter-errors` | Markdown, in-page | `adminguide/troubleshooting-router-error-responses`#gorouter-errors | — | no anchor |
| 18 | Diagnose Stale Routes in Gorouter | `#diagnose-stale-routes` | Markdown, in-page | (this page)#diagnose-stale-routes | — | resolves |
| 19 | Gorouter Error Classification Table | `#gorouter-error-classification` | Markdown, in-page | (this page)#gorouter-error-classification | — | resolves |
| 21 | Diagnose App Errors | `#app-errors` | Markdown, in-page | (this page)#app-errors | — | resolves |
| 23 | General Debugging Steps | `#debugging-steps` | Markdown, in-page | (this page)#debugging-steps | — | resolves |
| 33 | Dynamic Routing Table | `https://github.com/cloudfoundry/gorouter#dynamic-routing-table` | Markdown, external | — | — | external |
| 35 | HTTP Headers for Zipkin Tracing | `../concepts/http-routing.html#zipkin-headers` | Markdown, page-relative | `concepts/http-routing`#zipkin-headers | docs-cloudfoundry-concepts | resolves |
| 40 | metrics | `<%= vars.gorouter_metrics_link %>` = `../running/all_metrics.html#routing` | Markdown, variable target, page-relative | `running/all_metrics`#routing | docs-running-cf | resolves |
| 173 | Identity-aware routing | `../concepts/identity-aware-routing.html` | Markdown, page-relative | `concepts/identity-aware-routing` | docs-cloudfoundry-concepts | resolves |
| 204 | route-integrity | `#tls-to-back-end` | Markdown, in-page | (this page)#tls-to-back-end | — | no anchor |
| 234 | TLS to apps and other back end services | `../concepts/http-routing.html#tls-to-back-end` | Markdown, page-relative | `concepts/http-routing`#tls-to-back-end | docs-cloudfoundry-concepts | resolves |
| 291 | With TLS Enabled | `../concepts/http-routing.html#with-tls` | Markdown, page-relative | `concepts/http-routing`#with-tls | docs-cloudfoundry-concepts | no anchor |

The page keeps all 17 headings of the published page, the last one,
"Gorouter specific response headers", with the id the book generates for
it, `gorouter-specific-response-headers`.

## Cleanup and deviations

- `<%= vars.gather_routing_logs %>` (line 29) names no key of the book's
  variables file and is removed (variables round, accepted answer 2).
- The note under step 1 of "How to fix stale routes" is left out.
- Decision (this round): the three broken links are converted as written,
  not fixed, so the checks show how each tool reports them. Fixing them is
  a change at the source, to list with the
  [headings round's broken links](../../headings/broken-links.md).
