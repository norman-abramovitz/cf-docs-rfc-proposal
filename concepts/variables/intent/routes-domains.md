# Intent: `routes-domains`, Domains section

- Source: [`../../headings/source/routes-domains.html.md.erb`](../../headings/source/routes-domains.html.md.erb)
  (cloudfoundry/docs-dev-guide; the Domains section, lines 688–961, the
  headings round's excerpt)
- Published: <https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html>
  (copy: [`../../headings/published/routes-domains.html`](../../headings/published/routes-domains.html))
- Variables file: [`routes-domains.vars`](routes-domains.vars), 50 uses;
  anchors: the headings round's
  [`routes-domains.anchors`](../../headings/intent/routes-domains.anchors);
  notes: the notes round's [`routes-domains.notes`](../../notes/intent/routes-domains.notes)

## Cases this page covers

- **Variables in code**: 10 in fenced code blocks (`$ cf create-shared-domain <%= vars.app_domain %>`),
  12 in inline code. The book has 92 uses in
  fenced code, 98 in inline code and 44 in `<pre>`
  ([survey](../survey/README.md#where-variables-sit)).
- **Variables in HTML table cells**, header cells included (`<th>Target in <%= vars.app_runtime_abbr %></th>`).
- **Two variables that are not defined**, `domains_on_hosted` and
  `dns_warning`, each a paragraph of its own.
- **Example domains**: `app_domain`, `private_app_domain`,
  `tcp_app_domain`, three of the 174 uses of example-domain variables.
- The page was converted in the headings and notes rounds; only its
  variables change here.

## Variables to keep

By place (each line of [`routes-domains.vars`](routes-domains.vars) names
the source line):

| Place | Uses | Variables | Renders as |
|-------|------|-----------|------------|
| text | 16 | `app_runtime_abbr`, `app_domain` | Cloud Foundry, shared-domain.example.com |
| fenced code block | 10 | `app_domain`, `tcp_app_domain`, `private_app_domain` | shared-domain.example.com, tcp-domain.example.com, private-domain.example.com |
| inline code | 12 | `app_domain`, `tcp_app_domain`, `private_app_domain` | as above, with prefixes (`foo.example-app.shared-domain.example.com`) |
| HTML table cell | 8 | `app_domain`, `private_app_domain` | as above |
| HTML header cell | 2 | `app_runtime_abbr` | Target in Cloud Foundry |
| not defined | 2 | `domains_on_hosted`, `dns_warning` | nothing |

## What a conversion must keep

- **Each value in its code block**, the block still a code block of its
  type (`console`), so that a reader can copy the command
  ([R-06](../../../requirements/README.md#r-06) typed code blocks).
- **Each value in its inline code and table cell.**
- **Nothing where the undefined variables are.**
- The headings round's outline and anchors, and the notes round's notes.

## Cleanup and deviations

- **"Cloud Foundryrouters".** The source writes
  `<%= vars.app_runtime_abbr %>routers` with no space
  ([L693](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L693)),
  and the published page reads "Cloud Foundryrouters". Kept as written; a
  fix belongs to the page's owners.
- **The undefined variables**: removed in native mode.
- **No deviation** from the published text.
