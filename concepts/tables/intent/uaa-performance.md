# Intent: `uaa-performance` (first section)

- Source: [`../source/uaa-performance.html.md.erb`](../source/uaa-performance.html.md.erb)
- Published: <https://docs.cloudfoundry.org/running/uaa-performance.html>

The page is the example for a second table style. Only its first results
section is converted: lines 84–109, the heading, the endpoint line and
table 1. The other eleven tables have the same shape.

## Table 1 — Instances / Threads / Throughput

Source: lines 88–109. Three rows, one per instance count; each row holds two
chart thumbnails, each linked to its full-size image.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | header row | yes | `<thead>` |
| Table | style | `table-media` | a grid of charts, not data cells |
| Column 1 | role | value | instance counts (`1`, `2`, `4`) |
| Column 2 | role | (media) | one linked image per cell |
| Column 3 | role | (media) | one linked image per cell |

**The `table-media` style.** It is the example of a style beyond the
standard `table`, picked from the survey's media-grid family (12 tables, all
on this page). What the style means, in every tool:

- No cell borders. A rule under the header row and a thin line between body
  rows.
- The header row is not shaded.
- Cells are centered, horizontally and vertically.
- An image fills the width of its cell; the image columns share the width
  equally.

The class carries the style: passthrough tables have `class="table-media"`
in place of `class="table"`, and the extension mode names the style in each
tool's own syntax. A native Markdown table cannot carry a class, so it gets
the standard style (see [Template conventions](../README.md#template-conventions)).

**Cleanup needed:** the heading is written `###<a id='client-credentials'></a> Client credentials grant type`,
with no space after `###`. The published site's Markdown reads it as a
heading; CommonMark does not. The space is added.

**Deviations:**

- The class changes from `table` to `table-media`; that is the point of the page.
- The header cells wrap their text in `<strong>`. It is dropped: bold header
  cells are a convention the template provides.
- `data-fancybox="gallery"` on the links, and the jQuery and fancybox
  scripts at the top of the page, are left out. They open the full image in
  a lightbox; without them the link opens the image itself. Scripts on a
  page belong to another concept.

### Spot checks

- [ ] 3 body rows, each with 3 cells.
- [ ] 6 images, with their alt text (`Threads Level 1` … `Throughput Level 4`).
- [ ] Each image sits inside a link to the same image.
- [ ] Passthrough and extension: the table carries the `table-media` style.
      Native: it does not (standard style).
- [ ] The heading "Client credentials grant type" renders as a heading with
      the anchor `client-credentials`.
