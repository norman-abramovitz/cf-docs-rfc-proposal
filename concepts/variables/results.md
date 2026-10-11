# Variables round — results

Status: draft, incomplete — covers what is known as of 2026-10-11.

What each tool did with the five test pages' variables. A summary across
tools comes first, then one section per tool, then each place a variable
can sit, what to do with names that are not defined, where values that
hold markup should live, and the conventions to record. How the pages
were chosen and what the modes mean: [README](README.md). Per-page uses:
[intent/](intent/). How the book uses variables:
[survey](survey/README.md).

How to read the results:

- **Variables check:** the [variables check](checks/vars.py) reads a
  built page. It fails on any variable syntax left on the page, in its
  text, its attributes, its head or its table of contents, and on markup
  or Markdown shown as text. Then it looks for each use in the page's
  variables file ([intent/](intent/)): the value's text in the element and
  section where the book renders it, its links as links. "85 of 85" means
  every use on the five pages is in place; 4 of the 85 are names that are
  not defined, which pass when nothing of them is on the page.
- **Outline check:** the headings round's
  [outline check](../headings/checks/outline.py) on every page, with its
  anchors; and the notes round's [notes check](../notes/checks/notes.py)
  on `routes-domains`, the one page with notes.
- **Modes:** *passthrough* writes each `<%= vars.name %>` as the tool's
  own variable reference, with the book's values as they are and the
  forms the earlier rounds use; *native* uses the tool's mechanism fully:
  values prepared for the tool, every name required at build. *raw* is a
  page exactly as the book writes it.

All checks ran on 2026-10-11 against the published pages saved that day,
with the tool versions the earlier rounds pinned.

## Summary

In native mode every value is in place in every tool, on all five pages:
85 of 85, with every outline, anchor and note kept
([checks](results/)). Passthrough shows what a mechanical translation of
the tag gets: everything in Zensical; in the other three tools every
text value but not Markdown values; in Docusaurus and Starlight not link
targets or titles either, and in Docusaurus the table of contents only
through the site's heading plugin.

| | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| **Values in place, passthrough** | 75 of 85 | 85 of 85 | 73 of 85 | 78 of 85 |
| **Values in place, native** | 85 of 85 | 85 of 85 | 85 of 85 | 85 of 85 |
| **A variable in the source** | `{vars.name}` | `<%= vars.name %>`, as the book | `{% $vars.name %}` | `{name}` |
| **HTML value** | escaped text, unless the module holds JSX (native) or `dangerouslySetInnerHTML` | markup | escaped text, unless the config holds a Markdoc tree (native) or a `rawhtml` tag | markup |
| **Markdown value** | text, unless the module holds JSX | Markdown | text, unless the config holds a Markdoc tree | text, unless written as HTML |
| **In a code block** | `<CodeBlock>` with a template string | as written | in a fence, as written | `subs=attributes+` on the block |
| **As a link target** | `<a href={vars.name}>`; in a Markdown link, a broken link | as written | a `link` tag; in a Markdown link, no link and no message | `link:{name}[…]` |
| **In a heading's table-of-contents entry** | the value, through the site's heading plugin; without it, the expression's source | the value | the value | the value |
| **In the page title** | the value written in the front matter | the variable in the front matter | the value written in the front matter | `= {name} …` |
| **A name not defined, as the book does** | nothing, silent | nothing, silent | nothing, silent | nothing, silent |
| **A name not defined, reported** | build error, from a 10-line variables module | build error, `on_undefined = "strict"` (no page named) | a check before the build; the build drops the error | build fails, `attribute-missing: warn` and `failure_level: warn` |
| **An empty value (YAML null)** | nothing | prints `None` unless written as `""` | nothing | nothing |

- **The tag survives in every tool; what differs is what a value may
  hold and where.** In text, link text, table cells, notes and the
  headings themselves every tool shows every value in passthrough
  already. The failures are in
  values that hold Markdown (three uses on two pages, in Docusaurus,
  Starlight and Antora), link targets, and page metadata.
