# Antora conventions for variables

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#antora-321). Every page is AsciiDoc in every
mode; headings as the
[headings round's native mode](../../../headings/sites/antora/CONVENTIONS.md)
writes them (`[[id]]` above `== Text`), notes as the
[notes round's native mode](../../../notes/sites/antora/CONVENTIONS.md),
HTML tables in passthrough blocks as the
[tables round](../../../tables/sites/antora/CONVENTIONS.md) writes them.

```bash
make build      # install, fetch the pinned UI, write one playbook per mode, build both into site/
make serve      # serve site/ at http://localhost:8002
make check      # build, then the variables, outline and notes checks on every page, passthrough and native
make probe      # what the native playbook does with an undefined and an empty name
```

## The mechanism

A variable is an AsciiDoc attribute, written `{name}`. The site's
attributes are set in the playbook (`asciidoc.attributes`);
[playbook.js](playbook.js) writes one playbook per mode with the book's
keys as attributes. AsciiDoc replaces attribute references in text,
headings, the document title, link macros and, when a block asks for it
(`subs=attributes+`), in code blocks and passthrough blocks.

## Passthrough

Each `<%= vars.name %>` becomes `{name}`; every key of the book's file is
an attribute, its value as the book writes it; `attribute-missing: drop`,
as in the earlier rounds. 78 of 85 values in place
([check](../../results/antora-check.txt)):

- **Text, headings, link text, table cells, code** (with
  `subs=attributes+` on the block), **the document title**
  (`= {app_runtime_abbr} Component Metrics`) and **link targets**
  (`link:{gorouter_metrics_link}[metrics]`, and `href="{gorouter_metrics_link}"`
  in a passthrough block with `subs=attributes+`) all show the value.
- **HTML values are markup**: AsciiDoc escapes `<` and `>` before it
  replaces attributes, so the value's HTML passes through. The order of
  the steps is `specialcharacters`, `quotes`, `attributes`,
  `replacements`, `macros`, `post_replacements`
  ([`substitutors.rb` L16](https://github.com/asciidoctor/asciidoctor/blob/2c03d22eb9fe83d04ee452939581d1b842f6d8b4/lib/asciidoctor/substitutors.rb#L16)).
- **Markdown values stay as written**: the page shows
  `see [Configuring SSH Access](../../running/config-ssh.html).`
- **Forced change: the key `title` is left out.** AsciiDoc reads an
  attribute named `title` as the document title
  ([`document.rb` L721-L728](https://github.com/asciidoctor/asciidoctor/blob/2c03d22eb9fe83d04ee452939581d1b842f6d8b4/lib/asciidoctor/document.rb#L721-L728),
  Asciidoctor 2.0.23, which Asciidoctor.js 2.2.9 compiles), so with the
  book's `title: Cloud Foundry Documentation` every page's heading and
  `<title>` became "Cloud Foundry Documentation"
  ([check with the key](../../results/antora-title-key.txt)). It is the
  only key that matches an attribute AsciiDoc defines.
- **A name that is not defined renders as nothing**, and the build says
  nothing. An empty value (a YAML null) is no attribute at all, so it is
  treated the same way.

## Native

The same pages, with the values prepared for AsciiDoc and every name
required:

- **Markdown in a value is written as HTML** (links, code, bold, emphasis,
  escapes). AsciiDoc replaces attributes after it applies inline
  formatting, so backticks and asterisks in a value stay as they are,
  while HTML passes through. A link written `link:url[text]` in a value
  works too, because links are made after attributes are replaced; code
  does not. [playbook.js](playbook.js) does this for the test; the
  converter would write it.
- **A name that is not defined fails the build**:
  `attribute-missing: warn` logs "skipping reference to missing attribute:
  no_such_name"
  ([`substitutors.rb` L249-L250](https://github.com/asciidoctor/asciidoctor/blob/2c03d22eb9fe83d04ee452939581d1b842f6d8b4/lib/asciidoctor/substitutors.rb#L249-L250))
  and `runtime.log.failure_level: warn`
  ([schema L271-L277](https://gitlab.com/antora/antora/-/blob/v3.2.1/packages/playbook-builder/lib/config/schema.js#L271-L277))
  makes Antora exit with status 2 after writing the site; the page still
  shows `{no_such_name}` ([probe](../../results/antora-probe.txt)). The
  message names the file but not the line. Any other warning fails the
  build too; the native build has none
  ([build log](../../results/antora-build-warnings.txt)).
- **Empty values are written as `''`**, so they render nothing without a
  warning; the key `title` and the key that is not a name are left out.
- **References to names that are not defined are removed** from the pages.
- The home page's `+{name}+` (literal monospace) is how a page shows an
  attribute reference as text; without it, the native build failed on
  the home page's own example.

## How a variable reads in the source

```asciidoc
[[platform-ssh-config]]
== Configuring SSH access for {app_runtime_full}

** Are there any suspicious link:{gorouter_metrics_link}[metrics] spiking?

[source,console,subs=attributes+]
----
$ cf create-shared-domain {app_domain}
----
```

The shortest reference of the four tools. Code blocks name the
substitution they want, and a value's Markdown has to become HTML.
