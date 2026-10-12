# Intent: `bosh-networks` (CPI Limitations section)

- Source: [`../source/bosh-networks.md`](../source/bosh-networks.md)
  ([upstream, lines 485–521](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/networks.md#L485-L521))
- Published: <https://bosh.io/docs/networks/#cpi-limitations>
- Added 2026-10-12 with the other bosh.io pages, as test input for the
  candidate hints *row group* and *table notes*. Survey tables T3 and T4
  ([survey](../survey/README.md#boshio)).

The source is Markdown (MkDocs with Material for MkDocs), not HTML. Only the
"CPI Limitations" section is converted, lines 485–521: the `##` heading, the
intro sentence, T3 and its note, the `###` heading, and T4 and its two notes.
The modes read as follows for a Markdown source: *passthrough* is the
Markdown as written, with cleanup only (no hints); *extension* carries the
hints; *native* is the tool's own table syntax with whatever hints it can
carry.

New hints used below are candidates, approved but not yet specified:
**row group** (a full-width row that labels the rows under it), **table
notes** (notes under the table, linked from markers in cells), **style**
`table-compact` (a candidate only; the rule that assigns it is still being
worked out), and **align** (horizontal and vertical, per column).

## Table 1 (T3) — Networks per instance, IaaS × network type

Source: lines 489–494, then one note (line 496). Four rows, one per IaaS.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | header row | yes | pipe table header; the corner cell is empty |
| Table | row-header column | yes | column 1 names the IaaS; every column 1 cell is bold (`**AWS**`) |
| Table | notes | one note, marker `1` | `Multiple<sup>1</sup>` (row 1, column 2); the note is the `1:` paragraph under the table |
| Table | style | `table` (the default look) | a short reference table |
| Column 1 | role | key | IaaS names |
| Column 1 | wrap | avoid | single names |
| Columns 2–4 | role | value | short phrases ("Single (Elastic IP)") |
| Columns 2–4 | align | left, top | phrases, not marks |
| Header row | line break | keep | `Manual network<br>(per instance group)` and `Dynamic network<br>(per instance group)`: the qualifier sits on its own line |
| Cell | link | keep | row 3 column 2 links to `openstack-multiple-networks.md` |

**Wide table:** no. Four short columns fit the content column.

**Cleanup needed:** the bold on the column 1 cells is how the source marks a
row header; it is dropped where the row-header hint carries it, since row
headers are styled by the template (see
[Template conventions](../README.md#template-conventions)). Native pipe
tables have no row headers and keep the bold. `-` in the
vSphere row (two cells) means "none" where T4 uses `—`; both are kept as
written.

**Deviations:** with the notes hint, the `1:` paragraph becomes note 1 of
this table: the `1:` label is replaced by the marker, and the marker links
to the note. The note text is unchanged. In passthrough and in native
syntaxes without notes, the marker stays a superscript and the note stays
a paragraph after the table.

### Spot checks

- [ ] A header row of 4 cells and 4 body rows, each with 4 cells.
- [ ] The two network-type header cells keep the line break before
      "(per instance group)".
- [ ] One note marker in the table, a superscript `1`, in the AWS row.
- [ ] Extension: the marker links to its note, which follows the table.
- [ ] The note follows the table: "The maximum number of network
      interfaces attached to a VM is limited per instance type", with its
      two links (the AWS page `AvailableIpPerENI.html` and `manifest-v2`
      `#instance-groups`) and `nic_group` as code.
- [ ] Row 3 column 2 "Multiple" links to `openstack-multiple-networks`.
- [ ] The vSphere row shows `-` in its last two cells.
- [ ] The heading "CPI Limitations" has the anchor `cpi-limitations`, and
      the page shows no literal `{: #…}` text.

## Table 2 (T4) — Advanced network features, IaaS × network type × feature

Source: lines 500–512, then two notes (lines 514–521). Eleven body rows:
eight data rows, two per IaaS, and three blank spacer rows between the
groups.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | header row | yes | pipe table header; the corner cell is empty |
| Row | group (candidate) | AWS, Azure, OpenStack, vSphere | each IaaS name sits in column 1 of the first row of its group; the next row leaves column 1 blank ("same as above"); a blank spacer row ends each group but the last |
| Table | notes (candidate) | two notes, markers `1` and `2` | `Supported<sup>1</sup>` twice and `Supported<sup>2</sup>` once; notes are the `1:` and `2:` paragraphs under the table, note 1 with a four-item list |
| Table | style | `table`; `table-compact` candidate | matrix family; whether compact applies is decided by the rule from the survey, not here |
| Column 1 | role | key | network type (`Manual`, `VIP`) once the groups are rows |
| Columns 2–3 | role | value | `Supported`, `—` for none, one "(from v107.0.2)" |
| Columns 2–3 | align | center (candidate), top | matrix marks: `Supported` and `—` read as a grid |
| Cell | link | keep | Azure / Manual / NIC grouping links to `azure-cpi.md#dual-stack-networks` |

**Row groups.** The group hint turns each IaaS into a full-width row above
its two rows. The IaaS column then holds nothing the group row does not, so
it goes: the table has three columns (Network type, NIC grouping, Prefix
delegation), four group rows and eight data rows. The spacer rows go: the
group rows separate the groups. Native syntaxes that cannot span a row keep
the four columns, with the IaaS in column 1 of the first row of its group
(bold, as written) and column 1 blank below it, and drop the spacer rows.

**Wide table:** no.

**Cleanup needed:** the three spacer rows hold no content; they are layout
standing in for groups and are dropped in every converted mode except
passthrough. The Azure / Manual row's NIC grouping cell is wider than its
column in the source (the delimiter cell is shorter than the link); this is
alignment of the source text only and changes nothing.

**Deviations:** the IaaS column becomes group rows (above). With the notes
hint, `1:` and `2:` become notes 1 and 2 of this table, each linked from its
markers; note 1 keeps its list. The markers in T3 and T4 are both numbered
from 1, so the links must tell T3's note 1 from T4's note 1. Passthrough
keeps the table as written, spacer rows included.

### Spot checks

- [ ] The table holds `AWS`, `Azure`, `OpenStack` and `vSphere`, once each,
      in that order.
- [ ] Eight data rows, each with one `Manual` or `VIP` cell.
- [ ] `—` appears 11 times in the table.
- [ ] Three note markers in the table, superscripts: `1`, `2`, `1`.
- [ ] Passthrough: 11 body rows of 4 cells, spacer rows included.
- [ ] Every mode but passthrough: no body row with every cell empty.
- [ ] Extension: four group rows, each one cell spanning the full width,
      holding the IaaS name; the header row has as many cells as a data row.
- [ ] Extension: each marker links to its note after the table, and T4's
      note 1 is a different target from T3's note 1.
- [ ] Note 1 follows the table: "The maximum number of IP addresses
      assigned to one NIC", then a list of 4 items ("one IPv4 address" …
      "one IPv6 prefix delegation").
- [ ] Note 2 follows note 1 and links "Prefix delegation for AWS" to the
      AWS page `ec2-prefix-eni.html`.
- [ ] The Azure / Manual NIC grouping cell links "Supported" to `azure-cpi`
      `#dual-stack-networks`.
- [ ] The heading "Advanced Network Features" has the anchor
      `advanced-network-features`.
