# Intent: `troubleshooting_slow_requests`

- Source: [`../source/troubleshooting_slow_requests.html.md.erb`](../source/troubleshooting_slow_requests.html.md.erb)
- Published: <https://docs.cloudfoundry.org/adminguide/troubleshooting_slow_requests.html>

## Pattern: result / explanation / action

All six tables have the same three columns, one table per experiment. They
share one set of hints:

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | pattern | `result-explanation-action` | same headers in all six tables |
| Table | header row | yes | `<thead>` |
| Column 1 | role | key | "Result": the outcome each row is about |
| Column 1 | width | about 25% | `width="25%"` on a column 1 cell in Tables 2–6 |
| Column 1 | wrap | normal | results are sentences, not identifiers |
| Column 2 | role | prose | "Explanation" |
| Column 2 | width | about 25% | `width="25%"` on a column 2 cell in Tables 5 and 6 |
| Column 3 | role | prose | "Action" |
| Column 3 | width | the rest (about 50%) | |

**Width variants.** The source sets widths inconsistently: Table 1 sets
none, Tables 2–4 set column 1 only, and Tables 5 and 6 set columns 1 and 2.
The widths sit on one body cell and apply to the whole column only because
browsers size a column from its widest request. Three variants are rendered
and compared before choosing:

| Variant | Widths | Where |
|---------|--------|-------|
| A — as written | each table's own widths | passthrough |
| B — uniform | about 25% / 25% / 50% in all six tables | extension |
| C — roles only | no width hints; the `key` and `prose` defaults decide | extension |

**Cleanup needed (all tables):** none for well-formedness. Body rows sit
directly in `<table>` with no `<tbody>`; browsers insert one. Adding
`<tbody>` changes no content.

## Table 1 — Experiment 1: total round-trip app requests

Source: lines 69–100. Four rows. No widths in the source.

**Cleanup needed:** none.

### Spot checks

- [ ] 4 body rows × 3 cells.
- [ ] Row 3: `Could not resolve host: NONEXISTENT.com` as code.
- [ ] Row 4: "did not reach Cloud Foundry" (`vars.app_runtime_abbr`).

## Table 2 — Experiment 2: request time in access logs

Source: lines 149–183. Four rows. Source width: column 1, row 1 and 2.

**Cleanup needed:** none.

### Spot checks

- [ ] 4 body rows × 3 cells.
- [ ] `gorouter_time` and `response_time` as code; row 2 code spans across a
      source line break render as one span each.

## Table 3 — Experiment 3: duplicate latency on another endpoint

Source: lines 210–229. Two rows. Source width: column 1, row 1.

**Cleanup needed:** none.

### Spot checks

- [ ] 2 body rows × 3 cells.

## Table 4 — Experiment 4: remove the load balancer

Source: lines 275–296. Two rows. Source width: column 1, row 1.

**Cleanup needed:** none.

### Spot checks

- [ ] 2 body rows × 3 cells.

## Table 5 — Experiment 5: remove Gorouter

Source: lines 330–350. Two rows. Source widths: columns 1 and 2, row 1.

**Cleanup needed:** none.

### Spot checks

- [ ] 2 body rows × 3 cells.
- [ ] Row 2 links "Causes for Gorouter Latency" (`#gorouter-latency`) and
      "Operations Recommendations" (`#ops-recommendations`) go to the
      headings on the same page.

## Table 6 — Experiment 6: network between router and app

Source: lines 395–415. Two rows. Source widths: columns 1 and 2, row 1.

**Cleanup needed:** none.

### Spot checks

- [ ] 2 body rows × 3 cells.
- [ ] Row 2 link "Experiment 1: Measure Total Round-Trip App Requests" goes to
      `#total-latency`.

## Page-level checks

- [ ] `<%= vars.bosh_cli_link %>` (lines 257, 322, 367, outside the tables)
      renders as nothing each time: no error, no `undefined`, no literal tag.
- [ ] Heading "Use app logs to locate delays in Cloud Foundry" (variable in a
      heading, line 422).
