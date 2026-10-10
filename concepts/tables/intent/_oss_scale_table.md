# Intent: `_oss_scale_table` (partial)

- Source: [`../source/_oss_scale_table.html.md.erb`](../source/_oss_scale_table.html.md.erb)
- Included by `high-availability.html.md.erb` (docs-cloudfoundry-concepts, line 108)
- Published: <https://docs.cloudfoundry.org/concepts/high-availability.html>

## Table 1 — Component / Total Instances / Notes

Source: lines 5–83. Thirteen rows, one per component.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | header row | yes | `<thead>` |
| Table | row-header column | yes | column 1 names the component each row is about |
| Column 1 | role | key | component names |
| Column 1 | width | about 25% | `<col width="25%">` |
| Column 2 | role | value | short counts (`≥ 2`, `0 or 1`) |
| Column 2 | width | about 25% | `<col width="25%">` |
| Column 2 | wrap | avoid | `≥ 2` must not break between `≥` and `2` |
| Column 3 | role | prose | sentences, up to about 80 words |
| Column 3 | width | about 50% | `<col width="50%">` |

**Cleanup needed:** the three `<col width="…">` elements are not
self-closed (`<col>` is a void element). Browsers accept this; XML and JSX
parsers do not. The `width` attribute on `<col>` is also obsolete in current
HTML; the width hint carries the intent instead.

**Deviations:** the header cells wrap their text in `<strong>`. It is
dropped: bold header cells are a convention the template provides (see
[Template conventions](../README.md#template-conventions)). The header text is
unchanged. The table has no class; it gets `class="table"`, the standard
style, as every HTML table names its style.

### Spot checks

- [ ] 13 body rows, each with 3 cells.
- [ ] `≥` appears 12 times (source `&ge;`), never as the literal text `&ge;`.
- [ ] `<code>0</code>` in the PostgreSQL Server row renders as code.
- [ ] NATS Server row: "Cloud Foundry recommends scaling NATS VMs to 2 or more
      CPU." (`vars.recommended_by`).
- [ ] The Notes cells for MySQL Proxy and UAA are empty and the rows still have
      3 cells.
- [ ] The table renders inside its host page, after the host's introduction,
      not as a page of its own and not as a literal include line.
