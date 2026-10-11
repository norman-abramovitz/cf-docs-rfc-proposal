# Zensical conventions for notes

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#zensical-0069). Pages, variables and
partials follow the [tables round's conventions](../../../tables/sites/zensical/CONVENTIONS.md);
headings are as the source writes them, except on `routes-domains`, the
headings round's page.

```bash
make build      # install, generate vars.yml, build the site
make serve      # serve site/ at http://localhost:8001
make check      # build, then the outline and notes checks on every page, passthrough and native
make check-raw  # the same checks on the raw mode (notes exactly as written)
```

## Passthrough

- **The source's notes build as written.** `<p class="note">` and
  `<div class="note">` with their title spans, notes in lists and in table
  cells, and the note held in a variable all build unchanged, and every
  note keeps its kind, title and text
  ([check](../../results/zensical-check.txt)). Python-Markdown passes HTML
  blocks through, and the variable is rendered before the page is read.
- **Close every note.** A `<p class="note">` without `</p>` is not ended by
  a blank line: Python-Markdown reads the rest of the page as raw HTML, so
  every heading and note after it is lost as such and shows as Markdown
  text ([raw check](../../results/zensical-raw-check.txt),
  [built HTML](../../results/raw-html-excerpts.txt)). The cleanup adds the
  `</p>`.
- **The theme gives HTML notes no box.** Their bold title is all that sets
  them apart ([browser check](../../results/browser-checks.txt)).

## Native

Python-Markdown's admonition, on by default in a new project:

```markdown
!!! caution

    - **Backup artifacts can contain secrets.** Secure backup artifacts …
    - **The restore is a destructive operation.** …
```

- **The kind is the type, as written:** `!!! note`, `!!! important`,
  `!!! caution`. Python-Markdown lower-cases the type for the class and
  capitalizes it for the title, so the reader sees "Note", "Important",
  "Caution" with no title written
  ([`admonition.py` L176-L183](https://github.com/Python-Markdown/markdown/blob/0ffbf00cf667971d46f43aafba825e8d25098bc5/markdown/extensions/admonition.py#L176-L183)).
- **The body is indented four spaces**; Markdown inside it is read
  (lists, code spans, links, variables in ERB form).
- **In a list,** the admonition is indented under its item like any other
  block, and its body four spaces further.
- **In an HTML table cell,** the `md_in_html` extension reads Markdown
  inside HTML when asked: `markdown="1"` on the `<table>` and on the row,
  `markdown="block"` on the cell, the row's cells not indented, and the
  cell's text and the admonition separated by blank lines. The table's
  stray second `<tr>` had to go: with it, the row was read as Markdown and
  its indented cells became a code block.
- **A note held in a variable becomes a partial** in `partials/native/`,
  included where the variable was:
  `<% include "native/_external_vol_win_note.md" %>`.

## The look of the kinds

The theme styles `note` but has no rule for `important` or `caution`: its
stylesheet names neither ([theme styles](../../results/theme-admonition-styles.txt)),
so all three kinds get the note's blue box and differ only in their title
([browser check](../../results/browser-checks.txt)). Keeping the source's
kind names leaves the look to the template, as `class="table"` does for
tables: rules for `.admonition.important` and `.admonition.caution` in the
site's stylesheet would set it. Not tried in this round.

## How a note reads in the source

```markdown
!!! important

    For HTTP apps, <%= vars.company_name %> recommends setting the health check type to `http` instead of a simple port check.
```

Shorter than the HTML (one line for the kind and title instead of three
tags), but the indentation carries the meaning: a body line that loses its
four spaces ends the note.
