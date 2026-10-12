# Intent: `bpm-config` (Job Configuration section)

- Source: [`../source/bpm-config.md`](../source/bpm-config.md)
  ([upstream, lines 24–89](https://github.com/cloudfoundry/bpm-release/blob/6b9988a0271aefc2e0cd6444ad4f8d562f46b06e/docs/config.md#L24-L89))
- Published: <https://bosh.io/docs/bpm/config/#job-configuration>
  (bosh.io/docs includes bpm-release as a submodule at this commit; see the
  [survey](../survey/README.md#boshio), "bpm pages")
- Added 2026-10-12 as test input for `wrap: avoid` on identifiers: the
  published page breaks property names in the middle of the identifier.
  The table that matters is B2, the `process` schema.

The source is Markdown. The "Job Configuration" section is converted, lines
24–89: the `##` heading and its sentence, the `###` Schema heading, six
tables under their headings (B1–B6, one per object of one YAML schema),
the reference-link definition after B2, and the `*Note:` paragraph after
B6. All six tables are kept, not B2 alone, because the eight broken names
are spread over four of them, and because six tables with the same columns
on one page show whether their column edges line up. Modes for a Markdown
source are as in [`bosh-networks`](bosh-networks.md): passthrough is the
Markdown as written with cleanup only.

## Pattern: Property / Type / Required / Description

B1–B6 share one set of hints. B2 is described in full; the others differ
only in rows.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | header row | yes | every header cell is bold in the source (`**Property**`) |
| Table | row-header column | yes | column 1 names the property each row is about |
| Table | style | `table` | reference tables; none is long or a matrix |
| Column 1 (Property) | role | key | property names in code (`ephemeral_disk`) |
| Column 1 | wrap | avoid; never inside an identifier | see [Mid-identifier breaks](#mid-identifier-breaks) |
| Column 2 (Type) | role | value | `string`, `boolean`, `volume[]`, `string => string` |
| Column 2 | wrap | avoid | `string => string` breaks at a space on the published page |
| Column 3 (Required) | role | value | `Yes` / `No` |
| Column 3 | align | center (candidate, weak) | a two-value mark column |
| Column 4 (Description) | role | prose | one or two sentences, up to 126 characters (B2, `additional_volumes`) |
| All columns | align | top | Description wraps to two or three lines; the short cells stay at the top of the row |

### Mid-identifier breaks

On the published page, at 1280 × 900, eight property names break inside the
identifier. Material for MkDocs sets `word-break: break-word` and
`overflow-wrap: break-word` on code, and the browser sizes column 1 below
the names' width. Checked 2026-10-12 in Chromium by measuring, character by
character, where each Property code span starts a new line (content column
736 pixels; B1 626 pixels wide, B2–B6 688):

| Table | Breaks as `before\|after` |
|-------|---------------------------|
| B2 | `ephemeral_dis\|k`, `persistent_di\|sk`, `additional_vo\|lumes`, `shutdown_sign\|al` |
| B4 | `open_file\|s` |
| B5 | `unrestricted_vo\|lumes`, `host_pid_namesp\|ace` |
| B6 | `allow_execut\|ions` |

The same check found B2's Type cell `string => string` on two lines.

`wrap: avoid` on column 1 keeps each name on one line; past the cap the
template sets, text wraps between words, and an identifier has none, so a
name never breaks inside. Whether each tool can stop a break inside a code
span (hyphenation, `word-break`, `overflow-wrap`) is the separate
hyphenation and no-wrap work item.

## Table 1 (B1) — Schema (top level)

Source: lines 31–33. One row: `processes`, type `process[]`.

**Cleanup needed:** none. **Deviations:** the header cells' `**…**` is
dropped, as in every table here (header cells are bold by
[template convention](../README.md#template-conventions)); passthrough
keeps it.

## Table 2 (B2) — `process` schema

Source: lines 37–51, and the reference link definition at line 53.
Thirteen rows. Twenty code spans: the 13 property names, and 7 in
Description (`executable`, `/var/vcap/jobs/JOB`, `/var/vcap/data/JOB`,
`/var/vcap/store/JOB`, `TERM`, `INT`, `TERM`). One reference link,
`[capabilities][capabilities]`, to the `capabilities(7)` man page. Header
`Required?` with a question mark (B3–B6 have `Required`); kept as written.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| (as the pattern) | | | |
| Table | notes (candidate) | not applied | `additional_volumes` says "(see volume note below)"; the note is the `*Note:` paragraph after B6, four tables further down |

**Table notes.** The note B2 refers to sits under B6, and B5's
`unrestricted_volumes` is its other subject. The cell refers to it in words,
not with a marker, and the `*` in front of the note matches nothing.
Moving the note under B2 would move content between tables, which is an
editorial change, so the hint is not applied: the note stays after B6.
This case (a note under a different table from the one that refers to it)
is listed for the notes hint's specification.

**Cleanup needed:** none in the table.

**Deviations:** header `**…**` dropped (template convention). Type cells
that name another schema (`hooks`, `limits`, `unsafe`, `volume[]`) are not
linked to that schema's heading; the survey lists that as a conversion
rule, not a table hint, and it is not tested here.

### Spot checks

- [ ] A header row of 4 cells and 13 body rows, each with 4 cells.
- [ ] Column 1 of every body row is one code span, in source order:
      `name`, `executable`, `args`, `env`, `workdir`, `hooks`,
      `capabilities`, `limits`, `ephemeral_disk`, `persistent_disk`,
      `additional_volumes`, `unsafe`, `shutdown_signal`.
- [ ] 20 code spans in the table.
- [ ] The `env` row's Type reads `string => string`.
- [ ] "capabilities" links to the man page
      `man7.org/linux/man-pages/man7/capabilities.7.html`.
- [ ] Every mode but passthrough: no header cell wraps its text in bold
      markup (`<strong>`).
- [ ] In a browser, at 1280 and 390 pixels, none of the 13 names breaks
      inside the identifier, and `string => string` stays on one line.
      (Not automated; `spot-checks.sh` checks built HTML only.)

## Tables 3–6 (B3–B6) — `hooks`, `limits`, `unsafe`, `volume` schemas

Source: lines 57–59 (B3, 1 row), 63–67 (B4, 3 rows), 71–75 (B5, 3 rows),
79–85 (B6, 5 rows). Same hints as the pattern.

**Cleanup needed:** none in the tables. B5's delimiter row has spaces inside
its dash cells (`|--------------          |---------- |`); it is a valid
delimiter row and the published page reads it, so it changes nothing.
B3's Description has a double space and no final period; kept as written.

**Deviations:** header `**…**` dropped (template convention).

### Spot checks

- [ ] B3: 1 body row of 4 cells, `pre_start`.
- [ ] B4: 3 body rows of 4 cells, `memory`, `open_files`, `processes`.
- [ ] B5: 3 body rows of 4 cells, `privileged`, `unrestricted_volumes`,
      `host_pid_namespace`.
- [ ] B6: 5 body rows of 4 cells, `path`, `writable`, `allow_executions`,
      `mount_only`, `shared`.
- [ ] B1: 1 body row of 4 cells, `processes`.
- [ ] In a browser, `open_files`, `unrestricted_volumes`,
      `host_pid_namespace` and `allow_executions` do not break inside the
      identifier (not automated).

## Page-level

**Cleanup needed:** the note after B6 begins `*Note:`. The asterisk is a
marker with no match in any cell, and the published page shows it as a
literal `*`. It is removed: "Note: The volumes in additional volumes must
have a path inside `/var/vcap`." Passthrough keeps it.

### Spot checks

- [ ] Six tables, in source order B1–B6.
- [ ] The note follows the last table: "Note: The volumes in additional
      volumes must have a path inside `/var/vcap`", and
      `unrestricted_volumes` as code; every mode but passthrough shows no
      `*` before "Note".
