# Notes round — results

Status: draft, incomplete — covers what is known as of 2026-10-10.

What each tool did with the four test pages' notes. A summary across tools
comes first, then one section per tool, then how each tool maps the note
kinds, what happens to what notes hold, how notes read in the source, and
the conventions to record. How the pages were chosen and what the modes
mean: [README](README.md). Per-page notes: [intent/](intent/). How the book
writes notes: [survey](survey/README.md).

How to read the results:

- **Notes check:** the [notes check](checks/notes.py) finds every note on
  a built page and compares it, in order, with the page's notes file
  ([intent/](intent/)): its kind (through the site's map, in native mode),
  its title, its words, what it holds (list items, code, code blocks,
  links), the section it sits in and whether it sits in a list or a table
  cell. "16 of 16" means every note on the four pages passes.
- **Outline check:** the headings round's
  [outline check](../headings/checks/outline.py) on every page, so that
  converting the notes does not move a heading.
- **Modes:** *passthrough* keeps the HTML notes (with the changes the tool
  forces, listed per tool); *native* writes each note with the tool's own
  admonition; *raw* is the notes exactly as the source writes them, on the
  pages where that differs from passthrough.
- **Kind** is the book's class (`note`, `important`, `caution`); **title**
  is the word the reader sees (Note, Important, Caution).

All checks ran on 2026-10-10 against the published pages saved that day,
with the tool versions the earlier rounds pinned, plus Starlight's Markdoc
preset (`@astrojs/starlight-markdoc` 0.7.0) for its aside tag.

## Summary

Every tool keeps every note, in both modes: on all four pages, in
passthrough and native, the notes check passes for all 16 notes and the
outline check for every heading, in Docusaurus, Zensical, Starlight and
Antora ([checks](results/)). What differs is the cost: which changes the
HTML notes need before a tool takes them, and what each tool's own
admonition can say about the kind.

| | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|
| **Notes check, passthrough** | 16 of 16 | 16 of 16 | 16 of 16 | 16 of 16 |
| **Notes check, native** | 16 of 16 | 16 of 16 | 16 of 16 | 16 of 16 |
| **Native syntax** | `:::warning[Important]` … `:::` | `!!! important` + indented body | `{% aside type="caution" title="Important" %}` … `{% /aside %}` | `IMPORTANT: …`, or `[IMPORTANT]` + `====` block |
| **Book's three kinds as native types** | none of `important`, `caution` documented; mapped, title kept | any name accepted; theme styles `note` only | `note` and `caution` (no `important`); all three mapped by severity, title kept | all three |
| **HTML notes as written** | 3 of 4 raw pages fail to compile; the one that compiles has empty notes and a React error | build unchanged, except a note never closed, which swallows the rest of the page | a note never closed stops the build; elsewhere words run together and `>` becomes a blockquote, silently | in passthrough blocks; a Markdown code span inside stays literal |
| **Changes passthrough needs** | `<p>` notes as `<div>`, blank lines around notes inside `<td>`/`<li>`, `<br />`, notes closed | notes closed | note text on one line, `&#32;` and `&gt;` in three places, notes closed | `<code>` for one Markdown code span |
| **Note in a list** | indented directive | indented admonition | indented tag | `+` continuation; open block after a nested list |
| **Note in an HTML table cell** | directive inside the JSX `<td>` | `md_in_html` attributes on table, row and cell; stray `<tr>` removed | tag inside the `<td>` | AsciiDoc table with an `a\|` cell |
| **Note held in a variable** | partial imported as a component | partial included with `<% include %>` | partial tag | `include::partial$…[]` |
| **The kinds look different (default theme)** | yes: note grey, important amber, caution red | no: all blue, titles differ | yes: note blue, important amber, caution red | label colour differs, box the same |
| **Build checks links in notes** | native only (HTML links are not checked) | native (Markdown links) | no | no |

- **The kind survives as the title, everywhere.** In every mode of every
  tool the reader sees the source's word, Note, Important or Caution,
  because native mode writes it as the admonition's title where the tool's
  type has another name ([checks](results/)). On the published book the
  title is also the only thing that tells the kinds apart: the book's
  stylesheet has no rule for `important` or `caution`, so all three are the
  same yellow box
  ([survey](survey/README.md#how-the-book-styles-notes-today)).
- **Native notes pass with no workaround.** Native mode passes every
  check in every tool with nothing special written inside the notes, and
  its source is shorter. Passthrough passes only after tool-specific changes, and the
  failures as written are silent in two tools: Docusaurus builds an empty
  note box, Starlight joins words and turns `>=` into a blockquote, and no
  build reports either. The notes check finds them.
- **The headings round's pages had damaged notes no check saw.** Its
  Docusaurus and Starlight `routes-domains` pages, reused here as the raw
  mode, fail the notes check: three empty notes in Docusaurus and "theCloud
  Foundry documentation" in Starlight
  ([Docusaurus](results/docusaurus-raw-check.txt),
  [Starlight](results/starlight-raw-check.txt)). The outline check passed
  them, because it reads headings only.

## Docusaurus 3.10.2

Site: [sites/docusaurus/](sites/docusaurus/) — conventions:
[CONVENTIONS.md](sites/docusaurus/CONVENTIONS.md).

### Summary

- **Every note survives in passthrough and native**
  ([check](results/docusaurus-check.txt)).
- **A `<p class="note">` over several lines becomes an empty note.** MDX
  reads the note's text as a paragraph of its own inside the `<p>`; the
  static HTML the build writes is `<p class="note"></p><p><span class="note__title">…`,
  and the browser reports React error #418, a hydration mismatch
  ([built HTML](results/raw-html-excerpts.txt),
  [browser check](results/browser-checks.txt)). In the browser React then
  rebuilds the page and the text is back in the box, but the static HTML,
  which the notes check reads and a reader without JavaScript gets, holds
  an empty note. The build says nothing. Passthrough writes these notes as `<div class="note">`.
- **Three of the four raw pages do not compile** (MDX stops at the first
  error): the note never closed (`cf-backup`), and a note after text inside
  a `<td>` or an `<li>` that started on the same line as the text
  (`healthchecks`, `using-vol-services`)
  ([raw check](results/docusaurus-raw-check.txt)).
- **Native: documented types with the source's title.** `important` and
  `caution` are accepted but are "undocumented legacy admonition type
  aliases"
  ([`Types.tsx` L17-L34](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-theme-classic/src/theme/Admonition/Types.tsx#L17-L34));
  the pages use `:::warning[Important]` and `:::danger[Caution]`.
- **Native notes put their links under the build's link check.** The
  Markdown links in native notes to pages outside the test set are
  reported; the same links as HTML in passthrough notes are not
  ([build warnings](results/docusaurus-build-warnings.txt)).

### Grid

| Mode | cf-backup | using-vol-services | healthchecks | routes-domains |
|------|-----------|--------------------|--------------|----------------|
| passthrough | same; 3/3 | same; 4/4 | same; 4/4 | same; 5/5 |
| native | same; 3/3 | same; 4/4 | same; 4/4 | same; 5/5 |
| raw | does not compile | does not compile | does not compile | same; 2/5 (3 empty) |

"same" is the outline check; the fraction is notes kept.

## Zensical 0.0.69

Site: [sites/zensical/](sites/zensical/) — conventions:
[CONVENTIONS.md](sites/zensical/CONVENTIONS.md).

### Summary

- **The source's notes build as written**, title spans, lists, notes in
  lists and table cells and the note held in a variable included
  ([check](results/zensical-check.txt)). The one change is closing the
  two notes `cf-backup` leaves open.
- **A note never closed swallows the rest of the page.** Python-Markdown
  reads everything after the open `<p class="note caution">` as raw HTML:
  the page loses three headings and a note, and shows them as Markdown
  text ([raw check](results/zensical-raw-check.txt),
  [built HTML](results/raw-html-excerpts.txt)). The build reports nothing.
- **Native keeps the kind names** (`!!! important`, `!!! caution`), and
  Python-Markdown makes the title from the name. But the theme styles
  neither, so Important and Caution notes look like Notes, as on the
  published book ([theme styles](results/theme-admonition-styles.txt),
  [browser check](results/browser-checks.txt)).
- **A note in an HTML table cell needs `md_in_html`** attributes on the
  table, the row and the cell, and the table's stray `<tr>` removed; with
  the stray row, the row's indented cells became a code block.
- **The anchor check reaches native notes**: the native `cf-backup` note's
  Markdown link to `#selective-backup-restore-steps` is checked and passes;
  the build reports only the two links that leave the excerpts (`#routes`,
  `#migrate`) ([build warnings](results/zensical-build-warnings.txt)).
  Whether it reads links inside HTML notes was not tested.

### Grid

| Mode | cf-backup | using-vol-services | healthchecks | routes-domains |
|------|-----------|--------------------|--------------|----------------|
| passthrough | same; 3/3 | same; 4/4 | same; 4/4 | same; 5/5 |
| native | same; 3/3 | same; 4/4 | same; 4/4 | same; 5/5 |
| raw | 4 of 7 headings; 1/3 | (as passthrough) | (as passthrough) | (as passthrough) |

## Starlight 0.42.6

Site: [sites/starlight/](sites/starlight/) — conventions:
[CONVENTIONS.md](sites/starlight/CONVENTIONS.md).

### Summary

- **Every note survives in passthrough and native**
  ([check](results/starlight-check.txt)).
- **Markdoc changes HTML notes' text without a sign.** It reads the text
  inside HTML as Markdown: a space next to an inline tag disappears when the
  note's text runs over several lines or shares a line with a variable
  (`with the<code>cf set-health-check</code>command`), and
  `<code>>= v7.1.48</code>` becomes `<code><blockquote><p>= v7.1.48</p></blockquote></code>`
  ([built HTML](results/raw-html-excerpts.txt)). Four notes on three pages
  are hit ([raw check](results/starlight-raw-check.txt)); the check reports
  the first difference in each. These are the
  tables round's findings, now in notes.
- **A note never closed stops the build**: "Node 'html-tag' is missing
  closing" ([raw check](results/starlight-raw-check.txt)).
- **Native: the `aside` tag from Starlight's Markdoc preset.** Its types are
  `note`, `tip`, `caution` and `danger`
  ([preset L67-L85](https://github.com/withastro/starlight/blob/fe11bb470d2177a3696ddeac7379a9625b9f987b/packages/markdoc/index.mjs#L67-L85));
  Important becomes `caution` and Caution `danger`, titles kept. The text
  inside the tag is Markdown, so none of passthrough's problems arise.

### Grid

| Mode | cf-backup | using-vol-services | healthchecks | routes-domains |
|------|-----------|--------------------|--------------|----------------|
| passthrough | same; 3/3 | same; 4/4 | same; 4/4 | same; 5/5 |
| native | same; 3/3 | same; 4/4 | same; 4/4 | same; 5/5 |
| raw | stops the build | same; 3/4 | same; 2/4 | same; 4/5 |

## Antora 3.2.1

Site: [sites/antora/](sites/antora/) — conventions:
[CONVENTIONS.md](sites/antora/CONVENTIONS.md).

### Summary

- **Every note survives in passthrough and native**
  ([check](results/antora-check.txt)). Every page is AsciiDoc in every mode.
- **AsciiDoc has the book's three kinds.** `NOTE`, `IMPORTANT` and `CAUTION`
  are kept as they are, the label is the kind's name, and the default UI
  gives each its own colour of label (note blue, important red, caution
  purple) ([theme styles](results/theme-admonition-styles.txt),
  [browser check](results/browser-checks.txt)).
- **Passthrough notes sit in passthrough blocks**, which are not parsed: a
  Markdown code span inside one stays as backticks
  ([raw check](results/antora-raw-check.txt),
  [built HTML](results/raw-html-excerpts.txt)). The one such span on the
  test pages is written as `<code>` in passthrough.
- **Lists and list steps need AsciiDoc's block markers**: an example block
  (`====`) for a note that holds a list, a list continuation (`+`) for a
  note in a list item, an open block (`--`) for a step that holds a nested
  list and then a note.
- **No warnings** ([build log](results/antora-build-warnings.txt)).

### Grid

| Mode | cf-backup | using-vol-services | healthchecks | routes-domains |
|------|-----------|--------------------|--------------|----------------|
| passthrough | same; 3/3 | same; 4/4 | same; 4/4 | same; 5/5 |
| native | same; 3/3 | same; 4/4 | same; 4/4 | same; 5/5 |
| raw | — | same; 3/4 (a code span lost) | — | — |

## How each tool maps the kinds

Decision (this round), for review: **keep the title everywhere. Where the
tool accepts the book's kind names (Zensical, Antora), keep them. Where its
set of types is closed and lacks `important` (Docusaurus, Starlight), map
all three kinds onto its types by severity**, so that the three kinds stay
three different boxes. In Starlight that puts Important on `caution` and
Caution on `danger`, although Starlight has a `caution` type. The book
itself does not tell the kinds apart by look (all three are the same
yellow box), so the look is the template's choice, not content.

| Book's kind | Published look | Docusaurus | Zensical | Starlight | Antora |
|---|---|---|---|---|---|
| `note` | yellow box, bold "Note" | `:::note` (grey) | `!!! note` (blue) | `type="note"` (blue) | `NOTE:` (blue label) |
| `important` | the same yellow box, "Important" | `:::warning[Important]` (amber) | `!!! important` (blue, unstyled) | `type="caution" title="Important"` (amber) | `IMPORTANT:` (red label) |
| `caution` | the same yellow box, "Caution" | `:::danger[Caution]` (red) | `!!! caution` (blue, unstyled) | `type="danger" title="Caution"` (red) | `CAUTION:` (purple label) |
| `warning` (2 notes, `archive/` only) | pink box | not tested | not tested | not tested | `WARNING:` exists |

Colours from the [browser check](results/browser-checks.txt). Other maps
are possible: Docusaurus's own legacy alias puts `important` on `info`
([Types.tsx L30](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-theme-classic/src/theme/Admonition/Types.tsx#L30)).
The map is one table per site, applied by the converter; no page names a
tool's type for a reason of its own.

**Review (Docs WG lead, 2026-10-10): open.** First find out whether an
extension, HTML the build injects, or CSS can give Docusaurus and Starlight
the book's kind names. If none can, keep a tool's own type where it has the
book's name, such as Starlight's `caution` for Caution, and accept that
Important and Caution may then look alike: the price of not writing plain
HTML. Until that test is done, the map above is what was tested, not the
convention.

## What notes hold

- **Lists.** The book writes them as HTML `<ul>` inside a `<div>` note.
  Native mode writes a Markdown list (an AsciiDoc list in Antora) inside the
  admonition; the four items, their bold lead-ins, code and link survive in
  every tool (`cf-backup` note 1: `list=4 code=2 link=1` in every check).
- **Code.** Code spans survive in every mode. One code span written in
  Markdown inside an HTML note (`using-vol-services` note 4) is code on the
  published page because the note sits in a list step; it stays code in
  Docusaurus, Zensical and Starlight passthrough, and in every native mode,
  but not in an Antora passthrough block. No test page has a code block in
  a note (see [Not yet written](#not-yet-written)).
- **Variables.** A variable inside a note (`healthchecks` note 4) renders
  its value in every tool and mode, in each tool's variable syntax. In
  Starlight passthrough, the variable on the same line as an inline tag
  costs the space before the tag.
- **Links.** Every link survives. In Docusaurus only native notes' links
  are checked by the build.

### Notes never closed

Two of the four notes the book leaves open are on `cf-backup`. The book's
Markdown processor wraps each in a paragraph and the browser ends it at the
next block, so the published page is right
([published copy](published/cf-backup.html), line 603). As written:
Zensical loses the rest of the page, Starlight and Docusaurus stop, Antora
does not apply (every page is rewritten). Closing them is cleanup, not a
change of content ([R-24](../../requirements/README.md#r-24) markup cleanup
before conversion).

### Notes in a table cell

`healthchecks` note 3 sits in an HTML table cell after the cell's text. It
stays in the cell in every mode (`place table` in every check). Native mode
needs each tool's way into a cell: nothing in Docusaurus and Starlight but
blank lines, `md_in_html` attributes and a cleaned table in Zensical, an
AsciiDoc table with an `a|` cell in Antora.

### A note held in a variable

`using-vol-services` opens with `<%= vars.external_vol_win_note %>`, whose
value is a whole HTML note. Passthrough renders the value as markup in
every tool (Docusaurus and Starlight through the tables round's
HTML-variable forms). Native mode cannot put an admonition in a variable
the way the book does, so the note became a partial in each tool, holding
the tool's admonition, included where the variable was; it passes the
notes check in all four. Decision (this round): this is the converter's
rule for the 7 note-valued variables pages use; the 5 unused ones need no
conversion ([survey](survey/README.md#the-books-notes)). **Accepted**
(Docs WG lead, 2026-10-10).

## How notes read in the source

The same note, `healthchecks` note 4, as each mode writes it:

```html
<p class="note important">
<span class="note__title"><strong>Important</strong></span>
For HTTP apps, <%= vars.company_name %> recommends setting the health check type to <code>http</code> instead of a simple port check.
</p>
```

```markdown
:::warning[Important]

For HTTP apps, {vars.company_name} recommends setting the health check type to `http` instead of a simple port check.

:::
```

```markdown
!!! important

    For HTTP apps, <%= vars.company_name %> recommends setting the health check type to `http` instead of a simple port check.
```

```markdown
{% aside type="caution" title="Important" %}

For HTTP apps, {% $vars.company_name %} recommends setting the health check type to `http` instead of a simple port check.

{% /aside %}
```

```asciidoc
IMPORTANT: For HTTP apps, {company_name} recommends setting the health check type to `http` instead of a simple port check.
```

Every native form drops the title span and the closing tag; the kind is on
the first line. AsciiDoc's is one line. Docusaurus and Starlight show a
type that is not the book's kind (`warning`, `caution` for Important), with
the kind as a title beside it. Zensical's depends on indentation. In every
native form the note's text is Markdown (or AsciiDoc), so code and links
read as they do in the rest of the page
([R-11](../../requirements/README.md#r-11) readable source).

## Conventions to record

For `cf-docs-migrate convert`. Decisions of this round, for review:

1. **Write every note as the tool's own admonition** (native mode). It
   passes every check in every tool, and needs no workaround inside the
   note.
2. **Keep the title.** The admonition's title is the source's title (Note,
   Important, Caution), written out where the tool's type has another name.
3. **Map the kind through one table per site**: the kind's own names
   where the tool accepts them (Zensical, Antora); otherwise all three by
   severity (Docusaurus: `note`, `warning`, `danger`; Starlight: `note`,
   `caution`, `danger`). The look of each kind is the template's.
   **Open** (Docs WG lead, 2026-10-10): extensions and CSS are to be tested
   first ([how each tool maps the kinds](#how-each-tool-maps-the-kinds)).
4. **Close every note before converting**, where the browser closed it.
5. **A note's HTML list becomes the format's list**, inside the admonition;
   a list that holds a note becomes the format's list too, so the note can
   be an admonition.
6. **A note held in a variable becomes a partial** holding the admonition,
   included where the variable was. **Accepted** (Docs WG lead,
   2026-10-10).
7. **If HTML notes are kept** (passthrough): Docusaurus writes them as
   `<div class="note">`; Starlight writes each note's text on one line and
   escapes `>` and the spaces Markdoc drops; Antora writes Markdown inside
   them as HTML. The template then has to style `.note` and its kinds, as
   no theme does.
8. **The notes check runs on every converted page**, beside the outline
   check: [checks/notes.py](checks/notes.py).

## Requirements

- [R-07](../../requirements/README.md#r-07) notes and admonitions: every
  note becomes an admonition with the same text in every tool, the note
  held in a variable included; the kind survives as the title, and as the
  type through a map.
- [R-01](../../requirements/README.md#r-01) content and outline survive:
  checked for the notes (words, contents, place) and the headings; the rest
  of the body text was not compared.
- [R-10](../../requirements/README.md#r-10) simple text plus HTML where
  needed: HTML notes work in every tool, but in Docusaurus and Starlight
  only after changes to the HTML, and two of those failures are silent.
- [R-13](../../requirements/README.md#r-13) no per-WG extensions: no
  extension was written. Native notes use each tool's own syntax; Starlight
  adds its own Markdoc preset's tag, and Docusaurus and Starlight reuse the
  tables round's HTML-variable forms for passthrough.
- [R-24](../../requirements/README.md#r-24) markup cleanup before
  conversion: four notes in the book are never closed; one table needs its
  stray row removed.
- [R-11](../../requirements/README.md#r-11) readable source: native notes
  are shorter than the HTML and read like the rest of the page.
- [R-05](../../requirements/README.md#r-05) partials and reuse: the
  note held in a variable becomes a partial in every tool.

## Not yet written

- **The book's kind names in Docusaurus and Starlight.** Can an
  extension, injected HTML or CSS give these tools an `important` type, so
  that Starlight's Caution can stay on its own `caution` type? Not tested;
  the review asks for it first
  ([how each tool maps the kinds](#how-each-tool-maps-the-kinds)).

- **Code blocks in notes.** Two notes in the book hold a `<pre>` block
  inside a `<div class="note">` (`gsg-grails`, `gsg-spring`;
  [survey](survey/README.md#the-books-notes)). No test page has one. The
  earlier rounds found that `<pre>` blocks need work of their own in MDX and
  Markdoc; this belongs with the code blocks concept.
- **The `warning` kind.** Two notes, both in `archive/`, use it; they were
  not tested.
- **A template style for the kinds.** No theme styles the HTML `.note`
  classes, and Zensical styles neither `important` nor `caution`. Rules in
  each site's stylesheet would, as `class="table"` does for tables; not
  tried.
- **bosh.io's admonitions.** `docs-bosh` already writes 302
  Python-Markdown admonitions; which of its types its theme styles, and how
  its titles map to the book's kinds, were not checked.
- **Label paragraphs** (`* Note:` in a list, one in the book, twelve on
  bosh.io) were counted, not converted.
- **Body text outside notes** was not compared word by word.
- **Probes and on-paper tools.** Eleventy, Sphinx/MyST, Middleman, Hugo and
  VitePress were not part of this round.
- **Screenshots.** None were taken; the browser check records the colours
  instead.
