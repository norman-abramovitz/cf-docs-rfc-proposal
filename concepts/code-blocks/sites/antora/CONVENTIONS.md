# Antora conventions for code blocks

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#antora-321). Every page is AsciiDoc in every
mode. Everything outside code blocks follows the earlier rounds' native
conventions in both modes: `[[id]]` above each heading with a source id
(headings round), `[NOTE]` and `[IMPORTANT]` blocks (notes round),
product names as text and other variables as `{name}` (variables round).

```bash
make build          # install, fetch the pinned UI, build both modes into site/ (log in .check/build.log)
make serve          # serve site/ at http://localhost:4104
make check          # the code-block, outline and notes checks on every page, passthrough and native
make check-browser  # the same checks on the pages as Chrome holds them, each copy button clicked
```

## The site

The earlier rounds' playbook with this round's components, both modes in
one build ([antora-playbook.yml](antora-playbook.yml)). The three
variables used in code blocks are attributes in the playbook;
`attribute-missing: warn` logs a reference to a missing one. The default
UI is the earlier rounds' build, pinned by URL and SHA-256 in the
[Makefile](Makefile). The pages were drafted from the Zensical pages with
pandoc 3.12.1 (`commonmark_x` reader) and edited by hand.

## Native

- **Every code block is a source block with a type**:

  ```asciidoc
  [source,console,subs=attributes+]
  ----
  $ cf create-route {private_app_domain}
  ----
  ```

  53 of 53 blocks keep their text, type and copy button
  ([browser check](../../results/antora-browser-check.txt)).
  `subs=attributes+` goes on a block that holds a variable, as the
  variables round wrote it. In a list item the block follows a `+` line.
- **The default UI draws the copy button and runs highlight.js in the
  browser**; the static page has neither. The button is added to every
  `pre.highlight` and to a literal block whose first line starts with `$ `.
  Next to it the UI shows the type, except for `console`.
- **A `console` block's button copies the commands only**: each line that
  starts with `$ `, without the prompt, a backslash continuation joined
  to its line, the commands joined with ` && `. Other blocks copy their
  text. This is the UI's `js/site.js` in the pinned bundle; its source is
  `src/js/06-copy-to-clipboard.js` in antora-ui-default
  ([L65, L70](https://gitlab.com/antora/antora-ui-default/-/blob/0e38223adfd81eb74d4b1779e158f8ad05ff8923/src/js/06-copy-to-clipboard.js#L65-70),
  at master's commit on 2026-10-11; the bundle's own commit was not
  found).
- **`shell` is a session to highlight.js**: the UI registers its `shell`
  grammar with the alias `console`, and that grammar highlights only a
  line that starts with a prompt, handing the rest of the line to `bash`
  (`js/vendor/highlight.js` in the pinned bundle). A command without a
  prompt is written `[source,bash]`.
- **The UI's highlight.js has no NGINX grammar** (the bundle's
  `js/vendor/highlight.js` registers 35 languages, NGINX not among them),
  so `[source,nginx]`
  blocks keep their type and copy button but have no colour: all 11 on
  `nginx`. A custom UI bundle could add one; not tried.

## Passthrough

Code blocks as the book writes them, as far as AsciiDoc has a form for
them. 45 of 53 blocks pass
([browser check](../../results/antora-browser-check.txt)).

| Source | Written as | What happens |
|--------|------------|--------------|
| a fence with an info string | `[source,TYPE]` and `----` | as in native |
| a fence with no info string | a literal block, `....`, as the tables round wrote it | no type, no highlighting; a copy button only when the first line starts with `$ ` |
| `<pre class="terminal">`, `<pre><code>` | a passthrough block, `++++`, with `[subs=attributes+]` where it holds a variable | the HTML as written: text kept, no type, no copy button |
| `&lt;file&gt;` in a fence | in a literal block | shown as written |
| the book's odd fences | as pandoc's CommonMark reader reads them | the two fences after text in `backup` keep the list's indentation in their text; four backticks closed by three run on and take the `<pre>` |

**The build reports none of it**; its log holds the section-level
warnings that every excerpt starting below `==` gives
([build warnings](../../results/antora-build-warnings.txt)).

## Check artefacts

In the browser check, the copy icon (`<img>`) inside the note's code block
on `gsg-grails` counts as an image in the notes check.

## How a code block reads in the source

```asciidoc
[source,console]
----
$ cf create-route example-space tcp-domain.example.com --port 60035
----
```

Two lines more than a fence; the type is in the block's attribute line.
