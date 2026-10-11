# Intent: `troubleshoot-app-health` and `routes-domains`: one partial on two pages

- Sources: [`../source/troubleshoot-app-health.html.md.erb`](../source/troubleshoot-app-health.html.md.erb)
  (section "Routing conflict", lines 146–165) and the headings round's
  [`routes-domains`](../../headings/source/routes-domains.html.md.erb)
  (section "Map a route to multiple apps", lines 404–408); the partial
  [`_routing_conflict`](../source/_routing_conflict.html.md.erb);
  cloudfoundry/docs-dev-guide
- Published: <https://docs.cloudfoundry.org/devguide/deploy-apps/troubleshoot-app-health.html>
  (copy: [`../published/troubleshoot-app-health.html`](../published/troubleshoot-app-health.html))
  and the headings round's [`routes-domains`](../../headings/published/routes-domains.html)
- Partials files: [`troubleshoot-app-health.partials`](troubleshoot-app-health.partials),
  [`routes-domains.partials`](routes-domains.partials); anchors:
  [`troubleshoot-app-health.anchors`](troubleshoot-app-health.anchors),
  [`routes-domains.anchors`](routes-domains.anchors)

## Cases these pages cover

- **The one partial included from two pages**
  ([survey](../survey/README.md#findings)).
- **A variable in the partial** written without spaces,
  `<%=vars.product_short%>`, and a partial file without a final newline.
- **A shared partial in another content source.** No partial in the book
  reaches another repository today; before July 2026, 25 calls did, to
  another edition's folders ([survey](../survey/README.md#history)).
  Decision (this round): in native mode the partial lives in a second
  content source (a folder outside the docs, or an Antora component of its
  own), to test how each tool reaches it.
- **An HTML heading** above the partial on `routes-domains` (`<h4>`), which
  the headings round's convention writes as the tool's heading.

## What a conversion must keep

| Page | Section | Place | After the host's words | Before the host's words |
|---|---|---|---|---|
| troubleshoot-app-health | Routing conflict | body | the heading | "If you suspect a routing conflict" |
| routes-domains | Map a route to multiple apps | body | the heading | "For more information about troubleshooting this problem" |

The partial opens with "Cloud Foundry allows multiple apps, or versions of
the same app" (the variable's value) and ends with "to one of the apps on
the shared route."

## Cleanup and deviations

None. The links in the partial and on `routes-domains` lead outside the
excerpts; tools that check links report them.
