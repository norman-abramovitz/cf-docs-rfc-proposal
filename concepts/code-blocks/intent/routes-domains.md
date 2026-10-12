# Intent: `routes-domains`

- Source: [`../../headings/source/routes-domains.html.md.erb`](../../headings/source/routes-domains.html.md.erb),
  cloudfoundry/docs-dev-guide
- Excerpt: the Create a route section and its five subsections
  ([L106-L265](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L106-L265))
- Published: <https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html>
  (copy: [`../../headings/published/routes-domains.html`](../../headings/published/routes-domains.html))
- Code file: [`routes-domains.code`](routes-domains.code); notes file:
  [`routes-domains.notes`](routes-domains.notes); anchors:
  [`routes-domains.anchors`](routes-domains.anchors)

## Cases this page covers

- **`console` fences with a prompt and output**, at the top level and in a
  list item, with variables inside
  ([L248-L253](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L248-L253),
  [L260-L264](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L260-L264)).
- **`<pre><code>` blocks with variables and HTML inside**: six blocks
  write `username<span>@</span>example.com`, which keeps Cloudflare from
  hiding the address
  ([L148-L152](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L148-L152)),
  and one holds `'*'` and `*.foo.`, characters Markdown reads as emphasis
  ([L187-L191](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L187-L191)).
- **The same `<span>@</span>` inside a fence**, where it is text
  ([L121-L125](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L121-L125)).
- **A fence indented two spaces after a list item**, its lines indented
  too
  ([L248-L253](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L248-L253)).

## What a conversion must keep

Nine code blocks, all `console` in native mode, each with the text of the
published page and its variables' values (the code file). Two notes,
seven headings and six ids, as the earlier rounds check them.

## Cleanup and deviations

- **Block 1 shows `username@example.com`.** The published page shows the
  fence's `<span>@</span>` as text. Decision (this round): markup shown as
  text in a code block is a defect the converted page fixes; the
  published page fails the code-block check here
  ([published check](../results/published-check.txt)).
- **Block 8 is in the list item, without two leading spaces.** Redcarpet
  takes the fence's lines as written and puts the block after the list,
  so the published block starts each line with two spaces. In CommonMark
  the fence belongs to the list item and its indentation is removed from
  each line. Decision (this round): the CommonMark reading, which matches
  the author's layout; the published page fails here too.
- **The six `<pre><code>` blocks become fences** in native mode, and the
  `<span>@</span>` becomes `@`.
