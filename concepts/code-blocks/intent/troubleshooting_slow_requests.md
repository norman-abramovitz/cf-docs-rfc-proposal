# Intent: `troubleshooting_slow_requests`

- Source: [`../../tables/source/troubleshooting_slow_requests.html.md.erb`](../../tables/source/troubleshooting_slow_requests.html.md.erb),
  cloudfoundry/docs-cf-admin
- Excerpt: the whole page, as the headings and tables rounds converted it
- Published: <https://docs.cloudfoundry.org/adminguide/troubleshooting_slow_requests.html>
  (copy: [`../../headings/published/troubleshooting_slow_requests.html`](../../headings/published/troubleshooting_slow_requests.html))
- Code file: [`troubleshooting_slow_requests.code`](troubleshooting_slow_requests.code);
  anchors: the headings round's
  [`troubleshooting_slow_requests.anchors`](../../headings/intent/troubleshooting_slow_requests.anchors)

## Cases this page covers

- **Fences with no info string** holding one command each, at the top
  level and in list items (seven blocks).
- **`<pre class="terminal">` with a prompt, blank lines and `*/*`**
  ([L40-L60](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting_slow_requests.html.md.erb#L40-L60)),
  the tables round's finding: MDX reads `*/*` as emphasis.
- **`<pre class="terminal">` with a blank line inside a list item**
  ([L125-L131](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting_slow_requests.html.md.erb#L125-L131)),
  which stopped the tables round's Starlight build.
- **A terminal block that holds only log lines**, very long ones, with
  underscores inside words
  ([L428-L432](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting_slow_requests.html.md.erb#L428-L432)).

## What a conversion must keep

Eleven code blocks (the code file): in native mode the seven commands are
`bash`, the three sessions `console`, the log lines `text`. Thirteen
headings and twelve ids, as the headings round checks them.

## Cleanup and deviations

- **Block 4 is the source's whole block.** Redcarpet breaks a `<pre>` with
  a blank line inside a list item into paragraphs; the published page
  shows the prompt line in the block and the rest in `<p>` elements
  inside it. Decision (this round): the intent is the source's text; the
  published page fails the code-block check on this block.
- **Commands without a prompt are `bash`** and sessions with a prompt
  `console` (proposed convention 3).
