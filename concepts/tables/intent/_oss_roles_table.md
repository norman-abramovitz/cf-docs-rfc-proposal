# Intent: `_oss_roles_table` (partial)

- Source: [`../source/_oss_roles_table.html.md.erb`](../source/_oss_roles_table.html.md.erb)
- Included by `roles.html.md.erb` (docs-cloudfoundry-concepts, line 115)
- Published: <https://docs.cloudfoundry.org/concepts/roles.html#activeroles>
- Added 2026-10-12 as the seventh test page: a table wider than the content
  column.

## Table 1 — Activity and eleven roles

Source: lines 1–608, then nine notes (lines 610–626). Forty-two rows, one per
activity; one column per role.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | header row | yes | `<thead>` |
| Table | row-header column | yes | column 1 names the activity each row is about |
| Table | width | wider than the content column | 12 columns; the published page draws it 874 pixels wide in a 720-pixel column at a 1280-pixel window |
| Column 1 | role | prose | activities, up to about 15 words ("View the status, number of instances, service bindings, and resource use of apps") |
| Columns 2–12 | role | value | `Yes`, empty, `Org` or `Space`, some with a note marker |
| Columns 2–12 | width | sized by content | the source sets no widths |
| Header row | wrap | allowed | role names of up to three words ("Org Billing Manager") |
| Cells | note markers | keep | `<sup><strong>N</strong></sup>`, numbers 1–9, each pointing to a note below the table |

**Wide table:** the table is wider than the content column, so it scrolls
sideways in a box of its own and the page does not
([Template conventions](../README.md#template-conventions): a wide table
scrolls in its own box). The published page has no such box: the table spills
154 pixels into the right margin.

**Cleanup needed:** two cells in the "Create orgs" row (Admin Read-Only and
Global Auditor) hold an empty marker, `<sup><strong></strong></sup>`. It
shows nothing; the cells become empty.

**Deviations:** the table has no class; it gets `class="table"`, the standard
style, as every HTML table names its style. The table's `id`,
`oss-roles-permissions`, is kept. (The published page uses the same id on a
second table; that is listed for cleanup in the
[headings round's list](../../headings/broken-links.md).)

### Spot checks

- [ ] 42 body rows, each with 12 cells, and a header row of 12 cells.
- [ ] `Yes` appears 160 times in the table.
- [ ] 36 note markers in the table and 9 in the notes (45 in all), each a
      superscript number; no empty marker.
- [ ] The nine notes follow the table, note 1 first: "Not by default, unless
      feature flag `user_org_creation` is set to `true`."
- [ ] The notes keep their three links: to `app-ssh-overview` (with the
      fragment `#ssh-access-control-hierarchy`), to `cf-networking` (with
      `#-grant-permissions`), and to <https://v3-apidocs.cloudfoundry.org/>.
- [ ] The table renders inside its host page, after the host's introduction
      ("default permissions for various Cloud Foundry roles in active orgs",
      `vars.app_runtime_abbr`), not as a page of its own and not as a
      literal include line.
- [ ] At 1280 and 390 pixels the table scrolls in its own box and the page
      does not scroll sideways (`checks/wide-tables.mjs`).
