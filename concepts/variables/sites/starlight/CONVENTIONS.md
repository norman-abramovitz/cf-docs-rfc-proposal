# Starlight conventions for variables

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#starlight-0426). Pages are Markdoc with HTML
allowed, as in the earlier rounds; headings as the
[headings round's native mode](../../../headings/sites/starlight/CONVENTIONS.md)
writes them (`## Text {% #id %}`), notes as the
[notes round's native mode](../../../notes/sites/starlight/CONVENTIONS.md).

```bash
make build      # install, write vars.json, check native pages' variables, build both modes into dist/
make serve      # serve dist/ at http://localhost:4321
make check      # build, then the variables, outline and notes checks on every page, passthrough and native
make check-raw  # a page exactly as the book writes it: Markdoc's errors, the build, the checks
make probe      # what an undefined and an empty name do
```

## The mechanism

Markdoc reads `{% $name %}` as a variable from the `variables` object of
its config, and renders its value as text. The site builds once per mode
(`MODE=passthrough`, `MODE=native`), because the two modes give `$vars`
different values ([markdoc.config.mjs](markdoc.config.mjs),
[astro.config.mjs](astro.config.mjs)); `make build` merges the two into
`dist/`.

## Passthrough

Each `<%= vars.name %>` becomes `{% $vars.name %}`, with the book's file
as it is (vars.json). The earlier rounds' forms are kept: the tables
round's `{% rawhtml value=$vars.name /%}` tag for an HTML value, and code
blocks as `<pre><code>` with `&#10;` for each line break, as the headings
round wrote them. 73 of 85 values in place
([check](../../results/starlight-check.txt)):

| Source | What happens |
|--------|--------------|
| text, link text, table cells, headings, notes | the value; the table of contents shows it too |
| an HTML value through `rawhtml` | markup; as `{% $vars.name %}` it would be escaped text |
| a Markdown value | the Markdown as text |
| a Markdown link target, `[metrics]({% $vars.gorouter_metrics_link %})` | no link: the page shows `[metrics](../running/all_metrics.html#routing)` as text, and the build says nothing |
| an HTML `href="{% $vars.gorouter_metrics_link %}"` | the tag as written: `href="{% $vars.gorouter_metrics_link %}"` |
| the title set by ERB code (`all_metrics`) | the front matter is not read by Markdoc; the page keeps the front matter's title |
| a name that is not defined | nothing, and no message |

As written, the page builds and shows its ERB tags as text, in the
heading and the table of contents too
([raw check](../../results/starlight-raw-check.txt)).

## Native

Pages write `{% $vars.name %}` for every value, and `$vars` is
[vars-native.mjs](vars-native.mjs):

- **Values that hold markup are Markdown, parsed by Markdoc into the tree
  it renders**, in the config: `inline(md)` keeps the children of the
  value's one paragraph. `{% $vars.config_ssh_link %}` then renders a
  link, inline, in a sentence, a list item or a table cell. The converter
  writes the book's HTML values as Markdown; only the four the test pages
  use are written. This uses Markdoc's own `parse` and `transform`, in 3
  lines of config; `@markdoc/markdoc` comes with the Markdoc integration
  and is not listed in [package.json](package.json), as in the notes
  round's `markdoc-check.mjs`.
- **A link whose target is a variable** is a tag defined in the config,
  `{% link href=$vars.gorouter_metrics_link %}metrics{% /link %}`, which
  renders `<a>`: Markdown links take no tag in their target. It works
  inside an HTML table cell too.
- **Code blocks are fenced again**: a fence renders the variables inside
  it, because Markdoc processes a fence's content unless the fence says
  `process=false`
  ([`schema.ts` L52-L57](https://github.com/markdoc/markdoc/blob/16e1840c687e17c57d2b3664eac4edfbd01e7283/src/schema.ts#L52-L57),
  v0.5.10). The block keeps its type (`console`). The headings round
  recorded the opposite, the tag shown as text, and wrote `<pre><code>`
  instead; that was not reproduced here, and its cause was not traced.
  Inline code is still `<code>{% $vars.name %}</code>`: backticks keep
  their content as written.
- **The title is written as a value** in the front matter, which Markdoc
  does not read.
- **A name that is not defined is reported by a check, not by the build.**
  Markdoc's validator reports it ("Undefined variable: 'vars.no_such_name'",
  error id `variable-undefined`), but Astro's Markdoc integration drops
  that error on purpose
  ([`content-entry-type.ts` L246-L252](https://github.com/withastro/astro/blob/3571e2d2e80a66764254fa9b7750704a150ca3f6/packages/integrations/markdoc/src/content-entry-type.ts#L246-L252),
  @astrojs/markdoc 2.0.11: "Variables can be configured at runtime, so we
  cannot validate them at build time"). `make build` runs
  [vars-check.mjs](vars-check.mjs) on the native pages first, which fails
  on any: "probe.mdoc:5: Undefined variable: 'vars.no_such_name'"
  ([probe](../../results/starlight-probe.txt)).
- **References to names that are not defined are removed** from the pages.
- An empty value (a YAML null) renders nothing.

## A heading with a variable

The heading and the table of contents show the value, in both modes
([browser check](../../results/browser-checks.txt)).

## How a variable reads in the source

```markdoc
## Configuring SSH access for {% $vars.app_runtime_full %} {% #platform-ssh-config %}

<td>Configure the deployment to allow or prohibit SSH access (one-time). {% $vars.config_ssh_link %}</td>

- Are there any suspicious {% link href=$vars.gorouter_metrics_link %}metrics{% /link %} spiking?
```

Longer than ERB, but one form for text, code and markup; only link
targets need the tag.
