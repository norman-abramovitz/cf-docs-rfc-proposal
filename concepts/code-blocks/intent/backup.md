# Intent: `backup` and `backup-clean`

- Source: [`../source/backup.html.md.erb`](../source/backup.html.md.erb),
  cloudfoundry/docs-bbr
- Excerpts, each built as a page: `backup`, Connect to your jumpbox
  ([L18-L111](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L18-L111));
  `backup-clean`, Clean up after a failed backup
  ([L350-L400](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L350-L400))
- Published: <https://docs.cloudfoundry.org/bbr/backup.html>
  (copy: [`../published/backup.html`](../published/backup.html))
- Code files: [`backup.code`](backup.code), [`backup-clean.code`](backup-clean.code);
  notes file: [`backup.notes`](backup.notes); anchors:
  [`backup.anchors`](backup.anchors), [`backup-clean.anchors`](backup-clean.anchors)

## Cases these pages cover

The headings survey's two fences that only the book closes, and a third
case the code-block survey found:

- **A fence right after a line of text, in a nested list**
  ([L63-L66](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L63-L66)):
  `running:<br>` and the fence on the next line. The book makes inline code
  of it.
- **A fence closed by ```` ```<br> ````**
  ([L74-L77](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L74-L77)),
  also right after a line of text.
- **A fence opened with four backticks and closed with three**
  ([L359-L365](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L359-L365)),
  followed by a `<pre>` in the same list item.
- **Backslash line continuations** in commands and in `console` sessions,
  which matter to what a copy button copies.

## What a conversion must keep

`backup`: four `bash` blocks, the two in the nested list included; four
notes; four headings, three ids. `backup-clean`: two `bash` and two
`console` blocks in list steps; two headings, one id.

## Cleanup and deviations

- **The two fences after text are code blocks.** The published page shows
  them as inline code, the first over three lines; the author wrote
  fences. Decision (this round): the converted pages make them code
  blocks; the published page fails the code-block check on them
  ([published check](../results/published-check.txt)).
- **`<br>` next to a code block is dropped** in native mode: it was there
  to force a line break before a block the book did not draw.
- **The four-backtick fence closes with four** in native mode.