- **Zensical keeps the book's model.** It renders the page as a template
  before Python-Markdown reads it, as ERB does in the book, so every place
  and every kind of value behaves as on the published pages, Markdown
  inside HTML blocks included. Its two traps: an empty value prints
  "None", and Jinja's own delimiters clash with the book's content.
- **Docusaurus and Starlight render variables after the page is parsed.**
  A value is text unless the variables object holds markup in the tool's
  form (JSX; a Markdoc tree), and a variable cannot sit where the parser
  wants a literal: a Markdown link target, front matter, and (in
  Docusaurus) the table of contents. Native mode handles each with a form
  of its own.
- **No tool reports an undefined name by default.** Zensical and Antora
  can by configuration, Docusaurus by a small variables module. Starlight
  can only by a check outside the build, because Astro's Markdoc
  integration drops the validator's error on purpose.
- **The checks found what the builds did not report.** Of the 29 failing
  expectations in passthrough, the builds reported one: Docusaurus's link
  check names the link whose target is `{vars.gorouter_metrics_link}`
  ([build warnings](results/docusaurus-build-warnings.txt)).

## Docusaurus 3.10.2

Site: [sites/docusaurus/](sites/docusaurus/) — conventions:
[CONVENTIONS.md](sites/docusaurus/CONVENTIONS.md).

### Summary

- **Native: every value in place**, from a variables module that holds
  text values from the book's file and JSX for values that hold markup
  ([check](results/docusaurus-check.txt)).
- **Passthrough, with the book's file as JSON**: Markdown values show as
  text; a Markdown link with a variable target links to
  `/passthrough/{vars.gorouter_metrics_link}`; the description
  Docusaurus writes from the first paragraph holds
  `{vars.appruntimeabbr}`; the page title set by ERB code cannot be
  written.
- **The table of contents is made when the page compiles**, from the
  heading's source, so without help it shows the expression's source.
  The site's heading plugin ([`heading-vars.js`](sites/docusaurus/heading-vars.js),
  about 30 lines, run before Docusaurus's own plugins) writes each text
  value into its heading first, so the generated table of contents shows
  the value, in both modes, and no page writes its own; a name with no
  text value stops the build ([probe](results/docusaurus-probe.txt)). A
  page title taken from an `# …` heading still shows the expression. All
  27 headings with a variable in the book read a product name.
- **Front matter cannot hold an expression**, so titles and descriptions
  are written as values. An `# …` heading with an expression shows the
  value but gives the page the `<title>` "{vars.app_runtime_abbr} Component
  Metrics" ([probe](results/docusaurus-probe.txt)).
- **An undefined name** renders as nothing with a JSON import. The native
  module is a `Proxy` that throws: "Variable not defined:
  vars.no_such_name", with the page's path
  ([probe](results/docusaurus-probe.txt)).
- **As written**, `<%= … %>` does not compile
  ([raw check](results/docusaurus-raw-check.txt)).
- **React error #418 came from the tables**, not the variables: a `<tr>`
  straight in `<table>` causes a hydration mismatch, which `<tbody>`
  fixes, as the tables round writes it
  ([browser check](results/browser-checks.txt)).

### Grid

| Mode | app-ssh-overview | routes-domains | troubleshooting-router | container-security | all_metrics |
|------|------------------|----------------|------------------------|--------------------|-------------|
| passthrough | same; 6/9 | same; 50/50 | same; 7/8 | same; 12/16 | title differs; 0/2 |
| native | same; 9/9 | same; 50/50 | same; 8/8 | same; 16/16 | same; 2/2 |
| raw | does not compile | — | — | — | — |

"same" is the outline check; the fraction is values in place.

## Zensical 0.0.69

Site: [sites/zensical/](sites/zensical/) — conventions:
[CONVENTIONS.md](sites/zensical/CONVENTIONS.md).

### Summary

- **Every value in place in both modes**, the pages written as the book
  writes them ([check](results/zensical-check.txt)). The built-in macros
  extension renders each page as a Jinja template with ERB delimiters
  before Python-Markdown reads it.
- **A title can hold a variable**: the extension renders a front matter
  `title`. The book's ERB code line is not Jinja and stops the build
  ([raw check](results/zensical-raw-check.txt)); the converter moves the
  variable into the front matter.
