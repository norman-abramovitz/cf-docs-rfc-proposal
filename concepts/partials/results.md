# Partials round — results

Status: draft, incomplete — covers what is known as of 2026-10-11.

What each tool did with the test pages' partials. A summary across tools
comes first, then one section per tool, then the cases across tools, a
recommendation on partial names held in variables, and the conventions
to record. How the pages were chosen and what the modes mean:
[README](README.md). Per-page intent: [intent/](intent/). How the book
writes and resolves partials: [survey](survey/README.md).

How to read the results:

- **Partials check:** the [partials check](checks/partials.py) finds each
  partial's first and last words on a built page and compares their place
  with the page's partials file ([intent/](intent/)): the host's words just
  before and after, the section, whether it sits in a list item or the
  body, how often the partial's text appears, include syntax left on the
  page, ids used twice inside an included span, and, where the file asks,
  the ids in the table of contents. "6 of 6" means every test page passes.
- **Outline and notes checks:** the headings round's
  [outline check](../headings/checks/outline.py) on every page, with the
  page's anchors, and the notes round's [notes check](../notes/checks/notes.py)
  on the two pages with notes.
- **Modes:** *passthrough* is the include closest to the ERB call that the
  tool allows, the partial beside its page and named as today, its content
  as the earlier rounds' passthrough; *native* is the tool's own include
  and partial location, with native content; *variable* takes the
  partial's name from a variable; *raw* is the ERB call as written.
  Zensical adds *snippet*, its second include.

All checks ran on 2026-10-11 against the published pages saved that day
and the earlier rounds' copies, with the tool versions the earlier rounds
pinned (Docusaurus 3.10.2, Zensical 0.0.69, Starlight 0.42.6 with
`@astrojs/markdoc` 2.0.11, Antora 3.2.1).

## Summary

Every tool renders every partial in the right place, with its headings,
lists, notes, tables and variables, in both passthrough and native, once
the call sits on a line of its own. They differ in what a call next to
text needs, whether a partial's name can come from a variable, and what
the build says when something is wrong.

| | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| **Partials check, native** | 6 of 6 | 6 of 6 | 6 of 6 | 6 of 6, the table of contents checked in the browser |
| **Partials check, passthrough** | 6 of 6 | 4 of 6: step 5's last paragraph leaves the list, as published; table of contents uses generated ids | 6 of 6 | 6 of 6, the table of contents checked in the browser |
| **Include** | `import X from './_x.mdx'` and `<X />` | `<% include "native/_x.md" %>` (template engine); `--8<--` snippets render no variables | `{% partial file="./_x.mdoc" /%}` | `include::partial$x.adoc[]` |
| **Call after text in a list item** | builds; React hydration error #418 in the browser | builds; label and text joined in one paragraph | the build stops: "'partial' tag should be block" | not possible; the directive starts a line |
| **Partial that is a whole list step** | `1. <X />` | `filter indent(4)` around the include | `1. {% partial … /%}` | `. {empty}`, `+`, open block |
| **Headings in a partial in the table of contents** | yes | yes | yes | yes (built in the browser) |
| **Same partial twice: explicit id** | twice, no message | twice, no message | twice, no message | twice, with a warning naming partial and page |
| **Nested partial** | yes | yes (snippets: no) | yes | yes |
| **Partial in another content source** | `@site/shared/…`, no configuration | must sit under `include_dir`; snippets take a list of folders | a relative path out of the content folder, no configuration | `include::shared::partial$…[]`, another component |
| **Name from a variable** | only through page code (a map, `require`, a condition) | `<% include "native/_" ~ vars.scale_table ~ ".md" %>` | no: "Could not read partial file `[object Object]`"; a condition works | `include::native::partial${scale_table}.adoc[]` |
| **Missing partial** | build fails; names the folder, not the page | build fails; names neither | build fails; names the page | error in the log with page and line; exit status 0 unless `--log-failure-level` is set |
| **ERB call as written** | does not compile | build fails | text on the page | text on the page |

