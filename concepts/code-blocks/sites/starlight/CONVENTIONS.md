# Starlight conventions for code blocks

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#starlight-0426). Pages are Markdoc with HTML
allowed, as in the earlier rounds. Everything outside code blocks follows
the earlier rounds' native conventions in both modes: headings
`## Text {% #id %}` (headings round), notes as the preset's `aside` tag
(notes round), product names as text and other variables as
`{% $vars.name %}` (variables round).

```bash
make build          # install, write vars.json, build both modes into dist/ (log in .check/build.log)
make serve          # serve dist/ at http://localhost:4103
make check          # the code-block, outline and notes checks on every page, passthrough and native
make check-browser  # the same checks on the pages as Chrome holds them, each copy button clicked
make check-raw      # Markdoc's errors on the passthrough pages with <pre> blocks as the book writes them (raw/)
make probe          # how Shiki tokenizes a console line and a bash line (console-tokens.mjs)
```

## The site

The earlier rounds built Markdoc fences without Starlight's code
component. This site takes the fence node of Starlight's own Markdoc
preset, which draws a fence with Expressive Code, the code component
Starlight sets up: highlighting by Shiki, a frame, and a copy button
([`index.mjs` L18-L26](https://github.com/withastro/starlight/blob/fe11bb470d2177a3696ddeac7379a9625b9f987b/packages/markdoc/index.mjs#L18-L26),
`@astrojs/starlight-markdoc` 0.7.0; [markdoc.config.mjs](markdoc.config.mjs)).
One build holds both modes.

## Native

- **Every code block is a fence with a type.** 53 of 53 blocks keep their
  text, type and copy button
  ([browser check](../../results/starlight-browser-check.txt)).
- **The copy button is in the static HTML**, with the text it copies in
  its `data-code` attribute. It copies the block's text as shown, prompts
  and output included. `console` and `bash` blocks get a terminal frame.
- **A variable inside a fence needs site code.** The preset hands
  Expressive Code the fence's raw text, its `content` attribute, so
  `{% $vars.app_domain %}` showed as written. The site's fence node takes
  the text from the fence's children instead, where Markdoc has put each
  variable's value: eight lines in [markdoc.config.mjs](markdoc.config.mjs),
  with Markdoc's own `Tag` (`@markdoc/markdoc` comes with the Markdoc
  integration and is not listed in [package.json](package.json)), a
  shared extension in the sense of
  [R-13](../../../../requirements/README.md#r-13). The variables round's
  fences, without Expressive Code, rendered variables on their own.
- **`console` blocks are drawn in one colour.** Shiki's shell session
  grammar (Shiki 4.5.0) marks the prompt and the command but does not
  split the command into tokens; a `bash` line gets five colours
  ([probe](../../results/starlight-probe.txt)). 8 of the 9 console blocks
  on `routes-domains` have one colour; the check calls them not
  highlighted.

## Passthrough

Code blocks as the book writes them, with one forced change. 45 of 53
blocks pass ([browser check](../../results/starlight-browser-check.txt)).

- **Forced change: a `<pre>` keeps its line breaks only when each is
  written `&#10;`**, the headings and variables rounds' form. As the book
  writes them, a `<pre>` with a blank line inside a list item stops the
  whole build: "Node 'list' is missing closing"
  ([raw check](../../results/starlight-raw-check.txt): two of the five
  pages), and the tables round found Markdoc joins the lines otherwise.

| Source | What happens |
|--------|--------------|
| a fence with no info string | `plaintext`, a frame and a copy button |
| `<pre class="terminal">`, `<pre><code>` written with `&#10;` | the text is kept, but inline Markdown is still read: `Accept: */*` shows as `Accept: /`; no type, no copy button |
| `<span>@</span>` inside a fence | text |
| a fence right after a line of text | a code block (markdown-it reads CommonMark) |
| ```` ```<br> ```` | no closing fence: the block takes `` ```<br> `` and the rest of its list item |
| four backticks closed by three | the block runs to the end of the list step and holds the `<pre>` after it as text |
| `&lt;file&gt;` in a fence | shown as written, as on the published page |

**The build reports none of the passthrough results**; it stops only on
the blank line inside a `<pre>`
([build warnings](../../results/starlight-build-warnings.txt)).

## A check artefact

In the browser check, Expressive Code's "Copied!" message is in the note
that holds a code block after its button is clicked, and the notes check
reads it as the note's text
([browser check](../../results/starlight-browser-check.txt)).

## How a code block reads in the source

````markdoc
```console
$ cf create-route {% $vars.private_app_domain %}
OK
```
````

Like a Markdown fence, with Markdoc's variable tag inside.
