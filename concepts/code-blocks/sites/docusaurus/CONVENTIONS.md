# Docusaurus conventions for code blocks

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#docusaurus-3102). Everything outside code
blocks follows the earlier rounds' native conventions in both modes:
headings `## Text {#id}` (headings round), notes as admonitions
(`:::warning[Important]`, notes round), product names as text and other
variables as `{vars.name}` (variables round).

```bash
make build          # install, write vars.json, build both modes into build/ (log in .check/build.log)
make serve          # serve build/ at http://localhost:4101
make check          # the code-block, outline and notes checks on every page, passthrough and native
make check-browser  # the same checks on the pages as Chrome holds them, each copy button clicked
make check-raw      # the NGINX page with <code>{{port}}</code> as the book writes it
make probe          # a console fence with and without the console alias; a page in CommonMark format
```

## Native

- **Every code block is a fence with a type**, ```` ```console ````,
  ```` ```shell ````, ```` ```yaml ````, ```` ```nginx ````, ```` ```text ````.
  The classic theme draws it with Prism and a copy button
  ([check](../../results/docusaurus-browser-check.txt): 53 of 53 blocks
  with their text, type and copy button).
- **A block with a variable is `<CodeBlock>`** with a template literal, as
  the variables round wrote it:
  ``<CodeBlock language="console">{`$ cf create-route ${vars.private_app_domain}`}</CodeBlock>``.
  MDX evaluates no expression inside a fence.
- **Prism needs the shell grammars added**, and has no `console` grammar.
  The site adds `bash`, `shell-session`, `groovy` and `nginx` in
  `themeConfig.prism.additionalLanguages`
  ([docusaurus.config.js](docusaurus.config.js)). Prism's shell session
  grammar answers to `shell-session`, `sh-session` and `shellsession`
  ([`prism-shell-session.js` L68](https://github.com/PrismJS/prism/blob/76dde18a575831c91491895193f56081ac08b0c5/components/prism-shell-session.js#L68),
  Prism 1.30.0). A ```` ```console ```` block gets no tokens at all:
  `token plain` only ([probe](../../results/docusaurus-probe.txt)).
- **The site makes `console` a name for `shell-session`** in one line of
  an ejected copy of the theme's
  [`prism-include-languages.js`](src/theme/prism-include-languages.js).
  Docusaurus marks that file "eject: safe … Meant to be ejected"
  ([`getSwizzleConfig.ts` L435-L441](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-theme-classic/src/getSwizzleConfig.ts#L435-L441)).
  With it, a console block's prompt, command and arguments get tokens.
- **The copy button is drawn in the browser**: the static HTML holds none.
  It copies the block's text as shown, prompts and output included.

## Passthrough

Code blocks as the book writes them: fences with their info string or
none, `<pre>` and `<pre><code>` as HTML. 31 of 53 blocks pass
([browser check](../../results/docusaurus-browser-check.txt)).

| Source | What happens |
|--------|--------------|
| a fence with no info string | `language-text`: no highlighting, a copy button |
| `<pre class="terminal">`, `<pre><code>` | MDX reads the text as Markdown: lines become `<p>` elements, blank lines are lost, `*/*` becomes emphasis (`Accept: /`), a YAML file's `---` becomes `<hr>` and `- mysql` a list; no type, no copy button |
| a `<pre><code>` with `{vars.name}` | the value, but in `<p>` elements |
| `<span>@</span>` inside a fence | text: `username<span>@</span>example.com` |
| a fence right after a line of text | a code block (CommonMark), where the book has inline code |
| ```` ```<br> ```` | no closing fence: the block runs on and takes `` ```<br> `` and the rest of its list item |
| four backticks closed by three | the block runs to the end of the list step and holds the `<pre>` after it as text |
| `&lt;file&gt;` in a fence | shown as written, as on the published page |

**Forced change**: the NGINX page's prose `<code>{{port}}</code>` is an
MDX expression, and the build stops when it renders the page:
"ReferenceError: port is not defined"
([raw check](../../results/docusaurus-raw-check.txt)). Both modes write
`` `{{port}}` ``. `<br>` is written `<br/>`, as MDX requires.

**The CommonMark format does not help.** A page saved as `.md` is read as
CommonMark ([docusaurus.config.js](docusaurus.config.js), `format:
'detect'`), and its raw HTML is not rendered: the `<pre>` elements are
gone and their text runs into the page
([probe](../../results/docusaurus-probe.txt)).

**The build reports none of it.** Its log lists broken links and anchors
only ([build warnings](../../results/docusaurus-build-warnings.txt)).

## How a code block reads in the source

````mdx
```console
$ cf create-route example-space tcp-domain.example.com --port 60035
OK
```

<CodeBlock language="console">{`$ cf create-route ${vars.private_app_domain}
OK`}</CodeBlock>
````

A fence reads as in any Markdown; a variable turns the block into JSX.
