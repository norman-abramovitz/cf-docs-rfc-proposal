# Code blocks round — results

Status: draft, incomplete — covers what is known as of 2026-10-11.

What each tool did with the test pages' code blocks. A summary across
tools comes first, then one section per tool, then the cases across
tools, the conventions to record and the questions for the Docs WG lead.
How the pages were chosen and what the modes mean: [README](README.md).
Per-page intent: [intent/](intent/). How the book writes and renders code
blocks: [survey](survey/README.md).

How to read the results:

- **Code-block check:** the [code-block check](checks/codeblocks.py)
  finds every `<pre>` on a built page and compares it with the page's
  code file ([intent/](intent/)): its text exactly (after dropping
  trailing white space and blank lines at the ends), its section and
  place (body, list item, note, table), no template syntax or markup
  shown in it, and no block elements (`<p>`, `<hr>`, list items) made
  inside it. It also reads the type the block declares, whether it is
  highlighted, whether it has a copy button and what that button copies.
  "53 of 53" means every block on the seven test pages passes.
- **Browser check:** [codeblocks-browser.mjs](checks/codeblocks-browser.mjs)
  loads each page in Chrome, lets the tool's scripts run, clicks each copy
  button and records what it copied; the code-block check then reads the
  page as the browser holds it. Docusaurus, Zensical and Antora draw
  their copy buttons in the browser, and Antora highlights there too.
- **Highlighters:** Prism in Docusaurus, Pygments in Zensical, Shiki
  through Expressive Code (the code component Starlight sets up) in
  Starlight, highlight.js in Antora's default UI.
- **Outline and notes checks:** the headings round's
  [outline check](../headings/checks/outline.py) and the notes round's
  [notes check](../notes/checks/notes.py), on every page.
- **Modes:** *passthrough* writes each code block as the book writes it:
  fences with their info string or none, `<pre>` blocks as HTML;
  *native* writes every block as the tool's own code block with a type,
  and fixes the published page's defects. Everything outside code blocks
  is the same in both modes and follows the earlier rounds' native
  conventions.

All checks ran on 2026-10-11 against the published pages saved that day
and the earlier rounds' copies, with the tool versions the earlier rounds
pinned (Docusaurus 3.10.2, Zensical 0.0.69, Starlight 0.42.6 with
`@astrojs/markdoc` 2.0.11, Antora 3.2.1 with the default UI).

## Summary

In native mode every tool keeps every code block: 53 of 53 blocks with
their exact text, their type and a working copy button, in the right
section and place, on all seven pages
([checks](results/)). Passthrough shows what the book's own forms cost:
between 31 and 45 of the 53 blocks pass, and `<pre>` blocks lose their
copy button and type in every tool.

| | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| **Blocks that pass, native** | 53 of 53 | 53 of 53 | 53 of 53 | 53 of 53 |
| **Blocks that pass, passthrough** | 31 of 53 | 41 of 53 | 45 of 53 | 45 of 53 |
| **A code block in the source** | a fence | a fence | a fence | `[source,TYPE]` and `----` |
| **Highlighter** | Prism, at build time | Pygments, at build time | Shiki (Expressive Code), at build time | highlight.js, in the browser |
| **`console` highlighted** | only with a one-line alias in an ejected theme file | yes | no: one colour | yes |
| **Copy button** | on by default, drawn in the browser | a theme feature to turn on, drawn in the browser | on by default, in the static page | on by default, drawn in the browser |
| **What it copies from a `console` block** | the whole text | the whole text | the whole text | the commands only, prompts removed, joined with `&&` |
| **A variable in a code block** | `<CodeBlock>` with a template literal | as written, `<%= vars.name %>` | a fence, with eight lines of site code | `subs=attributes+` on the block |
| **A `<pre>` block as written** | read as Markdown: `<p>` inside, `*/*` lost, `---` becomes a rule | kept, but broken into paragraphs where it has a blank line in a list item | the build stops on a blank line in a list item; with `&#10;`, inline Markdown still read | kept, in a passthrough block |
| **The book's odd fences** | read as CommonMark | some as the book reads them, some neither way | read as CommonMark | as the converter reads them |
| **Problems the build reports** | none | none | the stop above | none |

- **The tools agree on fences.** A fence with a type keeps its text in
  every tool, in a list item, after a list, in a note, with a variable
  inside. Every difference in native mode is in highlighting and in
  what a copy button copies.
