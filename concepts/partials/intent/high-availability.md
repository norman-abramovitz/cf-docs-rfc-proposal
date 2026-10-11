# Intent: `high-availability`

- Source: [`../source/high-availability.html.md.erb`](../source/high-availability.html.md.erb)
  and its partial [`../source/_oss_scale_table.html.md.erb`](../source/_oss_scale_table.html.md.erb),
  cloudfoundry/docs-cloudfoundry-concepts
- Excerpt: the section "Recommended instance counts for high availability"
  (lines 98–102), under the page's front matter ([SOURCES](../source/SOURCES.md#notes))
- Published: <https://docs.cloudfoundry.org/concepts/high-availability.html>
  (copy: [`../published/high-availability.html`](../published/high-availability.html))
- Partials file (what the check reads): [`high-availability.partials`](high-availability.partials);
  anchors: [`high-availability.anchors`](high-availability.anchors)

## Cases this page covers

- **A partial whose name the book also holds in a variable.** The page
  calls `<%= partial 'oss_scale_table' %>`
  ([L102](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/high-availability.html.md.erb#L102));
  the book also maps `scale_table: "oss_scale_table"`
  ([`template_variables.yml` L287](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L287)),
  which no page uses. The sites build the page twice: with the name
  written (passthrough, native) and with the name taken from the variable
  (variable mode), to show what each tool can do with
  `partial vars.scale_table`, the form the book used until 2023
  ([survey](../survey/README.md#history)).
- **A partial that holds a table and a variable** (`vars.recommended_by` in
  the NATS row), converted in the tables round.
- **An empty variable before the partial** (`scaling_ert`, defined with no
  value).

## What a conversion must keep

| Partial | Section | Place | Opens with | Ends with |
|---|---|---|---|---|
| `_oss_scale_table` | Recommended instance counts for high availability | body, then the table | "The following table provides recommended instance counts" | "regardless of the number of instances or AZs." |

- Nothing between the heading and the partial: the empty variable renders
  as nothing.
- The partial's variable renders its value ("Cloud Foundry recommends").
- The table itself follows the tables round's intent
  ([`_oss_scale_table`](../../tables/intent/_oss_scale_table.md)); its spot
  checks are not rerun here.

## Cleanup and deviations

- **None in this round.** The partial's own cleanup (`<col />` closed,
  `class="table"`) is the tables round's.
- **Variable mode** is not a source form at the surveyed commit: it is the
  test of `partial vars.scale_table`.
