# Zensical conventions for code blocks

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#zensical-0069). Everything outside code
blocks follows the earlier rounds' native conventions in both modes:
headings `## Text {#id}` (headings round), notes as `!!! important`
(notes round), product names as text and other variables as
`<%= vars.name %>` read by the macros extension with ERB delimiters
(variables round).

```bash
make build          # install, write vars.yml, build both modes into site/ (log in .check/build.log)
make serve          # serve site/ at http://localhost:4102
make check          # the code-block, outline and notes checks on every page, passthrough and native
make check-browser  # the same checks on the pages as Chrome holds them, each copy button clicked
```

## The site

The earlier rounds' configuration plus one theme feature,
`content.code.copy`, which puts a copy button on code blocks
([zensical.toml](zensical.toml)). A new Zensical project turns it on
([bootstrap `zensical.toml` L31](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/bootstrap/zensical.toml#L31));
a site that lists no features has none
([`config.py` L641](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/config.py#L641)),
and the earlier rounds' sites listed none. Code is highlighted at build
time by Pygments through `pymdownx.highlight` and `pymdownx.superfences`,
as in a new project.

## Native

- **Every code block is a fence with a type**, written as the book writes
  fences. 53 of 53 blocks keep their text, type and copy button
  ([browser check](../../results/zensical-browser-check.txt)).
- **Variables inside a fence are written as in the book**,
  `<%= vars.app_domain %>`: the macros extension renders the page before
  Markdown reads it, so the fence holds the value.
- **A fence in a list item is indented four spaces**, and so is any
  paragraph that continues the item: Python-Markdown wants four.
  `multiple-processes` indents a paragraph three spaces in the source.
- **`console` without a prompt is shown as output.** Pygments' console
  lexer marks every line that does not start with a prompt as output
  (`<span class="go">`), so `cf marketplace` under ```` ```console ```` is
  drawn like command output. Native writes such blocks ```` ```shell ````
  (proposed convention 3).
- **The copy button is added in the browser** by the theme's script, on
  every `<pre>` that holds a `<code>`. It copies the block's text as
  shown, prompts and output included.

## Passthrough

Code blocks as the book writes them. 41 of 53 blocks pass
([browser check](../../results/zensical-browser-check.txt)).
Python-Markdown reads some of the book's odd forms the way Redcarpet
does, so some of the published page's defects come back:

| Source | What happens |
|--------|--------------|
| a fence with no info string | `language-text`, no highlighting, a copy button |
| `<pre class="terminal">` | passed through as written: the text is kept, no type, no copy button |
| `<pre><code>` | passed through; the theme adds a copy button |
| `<pre>` with a blank line in a list item | broken into paragraphs after its first line, as on the published page |
| a fence right after a line of text | a code block, as in CommonMark |
| a fence closed by ```` ```<br> ```` | not a code block |
| a fence indented four spaces under a paragraph indented three | an indented block that shows ```` ```yaml ````, as on the published page |
| four backticks closed by three | not a code block: inline code that starts with a stray backtick |
| a fence indented two spaces after a list item | a code block after the list, its indentation removed |
| `&lt;file&gt;` in a fence | shown as written, as on the published page |

**The build reports none of it.** Its log lists anchors that do not
exist, outside the excerpts
([build warnings](../../results/zensical-build-warnings.txt)).

## A check artefact

The notes check counts links in a note. `anchor_linenums`, on in a new
project, writes an `<a>` for each line of a code block, so the note that
holds a code block in `gsg-grails` counts three links where the source
has none ([check](../../results/zensical-check.txt)). The notes check
could leave out links inside `<pre>`; it belongs to the notes round.

## How a code block reads in the source

````markdown
```console
$ cf create-route <%= vars.private_app_domain %>
OK
```
````

The page reads as the book's does.
