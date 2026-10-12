# Intent: `bosh-cpi-api-v2` (Reference Table section)

- Source: [`../source/bosh-cpi-api-v2.md`](../source/bosh-cpi-api-v2.md)
  ([upstream, lines 46–61](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/cpi-api-v2.md#L46-L61))
- Published: <https://bosh.io/docs/cpi-api-v2/#reference-table-based-on-each-component-version>
- Added 2026-10-12 with the other bosh.io pages, as test input for the
  candidate hint *row emphasis*. Survey table T14
  ([survey](../survey/README.md#boshio)).

The source is Markdown. Only the "Reference Table" section is converted,
lines 46–61: the `###` heading, the intro sentence, the table and the `\*`
note under it. Modes for a Markdown source are as in
[`bosh-networks`](bosh-networks.md): passthrough is the Markdown as written
with cleanup only.

## Table 1 (T14) — Director / CPI / Stemcell version matrix

Source: lines 50–59, then one note (line 61). Eight rows, one per
combination of Director, CPI and stemcell API versions.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | header row | yes | pipe table header |
| Table | row-header column | no | the first three columns together name the combination |
| Row | emphasis (candidate) | row 4 (Director 2, CPI 2, Stemcell 2) | every cell of the row is bold (`**2**` … `**Yes**`); it is the only combination that does not write to the registry |
| Table | notes (candidate) | one note, marker `*` | the header of column 5 ends its italic text with an asterisk; the note is the `\*` paragraph under the table |
| Table | style | `table`; `table-compact` candidate | matrix family: three columns of `1` / `2` and a Yes / No column |
| Columns 1–3 | role | value | API versions `1` or `2` |
| Columns 1–3 | align | center (candidate) | matrix marks |
| Column 4 | role | value | "Update registry" / "Do not write to registry" |
| Column 5 | role | value | `Yes` / `No` |
| Column 5 | align | center (candidate) | matrix marks |
| All columns | align | middle or top (no preference) | every cell is one line |

**Row emphasis.** The bold row is the one the section is about: the only
combination that allows registry-less operation. The emphasis hint marks
the row as a whole, so the template styles it as a row; the five per-cell
`**…**` go. Native pipe tables cannot mark a row and keep the bold cells
as written.

**Row order.** The rows are not sorted (1-1-1, 1-1-2, 1-2-2, 2-2-2, 1-2-1,
2-2-1, 2-1-1, 2-1-2). The order is kept; sorting is an editorial change.

**Wide table:** no. Five short columns; the column 5 header is the widest
cell.

**Cleanup needed:** the column 5 header reads
``Add *full agent settings** to IaaS `user-metadata`?``. The second `*` of
`**` is the note marker, but Markdown reads `**` as the end of the italic,
so the published page renders `<em>full agent settings*</em>`: the
asterisk sits inside the italic text, and there is no marker. The italic
ends after "settings" and the asterisk follows it as the marker
(`*full agent settings*\*` in Markdown). The note line `\* see below …` is
written with an escaped asterisk and renders correctly.

**Deviations:** with the notes hint, the `*` becomes a note marker linked to
the note under the table; the note keeps its text ("see below for
information on the settings to write to `user-metadata`"). The marker
stays `*`, not a number. In passthrough and in native syntaxes without
notes, the marker is a plain asterisk after the italic text and the note
stays a paragraph after the table.

### Spot checks

- [ ] A header row of 5 cells and 8 body rows, each with 5 cells.
- [ ] Row 4 reads 2, 2, 2, "Do not write to registry", "Yes".
- [ ] Extension: row 4 is marked as a row (the row carries the emphasis,
      not five bold cells). Other modes: row 4 is marked as a row, or all
      five of its cells are bold.
- [ ] The column 5 header shows "full agent settings" in italics with the
      asterisk outside the italic text, and `user-metadata` as code.
- [ ] Extension: the `*` marker links to the note after the table.
- [ ] The note follows the table: "see below for information on the
      settings to write to `user-metadata`", with `user-metadata` as code.