- **`<pre>` blocks do not survive as HTML.** Docusaurus and Starlight
  read the text inside HTML as Markdown; Zensical passes the block
  through, but Python-Markdown splits it at a blank line in a list item,
  as the book's engine does; Antora keeps it in a passthrough block. In
  every tool a `<pre>` has no type, no highlighting and no copy button.
  592 of the book's 1,777 blocks are `<pre>` blocks
  ([survey](survey/README.md#findings)).
- **The published pages have defects the converted pages fix.** Five of
  the seven pages fail the code-block check as published, on 10 blocks
  ([published check](results/published-check.txt)): markup shown as text,
  character references shown as written, fence lines shown in a block,
  blocks broken into paragraphs, and two code blocks published as inline
  code. Native mode fixes all of them.
- **Type names mean different things to different highlighters.**
  highlight.js reads `shell` as a terminal session and highlights only
  lines with a prompt; Prism, Pygments and Shiki read it as a script.
  Pygments and Prism show a `console` line without a prompt as output.
  `bash` and `console` mean the same in all four.
- **The book's Markdown engine and CommonMark disagree on 14 files**
  ([survey](survey/README.md#fences-only-the-books-engine-closes-and-other-disagreements)).
  Docusaurus and Starlight read those blocks as CommonMark does, Zensical
  some as the book does; no reading is right everywhere, and no build
  says anything.

## Docusaurus 3.10.2

Site: [sites/docusaurus/](sites/docusaurus/) — conventions:
[CONVENTIONS.md](sites/docusaurus/CONVENTIONS.md).

### Summary

- **Native: 53 of 53**, every block a fence or, with a variable,
  `<CodeBlock>` ([browser check](results/docusaurus-browser-check.txt)).
- **Prism has no `console` grammar.** A ```` ```console ```` block gets no
  tokens; one line in an ejected copy of the theme's
  `prism-include-languages.js` makes `console` a name for Prism's
  `shell-session` ([probe](results/docusaurus-probe.txt)). Docusaurus
  marks that file as meant to be ejected.
- **The copy button copies the block's text as shown**, prompts and
  output included; it is drawn in the browser, not in the static page.
- **Passthrough: `<pre>` text is read as Markdown.** All six `<pre>`
  blocks on `routes-domains` hold `<p>` elements; `Accept: */*` loses its
  asterisks; a YAML file's `---` becomes `<hr>` and `- mysql` a list item
  ([check](results/docusaurus-check.txt)). The book's CommonMark-only
  fences become blocks, and its unclosed ones swallow what follows.
- **The CommonMark format drops raw HTML**: a `.md` page loses its `<pre>`
  elements ([probe](results/docusaurus-probe.txt)).
- **`<code>{{port}}</code>` in prose stops the build** when the page
  renders, "ReferenceError: port is not defined"
  ([raw check](results/docusaurus-raw-check.txt)); both modes write it as
  inline code.

### Grid

Blocks that pass, of each page's blocks; in native, the blocks
highlighted and what the copy buttons copied.

| Mode | routes-domains | troubleshooting | gsg-grails | backup | backup-clean | nginx | multiple-processes |
|------|------|------|------|------|------|------|------|
| passthrough | 2/9 | 7/11 | 2/5 | 2/4 | 1/4 | 11/13 | 6/7 |
| native | 9/9 | 11/11 | 5/5 | 4/4 | 4/4 | 13/13 | 7/7 |
| native, highlighted | 9 | 9 | 4 | 4 | 4 | 11 | 3 |
| native, copies | text | text | text | text | text | text | text |

## Zensical 0.0.69

Site: [sites/zensical/](sites/zensical/) — conventions:
[CONVENTIONS.md](sites/zensical/CONVENTIONS.md).

### Summary

- **Native: 53 of 53**, every block a fence written as the book writes
  fences, variables inside as `<%= vars.name %>`
  ([browser check](results/zensical-browser-check.txt)).
- **The copy button is a theme feature** a new project turns on and the
  earlier rounds' sites did not; it is added in the browser to every
  `<pre>` that holds a `<code>`, and copies the text as shown.
- **Pygments draws a `console` line without a prompt as output**, so
  native writes such blocks `bash`.
- **Passthrough repeats some published defects.** Python-Markdown reads
  a fence indented four spaces under a paragraph of three, and a `<pre>`
  with a blank line in a list item, the way the book's engine does, and
  shows `&lt;` as written ([check](results/zensical-check.txt)). It reads
  the other odd fences its own way: a fence right after text is a code
  block, a fence closed by ```` ```<br> ```` is none, four backticks
  closed by three are inline code. A `<pre class="terminal">` passes
  through with its text, but with no type or copy button.
- **One notes-check artefact**: the note that holds a code block counts
  the code's line anchors as links.

### Grid

| Mode | routes-domains | troubleshooting | gsg-grails | backup | backup-clean | nginx | multiple-processes |
|------|------|------|------|------|------|------|------|
| passthrough | 7/9 | 10/11 | 4/5 | 2/4 | 2/4 | 11/13 | 5/7 |
| native | 9/9 | 11/11 | 5/5 | 4/4 | 4/4 | 13/13 | 7/7 |
| native, highlighted | 9 | 7 | 3 | 3 | 4 | 12 | 1 |
| native, copies | text | text | text | text | text | text | text |

## Starlight 0.42.6

Site: [sites/starlight/](sites/starlight/) — conventions:
[CONVENTIONS.md](sites/starlight/CONVENTIONS.md).

### Summary

- **Native: 53 of 53**, every block a fence drawn by Expressive Code
  through the fence node of Starlight's Markdoc preset
  ([browser check](results/starlight-browser-check.txt)).
- **The copy button is in the static page** and copies the text as shown.
- **A variable inside a fence needed eight lines of site code**: the
  preset hands Expressive Code the fence's raw text, so the variable tag
  showed as written; the site's fence node takes the text Markdoc has
  filled in.
- **`console` blocks have one colour**: Shiki's shell session grammar
  does not split the command into tokens
  ([probe](results/starlight-probe.txt)).
- **Passthrough: a `<pre>` with a blank line in a list item stops the
  build** ([raw check](results/starlight-raw-check.txt)); written with
  `&#10;`, the earlier rounds' form, the text survives except for inline
  Markdown (`*/*`). Unlabelled fences are `plaintext` with a copy button.

### Grid

| Mode | routes-domains | troubleshooting | gsg-grails | backup | backup-clean | nginx | multiple-processes |
|------|------|------|------|------|------|------|------|
| passthrough | 8/9 | 10/11 | 5/5 | 3/4 | 1/4 | 11/13 | 7/7 |
| native | 9/9 | 11/11 | 5/5 | 4/4 | 4/4 | 13/13 | 7/7 |
| native, highlighted | 1 | 9 | 3 | 4 | 3 | 12 | 5 |
| native, copies | text | text | text | text | text | text | text |

## Antora 3.2.1

Site: [sites/antora/](sites/antora/) — conventions:
[CONVENTIONS.md](sites/antora/CONVENTIONS.md).

### Summary

- **Native: 53 of 53**, every block `[source,TYPE]`, with
  `subs=attributes+` where it holds a variable
  ([browser check](results/antora-browser-check.txt)).
- **The default UI copies a `console` block's commands only**: each `$ `
  line without its prompt, backslash continuations joined, the commands
  joined with ` && `. Other blocks copy their text.
- **highlight.js reads `shell` as a session**, so native writes commands
  without prompts as `bash`; the UI's highlight.js has no NGINX grammar,
  so none of the 11 `nginx` blocks has a colour.
- **Passthrough: `<pre>` blocks are kept in passthrough blocks**, with no
  type, highlighting or copy button; unlabelled fences become literal
  blocks, which get a copy button only when their first line starts with
  `$ `. The prose was converted with pandoc, so the book's odd fences come
  out as pandoc's CommonMark reader reads them
  ([check](results/antora-check.txt)).
- **One notes-check artefact in the browser**: the copy icon inside a
  note's code block counts as an image.

### Grid

| Mode | routes-domains | troubleshooting | gsg-grails | backup | backup-clean | nginx | multiple-processes |
|------|------|------|------|------|------|------|------|
| passthrough | 8/9 | 11/11 | 5/5 | 1/4 | 2/4 | 11/13 | 7/7 |
| native | 9/9 | 11/11 | 5/5 | 4/4 | 4/4 | 13/13 | 7/7 |
| native, highlighted | 9 | 5 | 3 | 2 | 2 | 1 | 1 |
| native, copies | commands | commands 3, text 8 | commands 2, text 3 | text | commands 2, text 2 | text | text |

## Across tools

### What a copy button copies

Three tools copy the block as shown. From a `console` block that is the
prompts and the output too, which a reader pasting into a terminal has to
remove. Antora's default UI copies
only the commands. The book has no copy button today
([survey](survey/README.md#how-the-book-renders-a-code-block)), and its
pages already split most commands from their output: a fence with the
command and its placeholders, then a `<pre class="terminal">` example
with a prompt and output (`gsg-grails`, `troubleshooting_slow_requests`,
`backup-clean`). A reader copies the first and reads the second. Which
behaviour the docs want is [question 1](#questions-for-the-docs-wg-lead).

### Type names

| Type | Prism (Docusaurus) | Pygments (Zensical) | Shiki (Starlight) | highlight.js (Antora UI) |
|------|------|------|------|------|
| `console` | no grammar, unless aliased to `shell-session` | session: prompt lines as commands, other lines as output | session, in one colour | session (the `shell` grammar) |
| `bash` | script | script | script | script |
| `shell` | script | script | script | **session**: lines without a prompt are not highlighted |
| `yaml`, `json` | yes | yes | yes | yes |
| `nginx` | added by the site | yes | yes | **no grammar** |
| `text` | no colour | no colour | no colour | no colour |

So commands without a prompt are `bash` and sessions `console` in every
tool. The book's 164 `console` fences without a prompt
([survey](survey/README.md#findings)) are drawn as output by Pygments and
Prism; native writes them `bash`. Sources:

- Prism makes `sh` and `shell` names for `bash`
  ([`prism-bash.js` L233-L234](https://github.com/PrismJS/prism/blob/76dde18a575831c91491895193f56081ac08b0c5/components/prism-bash.js#L233-L234))
  and has a `shell-session` grammar, not `console`
  ([`prism-shell-session.js` L68](https://github.com/PrismJS/prism/blob/76dde18a575831c91491895193f56081ac08b0c5/components/prism-shell-session.js#L68));
  Prism 1.30.0.
- Pygments 2.21.0, which Zensical's lock installs, gives `shell` to its
  bash lexer
  ([`shell.py` L31](https://github.com/pygments/pygments/blob/a43b45dcf081b6010c6ab4428f149f7f6d2499c4/pygments/lexers/shell.py#L31))
  and `console` to its session lexer
  ([L230](https://github.com/pygments/pygments/blob/a43b45dcf081b6010c6ab4428f149f7f6d2499c4/pygments/lexers/shell.py#L230)),
  which marks a line without a prompt as output
  ([L214](https://github.com/pygments/pygments/blob/a43b45dcf081b6010c6ab4428f149f7f6d2499c4/pygments/lexers/shell.py#L214)).
- Shiki gives `shell` to its shell-script grammar
  ([`shellscript.mjs`](https://unpkg.com/@shikijs/langs@4.5.0/dist/shellscript.mjs))
  and `console` to its session grammar
  ([`shellsession.mjs`](https://unpkg.com/@shikijs/langs@4.5.0/dist/shellsession.mjs)),
  `@shikijs/langs` 4.5.0; the [probe](results/starlight-probe.txt) shows
  the session grammar's one token.
- The Antora UI's highlight.js registers `shell` with the alias `console`
  and a rule that highlights only a line with a prompt
  (`js/vendor/highlight.js` in the pinned UI bundle, whose URL and
  SHA-256 are in the [Makefile](sites/antora/Makefile)).

### `<pre>` blocks

The book writes 592 `<pre>` blocks. Kept as HTML, no tool gives them a
type, highlighting or a copy button, and two tools change their text:

- **MDX and Markdoc read the text inside HTML as Markdown.** In
  Docusaurus, lines become paragraphs, blank lines disappear, `*/*`
  becomes emphasis, `---` a rule and `- item` a list. Starlight stops the
  build on a blank line inside a list item, and with each line break
  written `&#10;` still reads inline Markdown. These are the tables
  round's findings, now on every kind of `<pre>`
  ([tables results](../tables/results.md#summary)).
- **Zensical and Antora keep the text**, except where Python-Markdown
  breaks a `<pre>` with a blank line in a list item, as the book's
  Redcarpet does.

Native mode makes every `<pre>` a fence (or a source block), which every
tool handles alike. That is proposed convention 1.

### The book's odd fences

The survey found 14 files where the book's Markdown engine and CommonMark
find different code blocks. Four are on the test pages:

| Case | The book (published) | Docusaurus, Starlight | Zensical | Antora (through pandoc) |
|------|------|------|------|------|
| fence right after a line of text (`backup` L64) | inline code | code block | code block | code block with the list's indentation in its text |
| fence closed by ```` ```<br> ```` (`backup` L74) | block, ended by the list item | block that runs on | not a code block | code block with the list's indentation in its text |
| four backticks closed by three (`backup` L359) | block | block that runs on and takes the `<pre>` | inline code | block that runs on |
| fence indented four under a paragraph of three (`multiple-processes` L20) | block that shows the fence lines | YAML block | block that shows the fence lines | YAML block |

No reading is right for every case, and no build reports any of them.
The fix is in the source, before conversion (proposed convention 5;
[R-24](../../requirements/README.md#r-24)).

### Variables in code

Each tool writes the variables round's native form, and in native mode
all 8 blocks with variables on `routes-domains` show their values. One
change from that round: Starlight's Expressive Code fences need the
site's fence node, eight lines, because the preset passes the raw text.

### Template delimiters and character references

- **`{{…}}` in a fence is safe in every tool** (`nginx`: five blocks).
  Zensical's ERB delimiters, accepted in the variables round, leave
  `{{` alone. In Docusaurus prose, `<code>{{port}}</code>` stops the
  build; backticks do not.
- **A character reference written in a fence shows as written** in every
  tool, as on the published page; native writes the character.

### What the builds report

None of the passthrough failures above shows in any build log: Docusaurus
reports broken links and anchors, Zensical missing anchors, Antora
section levels, Starlight nothing
([build warnings](results/)). The one exception is Starlight's stop on a
blank line inside a `<pre>` in a list item. The code-block check is what
finds them.

### How a code block reads in the source

The same block, `routes-domains`' TCP route, in each tool's native form:

````markdown
```console
$ cf create-route example-space tcp-domain.example.com --port 60035
```
````

```asciidoc
[source,console]
----
$ cf create-route example-space tcp-domain.example.com --port 60035
----
```

Docusaurus, Zensical and Starlight write the same fence; with a variable
inside, Docusaurus writes `<CodeBlock>` and the others keep the fence
([R-11](../../requirements/README.md#r-11) readable source).

## Conventions to record

For `cf-docs-migrate convert`. Decisions of this round, for review:

1. **Every code block becomes the tool's own code block with a type**: a
   fence in Docusaurus, Zensical and Starlight, `[source,TYPE]` in
   Antora. `<pre class="terminal">`, `<pre>` and `<pre><code>` become
   fences; no `<pre>` HTML is left on a converted page.
2. **Type names**: `console` for a session with `$ ` prompts (and its
   output); `bash` for commands without prompts and for shell scripts;
   `yaml`, `json`, `xml`, `nginx` and the other languages by their
   names, lower case (`yml` becomes `yaml`, `c#` `csharp`); `text` for
   output, logs and anything else. Never `shell`, which highlight.js
   reads as a session.
3. **A block with no type, or a `console` block without a prompt, gets
   one from its text**: a first line with `$ ` is `console`; a YAML or
   JSON file is `yaml` or `json`; one or more commands are `bash`;
   anything else is `text`. Each type the converter chooses is listed
   for the page's owners ([question 2](#questions-for-the-docs-wg-lead)).
   **Accepted** (Docs WG lead, 2026-10-11), with `text` as the fallback.
4. **A code block's text is the published block's text**, without the
   list item's indentation, and with the published page's defects fixed:
   markup shown as text (`<span>@</span>` in a fence), character
   references written in a fence, fence lines shown in a block, blocks
   broken into paragraphs, and fences published as inline code. Each fix
   is listed ([question 3](#questions-for-the-docs-wg-lead)).
   **Accepted** (Docs WG lead, 2026-10-11).
5. **The book's odd fences are repaired before conversion** (R-24): a
   blank line before a fence that follows text, closing fences that match
   their opening, fences indented to their list item, `<pre>` not
   indented four spaces at the top level; the 14 files are in the
   [survey](survey/README.md#fences-only-the-books-engine-closes-and-other-disagreements),
   and each fix is in [cleanup.md](cleanup.md).
6. **A variable inside a code block** uses each tool's form: as written
   (Zensical), `subs=attributes+` on the block (Antora), `<CodeBlock>`
   with a template literal (Docusaurus), and the site's fence node that
   fills in variables (Starlight).
7. **Every site has copy buttons and the highlighting the types need**:
   Zensical turns on `content.code.copy`; Docusaurus adds Prism's
   `bash`, `shell-session` and `nginx` grammars and the `console` alias;
   the others as they come. What a console block's button copies follows
   question 1: each tool's default, **accepted** (Docs WG lead, 2026-10-11).
8. **The code-block check runs on every converted page**, in the build
   and in the browser: [checks/codeblocks.py](checks/codeblocks.py) with
   a code file per page, and
   [checks/codeblocks-browser.mjs](checks/codeblocks-browser.mjs) for copy
   buttons and highlighting drawn in the browser.

## Questions for the Docs WG lead

1. **What should a copy button copy from a `console` block?** Background:
   Docusaurus, Zensical and Starlight copy the whole block, prompts and
   output included; Antora's default UI copies the commands only. The
   book has no copy button today, and its pages mostly put the command in
   one block and the sample session in the next. Question: is copying a
   session's text, prompts and all, acceptable? Recommendation: accept
   each tool's default for now. Commands a reader runs are in `bash`
   blocks, which every tool copies whole; changing what three tools copy
   from `console` blocks would be site code (R-13).
   **Answer (Docs WG lead, 2026-10-11):** accepted; each tool's default.
2. **May the converter choose types?** Background: 807 fences have no
   type, 592 `<pre>` blocks have none, and 164 `console` fences hold
   commands without prompts, which Pygments and Prism draw as output.
   Question: should the converter type them from their text (convention
   3), listing each choice for the owners? Recommendation: yes, with
   `text` where no rule fits.
   **Answer (Docs WG lead, 2026-10-11):** yes, with `text` as the fallback.
3. **Are the published code-block defects defects?** Background: five of
   seven test pages show markup, character references or fence lines as
   text, break blocks into paragraphs, or publish a fence as inline code;
   the survey finds the same patterns elsewhere. Question: may the
   converted pages fix them, as the partials round's accepted decision
   did for its defects? Recommendation: yes, each fix listed (convention
   4).
   **Answer (Docs WG lead, 2026-10-11):** yes, each fix listed.
4. **Starlight's one-colour `console` blocks.** Background: Shiki's shell
   session grammar does not tokenize the command. Question: accept, or
   ask that Starlight be judged without it until the grammar changes?
   Recommendation: accept and record; the text, type and copy button are
   right, and the other three tools highlight `console`.
   **Answer (Docs WG lead, 2026-10-11):** accepted and recorded.

## Requirements

- [R-06](../../requirements/README.md#r-06) typed code blocks: every tool
  shows each block's type, keeps its text exactly and has a copy button,
  once blocks are written as the tool's code blocks with a type. Matching
  highlighting needs `bash` rather than `shell` (Antora), a `console`
  alias (Docusaurus), and is not there for `console` in Starlight or
  `nginx` in Antora.
- [R-01](../../requirements/README.md#r-01) content and outline survive:
  checked for every code block's text, and for headings and notes. Five
  published pages fail on their own defects.
- [R-04](../../requirements/README.md#r-04) variables everywhere: the 8
  blocks with variables keep their values in every tool.
- [R-10](../../requirements/README.md#r-10) simple text plus HTML where
  needed: HTML `<pre>` blocks are where the book's HTML costs most; a
  fence replaces each.
- [R-11](../../requirements/README.md#r-11) readable source: a fence reads
  the same in three tools; Docusaurus needs JSX for a block with a
  variable; Antora's source block is two lines longer.
- [R-13](../../requirements/README.md#r-13) no per-WG extensions:
  Docusaurus's `console` alias (one line in an ejected file) and
  Starlight's fence node (eight lines) are site code the Docs WG would
  keep.
- [R-24](../../requirements/README.md#r-24) markup cleanup before
  conversion: the 14 files whose fences the two Markdown readers read
  differently, the three `class=‘terminal’` attributes, the character
  references in fences.

## Not yet written

- **Code in notes and tables beyond one case.** One `<pre>` in a note
  was converted (`gsg-grails`); the four `<pre><code>` blocks in table
  cells (`_c2c_oss_enable`) and the second note (`gsg-spring`) were not.
- **`<pre>` with HTML inside** other than `<span>@</span>`: 58 blocks
  hold `<strong>`, links or other elements; none was converted.
- **Commands written as inline code** with `<br>` between steps
  (`gsg-grails` Step 9) were not converted or counted.
- **The 10 other files** with odd fences, and the book's home page,
  were not converted.
- **Line numbers, highlighted lines, titles on blocks**: the book uses
  none; not tried.
- **Tabs**: 73 blocks hold a tab; none is on a test page.
- **bosh.io's 1,180 fences** were counted, not converted.
- **What the copy buttons copy across lines with trailing spaces** and
  from blocks with tabs was not compared.
- **Probes and on-paper tools.** Eleventy, Sphinx/MyST, Middleman, Hugo
  and VitePress were not part of this round.
- **Screenshots.** None were taken.
