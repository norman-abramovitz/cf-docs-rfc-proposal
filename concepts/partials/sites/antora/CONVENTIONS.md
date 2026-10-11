# Antora conventions for partials

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#antora-321). Pages and variables follow the
[tables round's conventions](../../../tables/sites/antora/CONVENTIONS.md),
headings the [headings round's](../../../headings/sites/antora/CONVENTIONS.md),
notes the [notes round's](../../../notes/sites/antora/CONVENTIONS.md);
every page is AsciiDoc in every mode.

```bash
make build          # install, fetch the pinned UI, generate site-playbook.yml, build (log in .check/build.log)
make serve          # serve site/ at http://localhost:8002
make check          # build, then the partials, outline and notes checks: passthrough, native, variable
make check-raw      # the same checks on the ERB call as written (raw component)
make check-probe    # one partial with a heading included twice: ids and Asciidoctor's warning
make probe-missing  # a missing partial, here and in another component: message and exit status
```

## The include

AsciiDoc's `include::` directive, on a line of its own where the ERB call
was. Two forms work:

| Mode | Form | Where the partial lives |
|---|---|---|
| passthrough | `include::_oss_scale_table.adoc[]`, a path relative to the page | beside the page in `pages/`; a file whose path has a segment starting with `_` is not published ([`classify-content.js` L153](https://gitlab.com/antora/antora/-/blob/v3.2.1/packages/content-classifier/lib/classify-content.js#L153), [`content-catalog.js` L202](https://gitlab.com/antora/antora/-/blob/v3.2.1/packages/content-classifier/lib/content-catalog.js#L202)) |
| native | `include::partial$oss_scale_table.adoc[]`, a resource id | the module's `partials/` folder; the name needs no underscore |

Antora marks the relative form as deprecated: "bypassing resource ID
resolution for relative include path is @deprecated; scheduled to be
removed in Antora 4"
([`resolve-include-file.js` L22-L32](https://gitlab.com/antora/antora/-/blob/v3.2.1/packages/asciidoc-loader/lib/include/resolve-include-file.js#L22-L32)).
Decision (this round): **partials go in `partials/` and are included by
resource id.**

- **Attributes in a partial render** (`{product_short}`, `{platform_name}`).
- **A partial is AsciiDoc in both modes.** Passthrough keeps the source's
  HTML in passthrough blocks inside it, as the earlier rounds did.

## Where a call sits

The directive must start a line, so a partial is never on the same line
as text.

| Source | AsciiDoc | Result |
|--------|----------|--------|
| a call on a line of its own | the directive on a line of its own | the partial's blocks where the call was |
| `* **Log Cache:** <%= partial 'log_cache' %>`, after text | `* *Log Cache:*`, then `+`, then the directive | the label and the partial as two paragraphs of the item, as the published page looks |
| `1. <%= partial "…" %>`, a whole list step | `. {empty}`, `+`, then `--`, the directive, `--` (an open block) | the whole partial inside the step; the step opens with an empty paragraph (`<p></p>`) before it |

The step needs text on its marker line, so `{empty}` stands for it, and
the partial's several blocks need the open block to stay in the step, as
the tables and notes rounds found for steps that hold several blocks.

## Headings in a partial

- **They reach the table of contents**, which the default UI builds in the
  browser from the page's headings: `#nfs` and `#create-nfs` on
  `using-vol-services` ([browser check](../../results/browser-checks.txt)).
  The static HTML holds no table of contents, so the partials check
  reports its `toc` line as failed ([check](../../results/antora-check.txt)).
- **The same partial twice on one page**: the explicit id
  `[[old-metrics-collector]]` appears twice, and Asciidoctor warns: "id
  assigned to section already in use: old-metrics-collector", naming the
  partial's line and the including page's line. Generated ids are
  numbered (`metrics-collector`, `metrics-collector-2`)
  ([probe](../../results/antora-probe.txt)). It is the only tool of the
  four that reports the duplicate.
- **Excerpts that start below level 2** warn "section title out of
  sequence" (`troubleshoot-app-health`, `routes-domains`); this is the
  excerpt, not the partial ([build warnings](../../results/antora-build-warnings.txt)).

## Nested partials

`partials/using-vol-services.adoc` includes
`partial$external_vol_win_note.adoc`; it renders and passes every check.

## A partial in another content source

A partial in another component is reached by its resource id with the
component's name: `include::shared::partial$routing_conflict.adoc[]`
(component `shared`, module `ROOT`). It is the form for a partial that
lives in another repository: each repository is a content source, and
its components are named in its `antora.yml`.

## A partial chosen by a variable

Attribute references in the target are replaced before the file is
looked up, so the book's form works directly:

```asciidoc
include::native::partial${scale_table}.adoc[]
```

with `scale_table: oss_scale_table` among the attributes
(`variable/high-availability--attribute`). A condition also works:
`ifeval::["{scale_table}" == "oss_scale_table"]` … `endif::[]`
(`variable/high-availability--conditional`). Both pass every check. The
name is resolved at build time from the playbook's attributes.

## Missing partials and the ERB call

- **A missing partial is an error in the log, not a failed build.**
  "target of include not found: partial$does_not_exist.adoc", with the
  page and line; the page shows "Unresolved include directive in
  modules/ROOT/pages/missing.adoc - include::partial$does_not_exist.adoc[]"
  ([`include-processor.js` L59-L66](https://gitlab.com/antora/antora/-/blob/v3.2.1/packages/asciidoc-loader/lib/include/include-processor.js#L59-L66)).
  The build exits with status 0; with `--log-failure-level=error` it exits
  with status 2 ([probe](../../results/antora-probe.txt)). The same for a
  missing partial in another component.
- **The ERB call as written** shows as text (`raw/`,
  [check](../../results/antora-check.txt)).

## How a partial reads in the source

`include::partial$oss_scale_table.adoc[]` names the family and the file;
with another component, its name first. In a list step, the `{empty}`,
`+` and `--` lines around it are AsciiDoc's list markup, which a writer
who does not know AsciiDoc may not expect.
