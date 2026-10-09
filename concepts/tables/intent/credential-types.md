# Intent: `credential-types`

- Source: [`../source/credential-types.html.md.erb`](../source/credential-types.html.md.erb)
- Published: <https://docs.cloudfoundry.org/credhub/credential-types.html>

## Table 1 — Type / Description

Source: lines 17–46. Seven rows, one per credential type.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | header row | yes | `<thead>` |
| Table | row-header column | yes | column 1 names the type |
| Column 1 | role | key | `<code>` type names |
| Column 1 | width | about 20% | `<th style="width:20%">` |
| Column 1 | wrap | avoid | single identifiers |
| Column 2 | role | prose | one or two sentences |

**Cleanup needed:** `class=“table”` uses typographic quotes, so it is not a
valid attribute value. Browsers read the class as `“table”` (quotes
included), so on the published page the `table` class was never applied.
The quotes are made straight: `class="table"` names the standard table style
(see [Template conventions](../README.md#template-conventions)). *Changed:*
the class was dropped at first; it stays now that every HTML table names its
style.

**Deviations:** none. The body rows sit directly in `<table>` with no
`<tbody>`; adding one changes no content.

### Spot checks

- [ ] 7 body rows, each with 2 cells.
- [ ] Every type name in column 1 renders as code: `value`, `json`, `user`,
      `password`, `certificate`, `rsa`, `ssh`.
- [ ] No stray `“` or `”` characters appear anywhere on the page.
