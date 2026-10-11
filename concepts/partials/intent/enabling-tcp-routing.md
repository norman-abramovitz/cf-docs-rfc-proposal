# Intent: `enabling-tcp-routing`

- Source: [`../source/enabling-tcp-routing.html.md.erb`](../source/enabling-tcp-routing.html.md.erb)
  and its partial [`_tcp_modify_ports`](../source/_tcp_modify_ports.html.md.erb),
  cloudfoundry/docs-cf-admin
- Excerpt: "Prerequisites for activating TCP routing" up to "TLS for TCP
  Routing" (lines 57–88)
- Published: <https://docs.cloudfoundry.org/adminguide/enabling-tcp-routing.html>
  (copy: [`../published/enabling-tcp-routing.html`](../published/enabling-tcp-routing.html))
- Partials file: [`enabling-tcp-routing.partials`](enabling-tcp-routing.partials);
  notes file: [`enabling-tcp-routing.notes`](enabling-tcp-routing.notes);
  anchors: [`enabling-tcp-routing.anchors`](enabling-tcp-routing.anchors)

## Cases this page covers

- **A partial that is the whole of a list step.**
  `1. <%= partial "../adminguide/tcp_modify_ports" %>`
  ([L88](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/enabling-tcp-routing.html.md.erb#L88)).
  The partial's first line is the step's text; the rest is indented under
  it: an HTML `<pre>`, a paragraph, two `<br>`, and a last paragraph
  indented two spaces.
- **A path through the section's folder name** (`../adminguide/`), which
  resolves to the same folder only because the book names
  docs-cf-admin's folder `adminguide`.
- **A link in the partial to an anchor on the host page** (`#modify-ports`).
- **A note held in a variable** before the steps (`mutual_tls_tcp`), which
  the notes round's accepted convention turns into a partial in native
  mode.

## What a conversion must keep

| Partial | Section | Place | After the host's words | Opens with | Ends with |
|---|---|---|---|---|---|
| `_tcp_modify_ports` | Prerequisites for activating TCP routing | list, first to last word | "see Modify TCP Port Reservations." (end of step 4) | "(Optional) Configure the routing_api.router_groups manifest property" | "To modify the ports after you have deployed, see Modify TCP Port Reservations." |

- **The whole partial in step 5**, its last paragraph included. The
  partial indents that paragraph under the step.
- **The note** with its kind, title and text (the notes file).

## Cleanup and deviations

- **The published page puts the last paragraph after the list.** The book
  renders the partial to HTML first; the host's Markdown then reads a
  paragraph that starts at the left margin and ends the list
  ([published copy](../published/enabling-tcp-routing.html), line 628).
  Decision (this round): the intent is the source's, the paragraph inside
  step 5, and the published page fails the partials check on this point
  ([published check](../results/published-check.txt)). This is a defect
  of today's rendering, not content to keep
  ([R-24](../../../requirements/README.md#r-24) markup cleanup before
  conversion).
- **`<br><br>` is a paragraph break** in native modes, as the tables
  round decided for table cells.
- **`#modify-ports` is outside the excerpt**, so tools that check anchors
  report it.
