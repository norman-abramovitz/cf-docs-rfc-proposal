# Starlight conventions for partials

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#starlight-0426). Pages and variables follow
the [tables round's conventions](../../../tables/sites/starlight/CONVENTIONS.md),
headings the [headings round's](../../../headings/sites/starlight/CONVENTIONS.md)
(`## Text {% #id %}`), notes the [notes round's](../../../notes/sites/starlight/CONVENTIONS.md).

```bash
make build          # install, generate vars.json, build the site (log in .check/build.log)
make serve          # serve dist/ at http://localhost:4321
make check          # build, then the partials, outline and notes checks: passthrough, native, variable
make check-raw      # the same checks on the ERB call as written (raw/)
make check-probe    # one partial with a heading included twice: ids and table of contents
make probe-missing  # pages that stop the build: a missing partial, an inline partial, a name from a variable
```

## The include

Markdoc's partial tag, where the ERB call was:

```markdown
## Recommended instance counts for high availability {% #instance-counts %}

{% $vars.scaling_ert %}

{% partial file="./_oss_scale_table.mdoc" /%}
```

- **The file name keeps its leading underscore**, `_oss_scale_table.mdoc`,
  and sits beside its page; the content collection's pattern,
  `**/[^_]*.{md,mdx,mdoc}`, leaves it out of the pages
  ([content.config.ts](src/content.config.ts)).
- **The path is resolved like a module import**, from the page's file:
  Astro's Markdoc integration asks the bundler to resolve `file`, then
  `./` + `file`, and reads that file
  ([`content-entry-type.ts` L186-L208](https://github.com/withastro/astro/blob/3571e2d2e80a66764254fa9b7750704a150ca3f6/packages/integrations/markdoc/src/content-entry-type.ts#L186-L208),
  `@astrojs/markdoc` 2.0.11). So a partial can live anywhere the bundler
  reaches.
- **Variables in a partial render**: the partial shares the page's
  `$vars`. The tag also takes `variables=…`, values for the partial alone
  ([`partial.ts` L21-L27](https://github.com/markdoc/markdoc/blob/v0.5.10/src/tags/partial.ts#L21-L27)),
  the counterpart of ERB's `locals:`; no page in the book uses `locals:`.
- **Passthrough and native use the same tag**; they differ in the
  partial's content (HTML kept, with the earlier rounds' forced changes, or
  Markdown with asides).

## Where a call sits

| Source | Markdoc | Result |
|--------|---------|--------|
| a call on a line of its own | the tag on a line of its own | the partial's blocks where the call was |
| `1. <%= partial "…" %>`, a whole list step | `1. {% partial file="./_tcp_modify_ports.mdoc" /%}` | the whole partial inside the step, its last paragraph included |
| `* **Log Cache:** <%= partial 'log_cache' %>`, after text | as written: the build stops, "'partial' tag should be block" (three times, for the three calls; [probe](../../results/starlight-probe.txt)) | the tag is a block tag ([`partial.ts` L22](https://github.com/markdoc/markdoc/blob/v0.5.10/src/tags/partial.ts#L22), [`validator.ts` L149-L155](https://github.com/markdoc/markdoc/blob/v0.5.10/src/validator.ts#L149-L155)) |
| | the label, a blank line, and the tag indented under the item (passthrough and native) | the label and the partial as two paragraphs of the item, as the published page looks |

Forced change: **a partial after text goes on a line of its own**, under
the item. Passthrough and native `architecture` are therefore the same
file.

## Headings in a partial

- **They reach the table of contents** with their ids (`#nfs`,
  `#create-nfs` on `using-vol-services`), static in the HTML
  ([check](../../results/starlight-check.txt)).
- **The same partial twice on one page**: the explicit id
  (`{% #old-metrics-collector %}`) appears twice; generated ids are
  numbered (`metrics-collector`, `metrics-collector-1`). No warning
  ([probe](../../results/starlight-probe.txt)).
- **No link check** at build time, as in the earlier rounds.

## Nested partials

A partial's own `{% partial %}` tag is resolved from the partial's file
(the integration resolves partials of partials,
[L154-L230](https://github.com/withastro/astro/blob/3571e2d2e80a66764254fa9b7750704a150ca3f6/packages/integrations/markdoc/src/content-entry-type.ts#L154-L230));
`_using-vol-services.mdoc` includes `./_external_vol_win_note.mdoc` and
passes every check.

## A partial in another content source

`{% partial file="../../../../shared/_routing_conflict.mdoc" /%}` reaches
`shared/`, a folder outside `src/content/`, with no configuration. Because
the bundler resolves the path, an alias set in the Astro configuration
would also work; not tried.

## A partial chosen by a variable

| Form | Result |
|---|---|
| `{% partial file=$vars.scale_table /%}` | the build stops: "Could not read partial file `[object Object]`. Does the file exist?" ([probe](../../results/starlight-probe.txt)): partials are resolved before variables have values |
| `{% if equals($vars.scale_table, "oss_scale_table") %}` `{% partial file="../native/_oss_scale_table.mdoc" /%}` `{% /if %}` | builds and passes every check (`variable/high-availability--conditional`); one condition per possible partial; from the source, every partial tag in the page is resolved and read, whatever the condition, because the integration walks the whole tree ([L174](https://github.com/withastro/astro/blob/3571e2d2e80a66764254fa9b7750704a150ca3f6/packages/integrations/markdoc/src/content-entry-type.ts#L174)); not tested with a missing partial |

Decision (this round): the converter resolves the name when it converts.

## Missing partials and the ERB call

- **A missing partial stops the build**, naming the page: "**src/content/docs/probe/missing.mdoc**
  contains invalid content: Could not read partial file
  `./_does_not_exist.mdoc`. Does the file exist?"
  ([probe](../../results/starlight-probe.txt)).
- **The ERB call as written** builds and shows as text,
  `<%= partial 'oss_scale_table' %>` ([check](../../results/starlight-check.txt), `raw/`).

## How a partial reads in the source

`{% partial file="./_oss_scale_table.mdoc" /%}` names the file where the
content appears, as the source's call does, with the full file name.
