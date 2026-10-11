# Intent: `all_metrics`

- Source: [`../source/all_metrics.html.md.erb`](../source/all_metrics.html.md.erb)
  (cloudfoundry/docs-running-cf; the whole page without the eight lines
  that include its metric tables as partials:
  [SOURCES](../source/SOURCES.md#notes))
- Published: <https://docs.cloudfoundry.org/running/all_metrics.html>
  (copy: [`../published/all_metrics.html`](../published/all_metrics.html))
- Variables file: [`all_metrics.vars`](all_metrics.vars);
  anchors: [`all_metrics.anchors`](all_metrics.anchors)

## Cases this page covers

- **A page title set from a variable.** The page's front matter says
  `title: Cloud Foundry component metrics`; line 6 replaces it with ERB
  code, `<% current_page.data.title = vars.app_runtime_abbr + " Component Metrics" %>`.
  It is the only page in the book that sets its title from a variable, and
  the only `<% %>` tag (code, not output) that reads one
  ([survey](../survey/README.md#where-variables-sit)). No front matter in
  the book holds a variable.

## Variables to keep

| # | Variable | Value | Place | Renders as | Source |
|---|----------|-------|-------|------------|--------|
| 1 | `app_runtime_abbr` | `Cloud Foundry` ([L25](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L25)) | the page title, by code | `<title>` "Cloud Foundry Component Metrics \| Cloud Foundry Docs" and the page's `h1` "Cloud Foundry Component Metrics" | [L6](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/all_metrics.html.md.erb#L6) |

The published page shows the title the code sets
([published copy](../published/all_metrics.html), lines 11 and 512):
Middleman renders the page body before its layout, so the layout's
`current_page.data.title`
([`layout.erb` L11-L12](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/layout.erb#L11-L12))
reads the new value.

## What a conversion must keep

- **The title "Cloud Foundry Component Metrics"** in the page's `<title>`
  and its heading. The check looks for it in both.
- **No code in the page**: the line that sets the title has no place in
  any tool's page format.

## Cleanup and deviations

- **The front matter's title** ("component metrics", lower case) is not
  what readers see; the converted title is the one the code sets.
  Decision (this round): the title takes the code's value; where a tool's
  front matter cannot hold a variable, the converter writes the value.
- **The metric tables** come from eight partials and are left out; the
  partials round owns them.
