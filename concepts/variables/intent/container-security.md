# Intent: `container-security`

- Source: [`../source/container-security.html.md.erb`](../source/container-security.html.md.erb)
  (cloudfoundry/docs-cloudfoundry-concepts; every heading, and the bodies
  of four parts: [SOURCES](../source/SOURCES.md#notes))
- Published: <https://docs.cloudfoundry.org/concepts/container-security.html>
  (copy: [`../published/container-security.html`](../published/container-security.html))
- Variables file: [`container-security.vars`](container-security.vars);
  anchors: [`container-security.anchors`](container-security.anchors)

## Cases this page covers

- **Variables in link text**, in a paragraph and in a list item:
  `[<%= vars.app_runtime_abbr %> Security](security.html)`. 33 uses in the
  book.
- **A Markdown value at the end of a list item**, twice
  (`app_sec_groups_link`), the second time right after a text value
  (`<%= vars.app_sec_groups_default %> <%= vars.app_sec_groups_link %>`),
  so that the whole list item is two values.
- **An HTML value at the end of a list item** (`container_network_link`).
- **A variable in a heading** with an explicit id, and the page's first
  sentence starting with a variable's text.
- **A value whose link reaches its page only through a redirect**:
  `../adminguide/app-sec-groups.html` is redirected to `/concepts/asg.html`
  ([`redirects.rb` L92](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L92)).

## Variables to keep

| # | Variable | Value | Place | Renders as | Source |
|---|----------|-------|-------|------------|--------|
| 1 | `app_runtime_first` | `Cloud Foundry` ([L22](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L22)) | the first sentence | Cloud Foundry | [L6](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/container-security.html.md.erb#L6) |
| 2, 3 | `app_runtime_abbr` | `Cloud Foundry` | text, and the text of a link to `security.html` | Cloud Foundry | [L9](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/container-security.html.md.erb#L9) |
| 4–6 | `app_runtime_abbr` | `Cloud Foundry` | list items, once in a link's text | Cloud Foundry | [L15](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/container-security.html.md.erb#L15), [L17](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/container-security.html.md.erb#L17) |
| 7 | `app_runtime_abbr` | `Cloud Foundry` | the heading `## <a id='networking'></a> Inbound and outbound traffic from …` | Inbound and outbound traffic from Cloud Foundry | [L147](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/container-security.html.md.erb#L147) |
| 8–11 | `app_runtime_abbr` | `Cloud Foundry` | text and list items | Cloud Foundry | L149, L177, L183 (twice) |
| 12 | `app_sec_groups_link` | `For more information about ASGs, see [App Security Groups](../adminguide/app-sec-groups.html).` ([L60](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L60)) | end of a list item | a sentence with a link | [L181](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/container-security.html.md.erb#L181) |
| 13 | `container_network_link` | `For information about administering container-to-container network policies, see <a href="../devguide/deploy-apps/cf-networking.html">Configuring Container-to-Container Networking</a>.` ([L93](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L93)) | end of a list item | a sentence with a link | [L183](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/container-security.html.md.erb#L183) |
| 14 | `app_runtime_abbr` | `Cloud Foundry` | the start of a paragraph | Cloud Foundry | [L187](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/container-security.html.md.erb#L187) |
| 15, 16 | `app_sec_groups_default`, `app_sec_groups_link` | text ([L59](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L59)), then as 12 | a whole list item | two sentences, the last with a link | [L193](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/container-security.html.md.erb#L193) |

## What a conversion must keep

- **Each value's text in its place, its links as links**
  ([published copy](../published/container-security.html), lines 764,
  765 and 775).
- **The heading's text** in the heading and the table of contents, and its
  id `networking`; the link `[Inbound and Outbound Traffic from …](#networking)`
  above it keeps working.
- **Any page description** a tool writes from the first sentence shows the
  value, not the variable.

## Cleanup and deviations

- **Link targets**: the check accepts a target that ends in the value's
  path. The redirect target is the cross-repository links concept's.
- **No deviation** from the published text.
