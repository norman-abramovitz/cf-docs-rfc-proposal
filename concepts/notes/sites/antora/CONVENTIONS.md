# Antora conventions for notes

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#antora-321). Pages and variables follow the
[tables round's conventions](../../../tables/sites/antora/CONVENTIONS.md),
headings the [headings round's](../../../headings/sites/antora/CONVENTIONS.md);
every page is AsciiDoc in every mode.

```bash
make build      # install, fetch the pinned UI, generate site-playbook.yml, build (log in .check/build.log)
make serve      # serve site/ at http://localhost:8002
make check      # build, then the outline and notes checks on every page, passthrough and native
make check-raw  # the checks on the raw component (one page)
```

## Passthrough

Each HTML note sits in a passthrough block, as the tables round did for
HTML tables:

```asciidoc
[subs=attributes+]
++++
<p class="note important">
<span class="note__title"><strong>Important</strong></span>
For HTTP apps, {company_name} recommends setting the health check type to <code>http</code> instead of a simple port check.
</p>
++++
```

- **`[subs=attributes+]` only where the note holds a variable**, so that
  `{company_name}` is replaced.
- **A note held in a variable** is the attribute alone in such a block.
- **Markdown inside a passthrough note stays as written.** The block is not
  parsed, so `` `vers=3.0` `` shows with its backticks, where the
  published page shows code; the converter writes `<code>vers=3.0</code>`
  ([raw check](../../results/antora-raw-check.txt),
  [built HTML](../../results/raw-html-excerpts.txt)).
- **A note in a list step** goes in the step with a list continuation
  (`+`) above the block.
- The default UI gives HTML notes no box; their bold title is all that sets
  them apart ([browser check](../../results/browser-checks.txt)).

## Native

AsciiDoc's admonitions. **All three of the book's kinds are AsciiDoc kinds**
(the default UI styles `NOTE`, `TIP`, `IMPORTANT`, `CAUTION` and `WARNING`),
so the kind is kept as it is and the label needs no title:

```asciidoc
IMPORTANT: For HTTP apps, {company_name} recommends setting the health check type to `http` instead of a simple port check.

[CAUTION]
====
* *Backup artifacts can contain secrets.* Secure backup artifacts …
* *The restore is a destructive operation.* …
====
```

- **One paragraph:** `KIND:` at the start of the paragraph.
- **More than one block** (a list, several paragraphs): `[KIND]` above an
  example block (`====` … `====`).
- **In a list step,** a list continuation (`+`) attaches the admonition to
  the item. A step that holds a nested list and then a note wraps its
  content in an open block (`--` … `--`), as the tables round found:
  otherwise the note attaches to the nested list's last item.
- **In a table cell,** the table is AsciiDoc's own, and the cell an
  AsciiDoc cell (`a|`) that holds the text and then `IMPORTANT: …`.
- **A note held in a variable becomes a partial**,
  `modules/ROOT/partials/external_vol_win_note.adoc`, included with
  `include::partial$external_vol_win_note.adoc[]`.
- **Line breaks** (`<br>`) are a space and `+` at the end of the line.
- **Code that holds `--`** is written as literal monospace,
  `` `+--enforce-route-policies+` ``, so that `--` is never turned into a
  dash.
- **The labels:** the default UI shows each kind's name in capitals on a
  mark of its own colour (note blue, important red, caution purple), above
  the same grey box ([theme styles](../../results/theme-admonition-styles.txt),
  [browser check](../../results/browser-checks.txt)).
- **No warnings** from Asciidoctor ([build log](../../results/antora-build-warnings.txt)).

## How a note reads in the source

`IMPORTANT: …` is the shortest form of any tool: the kind is the first
word. Notes with lists need the `[KIND]` and `====` lines, and notes in
list steps the `+` and `--` markers, which a writer who does not know
AsciiDoc may not expect.
