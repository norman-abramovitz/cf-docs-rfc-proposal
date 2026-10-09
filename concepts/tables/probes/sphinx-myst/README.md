# Probe: Sphinx 9.1.0 with MyST 5.1.0

**Question:** can a MyST `list-table`'s directive options carry the table
hints?

**What was done:** the `_oss_scale_table` partial is written as a MyST
`list-table` and included by a host page, as `high-availability` includes it.
Sphinx 9.1.0, myst-parser 5.1.0 (docutils 0.22.4), the default theme
(Alabaster 1.0.0). The variables come from
[`../../source/template_variables.yml`](../../source/template_variables.yml)
as `myst_substitutions`, so `<%= vars.recommended_by %>` is
`{{recommended_by}}`. `&ge;` stays as written. `make check` builds the page
and runs the shared spot checks for this table; all five pass.

````markdown
```{list-table}
:header-rows: 1
:stub-columns: 1
:widths: 25 25 50
:class: table hinted col1-key col2-value col3-prose col1-nowrap

* - Component
  - Total Instances
  - Notes
* - Diego Cell
  - &ge; 2
  - The optimal balance between …
```
````

**Answer:** mostly yes, with no code.

| Hint | Directive option | Result |
|------|------------------|--------|
| Header row | `:header-rows: 1` | `<thead>` with `<th>` cells |
| Row headers | `:stub-columns: 1` | column 1 is `<th class="stub">` |
| Widths | `:widths: 25 25 50` | a `colgroup` with 25/25/50% |
| Column roles, no-wrap | `:class:` | classes on the table; a stylesheet gives them their meaning |
| Standard style | `:class: table` | `class="table"` on the table |

- **Classes are the extension point.** `:class:` puts any classes on the
  `<table>`, next to the `docutils` class Sphinx always adds. The roles and the
  capped no-wrap work like the Antora roles: rules in
  [`docs/_static/hints.css`](docs/_static/hints.css), with the shared
  variables `--table-nowrap-max`, `--table-row-header-weight` and
  `--table-row-header-align` (checked in the browser: each changes only what
  it names). With the hints, "Cloud Controller Worker" stays on one line and
  the columns measure 37/22/41; without them, 25/25/50.
- **The theme styles every table through `table.docutils`**, so
  `class="table"` changes nothing in the default theme; it is a hook a
  template can format.
- **The theme hyphenates.** It sets `hyphens: auto` on body paragraphs, cell
  paragraphs included ("in-stance", "re-sources"). The stylesheet turns it
  off in tables, as decided for the other sites.
- **Row headers in the header row.** `:stub-columns:` also makes the header
  row's first cell a stub (`class="head stub"`); it renders as a column
  header.
- **Inline code is rewritten.** Sphinx writes `` `0` `` as
  `<code class="docutils literal notranslate"><span class="pre">0</span></code>`
  (one `span` per word). The check puts back plain `<code>` before running
  the shared spot checks.
- **Partials are includes.** `{include}` reads the partial as MyST, so the
  substitutions work inside it. The `_*.md` files are excluded from the build
  so the partial is not also a page of its own.
- **Not carried:** a second header row (a title spanning the table) and
  per-cell alignment; `:align:` places the whole table.

## Files

- [`docs/conf.py`](docs/conf.py) — MyST, substitutions from the shared
  variables, the hint stylesheet
- [`docs/scale-table-host.md`](docs/scale-table-host.md) — host page
- [`docs/_oss_scale_table.md`](docs/_oss_scale_table.md) — the table
- [`docs/_static/hints.css`](docs/_static/hints.css) — what the roles mean

`make install build check`; `make serve` serves on port 8004.
