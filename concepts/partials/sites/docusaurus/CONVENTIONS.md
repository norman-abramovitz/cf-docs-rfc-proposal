# Docusaurus conventions for partials

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#docusaurus-3102). Pages and variables follow
the [tables round's conventions](../../../tables/sites/docusaurus/CONVENTIONS.md),
headings the [headings round's](../../../headings/sites/docusaurus/CONVENTIONS.md)
(`## Text {#id}`), notes the [notes round's](../../../notes/sites/docusaurus/CONVENTIONS.md).

```bash
make build          # install, generate vars.json, build the site (log in .check/build.log)
make serve          # serve build/ at http://localhost:3000
make check          # build, then the partials, outline and notes checks: passthrough, native, variable
make check-raw      # the MDX error for the ERB call as written (raw-mdx/)
make check-probe    # one partial with a heading included twice: ids and table of contents
make probe-missing  # a page that includes a partial that does not exist: the build's message
```

## The include

MDX has one include: the partial is an MDX file, imported at the top of
the page and used as a component where the ERB call was.

```mdx
import OssScaleTable from './_oss_scale_table.mdx';

## Recommended instance counts for high availability {#instance-counts}

<OssScaleTable />
```

- **The file name keeps its leading underscore**, `_oss_scale_table.mdx`:
  the docs plugin does not make a page of a file whose name starts with
  `_` (its default `exclude`,
  [`globUtils.ts` L24-L26](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-utils/src/globUtils.ts#L24-L26)).
- **The component name** is the file name in PascalCase without the
  underscore: `_routing_conflict.mdx` → `RoutingConflict`.
- **Variables in a partial**: the partial imports `vars` itself
  (`import vars from '@site/vars.json';`), as in the tables round.
- **Passthrough and native use the same include**; they differ in the
  partial's content (HTML kept, or Markdown, admonitions and native heading
  ids).

## Where a call sits

| Source | MDX | Result |
|--------|-----|--------|
| a call on a line of its own | `<Partial />` on a line of its own | the partial's blocks where the call was ([check](../../results/docusaurus-check.txt)) |
| `1. <%= partial "…" %>`, a whole list step | `1. <TcpModifyPorts />` | the whole partial inside the step, its last paragraph included, which the published page puts after the list |
| `* **Log Cache:** <%= partial 'log_cache' %>`, after text in an item | passthrough: `* **Log Cache:** <LogCache />`; native: the label, a blank line, and `  <LogCache />` indented under the item | passthrough builds, and the static HTML holds the label and the partial's paragraph as two paragraphs; in the browser React reports error #418, a hydration mismatch ([browser check](../../results/browser-checks.txt)). Native has no error and looks as the published page does |

Decision (this round): **a partial that holds blocks goes on a line of its
own**; after text in a list item, the label stays the item's first
paragraph and the partial follows, indented under the item.

## Headings in a partial

- **They reach the table of contents.** `using-vol-services` is a page
  whose only content is `<UsingVolServices />`; its table of contents
  lists `#nfs` and `#create-nfs` from the partial
  ([check](../../results/docusaurus-check.txt)). Docusaurus collects the
  table of contents of an imported Markdown file used as a component on a
  line of its own (`mdxJsxFlowElement`), when the import path ends in
  `.md` or `.mdx`
  ([`toc/index.ts` L101-L106, L124-L150](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-mdx-loader/src/remark/toc/index.ts#L101-L150),
  [`toc/utils.ts` L30-L36](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-mdx-loader/src/remark/toc/utils.ts#L30-L36)).
  From that source, a partial used inline after text, or one chosen by a
  variable (below), would not add its headings; no test page has headings
  in such a partial.
- **The same partial twice on one page gives the same ids twice.** Both
  the explicit id (`{#old-metrics-collector}`) and the generated one
  (`metrics-collector`) appear twice, and the table of contents links to
  each twice; the build says nothing
  ([probe](../../results/docusaurus-probe.txt)). Each imported file is
  given its ids on its own.

## Nested partials

A partial imports another partial the same way: `_using-vol-services.mdx`
imports `_external_vol_win_note.mdx` (the note held in a variable, a
partial since the notes round). It passes every check.

## A partial in another content source

`import RoutingConflict from '@site/shared/_routing_conflict.mdx';`
includes a partial from `shared/`, a folder outside `docs/`. It builds
with no configuration, and the build's link check reports the links inside
it on the including page ([build warnings](../../results/docusaurus-build-warnings.txt)).
A partial from another repository would need that repository's files in
the site's folder (a checkout or a package) and an import path to them.

## A partial chosen by a variable

ESM imports name a fixed file, so `partial vars.scale_table` has no direct
form. Three forms build and pass every check (`docs/variable/`):

| Page | Form | When the name is resolved |
|---|---|---|
| `high-availability--map` | `import OssScaleTable …;` then `export const partials = {oss_scale_table: OssScaleTable};` and `<ScaleTable />` with `ScaleTable = partials[vars.scale_table]` | at build time from `vars.json`, among the partials the page imports |
| `high-availability--require` | ``export const ScaleTable = require(`../native/_${vars.scale_table}.mdx`).default;`` | at build time; webpack bundles every file the pattern can match |
| `high-availability--conditional` | `{vars.scale_table === 'oss_scale_table' && <OssScaleTable />}` | at build time; one condition per choice |

All three put JavaScript in the page. The map and the condition must list
every possible partial. Decision (this round): the converter resolves the
name when it converts and writes a plain import (convert-time resolution).

## Missing partials and the ERB call

- **A missing partial stops the build**: "Module not found: Error: Can't
  resolve './_does_not_exist.mdx' in '<site>/docs/probe'", exit status 1.
  The message names the folder, not the page
  ([probe](../../results/docusaurus-probe.txt)).
- **The ERB call as written does not compile**: "Unexpected character `%`
  (U+0025) before name" ([raw check](../../results/docusaurus-raw-check.txt)).

## How a partial reads in the source

The import line at the top names the file; the call in the body is a
component name. A reader sees where the content comes from only by
looking up the import. The source's one-line call becomes two lines, one
of them far from the place where the content appears.
