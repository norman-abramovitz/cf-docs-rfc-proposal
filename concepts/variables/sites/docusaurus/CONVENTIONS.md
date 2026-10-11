# Docusaurus conventions for variables

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#docusaurus-3102). Pages follow the earlier
rounds' conventions: headings as the
[headings round's native mode](../../../headings/sites/docusaurus/CONVENTIONS.md)
writes them (`## Text {#id}`), notes as the
[notes round's native mode](../../../notes/sites/docusaurus/CONVENTIONS.md),
tables with the [tables round's](../../../tables/sites/docusaurus/CONVENTIONS.md)
cleanup.

```bash
make build      # install, write vars.json, build the site (log in .check/build.log)
make serve      # serve build/ at http://localhost:3000
make check      # build, then the variables, outline and notes checks on every page, passthrough and native
make check-raw  # the first MDX error of a page exactly as the book writes it
make probe      # what an undefined and an empty name do, with each variables module
```

## The mechanism

MDX reads `{…}` as a JavaScript expression. A page imports an object and
writes `{vars.name}`; the expression is evaluated when the page renders.

## Passthrough

Each `<%= vars.name %>` becomes `{vars.name}`, with
`import vars from '@site/vars.json'`: the book's file as it is, written as
JSON by [vars.js](vars.js). The earlier rounds' forms are kept:
`<CodeBlock>` with a template string for a code block that holds a
variable, `<code>{vars.name}</code>` for inline code, and
`<span dangerouslySetInnerHTML={{__html: vars.name}} />` for an HTML value.
75 of 85 values in place ([check](../../results/docusaurus-check.txt)):

| Source | What happens |
|--------|--------------|
| text, link text, table cells, notes | the value, as in the book |
| an HTML value through `dangerouslySetInnerHTML` | markup; as `{vars.name}` it would be escaped text |
| a Markdown value, `{vars.platform_ssh_configuration}` | the Markdown as text: `see [Configuring SSH Access](../../running/config-ssh.html).` |
| a heading, `## Configuring SSH access for {vars.app_runtime_full} {#platform-ssh-config}` | the heading shows the value; the table of contents shows the expression's source, "Configuring SSH access for vars.app_runtime_full" ([browser check](../../results/browser-checks.txt)) |
| a Markdown link target, `[metrics]({vars.gorouter_metrics_link})` | MDX reads no expression in a link target: the link goes to `/passthrough/{vars.gorouter_metrics_link}`; the build's link check reports it as `%7Bvars.gorouter_metrics_link%7D` ([build warnings](../../results/docusaurus-build-warnings.txt)) |
| an HTML `href="<%= vars.x %>"` | `href={vars.x}`, a JSX attribute: the value |
| the first paragraph holds a variable | Docusaurus writes the page description from the source text, with the expression and without its underscores: `{vars.appruntimeabbr}` (the tables round's finding 7) |
| the title set by ERB code (`all_metrics`) | no front matter can hold an expression; the page keeps the front matter's title, "Cloud Foundry component metrics" |
| a name that is not defined | nothing, and no message ([probe](../../results/docusaurus-probe.txt)) |

As written, `<%= vars.name %>` does not compile: "Unexpected character `%`
(U+0025) before name" ([raw check](../../results/docusaurus-raw-check.txt)).

## Native

Pages import a variables module, `import vars from '@site/src/vars'`
([src/vars.js](src/vars.js)), and write `{vars.name}` for every value:

- **Values that hold markup are JSX in the module**, written by the
  converter from the book's HTML or Markdown:
  `config_ssh_link: <>For more information, see <a href="../../running/config-ssh.html">…</a>.</>`.
  `{vars.config_ssh_link}` then renders a link, inline, in a sentence, a
  list item or a table cell, with no wrapper element. Only the four the
  test pages use are written; the book's file has 131 such keys, 78 of
  them used by pages.
- **A value that is a paragraph of its own** is written
  `<p>{vars.platform_ssh_configuration}</p>`: an expression alone on a
  line is not a paragraph in MDX.
- **A link whose target is a variable** is a JSX link:
  `<a href={vars.gorouter_metrics_link}>metrics</a>`. The build's link
  check does not read it, as it does not read other HTML links.
- **A heading with a variable** keeps it, and the page writes its table of
  contents itself: `export const toc = [{value: \`Configuring SSH access for ${vars.app_runtime_full}\`, id: 'platform-ssh-config', level: 2}, …]`.
  Docusaurus makes the table of contents when it compiles the page, and
  writes an expression in a heading as its source text
  ([`utils.ts` L225-L248](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-mdx-loader/src/remark/toc/utils.ts#L225-L248));
  a page that exports `toc` keeps its own
  ([`index.ts` L165-L169](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-mdx-loader/src/remark/toc/index.ts#L165-L169)).
  The export lists every heading at the levels the table of contents
  shows (`h2`, `h3`). The other way is to write the value in the heading.
- **The title and the description are written as values** in the front
  matter (`title: Cloud Foundry Component Metrics`,
  `description: Are your 502 errors the result of your infrastructure, Cloud Foundry, or an app? …`):
  front matter is YAML, read before any expression runs. A heading `# …`
  that holds an expression is no way out: it shows the value, but the
  page's `<title>` shows the expression's source,
  "{vars.app_runtime_abbr} Component Metrics"
  ([probe](../../results/docusaurus-probe.txt)).
- **A name that is not defined stops the build.** The module is a
  JavaScript `Proxy` that throws on a name it does not hold; the build
  stops with "Can't render static file for pathname "/probe"" and
  "Variable not defined: vars.no_such_name"
  ([probe](../../results/docusaurus-probe.txt)). It is 10 lines of site
  code, a shared extension in the sense of
  [R-13](../../../../requirements/README.md#r-13) no per-WG extensions.
- **References to names that are not defined are removed** from the pages.
- An empty value (a YAML null) renders nothing.

## Tables

`<tbody>` around the body rows, as the tables round writes it: a `<tr>`
straight inside `<table>` makes React report error #418, a hydration
mismatch, on load, with nothing in the build's output
([browser check](../../results/browser-checks.txt)). A cell that starts on
the line of its `<td>` and runs over several lines is written on one line
(the notes round's finding).

## How a variable reads in the source

```mdx
## Configuring SSH access for {vars.app_runtime_full} {#platform-ssh-config}

<td>Configure the deployment to allow or prohibit SSH access (one-time). {vars.config_ssh_link}</td>

- Are there any suspicious <a href={vars.gorouter_metrics_link}>metrics</a> spiking?

<CodeBlock language="console">{`$ cf create-shared-domain ${vars.app_domain}`}</CodeBlock>
```

Short in text; code blocks and link targets need JSX, and a page with a
variable in a heading carries its table of contents as code.
