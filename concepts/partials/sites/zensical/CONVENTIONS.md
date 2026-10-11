# Zensical conventions for partials

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#zensical-0069). Pages and variables follow
the [tables round's conventions](../../../tables/sites/zensical/CONVENTIONS.md),
notes the [notes round's](../../../notes/sites/zensical/CONVENTIONS.md).

```bash
make build          # install, generate vars.yml, build the site (log in .check/build.log)
make serve          # serve site/ at http://localhost:8001
make check          # build, then the partials, outline and notes checks: passthrough, native, snippet, variable
make check-probe    # one partial with a heading included twice: ids and table of contents
make probe-missing  # pages that stop the build: missing partials, a path outside partials/, the ERB call as written
```

## Two includes

Zensical offers two ways to include a file, and they run in a fixed
order:

| | Template engine (macros) | Snippets (pymdownx.snippets) |
|---|---|---|
| Syntax | `<% include "native/_oss_scale_table.md" %>` (Jinja's `include`, in the ERB delimiters the earlier rounds set) | `--8<-- "_oss_scale_table.md"` on a line of its own |
| Runs | first: priority 35 ([`macros.py` L542](https://github.com/zensical/zensical/blob/v0.0.69/python/zensical/extensions/macros.py#L542)) | after the template engine: priority 32 ([`snippets.py` L464](https://github.com/facelessuser/pymdown-extensions/blob/12.1/pymdownx/snippets.py#L464)) |
| Variables in the partial | rendered | **left as written**: `<%= vars.recommended_by %>` shows on the page ([check](../../results/zensical-check.txt)) |
| A partial inside the partial | rendered | left as written |
| Where partials live | one folder, `include_dir` ([`macros.py` L398-L401](https://github.com/zensical/zensical/blob/v0.0.69/python/zensical/extensions/macros.py#L398-L401)); a path that leaves it is refused ("TemplateNotFound: ../probes/_outside.md", [L576-L602](https://github.com/zensical/zensical/blob/v0.0.69/python/zensical/extensions/macros.py#L576-L602)) | a list of folders, `base_path`; by default a path may not leave them ([`snippets.py` L433-L439](https://github.com/facelessuser/pymdown-extensions/blob/12.1/pymdownx/snippets.py#L433-L439)) |
| Indentation | the partial's text is inserted as it is; only its first line has the indentation of the tag | every line gets the indentation of the `--8<--` line ([`snippets.py` L398](https://github.com/facelessuser/pymdown-extensions/blob/12.1/pymdownx/snippets.py#L398)) |
| A missing file | the build stops: "TemplateNotFound: native/_does_not_exist.md" | skipped without a message by default (`check_paths` defaults to false; [L406-L407](https://github.com/facelessuser/pymdown-extensions/blob/12.1/pymdownx/snippets.py#L406-L407)); with `check_paths = true`, as this site sets it, the build stops: "SnippetMissingError: Snippet at path '_does_not_exist.md' could not be found" |

Neither message names the page that holds the include
([probe](../../results/zensical-probe.txt)).

Decision (this round): **partials are included with the template engine**
(passthrough and native). Snippets are kept as a mode of their own,
`snippet/`, to show why: five of its six pages fail, every failure a
variable or a nested include left as written.

## The include

```markdown
## Recommended instance counts for high availability {#instance-counts}

<%= vars.scaling_ert %>

<% include "native/_oss_scale_table.md" %>
```

- **Partials live in `partials/<mode>/`**, outside `docs/`, so they are
  never pages; `include_dir = "partials"`.
- **The file name keeps its leading underscore** and ends in `.md`.
- **Passthrough** includes the source partial with the source's content;
  **native** includes a partial whose content is Markdown, with native
  admonitions and native heading ids (`## Text {#nfs}`).
- **Do not make the site's folder the include folder.** With
  `include_dir = "."` (the folder that holds `.venv/`), the build printed
  "Build started" and then nothing for more than 100 seconds, twice; the
  same pages and settings in a folder without `.venv/` built in 0.5
  seconds. The cause was not traced.

## Where a call sits

| Source | Zensical | Result |
|--------|----------|--------|
| a call on a line of its own | the include on a line of its own | the partial's blocks where the call was |
| `* **Log Cache:** <%= partial 'log_cache' %>` | passthrough: `* **Log Cache:** <% include "passthrough/_log_cache.md" %>` | one paragraph: label and text together |
| | native: the label, a blank line, and the include indented four spaces under the item | the label and the partial as two paragraphs of the item, as the published page looks |
| `1. <%= partial "…" %>`, a whole list step, partial with indented blocks | passthrough: `1. <% include "passthrough/_tcp_modify_ports.md" %>` | the partial's last paragraph, indented two spaces in the source, ends the list, as on the published page ([check](../../results/zensical-check.txt)) |
| | native: `1. <% filter indent(4) %><% include "native/_tcp_modify_ports.md" %><% endfilter %>` | the whole partial inside the step |
| | snippet: `1. <!-- -->`, then the `--8<--` line indented four spaces | the whole partial inside the step; a list item cannot start with a snippet line, so the item opens with an empty comment |

Decision (this round): **a partial included in a list item is wrapped in
Jinja's `indent` filter** with the item's content indent, so every line of
it belongs to the item. The partial's own text needs no indentation.

## Headings in a partial

- **They reach the table of contents**: the template engine renders the
  page before Markdown reads it. With the partial's headings written
  `## Text {#nfs}`, the table of contents links to `#nfs` and
  `#create-nfs`. With the source's `## <a id='nfs'></a> Text`
  (passthrough), it links to the generated ids instead
  (`#create-and-use-nfs-volume-services`), as the headings round found
  for any heading.
- **The same partial twice on one page**: the explicit id appears twice;
  generated ids are numbered (`metrics-collector`, `metrics-collector_1`),
  because the page is one Markdown document by then. No warning
  ([probe](../../results/zensical-probe.txt)).
- **The build's anchor check does not see a partial's links.** It reports
  the host page's `#modify-ports` and `#system-metrics-agents`, with file
  and line, but not the `#modify-ports` and `#migrate` links inside the
  partials ([build warnings](../../results/zensical-build-warnings.txt)).

## Nested partials

`partials/native/_using-vol-services.md` includes
`native/_external_vol_win_note.md` with the same tag; it renders. Through
snippets it would stay as text.

## A partial in another content source

Every template-engine include resolves under `include_dir`, so a shared
partial from another source has to sit under it:
`partials/shared/_routing_conflict.md`, included as
`<% include "shared/_routing_conflict.md" %>`. A checkout of another
repository would go there. Snippets can list folders anywhere in
`base_path` (`["partials/native", "partials/shared"]`), but render no
variables.

## A partial chosen by a variable

The template engine takes an expression for the name:

```markdown
<% include "native/_" ~ vars.scale_table ~ ".md" %>
```

It passes every check (`docs/variable/high-availability--include.md`). The
name is resolved at build time, from `vars.yml`.

## Variables with no value

`scaling_ert:` has no value in the book's file; YAML reads it as null, and
the template engine printed "None" in its place. The site's `vars.yml`
writes such values as `""` (see the Makefile). This belongs to the
variables concept.

## The ERB call as written

`<%= partial 'oss_scale_table' %>` stops the build: "TemplateSyntaxError:
expected token 'end of print statement', got 'string'"
([probe](../../results/zensical-probe.txt)).

## How a partial reads in the source

`<% include "native/_oss_scale_table.md" %>` reads like the source's call,
with the file's folder and full name. In a list step the `filter indent`
wrapper adds two tags around it.
