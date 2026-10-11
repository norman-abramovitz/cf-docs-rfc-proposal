# Docusaurus conventions for notes

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#docusaurus-3102). Pages, variables and
partials follow the [tables round's conventions](../../../tables/sites/docusaurus/CONVENTIONS.md),
headings the [headings round's](../../../headings/sites/docusaurus/CONVENTIONS.md)
(`## Text {#id}`).

```bash
make build      # install, generate vars.json, build the site (log in .check/build.log)
make serve      # serve build/ at http://localhost:3000
make check      # build, then the outline and notes checks on every page, passthrough and native
make check-raw  # the first MDX error of each raw page that does not compile, and the checks on the one that does
```

## Passthrough

The HTML notes stay, with the changes MDX needs:

| Source | MDX | Why |
|--------|-----|-----|
| `<p class="note">` with its title and text on lines of their own | `<div class="note">` | MDX reads the text as a paragraph of its own, so the page holds a `<p>` inside a `<p>`. The static HTML closes the note before its text, so the note is empty and its text follows it; in the browser React reports error #418, a hydration mismatch ([raw check](../../results/docusaurus-raw-check.txt), [built HTML](../../results/raw-html-excerpts.txt), [browser check](../../results/browser-checks.txt)). `div` keeps the source's lines and the class the book's stylesheet reads. |
| a `<p class="note">` without `</p>` | the note closed | MDX stops: "Expected a closing tag for `<p>`" |
| text, then a note, inside one HTML element (`<td>The …<br>` then `<p class="note">`, or `<li>text` then the note) | the element's content starting on its own line, and a blank line before the note | MDX reads an element that starts on a line with text as inline, and stops at the block inside it: "Expected a closing tag for `<td>` … before the end of `paragraph`" |
| `Where:` then `<ul>` on the next line | a blank line between them | the same |
| `<br>` | `<br />` | JSX |
| `<%= vars.external_vol_win_note %>`, a variable whose value is a note | `<div dangerouslySetInnerHTML={{__html: vars.external_vol_win_note}} />` | the tables round's form for an HTML-valued variable |

The theme gives HTML notes no box; their bold title is all that sets them
apart ([browser check](../../results/browser-checks.txt)).

## Native

Docusaurus's admonition directive:

```markdown
:::warning[Important]

The health check configuration that you provide with
`cf push` overrides any configuration in the app manifest.

:::
```

- **The documented types are `note`, `tip`, `info`, `warning` and
  `danger`.** `important` and `caution` also work, as "undocumented legacy
  admonition type aliases": `important` renders as `info` with the title
  "important", `caution` has a component of its own
  ([`Types.tsx` L17-L34](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-theme-classic/src/theme/Admonition/Types.tsx#L17-L34),
  [keywords](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-mdx-loader/src/remark/admonitions/index.ts#L17-L27),
  v3.10.2). Decision (this round): use documented types only, chosen by
  severity, with the source's title in brackets: `note` → `:::note`,
  `important` → `:::warning[Important]`, `caution` → `:::danger[Caution]`.
- **A note with no title written shows the type** ("note", in capitals
  through CSS), so `:::note` needs no `[Note]`.
- **Markdown inside is read:** lists, code spans, links, and variables as
  `{vars.name}`.
- **In a list,** the directive is indented under its item.
- **In an HTML table cell** it works inside the JSX `<td>`, with blank
  lines around it.
- **A note held in a variable becomes a partial**, `_external_vol_win_note.mdx`,
  imported and used as a component: `<ExternalVolWinNote />`.
- **The build checks the links in a native note.** Links written as HTML
  inside a passthrough note are not checked; the same links written as
  Markdown in the native note are, and the ones to pages outside the test
  set are reported (`restore.html` on `cf-backup`,
  `identity-aware-routing.html` on `routes-domains`;
  [build warnings](../../results/docusaurus-build-warnings.txt)).

## How a note reads in the source

```markdown
:::danger[Caution]

Selective backups increase
your overall recovery time. …

:::
```

Four lines of markup become two, and the body needs no indentation. The
title and the type are separate, so "Caution" can sit on a `danger` box;
the reader of the source sees both.
