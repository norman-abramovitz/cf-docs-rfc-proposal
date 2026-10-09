# Intent: `uaa-concepts`

- Source: [`../source/uaa-concepts.html.md.erb`](../source/uaa-concepts.html.md.erb)
- Published: <https://docs.cloudfoundry.org/uaa/uaa-concepts.html>

## Table 1 — Grant type / User / Details

Source: lines 174–220, under "Selecting the client grant type". Five rows.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | header row | yes | `<thead>` |
| Table | row-header column | yes | column 1 names the grant type |
| Column 1 | role | key | `<code>` grant type names |
| Column 1 | width | about 30% | `<th width="30%">` |
| Column 1 | wrap | avoid | identifiers such as `client_credentials` must not break at `_` |
| Column 2 | role | prose | short phrases ("Developers building web apps") |
| Column 3 | role | prose | sentences |

**Cleanup needed:** the `implicit` row (line 202) ends with `</td>` instead of
`</tr>`. Browsers ignore the stray end tag and close the row at the next
`<tr>`; strict parsers fail.

**Deviations:** none.

### Spot checks

- [ ] 5 body rows, each with 3 cells; the `implicit` row is followed by the
      `client_credentials` row, not merged into it.
- [ ] All code spans render as code, including those that wrap across source
      lines (`refresh_token` row).
- [ ] Column 1 identifiers do not break inside the word.

## Table 2 — Key / Value (`client.additional_information`)

Source: lines 285–328. Five rows.

| Level | Hint | Value | From source |
|-------|------|-------|-------------|
| Table | header row | yes | `<thead>` |
| Table | row-header column | yes | column 1 names the key |
| Column 1 | role | key | `<code>` key names |
| Column 1 | width | about 25% | `<th width="25%">` |
| Column 1 | wrap | avoid | key names |
| Column 2 | role | prose | sentences |
| Cell | block content | paragraphs | `allowed providers` row: `<br/><br/>` between two paragraphs |

**Cleanup needed:** none.

**Deviations:** in the `allowed providers` row, the two paragraphs separated
by `<br/><br/>` become two paragraphs. The text is unchanged; the line breaks
were standing in for a paragraph break.

### Spot checks

- [ ] 5 body rows, each with 2 cells.
- [ ] `allowed providers` row: two paragraphs, the second starting "You can
      limit UAA to only issue …".
- [ ] "in a Cloud Foundry deployment" and "in the Cloud Foundry ecosystem"
      (`vars.platform_name`, twice).
- [ ] The `client.client_id` link in the `name` row goes to the `#clientid`
      anchor on the same page.
- [ ] `<code>allowed providers="ldap"</code>` keeps its quotes as straight
      quotes inside code.
