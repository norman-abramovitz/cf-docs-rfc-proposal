# Input formats

Status: draft, incomplete — covers what is known as of 2026-10-10.

An input format is the kind of text an author writes and a tool reads to
build a page. Each tool in this evaluation reads one or two formats. This
page describes each format and shows one real table written in it, taken
from the page sources built in the tables round. Nothing here is written
for this page: every snippet is copied from a file in this repository, and
each one links to that file.

What these snippets look like once built, tool by tool, with screenshots:
[poc/tables.md](../poc/tables.md#credential-types).

## The sample table

The table is the only table on `credential-types.html.md.erb` from the
`cloudfoundry/docs-credhub` repository
([lines 17–46 at commit `e074f74`](https://github.com/cloudfoundry/docs-credhub/blob/e074f74717422c0082ca24a2a6da7fbbf8114999/credential-types.html.md.erb#L17-L46)),
published at
<https://docs.cloudfoundry.org/credhub/credential-types.html>. It has a
header row, seven body rows and two columns. The first column names a
credential type, written as code, and its header cell asks for 20% of the
table's width; the second column holds one or two sentences.

What the table asks for, written as hints (tool-independent statements of
intent, from its
[intent file](../concepts/tables/intent/credential-types.md)):

| Hint | Value | Where the source says it |
|------|-------|--------------------------|
| header row | yes | `<thead>` |
| row-header column | yes | column 1 names the type |
| column 1 role | `key` (a short label) | `<code>` type names |
| column 1 width | about 20% | `<th style="width:20%">` |
| column 1 wrap | avoid (stay on one line) | single identifiers |
| column 2 role | `prose` (sentences) | one or two sentences per cell |

The source has one defect: `class=“table”` is written with typographic
quotes, so browsers never apply the class: a typographic quote is not an
attribute quote, so the value is read as an
[unquoted attribute value](https://html.spec.whatwg.org/multipage/syntax.html#unquoted),
`“table”` with the quotes in it. Every converted version makes
the quotes straight ([R-24](../requirements/README.md#r-24) markup cleanup before conversion). Requirement
IDs are listed in [requirements/](../requirements/README.md).

The modes named below are defined in the [Tooling README](README.md#modes):
raw passthrough (HTML exactly as written), passthrough (HTML after
cleanup), extension (the tool's extension point carries the hints), native
(the tool's own table syntax), and native-plain (native without widths).

## Formats at a glance

| Format | What it is | Read by (modes) | Learn more |
|--------|------------|-----------------|------------|
| [HTML](#html) | The markup language of web pages | today's site; passthrough in every tool | [WHATWG HTML](https://html.spec.whatwg.org/), [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML) |
| [ERB](#erb) | Ruby code in `<% %>` tags inside a text file | today's site; Middleman probe | [ERB](https://github.com/ruby/erb) |
| [EJS](#ejs) | JavaScript code in `<% %>` tags, the same tag shapes as ERB | Eleventy probe | [EJS](https://ejs.co/) |
| [MDX](#mdx) | Markdown in which HTML is read as JSX | Docusaurus (passthrough, extension) | [MDX](https://mdxjs.com/), [JSX](https://react.dev/learn/writing-markup-with-jsx) |
| [Pipe table](#pipe-table) | The Markdown table written with `\|` and `---` | Docusaurus native; Zensical and Starlight native-plain | [GFM](https://github.github.com/gfm/) |
| [Python-Markdown](#python-markdown) | The Markdown dialect Zensical reads; its attribute lists add widths to cells | Zensical native | [Python-Markdown](https://python-markdown.github.io/) |
| [Markdoc](#markdoc) | Markdown with `{% %}` tags | Starlight (all modes) | [Markdoc](https://markdoc.dev/) |
| [AsciiDoc](#asciidoc) | A plain-text format with its own table syntax | Antora (all modes) | [AsciiDoc](https://asciidoc.org/), [Asciidoctor](https://asciidoctor.org/) |
| [List table](#list-table) | A table written as a nested list, one item per row and per cell | Docusaurus and Zensical extension | [MyST list-table](https://myst-parser.readthedocs.io/) |
| [MyST](#myst) | Markdown with directives (named blocks with options) | Sphinx probe | [MyST](https://mystmd.org/), [MyST parser](https://myst-parser.readthedocs.io/) |

## HTML

HTML (HyperText Markup Language) is the markup language browsers read:
`<table>`, `<tr>` (row), `<th>` (header cell), `<td>` (cell). Browsers
repair broken HTML without saying so: the HTML standard defines how a
browser recovers from each
[parse error](https://html.spec.whatwg.org/multipage/parsing.html#parse-errors).
That is why defects in today's source never showed. Learn more: [WHATWG HTML](https://html.spec.whatwg.org/),
[MDN](https://developer.mozilla.org/en-US/docs/Web/HTML); see also the
[glossary](../glossary.md#html).

Today's source is HTML inside a Markdown page inside an ERB file
(`.html.md.erb`). The table as written in
[source/credential-types.html.md.erb](../concepts/tables/source/credential-types.html.md.erb),
lines 17–46, unchanged:

```html
<table class=“table”>
<thead>
  <tr>
    <th style="width:20%">Type</th>
    <th>Description</th>
  </tr>
  </thead>
  <tr>
    <td><code>value</code></td>
    <td>A single string value for arbitrary configurations and other non-generated or validated strings.</td>
  </tr><tr>
    <td><code>json</code></td>
    <td>An arbitrary JSON object for static configurations with many values.</td>
  </tr><tr>
    <td><code>user</code></td>
    <td>Three string values for username, password, and password hash.</td>
  </tr><tr>
    <td><code>password</code></td>
    <td>A single string value for passwords and other random string credentials. Values for this type can be automatically generated.</td>
  </tr><tr>
    <td><code>certificate</code></td>
    <td>An object containing a root CA, certificate, and private key. Use this type for key pair apps that utilize a certificate, such as TLS connections. Values for this type can be automatically generated.</td>
  </tr><tr>
    <td><code>rsa</code></td>
    <td>An object containing an RSA public key and private key without a certificate. Values for this type can be automatically generated.</td>
  </tr><tr>
    <td><code>ssh</code></td>
    <td>An object containing an SSH-formatted public key and private key. Values for this type can be automatically generated.</td>
  </tr>
</table>
```

**Raw passthrough** in every tool keeps this HTML exactly (Antora wraps it
in a passthrough block, below). Zensical, Starlight and Antora build it;
Docusaurus does not (see [MDX](#mdx)).

**Passthrough** in Zensical and Starlight is the same text with one change,
the first line:

```html
<table class="table">
```

Files: [Zensical](../concepts/tables/sites/zensical/docs/passthrough/credential-types.md),
[Starlight](../concepts/tables/sites/starlight/src/content/docs/passthrough/credential-types.mdoc).

**Antora** reads AsciiDoc, not Markdown, so the HTML goes inside an AsciiDoc
passthrough block, `++++` above and below, which hands the HTML to the
browser unread: Asciidoctor treats `++++` as a
[raw block](https://github.com/asciidoctor/asciidoctor/blob/30fb8cd5f7145c57274b04524ceaa99812f830e0/lib/asciidoctor/block.rb#L21)
with [no substitutions](https://github.com/asciidoctor/asciidoctor/blob/30fb8cd5f7145c57274b04524ceaa99812f830e0/lib/asciidoctor/substitutors.rb#L1294-L1296)
([file](../concepts/tables/sites/antora/passthrough/modules/ROOT/pages/credential-types.adoc)):

<details><summary>Antora passthrough (first and last lines)</summary>

```asciidoc
++++
<table class="table">
<thead>
  <tr>
    <th style="width:20%">Type</th>
    <th>Description</th>
  </tr>
  </thead>
  …
</table>
++++
```

</details>

A table that holds a variable also needs `[subs=attributes+]` on the line
above `++++`, so the variable is filled in
([custom `subs` on a block](https://github.com/asciidoctor/asciidoctor/blob/30fb8cd5f7145c57274b04524ceaa99812f830e0/lib/asciidoctor/substitutors.rb#L1302-L1303));
this table has none.

## ERB

ERB (Embedded Ruby) puts Ruby code in a text file between `<%` and `%>`;
`<%= … %>` inserts the result into the page
([ERB's tag kinds, in `lib/erb.rb`](https://github.com/ruby/erb/blob/934d51e24b1553d3fe6c92afea3751defd99038b/lib/erb.rb#L60-L85)).
Today's pages use it for variables (defined in the book's
[`template_variables.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml))
and for including one file in another. Learn more:
[ERB](https://github.com/ruby/erb); see also the
[glossary](../glossary.md#erb).

The `credential-types` table holds no ERB tag. The
[Middleman probe](../concepts/tables/probes/middleman/README.md) built
this page from the source file itself, unchanged, and every table matched
the published page cell for cell. ERB as it appears in other test pages:

- A variable inside a table cell, from
  [`_oss_scale_table`](../concepts/tables/source/_oss_scale_table.html.md.erb)
  (cell text shortened here):

  ```erb
  <td>You might run a single NATS instance … <%= vars.recommended_by %> recommends scaling NATS VMs to 2 or more CPU.</td>
  ```

- Including a partial (a file inserted into another page), from the probe's
  [host page](../concepts/tables/probes/middleman/source/scale-table-host.html.md.erb):

  ```erb
  <%= partial 'oss_scale_table' %>
  ```

## EJS

EJS (Embedded JavaScript templates) uses the same tag shapes as ERB, with
JavaScript inside. One difference matters: EJS's `<%=` escapes HTML (shows
`<p>` as text), and `<%-` inserts it as markup
([tag modes](https://github.com/mde/ejs/blob/ebba1b9d5b5e38239b52a968ba04479ce378ee00/lib/esm/ejs.js#L805-L810)
and [what each outputs](https://github.com/mde/ejs/blob/ebba1b9d5b5e38239b52a968ba04479ce378ee00/lib/esm/ejs.js#L850-L855)
in EJS's source). In Middleman, ERB's `<%=` does not escape
([Middleman probe](../concepts/tables/probes/middleman/README.md#results)). Learn more: [EJS](https://ejs.co/); see also the
[glossary](../glossary.md#ejs).

**No EJS copy of `credential-types` exists in this repository.** The
[Eleventy probe](../concepts/tables/probes/eleventy/README.md) built
`uaa-concepts` and the scale table from unchanged copies of the source, and
their tables came out byte for byte as written. `credential-types` holds no
ERB tags, so its EJS form would be the source file as it is; that was not
built. EJS from the probe's files:

- An HTML-valued variable, both ways, from
  [src/escaping.md](../concepts/tables/probes/eleventy/src/escaping.md):

  ```ejs
  <%= vars.route_services %>

  <%- vars.route_services %>
  ```

  The first shows the variable's `<p class="note">` as text; the second
  renders the note.

- An include, from
  [src/scale-table-host.md](../concepts/tables/probes/eleventy/src/scale-table-host.md).
  It needs `<%-` and the full file name, where ERB's `partial` needs
  neither:

  ```ejs
  <%- include('/_oss_scale_table.md') %>
  ```

## MDX

MDX is Markdown in which HTML is read as JSX. JSX is the HTML-like syntax
of React, a JavaScript library: it requires every tag to be closed, writes
a `style` as a JavaScript object, and treats `{…}` as JavaScript code. The
MDX project's own documentation says so
([HTML replaced by JSX, `{` must be escaped](https://github.com/mdx-js/mdx/blob/52285a6758fa078ec57f3d4bd8803d9cbfb12065/docs/docs/what-is-mdx.mdx#L165-L171);
[a `style` object](https://github.com/mdx-js/mdx/blob/52285a6758fa078ec57f3d4bd8803d9cbfb12065/docs/docs/what-is-mdx.mdx#L250)).
Docusaurus reads `.md` and `.mdx` files
([default `include`](https://github.com/facebook/docusaurus/blob/c245217563f6491fdb79bf5ac91bfa16536e5de9/packages/docusaurus-plugin-content-docs/src/options.ts#L31)). Learn more: [MDX](https://mdxjs.com/),
[JSX](https://react.dev/learn/writing-markup-with-jsx); see also the
glossary entries for [MDX](../glossary.md#mdx) and [JSX](../glossary.md#jsx).

**Raw passthrough does not build.** MDX stops at the first error: the
typographic `“` before an attribute value
([raw passthrough errors](../concepts/tables/results.md#raw-passthrough-errors)).

**Passthrough** after cleanup
([file](../concepts/tables/sites/docusaurus/docs/passthrough/credential-types.mdx)).
Three things differ from the source: straight quotes, the width written as a
JSX object, and the body rows wrapped in `<tbody>` (without it the page
builds, but React reports an error in the browser):

```mdx
<table class="table">
<thead>
  <tr>
    <th style={{width: '20%'}}>Type</th>
    <th>Description</th>
  </tr>
  </thead>
  <tbody>
<tr>
    <td><code>value</code></td>
    <td>A single string value for arbitrary configurations and other non-generated or validated strings.</td>
  </tr><tr>
    <td><code>json</code></td>
    <td>An arbitrary JSON object for static configurations with many values.</td>
  </tr><tr>
    <td><code>user</code></td>
    <td>Three string values for username, password, and password hash.</td>
  </tr><tr>
    <td><code>password</code></td>
    <td>A single string value for passwords and other random string credentials. Values for this type can be automatically generated.</td>
  </tr><tr>
    <td><code>certificate</code></td>
    <td>An object containing a root CA, certificate, and private key. Use this type for key pair apps that utilize a certificate, such as TLS connections. Values for this type can be automatically generated.</td>
  </tr><tr>
    <td><code>rsa</code></td>
    <td>An object containing an RSA public key and private key without a certificate. Values for this type can be automatically generated.</td>
  </tr><tr>
    <td><code>ssh</code></td>
    <td>An object containing an SSH-formatted public key and private key. Values for this type can be automatically generated.</td>
  </tr>
</tbody>

</table>
```

Every `.mdx` page that uses variables also imports them once, after the
front matter (the settings block at the top of a page):

```mdx
import vars from '@site/vars.json';
```

and a variable is then written `{vars.recommended_by}`. Native mode in
Docusaurus is a [pipe table](#pipe-table); extension mode is a
[list table](#list-table).

## Pipe table

A pipe table is the table syntax most Markdown tools share, from GFM
(GitHub Flavored Markdown, GitHub's dialect of CommonMark, the common
Markdown specification;
[GFM spec](https://github.com/github/cmark-gfm/blob/27d942c8b0a62d192f616e5bf3578f4b6a89e180/test/spec.txt#L12-L19)).
Each row is one line; `|` separates cells; a line
of `---` ends the header row. A cell holds one line of text: no lists or
paragraphs unless written as inline HTML, and no widths; the delimiter row
carries only alignment
([GFM spec, tables](https://github.com/github/cmark-gfm/blob/27d942c8b0a62d192f616e5bf3578f4b6a89e180/test/spec.txt#L3307-L3324)). Learn more:
[GFM](https://github.github.com/gfm/), [CommonMark](https://commonmark.org/); see also the
[glossary](../glossary.md#pipe-table).

Docusaurus native
([file](../concepts/tables/sites/docusaurus/docs/native/credential-types.mdx)).
Zensical native-plain and Starlight native-plain are the same table
([Zensical](../concepts/tables/sites/zensical/docs/native-plain/credential-types.md),
[Starlight](../concepts/tables/sites/starlight/src/content/docs/native-plain/credential-types.mdoc)):

```markdown
| Type | Description |
| --- | --- |
| `value` | A single string value for arbitrary configurations and other non-generated or validated strings. |
| `json` | An arbitrary JSON object for static configurations with many values. |
| `user` | Three string values for username, password, and password hash. |
| `password` | A single string value for passwords and other random string credentials. Values for this type can be automatically generated. |
| `certificate` | An object containing a root CA, certificate, and private key. Use this type for key pair apps that utilize a certificate, such as TLS connections. Values for this type can be automatically generated. |
| `rsa` | An object containing an RSA public key and private key without a certificate. Values for this type can be automatically generated. |
| `ssh` | An object containing an SSH-formatted public key and private key. Values for this type can be automatically generated. |
```

The 20% width and the row headers are gone; the columns are sized by their
content. A pipe table also needs a blank line before it, where an HTML
table does not
([Docusaurus finding 3](../concepts/tables/results.md#findings),
[Zensical conventions](../concepts/tables/sites/zensical/CONVENTIONS.md#native)).

## Python-Markdown

Python-Markdown is the Markdown dialect Zensical reads (Zensical
[depends on `markdown`](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/pyproject.toml#L58),
the Python-Markdown package). Its attribute lists
extension (`attr_list`) lets an author attach HTML attributes to an element
by writing `{: … }` after it, including at the end of a table cell
([`attr_list.py`](https://github.com/Python-Markdown/markdown/blob/0bf535bc406c95dad66050f07c8402af03fe07d5/markdown/extensions/attr_list.py#L104-L110)).
It works on a single table cell, not on a whole table
([Zensical conventions](../concepts/tables/sites/zensical/CONVENTIONS.md#native)). Learn more: [Python-Markdown](https://python-markdown.github.io/);
see also the [glossary](../glossary.md#python-markdown).

Zensical native is the pipe table with one attribute list on the first
header cell
([file](../concepts/tables/sites/zensical/docs/native/credential-types.md)):

```markdown
| Type {: style="width:20%" } | Description |
| --- | --- |
| `value` | A single string value for arbitrary configurations and other non-generated or validated strings. |
| `json` | An arbitrary JSON object for static configurations with many values. |
| `user` | Three string values for username, password, and password hash. |
| `password` | A single string value for passwords and other random string credentials. Values for this type can be automatically generated. |
| `certificate` | An object containing a root CA, certificate, and private key. Use this type for key pair apps that utilize a certificate, such as TLS connections. Values for this type can be automatically generated. |
| `rsa` | An object containing an RSA public key and private key without a certificate. Values for this type can be automatically generated. |
| `ssh` | An object containing an SSH-formatted public key and private key. Values for this type can be automatically generated. |
```

The width is kept; row headers are not. `{: .class }` on the line after a
pipe table does not attach to the table: it becomes an extra row showing
that text ([Zensical finding 6](../concepts/tables/results.md#findings-1)).

Zensical keeps today's variable form, `<%= vars.recommended_by %>`, as
written: its template engine is set to read ERB-style tags
([zensical.toml](../concepts/tables/sites/zensical/zensical.toml)).

## Markdoc

Markdoc is Markdown with tags written `{% name %}` … `{% /name %}`
([tag delimiters](https://github.com/markdoc/markdoc/blob/df5ac9aae57505eae5e7572aab3dda50d61f434c/src/utils.ts#L13-L14)). Its
own `{% table %}` tag writes a table as a list: `*` starts a cell and `---`
starts a new row
([table transform](https://github.com/markdoc/markdoc/blob/df5ac9aae57505eae5e7572aab3dda50d61f434c/src/transforms/table.ts#L41-L86)),
so a cell can hold lists and paragraphs
([cell schema](https://github.com/markdoc/markdoc/blob/df5ac9aae57505eae5e7572aab3dda50d61f434c/src/schema.ts#L124-L143)).
Starlight, a documentation theme for the Astro site builder
([depends on `astro`](https://github.com/withastro/starlight/blob/67de74077524001c79ec233e1b113e86b2b800b0/packages/starlight/package.json#L51)),
reads Markdoc pages (`.mdoc`) in this evaluation, through Astro's Markdoc
integration
([`@astrojs/markdoc`](https://github.com/withastro/astro/blob/9050e3819c51b0383cced278c278bc6f45c63468/packages/integrations/markdoc/package.json#L44)). Learn more: [Markdoc](https://markdoc.dev/),
[Starlight](https://starlight.astro.build/); see also the
[glossary](../glossary.md#markdoc).

Starlight native, Markdoc's table tag with only what Markdoc defines, here
`width` on a header cell (Markdoc defines `width` for `th` only:
[schema](https://github.com/markdoc/markdoc/blob/df5ac9aae57505eae5e7572aab3dda50d61f434c/src/schema.ts#L145-L153))
([file](../concepts/tables/sites/starlight/src/content/docs/native/credential-types.mdoc)):

```markdoc
{% table %}
* Type {% width="20%" %}
* Description
---
* `value`
* A single string value for arbitrary configurations and other non-generated or validated strings.
---
* `json`
* An arbitrary JSON object for static configurations with many values.
---
* `user`
* Three string values for username, password, and password hash.
---
* `password`
* A single string value for passwords and other random string credentials. Values for this type can be automatically generated.
---
* `certificate`
* An object containing a root CA, certificate, and private key. Use this type for key pair apps that utilize a certificate, such as TLS connections. Values for this type can be automatically generated.
---
* `rsa`
* An object containing an RSA public key and private key without a certificate. Values for this type can be automatically generated.
---
* `ssh`
* An object containing an SSH-formatted public key and private key. Values for this type can be automatically generated.
{% /table %}
```

Starlight extension is the same table tag with hint attributes on the
opening line. The attributes are added by
[list-table.mjs](../concepts/tables/sites/starlight/list-table.mjs); the
rest of the table does not change, except that the width moves from the
cell to the tag
([file](../concepts/tables/sites/starlight/src/content/docs/extension/credential-types.mdoc)):

<details><summary>Starlight extension: the changed lines</summary>

```markdoc
{% table widths="20 auto" header-rows=1 stub-columns=1 roles="key prose" %}
* Type
* Description
---
…
{% /table %}
```

</details>

Starlight native-plain is the [pipe table](#pipe-table). Starlight
passthrough is the [HTML](#html) after cleanup, but Markdoc reads text
inside HTML as Markdown, so on other pages it needed more changes than the
cleanup ([Starlight summary](../concepts/tables/results.md#starlight-0426)).
A variable is written `{% $vars.recommended_by %}`.

## AsciiDoc

AsciiDoc is a plain-text format with its own syntax for headings, lists
and tables; Asciidoctor is the program that reads it, and Antora builds
sites from it
([Antora depends on `@asciidoctor/core`](https://gitlab.com/antora/antora/-/blob/87797da7a7f337301ec9b1ad26aa291a28342d56/packages/asciidoc-loader/package.json#L33)).
A table is written between `|===` lines
([delimiters](https://github.com/asciidoctor/asciidoctor/blob/30fb8cd5f7145c57274b04524ceaa99812f830e0/lib/asciidoctor.rb#L284-L285));
settings in `[ ]` above it describe the columns. Learn more:
[AsciiDoc](https://asciidoc.org/), [Asciidoctor](https://asciidoctor.org/);
see also the [glossary](../glossary.md#asciidoc).

Antora native
([file](../concepts/tables/sites/antora/native/modules/ROOT/pages/credential-types.adoc)):

```asciidoc
[%header,cols=".<20%h,.<~"]
|===
|Type |Description

|`value`
|A single string value for arbitrary configurations and other non-generated or validated strings.

|`json`
|An arbitrary JSON object for static configurations with many values.

|`user`
|Three string values for username, password, and password hash.

|`password`
|A single string value for passwords and other random string credentials. Values for this type can be automatically generated.

|`certificate`
|An object containing a root CA, certificate, and private key. Use this type for key pair apps that utilize a certificate, such as TLS connections. Values for this type can be automatically generated.

|`rsa`
|An object containing an RSA public key and private key without a certificate. Values for this type can be automatically generated.

|`ssh`
|An object containing an SSH-formatted public key and private key. Values for this type can be automatically generated.
|===
```

The settings line, read left to right: `%header` makes the first row the
header row; `cols` describes each column. `.<` is top alignment, `20%` the
width, `h` makes the column's cells row headers, and `~` sizes the second
column by its content
([Antora conventions](../concepts/tables/sites/antora/CONVENTIONS.md);
in Asciidoctor's source:
[`cols` parsing](https://github.com/asciidoctor/asciidoctor/blob/30fb8cd5f7145c57274b04524ceaa99812f830e0/lib/asciidoctor/parser.rb#L2469-L2513),
[`<` is top, `h` is header](https://github.com/asciidoctor/asciidoctor/blob/30fb8cd5f7145c57274b04524ceaa99812f830e0/lib/asciidoctor/parser.rb#L63-L79),
[`%header`](https://github.com/asciidoctor/asciidoctor/blob/30fb8cd5f7145c57274b04524ceaa99812f830e0/lib/asciidoctor/parser.rb#L2337-L2338)).

The other Antora modes change only the settings line:

<details><summary>Antora native-plain and extension: the settings line</summary>

Native-plain
([file](../concepts/tables/sites/antora/native-plain/modules/ROOT/pages/credential-types.adoc)).
With no `cols`, Asciidoctor gives both columns the same width
([`assign_column_widths`](https://github.com/asciidoctor/asciidoctor/blob/30fb8cd5f7145c57274b04524ceaa99812f830e0/lib/asciidoctor/table.rb#L142-L145)):

```asciidoc
[%header]
```

Extension
([file](../concepts/tables/sites/antora/extension/modules/ROOT/pages/credential-types.adoc)).
The words after each `.` are roles (class names;
[shorthand parsing](https://github.com/asciidoctor/asciidoctor/blob/30fb8cd5f7145c57274b04524ceaa99812f830e0/lib/asciidoctor/parser.rb#L2605-L2616))
that a stylesheet gives meaning to: column 1 is a key that does not wrap, column 2 is prose:

```asciidoc
[.hinted.col1-key.col2-prose.col1-nowrap%header,cols=".<20%h,.<~"]
```

</details>

Passthrough is the [HTML](#html) inside a `++++` block. A variable is
written `{recommended_by}`, an AsciiDoc attribute.

## List table

A list table writes a table as a nested list: each row is a list item, and
each cell is an item inside it. Because a cell is a list item, it can hold
lists and paragraphs. The form is the `list-table` directive of
reStructuredText, defined in docutils
([`ListTable`, in the GitHub mirror of docutils](https://github.com/docutils/docutils/blob/f8602b0fc745405a2262872bebae9f343940adef/docutils/docutils/parsers/rst/directives/tables.py#L368-L381)),
which MyST also reads (see [MyST](#myst)). The Docusaurus and Zensical
extensions built for this evaluation use the same option names (`widths`,
`header-rows`, `stub-columns`) plus the hint options (`roles`, `wrap`,
`title`). Learn
more: [MyST parser](https://myst-parser.readthedocs.io/); see also the
[glossary](../glossary.md#list-table).

Docusaurus extension, a `:::list-table` block read by a remark plugin
written for this evaluation,
[plugins/list-table.js](../concepts/tables/sites/docusaurus/plugins/list-table.js)
([file](../concepts/tables/sites/docusaurus/docs/extension/credential-types.mdx)):

```markdown
:::list-table{widths="20 auto" header-rows="1" stub-columns="1" roles="key prose"}
- - Type
  - Description
- - `value`
  - A single string value for arbitrary configurations and other non-generated or validated strings.
- - `json`
  - An arbitrary JSON object for static configurations with many values.
- - `user`
  - Three string values for username, password, and password hash.
- - `password`
  - A single string value for passwords and other random string credentials. Values for this type can be automatically generated.
- - `certificate`
  - An object containing a root CA, certificate, and private key. Use this type for key pair apps that utilize a certificate, such as TLS connections. Values for this type can be automatically generated.
- - `rsa`
  - An object containing an RSA public key and private key without a certificate. Values for this type can be automatically generated.
- - `ssh`
  - An object containing an SSH-formatted public key and private key. Values for this type can be automatically generated.
:::
```

Zensical extension, a `/// list-table` block read by a Python-Markdown
extension written for this evaluation,
[list_table.py](../concepts/tables/sites/zensical/list_table.py)
([file](../concepts/tables/sites/zensical/docs/extension/credential-types.md)).
Python-Markdown's list rules need four-space indents and a blank line
between rows:

```markdown
/// list-table
    widths: 20 auto
    header-rows: 1
    stub-columns: 1
    roles: key prose

-   - Type
    - Description

-   - `value`
    - A single string value for arbitrary configurations and other non-generated or validated strings.

-   - `json`
    - An arbitrary JSON object for static configurations with many values.

-   - `user`
    - Three string values for username, password, and password hash.

-   - `password`
    - A single string value for passwords and other random string credentials. Values for this type can be automatically generated.

-   - `certificate`
    - An object containing a root CA, certificate, and private key. Use this type for key pair apps that utilize a certificate, such as TLS connections. Values for this type can be automatically generated.

-   - `rsa`
    - An object containing an RSA public key and private key without a certificate. Values for this type can be automatically generated.

-   - `ssh`
    - An object containing an SSH-formatted public key and private key. Values for this type can be automatically generated.
///
```

Starlight's extension carries the same options as attributes on Markdoc's
own table tag (see [Markdoc](#markdoc)), so it needs no new block syntax.

## MyST

MyST (Markedly Structured Text) is Markdown with directives: named blocks,
written as a fenced code block whose first line names the directive in
braces (`{list-table}`), with options on `:name: value` lines (MyST
parser source:
[fence with `{name}`](https://github.com/executablebooks/MyST-Parser/blob/723cffcf84213f0cb58695b27eec9ad72052b53a/myst_parser/mdit_to_docutils/base.py#L774-L785),
[option lines](https://github.com/executablebooks/MyST-Parser/blob/723cffcf84213f0cb58695b27eec9ad72052b53a/myst_parser/parsers/directives.py#L222-L230)).
Sphinx, a documentation generator from the Python world, reads it through
the MyST parser
([which depends on Sphinx](https://github.com/executablebooks/MyST-Parser/blob/723cffcf84213f0cb58695b27eec9ad72052b53a/pyproject.toml#L33)). Learn more:
[MyST](https://mystmd.org/), [MyST parser](https://myst-parser.readthedocs.io/);
see also the [glossary](../glossary.md#myst).

**No MyST copy of `credential-types` exists in this repository.** The
[Sphinx probe](../concepts/tables/probes/sphinx-myst/README.md) wrote the
scale table (`_oss_scale_table`) instead. Its opening lines, from
[docs/_oss_scale_table.md](../concepts/tables/probes/sphinx-myst/docs/_oss_scale_table.md)
(the rest of the rows omitted here):

~~~markdown
```{list-table}
:header-rows: 1
:stub-columns: 1
:widths: 25 25 50
:class: table hinted col1-key col2-value col3-prose col1-nowrap

* - Component
  - Total Instances
  - Notes
* - Diego Cell
  - &ge; 2
  - The optimal balance between …
```
~~~

`:header-rows:`, `:stub-columns:` (row headers), `:widths:` and `:class:`
are the options of docutils' `list-table`
([option list](https://github.com/docutils/docutils/blob/f8602b0fc745405a2262872bebae9f343940adef/docutils/docutils/parsers/rst/directives/tables.py#L376-L381)),
which MyST passes through. `:class:` puts classes on the table, and a stylesheet gives
the role and no-wrap classes their meaning, with no code. A variable is
written `{{recommended_by}}`.

## What each format carried

For the sample table, measured in a browser at a 1280-pixel window
(columns as percent of the table). Source:
[results.md](../concepts/tables/results.md); screenshots in
[poc/tables.md](../poc/tables.md#credential-types).

| Tool | Mode | Format | 20% width | Row headers | No-wrap key column |
|------|------|--------|-----------|-------------|--------------------|
| Docusaurus | passthrough | MDX (HTML as JSX) | yes | no | no |
| Docusaurus | extension | list table | yes | yes | yes |
| Docusaurus | native | pipe table | no (18/82) | no | no |
| Zensical | passthrough | HTML | yes (20/80) | no | no |
| Zensical | extension | list table | yes (20/80) | yes | yes |
| Zensical | native | pipe table with attribute list | yes (20/80) | no | no |
| Zensical | native-plain | pipe table | no (15/84) | no | no |
| Starlight | passthrough | HTML in Markdoc | yes (20/80) | no | no |
| Starlight | extension | Markdoc table tag with hint attributes | yes (20/80) | yes | yes |
| Starlight | native | Markdoc table tag | yes (20/80) | no | no |
| Starlight | native-plain | pipe table | no (18/82) | no | no |
| Antora | passthrough | HTML in a `++++` block | yes (20/80) | no | no |
| Antora | extension | AsciiDoc table with roles | yes (20/80) | yes | yes |
| Antora | native | AsciiDoc table | yes (20/80) | yes | no |
| Antora | native-plain | AsciiDoc table, no `cols` | no (50/50) | no | no |

The passthrough rows keep the source's `<th>` header row but have no row
headers, because the source has none: its first column is ordinary cells.
Every mode in every tool passes the table's three spot checks (seven rows
of two cells, type names as code, no stray typographic quotes) after
cleanup. The Middleman probe built the source unchanged and matched the
published table cell for cell; the Eleventy and Sphinx probes did not build
this page.

## Formats not yet written

**Not yet written:** Hugo's input (Markdown read by goldmark,
[a Hugo dependency](https://github.com/gohugoio/hugo/blob/0732eadd5aead94d4bd4674d87e9bfc79aaf10a7/go.mod#L72),
with [shortcodes](https://github.com/gohugoio/hugo/blob/0732eadd5aead94d4bd4674d87e9bfc79aaf10a7/hugolib/shortcode.go))
and VitePress's input (Markdown read by markdown-it, with Vue components;
[VitePress dependencies](https://github.com/vuejs/vitepress/blob/633e48af9ec25a9cc28fc3ebf1e9063b359adb2e/package.json#L111-L112),
[markdown-it](https://github.com/vuejs/vitepress/blob/633e48af9ec25a9cc28fc3ebf1e9063b359adb2e/package.json#L150)). Neither tool has been assessed; no page source exists for
either.

**Not yet written:** the other test pages in every format. Their sources
are in each site folder under
[concepts/tables/sites/](../concepts/tables/sites/), and the conventions
for each tool are in its `CONVENTIONS.md`, for example
[Docusaurus](../concepts/tables/sites/docusaurus/CONVENTIONS.md).
