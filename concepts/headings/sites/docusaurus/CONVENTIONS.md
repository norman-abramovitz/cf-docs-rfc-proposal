# Docusaurus conventions for headings

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#docusaurus-3102). Pages, variables and
partials follow the [tables round's conventions](../../../tables/sites/docusaurus/CONVENTIONS.md).

```bash
make build   # install, generate vars.json, build the site (log in .check/build.log)
make serve   # serve build/ at http://localhost:3000
make check   # build, then run the outline check on every page and mode
```

## Headings

- **Write an explicit id with Docusaurus's heading-id syntax:**
  `## <a id="about"></a> About metadata` becomes `## About metadata {#about}`.
  The id goes on the heading itself, the table of contents links to it, and
  the build's anchor check sees it.
- **Never keep the `<a id>` inside the heading.** It builds, but the table
  of contents copies the empty anchor into its own link (`<a href="#-about-metadata"><a></a> About metadata</a>`),
  a link inside a link that the browser's parser splits, and React reports
  a hydration error (#418) on every such page. The table of contents then
  links to the generated id, not to the source's id, and the build's
  broken-anchor check reports links to the source's ids as broken even
  though the `<a id>` is on the page
  ([build warnings](../../results/docusaurus-build-warnings.txt),
  [browser check](../../results/browser-checks.txt)).
- **An HTML heading (`<h4><a id="x"></a>Text</h4>`) becomes a Markdown
  heading** with `{#x}`. As JSX it renders, but it is not part of the
  table of contents and gets no generated id.
- **A heading with a variable needs an explicit id.**
  `### Use app logs to locate delays in {vars.app_runtime_abbr}` renders the
  value in the heading, but the generated id is made from the expression's
  source (`use-app-logs-to-locate-delays-in-varsapp_runtime_abbr`), and the
  table of contents shows the source too: "Use app logs to locate delays in
  vars.app_runtime_abbr", in every mode
  ([toc](../../results/docusaurus-toc.txt)). The explicit id fixes the id,
  not the table-of-contents text; no fix was tried for the text.
- **Skipped levels stay as written.** `####` under `##` renders as `h4`;
  Docusaurus does not warn.
- **The page title is the front matter's `title`**, rendered as the `h1`.
  The pages have no `#` heading.

## Generated ids

For a heading without an explicit id: lowercase, spaces become hyphens,
punctuation such as `:` and `.` is dropped, and a repeated id gets `-1`,
`-2` (`add-metadata-to-a-resource`, `add-metadata-to-a-resource-1`). A
space at the start of the heading text (after an `<a id></a>`) gives a
leading hyphen (`-about-metadata`).

## Table of contents

`h2` and `h3` only (the defaults), every heading at those levels.

## Body changes the new pages needed

Not headings, but needed for the content to survive; they belong to the
variables and code blocks concepts:

| Source | Docusaurus |
|--------|------------|
| a variable in a fenced code block | ``<CodeBlock language="console">{`$ cf create-shared-domain ${vars.app_domain}`}</CodeBlock>`` (`import CodeBlock from '@theme/CodeBlock'`) |
| a variable in inline code, `` `<%= vars.app_domain %>` `` | `<code>{vars.app_domain}</code>` |
| `<td>*.<%= vars.app_domain %></td>` | `<td>\*.{vars.app_domain}</td>`; unescaped, two `*` in a row's cells parse as emphasis and the build fails |
| `<pre class="terminal">` with blank lines and indented lines | the text as one JavaScript string, `<pre class="terminal">{"$ cf service-access\n…"}</pre>`; as written MDX splits it into paragraphs and drops the indentation, and a template literal also loses the indentation |