- **An empty value prints "None"** with the book's file loaded as it is
  ([probe](results/zensical-probe.txt)). 44 uses on the book's pages read
  an empty key.
- **`on_undefined = "strict"`** stops the build on an undefined name, with
  a message that names the variable and not the page. `keep` prints a
  debug string on the page; `silent` and `lax` print nothing.
- **Jinja's own delimiters clash with the book**: `{#id}` on a heading
  starts a comment and stops the build, and the nginx buildpack page's
  `{{port}}` becomes a variable, silently empty with `silent`
  ([probe](results/zensical-probe.txt)). Decision (this round): keep the
  ERB delimiters in native mode too.
- **Relative links** in values and pages are rewritten one folder deeper,
  for pages served as folders.

### Grid

| Mode | app-ssh-overview | routes-domains | troubleshooting-router | container-security | all_metrics |
|------|------------------|----------------|------------------------|--------------------|-------------|
| passthrough | same; 9/9 | same; 50/50 | same; 8/8 | same; 16/16 | same; 2/2 |
| native | same; 9/9 | same; 50/50 | same; 8/8 | same; 16/16 | same; 2/2 |
| raw | — | — | — | — | the ERB code line stops the build |

## Starlight 0.42.6

Site: [sites/starlight/](sites/starlight/) — conventions:
[CONVENTIONS.md](sites/starlight/CONVENTIONS.md).

### Summary

- **Native: every value in place** ([check](results/starlight-check.txt)),
  with values that hold markup parsed by Markdoc into render trees in the
  config, a `link` tag for variable link targets, and code blocks as
  fences.
- **Passthrough**: Markdown values show as text; a Markdown link with a
  variable target is no link, the page shows
  `[metrics](../running/all_metrics.html#routing)`; an HTML `href` keeps
  the tag as text; the title set by ERB code cannot be written. The build
  reports none of it.
- **Fences process variables.** Markdoc renders tags and variables inside
  a fence unless it says otherwise, so native code blocks keep their type.
  The headings round recorded the tag as text in a fence. Rebuilt with
  that round's own configuration and package lock, the fence renders the
  value too, so the headings round's record is corrected. Inline code
  does keep the tag as text, as that round found.
- **An undefined name is never reported by the build**: Astro's Markdoc
  integration drops Markdoc's `variable-undefined` error. A check script
  run by `make build` reports it ([probe](results/starlight-probe.txt)).
- **As written**, the page builds and shows its ERB tags as text, in the
  heading and the table of contents too
  ([raw check](results/starlight-raw-check.txt)).

### Grid

| Mode | app-ssh-overview | routes-domains | troubleshooting-router | container-security | all_metrics |
|------|------------------|----------------|------------------------|--------------------|-------------|
| passthrough | same; 6/9 | same; 50/50 | same; 5/8 | same; 12/16 | title differs; 0/2 |
| native | same; 9/9 | same; 50/50 | same; 8/8 | same; 16/16 | same; 2/2 |
| raw | heading differs; 1/9 | — | — | — | — |

## Antora 3.2.1

Site: [sites/antora/](sites/antora/) — conventions:
[CONVENTIONS.md](sites/antora/CONVENTIONS.md).

### Summary

- **Native: every value in place** ([check](results/antora-check.txt)),
  with Markdown in values written as HTML.
- **Passthrough**: every value but the three Markdown ones, which show as
  text. Attributes work in text, headings, the document title, link
  macros, and (when the block asks) code blocks and passthrough blocks.
- **The key `title` renames every page**: AsciiDoc reads an attribute of
  that name as the document title
  ([check with the key](results/antora-title-key.txt)). Passthrough leaves
  it out as a forced change.
