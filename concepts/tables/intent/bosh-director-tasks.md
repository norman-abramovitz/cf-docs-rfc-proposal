# Intent: `bosh-director-tasks` (Currently active tasks section)

- Source: [`../source/bosh-director-tasks.md`](../source/bosh-director-tasks.md)
  ([upstream, lines 22–37](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/director-tasks.md#L22-L37))
- Published: <https://bosh.io/docs/director-tasks/#active>
- Added 2026-10-12 with the other bosh.io pages, as test input for the
  `table-output` style. Survey table T18
  ([survey](../survey/README.md#boshio)).

The source is Markdown. Only the "Currently active tasks" section is
converted, lines 22–37: the `##` heading, two sentences, the `bosh tasks`
code block, "Should result in:" and the table. Modes for a Markdown source
are as in [`bosh-networks`](bosh-networks.md): passthrough is the Markdown
as written with cleanup only.

## Table 1 (T18) — Sample `bosh tasks` output

Source: lines 34–37. Two rows, one per task, as the command prints them.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | header row | yes | the command's column titles |
| Table | row-header column | no | output rows, not labelled rows |
| Table | style | `table-output` | command output shown as a table: it follows "Should result in:" after a `bosh tasks` code block; the other outputs on the page are code blocks |
| Column 1 (`#`) | role | value | task ids `766`, `765` |
| Column 2 (State) | role | value | `processing`, `queued` |
| Column 3 (Timestamp) | role | value | `2015-01-27 21:39:30 UTC` |
| Column 3 | wrap | avoid | a timestamp must not break between date and time |
| Column 4 (User) | role | value | `admin` |
| Column 5 (Description) | role | value | "scheduled SnapshotDeployments" |
| Column 6 (Result) | role | value | empty in both rows |

**The `table-output` style**, as proposed, in words (the specification
comes later and may change it): text in the code font, as the terminal prints it; no wrapping
inside cells, so each output row stays one line and the table scrolls
sideways in its own box when it does not fit; tight padding; a rule under
the header row and no other borders; no shading. It says "this is what a
command printed", not "this is reference data".

**Wide table:** at desktop widths the six columns fit the content column;
at phone width they do not, and the table scrolls in its own box
([Template conventions](../README.md#template-conventions)). `table-output`
does not wrap, so this is expected.

**Cleanup needed:** none. The empty Result column is what the command
prints for unfinished tasks; it is kept.

**Deviations:** the table has no class in the source (a pipe table cannot
carry one); the extension gives it `table-output`. Passthrough keeps the
pipe table, which gets the default look. Converting the table to a code
block, as the rest of the page shows command output, is a different
choice and is not made here.

### Spot checks

- [ ] A header row of 6 cells (`#`, State, Timestamp, User, Description,
      Result) and 2 body rows, each with 6 cells.
- [ ] The Result cell is empty in both rows.
- [ ] Row 1: `766`, `processing`, `2015-01-27 21:39:30 UTC`, `admin`,
      `create deployment`.
- [ ] The table follows the `bosh tasks` code block and "Should result in:".
- [ ] Extension: the table carries the `table-output` style.
- [ ] The heading "Currently active tasks" has the anchor `active`, and the
      page shows no literal `{: #…}` text.
- [ ] At 390 pixels the table scrolls in its own box and the page does not
      scroll sideways (`checks/wide-tables.mjs`).