- **The book's own rendering has two defects the tools do not have.** The
  book renders a partial to HTML before the page's Markdown reads it. So
  `_tcp_modify_ports`, the whole of a list step, loses its last paragraph
  to the space after the list on the published page, and the "On this
  page" list leaves out every heading a partial holds:
  `using-vol-services` has an empty one
  ([published check](results/published-check.txt);
  [survey](survey/README.md#how-the-book-resolves-a-partial)). In
  Docusaurus, Starlight and Antora, and in Zensical native, the paragraph
  stays in the step and the headings are in the table of contents.
  Treated as defects (Docs WG lead, 2026-10-11): the converted pages fix them.
- **The book needs few partial patterns.** 45 calls, all
  `<%= partial '…' %>` with a literal name, none in a conditional, none
  with `locals:`, none crossing a repository, no nesting, and four in list
  items ([survey](survey/README.md#findings)). The converter's rules are
  correspondingly few ([Conventions](#conventions-to-record)).
- **No page uses a partial name held in a variable**, and none has since
  August 2024 ([below](#are-partial-names-in-variables-still-needed)).

## Docusaurus 3.10.2

Site: [sites/docusaurus/](sites/docusaurus/) — conventions:
[CONVENTIONS.md](sites/docusaurus/CONVENTIONS.md).

### Summary

- **Every partial renders in place in passthrough, native and the three
  variable forms** ([check](results/docusaurus-check.txt)).
- **A partial after text in a list item breaks the page in the browser.**
  `* **Log Cache:** <LogCache />` builds, and the static HTML splits the
  label and the partial's paragraph; React then reports error #418, a
  hydration mismatch, on load ([browser check](results/browser-checks.txt)).
  Native puts the partial on its own line under the item: no error.
- **Headings in an imported partial reach the table of contents**, through
  the docs plugin's handling of imported Markdown
  ([conventions](sites/docusaurus/CONVENTIONS.md#headings-in-a-partial)).
- **The build's link check covers partials**: links inside a partial are
  reported on the including page (`#modify-ports`, `#migrate`;
  [build warnings](results/docusaurus-build-warnings.txt)).
- **A name from a variable needs code in the page**: an object of imports,
  `require` with a template string, or a condition.

### Grid

| Mode | high-availability | architecture | enabling-tcp-routing | troubleshoot-app-health | routes-domains | using-vol-services |
|------|------|------|------|------|------|------|
| passthrough | ok | ok; React #418 in the browser | ok | ok | ok | ok; toc ok |
| native | ok | ok | ok | ok (shared partial) | ok (shared partial) | ok; toc ok; nested |
| variable | map, require, condition: ok | | | | | |
| raw | does not compile | | | | | |

"ok" is the partials, outline and (where the page has notes) notes checks.

## Zensical 0.0.69

Site: [sites/zensical/](sites/zensical/) — conventions:
[CONVENTIONS.md](sites/zensical/CONVENTIONS.md).

### Summary

- **The template engine's include renders partials, snippets do not.**
  The template engine runs before snippets, so a snippet's variables and
  nested includes stay as written: five of six snippet pages fail
  ([check](results/zensical-check.txt)). Native, with the template
  engine, passes on every page.
- **The include is textual**: the partial's lines go where the tag is,
  with no indentation added. Passthrough's step 5 therefore ends the list
  at the partial's last paragraph, as the published page does; native
  wraps the include in Jinja's `indent` filter and keeps it in the step.
- **The name can come from a variable**: Jinja's include takes an
  expression.
- **Errors name neither the page nor the line**: "TemplateNotFound:
  native/_does_not_exist.md" ([probe](results/zensical-probe.txt)).
- **The anchor check does not see a partial's links**; it reports the
  host pages' broken anchors only ([build warnings](results/zensical-build-warnings.txt)).
- **Two findings for other concepts**: an empty variable prints "None"
  (the site writes empty values as `""`), and an include folder that holds
  the virtual environment made the build hang
  ([conventions](sites/zensical/CONVENTIONS.md#the-include)).

### Grid

| Mode | high-availability | architecture | enabling-tcp-routing | troubleshoot-app-health | routes-domains | using-vol-services |
|------|------|------|------|------|------|------|
| passthrough | ok | ok | step 5's last paragraph after the list | ok | ok | toc links to generated ids |
| native | ok | ok | ok | ok (shared partial) | ok (shared partial) | ok; toc ok; nested |
| snippet | variable left as ERB | variables left as ERB | ok | variable left as ERB | variable left as ERB | variables and nested include left as ERB |
| variable | `include` with an expression: ok | | | | | |
| raw | build fails | | | | | |

## Starlight 0.42.6

Site: [sites/starlight/](sites/starlight/) — conventions:
[CONVENTIONS.md](sites/starlight/CONVENTIONS.md).

### Summary

- **Every partial renders in place in passthrough and native**
  ([check](results/starlight-check.txt)).
- **The partial tag is a block tag.** After text in a list item it stops
  the build ("'partial' tag should be block"); on its own line under the
  item it works, in both modes ([probe](results/starlight-probe.txt)).
- **The path is resolved like an import**, so a partial outside the
  content folder needs no configuration.
- **A name cannot come from a variable**: partials are read before
  variables have values. A Markdoc condition works.
- **A missing partial stops the build and names the page.**

### Grid

| Mode | high-availability | architecture | enabling-tcp-routing | troubleshoot-app-health | routes-domains | using-vol-services |
|------|------|------|------|------|------|------|
| passthrough | ok | ok (partial moved below the label) | ok | ok | ok | ok; toc ok |
| native | ok | ok | ok | ok (shared partial) | ok (shared partial) | ok; toc ok; nested |
| variable | condition: ok; `file=$vars…`: build stops | | | | | |
| raw | ERB call shown as text | | | | | |

## Antora 3.2.1

Site: [sites/antora/](sites/antora/) — conventions:
[CONVENTIONS.md](sites/antora/CONVENTIONS.md).

### Summary

- **Every partial renders in place in passthrough and native**
  ([check](results/antora-check.txt)); the table of contents, built in the
  browser, lists the partial's headings ([browser check](results/browser-checks.txt)).
- **Partials have a place of their own**: the module's `partials/` folder,
  included by resource id; another component's by its name. The relative
  include of a file beside the page works but is deprecated.
- **The book's variable form works as it is**:
  `include::native::partial${scale_table}.adoc[]`.
- **The only tool that warns about an id used twice**, naming the
  partial's line and the page's.
- **A missing partial is logged as an error** with page and line, but the
  build succeeds unless `--log-failure-level` is set
  ([probe](results/antora-probe.txt)).

### Grid

| Mode | high-availability | architecture | enabling-tcp-routing | troubleshoot-app-health | routes-domains | using-vol-services |
|------|------|------|------|------|------|------|
| passthrough | ok | ok | ok | ok | ok | ok; toc in the browser |
| native | ok | ok | ok | ok (shared component) | ok (shared component) | ok; toc in the browser; nested |
| variable | attribute in the path, condition: ok | | | | | |
| raw | ERB call shown as text | | | | | |

## Across tools

### Where a call sits

The survey found four calls that are not on a line of their own, all in
list items ([survey](survey/README.md#findings)):

- **After a bold label** (`architecture`, three calls). Today the book
  publishes `<p><strong>Log Cache:</strong> <p>…</p></p>`, which a browser
  shows as two paragraphs. No tool takes the call as written without a
  cost: Starlight and Antora cannot, Docusaurus builds a page that errors
  in the browser, Zensical joins label and text into one paragraph.
  Decision (this round): the label stays the item's first paragraph, the
  partial follows on its own line under it. That reproduces the published
  look in every tool and passes every check.
- **As the whole of a list step** (`enabling-tcp-routing`). The tools that
  read a partial as a document of its own (Docusaurus, Starlight) keep all
  of it in the step. The textual includes (Zensical's template engine,
  Antora) need the partial's lines placed inside the item: Jinja's
  `indent` filter, or AsciiDoc's `+` and open block.

### Headings, ids and the table of contents

- **Headings inside a partial reach the table of contents in every tool**,
  with the ids written in the tool's heading syntax. In the book they do
  not.
- **A partial included twice repeats its explicit ids in every tool.**
  Generated ids are numbered in Zensical, Starlight and Antora (the page is
  one document when ids are made) and repeated in Docusaurus (each imported
  file gets its ids on its own) ([probes](results/)). Only Antora warns.
  The book has no partial with a heading included twice today
  ([survey](survey/README.md#findings)), so this is a rule to keep, not a
  page to fix.

### Partials in other repositories

No partial call in the book crosses a repository today; the 25 that did
pointed at the commercial edition's folders and were removed in July 2026
([survey](survey/README.md#history)). Every tool can reach a partial
outside the page's content tree: Docusaurus and Starlight by import path,
Zensical by putting the files under its include folder, Antora by
component name. Which of these fits depends on where the content lives
after migration ([R-08](../../requirements/README.md#r-08) cross-repository
links), not on the partials.

### Missing partials

Every tool notices a missing partial at build time. Docusaurus, Zensical
and Starlight fail the build; Antora logs an error and succeeds unless its
failure level is set, and then shows "Unresolved include directive" on the
page. Starlight and Antora name the page; Docusaurus names its folder;
Zensical names neither. The book, through Middleman, fails the build and
goes on rendering the other pages
([survey](survey/README.md#how-the-book-resolves-a-partial)).

### How a partial reads in the source

The same call, `high-availability`'s, as each tool writes it:

```erb
<%= partial 'oss_scale_table' %>
```

```mdx
import OssScaleTable from './_oss_scale_table.mdx';

<OssScaleTable />
```

```markdown
<% include "native/_oss_scale_table.md" %>
```

```markdown
{% partial file="./_oss_scale_table.mdoc" /%}
```

```asciidoc
include::partial$oss_scale_table.adoc[]
```

Zensical, Starlight and Antora write one line where the source has one,
with the file's name in it. Docusaurus writes two, far apart, and names the
file only in the import ([R-11](../../requirements/README.md#r-11) readable
source).

## Are partial names in variables still needed?

The research area asks whether a page must still be able to pick its
partial from a variable
([research area](../../requirements/research-areas.md#are-partial-names-in-variables-still-needed)).
Evidence from this round:

1. **No page does it.** Ten values in the book's variables name a partial
   file; no page at the surveyed commits uses any of them, and every
   partial they name is included by its literal name
   ([survey](survey/README.md#partial-names-held-in-variables)).
2. **It served two editions.** The form came in to let one source include
   a different partial in the open-source and the commercial book
   ("moving partials into variables to remove commercial refs in OSS",
   2018). Literal names replaced it from 2023; the last change to such a
   call is dated 2024-08-20. The commercial branches were removed in July
   2026, when the repositories came to serve "only the OSS Cloud Foundry
   doc set" ([survey](survey/README.md#history)).
3. **Tools differ exactly here.** Zensical and Antora take a name from a
   variable directly; Docusaurus needs JavaScript in the page; Starlight
   cannot, except through a condition that lists every partial
   ([grids above](#summary)). A requirement to keep the form would rule
   out, or add code to, two of the four tools for a feature with no user.

Recommendation, accepted (Docs WG lead, 2026-10-11): **partial names in variables
are not needed.**
The converter resolves any such name when it converts and writes a plain
include, and the ten unused variables are removed from the book's
variables file in the cleanup before conversion
([R-24](../../requirements/README.md#r-24) markup cleanup before
conversion; list: [cleanup.md](cleanup.md)). If a second edition returns, each tool's own mechanism (an
attribute in Antora, an expression in Zensical, a condition in the
others) can be chosen then.

## Conventions to record

For `cf-docs-migrate convert`. Decisions of this round, for review:

1. **A partial becomes a file of the tool's own format, included with the
   tool's own include** (native mode): an imported MDX component
   (Docusaurus), the template engine's `include` (Zensical), the Markdoc
   partial tag (Starlight), `include::partial$…[]` (Antora).
2. **Where partial files live:** beside their pages with the leading
   underscore kept, `_name.mdx` (Docusaurus) and `_name.mdoc` (Starlight);
   under `partials/` outside `docs/` (Zensical); the module's `partials/`
   folder without the underscore (Antora). The source's `_name.html.md.erb`
   loses `.html.md.erb` for the tool's extension.
3. **The converter's rule for each call form in the book:**
   `<%= partial 'name' %>` and `"name"` alike; `./name` and `./dir/name`
   relative to the page; `../<directory>/name` resolved through the book's
   `config.yml` to the repository and file it names today. A call on a
   line of its own becomes the tool's include on a line of its own.
4. **A partial after text in a list item goes on its own line under the
   item**, after the text, which stays the item's first paragraph.
   **Accepted** (Docs WG lead, 2026-10-11).
5. **A partial that is a list step's content is placed inside the step**:
   the include indented under the item (Docusaurus, Starlight), wrapped in
   `filter indent(N)` (Zensical), or after `{empty}`, `+` and inside an
   open block (Antora).
6. **A partial name held in a variable is resolved at conversion time**;
   no converted page takes a partial's name from a variable
   ([recommendation](#are-partial-names-in-variables-still-needed)).
   **Accepted** (Docs WG lead, 2026-10-11).
7. **Headings in partials carry explicit ids in the tool's syntax**, as on
   pages (headings round), and a partial with headings is not included
   twice on one page; the partials check fails on an id used twice inside
   an included span.
8. **The build fails on a missing partial**: Zensical with
   `on_error_fail` (and `check_paths` if snippets are used), Antora with
   `--log-failure-level=error`; Docusaurus and Starlight do by default.
   **Accepted** (Docs WG lead, 2026-10-11), for CI as well.
9. **The partials check runs on every converted page that includes a
   partial**, beside the outline and notes checks:
   [checks/partials.py](checks/partials.py).

## Requirements

- [R-05](../../requirements/README.md#r-05) partials and reuse: every tool
  includes a partial and renders it inside the page, with headings, lists,
  notes, tables and variables; a name from a variable is possible in two
  tools and not needed by any page.
- [R-01](../../requirements/README.md#r-01) content and outline survive:
  checked for each partial's place and the page's headings; the
  published page itself loses a paragraph from a list step and its quick
  links. Body text was not compared word by word.
- [R-04](../../requirements/README.md#r-04) variables everywhere:
  variables inside partials render in every tool's main include; not
  through Zensical's snippets. An empty variable prints "None" in Zensical
  unless written as `""`.
- [R-07](../../requirements/README.md#r-07) notes and admonitions: the two
  notes held in variables on the test pages become partials (accepted
  convention), one of them nested in another partial; both pass the notes
  check.
- [R-08](../../requirements/README.md#r-08) cross-repository links: every
  tool reaches a partial in another content source; none is needed today.
- [R-11](../../requirements/README.md#r-11) readable source: three tools
  write a one-line include naming the file; Docusaurus splits it into an
  import and a component.
- [R-13](../../requirements/README.md#r-13) no per-WG extensions: no
  extension was written; Docusaurus's variable forms put code in the page.
- [R-24](../../requirements/README.md#r-24) markup cleanup before
  conversion: the ten unused partial-name variables and the three partials
  no page includes are candidates for removal.

## Not yet written

- **Body text.** The partials check compares each partial's first and
  last words and their place; the words between were not compared.
- **The other partials with headings.** Eight more partials hold headings
  (`_c2c_oss_*`, `_oss_credhub`, `_oss_xfcc_*`, `_old_collector`,
  `_go_tcp_routers_health_check_oss`); only `_using-vol-services` was
  converted. The probe used `_old_collector`'s heading.
- **`./metrics/…` partials** in a subfolder (`all_metrics`, eight calls):
  resolved by the survey, not converted. Relative links inside a partial
  resolve against the including page in the book; that was not tested in
  the tools.
- **A missing partial named by a variable**, and Docusaurus's `require`
  form when the variable names no file, were not tested.
- **Starlight with an alias** for a shared folder, and Docusaurus with a
  partial from an installed package, were not tried.
- **`docs-bosh` snippets** (two SVG diagrams) were counted, not converted.
- **Probes and on-paper tools.** Eleventy, Sphinx/MyST, Middleman, Hugo and
  VitePress were not part of this round. The tables round's Middleman probe
  ran the book's partial call unchanged.