- **An undefined name** renders as nothing with `attribute-missing: drop`
  (the earlier rounds'). With `warn` it logs "skipping reference to
  missing attribute: no_such_name" and leaves `{no_such_name}` on the
  page; with `runtime.log.failure_level: warn` the build then fails
  ([probe](results/antora-probe.txt)).
- **No warnings** in either mode
  ([build log](results/antora-build-warnings.txt)).

### Grid

| Mode | app-ssh-overview | routes-domains | troubleshooting-router | container-security | all_metrics |
|------|------------------|----------------|------------------------|--------------------|-------------|
| passthrough | same; 6/9 | same; 50/50 | same; 8/8 | same; 12/16 | same; 2/2 |
| native | same; 9/9 | same; 50/50 | same; 8/8 | same; 16/16 | same; 2/2 |

Every page is AsciiDoc in every mode, so there is no raw mode.

## Each place a variable can sit

How the book's places map to each tool, in native mode. Counts are the
book's uses ([survey](survey/README.md#where-variables-sit)).

| Place (uses) | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| Text, link text, table cell, note (1,238) | `{vars.name}` | `<%= vars.name %>` | `{% $vars.name %}` | `{name}` |
| Inline code (98) | `<code>{vars.name}</code>` | in backticks, as written | `<code>{% $vars.name %}</code>` | in backticks |
| Fenced code (92), `<pre>` (44) | `<CodeBlock language="console">{\`… ${vars.name}\`}</CodeBlock>` | as written | in a fence | `[source,console,subs=attributes+]` |
| Heading (27) | the reference; the site's heading plugin writes the value | the reference | the reference | the reference |
| Link target (3) | `<a href={vars.name}>…</a>` | as written | `{% link href=$vars.name %}…{% /link %}` | `link:{name}[…]`; in HTML, `subs=attributes+` |
| Page title (1, by ERB code) | the value, in front matter | the reference, in front matter | the value, in front matter | `= {name} …` |
| Page description (none in the book; tools write one) | the value, in front matter, where the first paragraph holds a variable | not written | not written | not written |
| Expression with a condition (2) | — | — | — | — |

The two conditions
([`stacks` L11](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/stacks.html.md.erb#L11),
`windows-stacks` L9) were not converted. Every tool can write the result;
only Zensical and Docusaurus could keep the condition.

## Names that are not defined, and empty values

The book has 38 uses of 28 names no key defines and 44 uses of 31 keys
with no value; all 82 render as nothing on the published pages
([survey](survey/README.md#variables-used-but-not-defined-or-empty)).
[R-04](../../requirements/README.md#r-04) variables everywhere asks that
"a variable that is not defined is reported when the site builds, instead
of showing as empty text"; the tables round's [sources note](../tables/source/SOURCES.md#notes)
asked for the opposite, empty text, before the requirement was written.

| | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| Default | nothing, no message | nothing (`silent`, the earlier rounds' setting), no message | nothing, no message | `{name}` on the page (`skip`); nothing with `drop` (the earlier rounds') |
| Reported | build error: "Variable not defined: vars.no_such_name" and the page's path | build error: "UndefinedError: 'dict object' has no attribute 'no_such_name'", no page named | check before the build: "probe.mdoc:5: Undefined variable: 'vars.no_such_name'" | warning "skipping reference to missing attribute: no_such_name", file named, no line; fails the build with `failure_level: warn` |
| How | a `Proxy` in the variables module (site code) | `on_undefined = "strict"`, `on_error_fail = true` | a script with Markdoc's validator (site code) | playbook settings |
| Empty value | nothing | "None", unless written `""` | nothing | nothing |

Evidence: [Docusaurus](results/docusaurus-probe.txt),
[Zensical](results/zensical-probe.txt),
[Starlight](results/starlight-probe.txt),
[Antora](results/antora-probe.txt).

Decision (this round): native mode removes the 4 references the test
pages make to undefined names, since they render as nothing today, and
requires every name. A reference that is left fails the build in every
tool.

## Where values that hold markup should live

131 of the book's 273 values hold HTML or Markdown; pages use 78 of them,
97 times ([survey](survey/README.md#what-the-values-hold)). Most are a
sentence with a link, used at the end of a paragraph, list item or table
cell; 28 of the 49 uses of an HTML value sit inside a sentence.

- **A partial cannot replace an inline value** in three tools
  ([scratch test](results/inline-partials.txt)). An MDX partial renders a
  paragraph: in a table cell it becomes a second block, and in a sentence
  it splits the paragraph in two. A Markdoc partial inside a sentence
  stops the build: "'partial' tag should be block". An AsciiDoc include
  is a line of its own
  ([`rx.rb` L92](https://github.com/asciidoctor/asciidoctor/blob/2c03d22eb9fe83d04ee452939581d1b842f6d8b4/lib/asciidoctor/rx.rb#L92);
  not built). So the notes round's rule (a note held in a variable becomes
  a partial, accepted) fits block values only. Zensical's `include` works
  inline, since it inserts text before Markdown is read; not tested here.
- **What worked**, with the page writing the plain reference in every
  case: Zensical reads the value as part of the page; Antora renders HTML
  in an attribute; Docusaurus renders JSX from a variables module;
  Starlight renders a Markdoc tree built in its config.
- Decision (this round): **one shared variables file stays the source**
  (today's `template_variables.yml`), and each site's build or the
  converter writes the tool's form from it: Markdown and HTML as JSX for
  Docusaurus, as Markdown parsed by Markdoc for Starlight, as HTML for
  Antora, as written for Zensical. Values that are blocks (notes, lists,
  headings, table rows) become partials.

## Product names

1,060 of the book's 1,503 uses (71%) read a product name, "Cloud Foundry",
"CF" or "cf", through `app_runtime_abbr` and eleven other keys; they cover
all 27 headings with a variable and all 33 link texts
([survey](survey/README.md#what-the-values-hold)). Such variables
let other books build the same pages with their own names; a comment in
`overview` mentions "private/commercial books". If no other book builds from these
repositories any more, writing the name as text would remove most uses,
every heading case, and with it the Docusaurus table-of-contents
workaround. Decision (Docs WG lead, 2026-10-11): **the names are
written as text.** No open-source book other than this one builds from
these repositories;
`pivotal-cf/docs-book-tiledev`, whose `config.yml` names `docs-services`,
is a commercial book (convention 9).

## Copyright and build-time values

The footer's `<%= Time.now.year %>`
([`_book-footer.erb` L3](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/_book-footer.erb#L3))
is the book's one build-time value. It is counted in the survey and not
converted: it belongs to the copyright concept and to
[R-25](../../requirements/README.md#r-25) build-time values are expected
differences. The layouts' other variables (`book_title_short`,
`domain_name`, `ga_account_id`, `support_url`, and Bookbinder's header's)
are site settings for each tool's configuration, not page variables.

## Conventions to record

For `cf-docs-migrate convert`. Decisions of this round, for review:

1. **One reference form per tool, from one shared file**: `{vars.name}`
   (Docusaurus), `<%= vars.name %>` (Zensical, macros extension with ERB
   delimiters), `{% $vars.name %}` (Starlight), `{name}` (Antora). The
   book's `template_variables.yml`, or its successor, stays the one place
   values are written. Zensical's ERB delimiters: **Accepted** (Docs WG
   lead, 2026-10-11).
2. **The build writes each tool's variables from that file**: text as
   text; empty values as `""`; values that hold HTML or Markdown in the
   form the tool renders inline (JSX; a Markdoc tree; HTML; as written).
   Values that are blocks become partials. Keys only layouts read go to
   the site's configuration; `title` is never an AsciiDoc attribute; the
   key that is not a name is dropped. Whether the source is one file or
   one shared folder of several files (fewer values reached by one
   editor's mistake) is decided at implementation (Docs WG lead,
   2026-10-11).
3. **Every site requires every name at build**: Docusaurus through its
   variables module, Zensical with `on_undefined = "strict"`, Starlight
   with a validator run in `make build`, Antora with
   `attribute-missing: warn` and `failure_level: warn`. **Accepted**
   (Docs WG lead, 2026-10-11), with a note that Starlight's validator
   runs outside the tool; a check of variables outside every tool may
   be worth having as well.
4. **References to undefined and empty names are removed before
   conversion**, each listed in the cleanup record (82 uses on 59 names);
   they render as nothing today
   ([R-24](../../requirements/README.md#r-24) markup cleanup before
   conversion). **Accepted** (Docs WG lead, 2026-10-11): the list stays
   with the Docs WG, which does the conversion, rather than going to page
   owners.
5. **Each place has a rule per tool**, as in
   [Each place a variable can sit](#each-place-a-variable-can-sit):
   code blocks keep their type; link targets use the tool's link form;
   titles and descriptions take the value where front matter cannot hold
   a variable; in Docusaurus, the site's heading plugin writes a
   heading's variable as its value before the table of contents is made
   (tested 2026-10-11, in place of hand-written tables of contents).
   After convention 9 few such headings remain.
6. **Code that only computes text is evaluated by the converter**: the
   title line of `all_metrics` and the two conditions on the stacks pages
   become their result, listed for the owners.
7. **The variables check runs on every converted page**, beside the
   outline and notes checks: [checks/vars.py](checks/vars.py), with a
   variables file per page; and a browser check where the tool builds
   content in the browser ([checks/vars-browser.mjs](checks/vars-browser.mjs)).
8. **The copyright year is not a variable**: it stays with the copyright
   concept ([R-25](../../requirements/README.md#r-25) build-time values
   are expected differences).
9. **Product names are written as text**: "Cloud Foundry", "CF" and
   "cf" from `app_runtime_abbr` and the eleven other keys
   ([Product names](#product-names)). **Accepted** (Docs WG lead,
   2026-10-11).

## Requirements

- [R-04](../../requirements/README.md#r-04) variables everywhere: in
  native mode every tool shows every value in prose, table cells, inside
  HTML, code, headings, link targets and titles, and renders HTML values
  as markup; every tool can report an undefined name at build, Starlight
  only through a check outside its build. Only Docusaurus writes a page
  description, and it holds the value only when the converter writes it
  in the front matter.
- [R-01](../../requirements/README.md#r-01) content and outline survive:
  checked for the variables, the headings and the notes; body text was
  not compared word by word.
- [R-06](../../requirements/README.md#r-06) typed code blocks: code
  blocks that hold a variable keep their type in native mode in every
  tool (Docusaurus through `<CodeBlock language>`).
- [R-13](../../requirements/README.md#r-13) no per-WG extensions:
  Docusaurus's variables module (a `Proxy` of about 10 lines) and heading
  plugin (about 30 lines), and Starlight's config (a `link` tag, 3 lines that parse values) and check
  script are site code the Docs WG would maintain once.
- [R-24](../../requirements/README.md#r-24) markup cleanup before
  conversion: 82 references to undefined or empty names; `<tbody>` in
  Docusaurus tables.
- [R-11](../../requirements/README.md#r-11) readable source: Zensical's
  pages read as the book's; Antora's references are the shortest;
  Docusaurus's and Starlight's need JSX or tags for link targets and
  code.
- [R-25](../../requirements/README.md#r-25) build-time values are
  expected differences: the copyright year is the only one; not
  converted.

## Not yet written

- **Block values other than notes.** Values that hold a heading
  (`max_in_flight_header`, `disable_custom`), a list (the five role
  values on `roles`), or a table row (`r_buildpack`) are on no test page.
  A heading held in a variable is part of the page's outline.
- **A Markdown value inside an HTML block** (`configure-lb-healthcheck`
  L92), which the book shows as text: kept as text by Zensical as written,
  rendered by the native forms of the others. Which the owners want was
  not asked.
- **The conditions on the stacks pages** were not converted.
- **Relative links after conversion.** Values with links relative to the
  page work only at their pages' depth; Zensical rewrites them for folder
  URLs. Whether every link still reaches its page in each tool belongs to
  the cross-repository links concept.
- **Empty values on a test page.** "None" in Zensical was seen in the
  probe only.
- **bosh.io's ERB examples and the MkDocs tutorial's variables** were
  counted, not converted.
- **The layouts' variables** were not moved into any tool's
  configuration.
- **Body text outside variables** was not compared word by word. In
  Starlight the classification table's cell still loses a space after
  `</code>`, the tables round's known issue.
- **Escaped underscores in values** (`` [`enable\_service\_discovery`](…) ``)
  are on no test page.
- **Probes and on-paper tools.** Eleventy, Sphinx/MyST, Middleman, Hugo
  and VitePress were not part of this round; the tables round's probes
  found that Eleventy's EJS escapes HTML values unless written `<%-`.
- **Screenshots.** None were taken.
