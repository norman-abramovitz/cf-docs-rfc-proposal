# Intent: `troubleshooting-router-error-responses`

- Source: [`../source/troubleshooting-router-error-responses.html.md.erb`](../source/troubleshooting-router-error-responses.html.md.erb)
  (cloudfoundry/docs-cf-admin; every heading, and the bodies of four parts:
  [SOURCES](../source/SOURCES.md#notes))
- Published: <https://docs.cloudfoundry.org/adminguide/troubleshooting-router-error-responses.html>
  (copy: [`../published/troubleshooting-router-error-responses.html`](../published/troubleshooting-router-error-responses.html))
- Variables file: [`troubleshooting-router-error-responses.vars`](troubleshooting-router-error-responses.vars);
  anchors: [`troubleshooting-router-error-responses.anchors`](troubleshooting-router-error-responses.anchors)

## Cases this page covers

- **A variable as a link target**, twice, the only page in the book with
  both forms: in a Markdown link in a nested list, and in an HTML `href` in
  a table cell. Three uses in the book put a variable in a link target
  ([survey](../survey/README.md#where-variables-sit)). The value is a path
  relative to the page, `../running/all_metrics.html#routing`.
- **A variable in the page's first sentence**, which a tool that writes a
  page description from the first paragraph copies into it.
- **A variable in an HTML table cell** that runs over two lines.
- **A variable that is not defined**, `gather_routing_logs`, at the end of a
  list item.

## Variables to keep

| # | Variable | Value | Place | Renders as | Source |
|---|----------|-------|-------|------------|--------|
| 1 | `app_runtime_abbr` | `Cloud Foundry` ([L25](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L25)) | the first sentence | Cloud Foundry | [L7](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb#L7) |
| 2 | `gather_routing_logs` | not defined | end of the first item of an ordered list | nothing | [L29](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb#L29) |
| 3 | `gorouter_metrics_link` | `../running/all_metrics.html#routing` ([L341](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L341)) | the target of `[metrics](…)`, in a list nested in a list item | a link "metrics" to the Routing section of the metrics page | [L40](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb#L40) |
| 4 | `app_runtime_abbr` | `Cloud Foundry` | the `fatal` row's Examples cell, an HTML table | Cloud Foundry | [L60](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb#L60) |
| 5 | `gorouter_metrics_link` | as 3 | the `href` of `<a>` in the `unknown` row's Evidence cell | a link "Router Error: 502 Bad Gateway" | [L388](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb#L388) |

## What a conversion must keep

- **Both links**, with the value as their target
  ([published copy](../published/troubleshooting-router-error-responses.html),
  lines 590 and 958), and no variable syntax in any `href`.
- **The text with the value** in the first sentence and in the table cell,
  and in any page description the tool writes.
- **Nothing where the undefined variable is.**

## Cleanup and deviations

- **Link targets.** The published page writes the Markdown link as
  `/running/all_metrics.html#routing` and leaves the HTML one as written;
  the check accepts a target that ends in `running/all_metrics.html#routing`.
- **The tables**, in Docusaurus: `<tbody>` around the rows, as the tables
  round's cleanup does (without it React reports a hydration mismatch,
  [browser check](../results/browser-checks.txt)); the classification
  table's header cells, which sit in `<thead>` with no `<tr>`, get one; the
  Evidence cell that runs over four lines is written on one line, which
  MDX and Markdoc need ([notes round](../../notes/results.md#docusaurus-3102)).
- **The undefined variable**: removed in native mode, as on every page.
- **No deviation** from the published text.
