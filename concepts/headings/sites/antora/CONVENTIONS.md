# Antora conventions for headings

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#antora-321). Pages and variables follow the
[tables round's conventions](../../../tables/sites/antora/CONVENTIONS.md).

```bash
make build  # install, fetch the pinned UI, generate site-playbook.yml, build (log in .check/build.log)
make serve  # serve site/ at http://localhost:8002
make check  # build, then run the outline check on every page and mode
```

## Headings

- **Native: a block anchor above the section title.**
  `## <a id="about"></a> About metadata` becomes `[[about]]` on the line
  above `== About metadata` (as in the tables round).
- **Set `idprefix` and `idseparator` site-wide.** Asciidoctor's default
  generated id is `_about_metadata`, so a heading with no explicit id loses
  the id the published page gives it (`limitations`, not `_limitations`).
  The playbook sets `idprefix: ''` and `idseparator: '-'`
  ([antora-playbook.yml](antora-playbook.yml)); the generated ids then match
  the other tools'. Results with the defaults:
  [antora-default-ids-check.txt](../../results/antora-default-ids-check.txt).
- **Passthrough keeps the `<a id>` as inline HTML:**
  `== +++<a id="about"></a>+++ About metadata`. Links to `#about` work; the
  section also gets a generated id, and the table of contents links to it.
- **An HTML heading is not a section.** Kept in a passthrough block
  (`++++` … `<h4>…</h4>` … `++++`) it renders, but it is not in the table
  of contents, and the blocks after it belong to the section above it in
  AsciiDoc's structure. Native writes it as a section: `[[x]]` and
  `==== Text`.
- **Variables in headings work in every mode.** `{app_runtime_abbr}` in a
  section title is replaced before the id is made.
- **Skipped levels stay as written, with a warning.** `====` under `==`
  renders as `h4`, and Asciidoctor logs "section title out of sequence:
  expected level 2, got level 3" for each one
  ([build warnings](../../results/antora-build-warnings.txt)). The warning
  does not stop the build.
- **The page title is the document title**, `= Managing access to Service Plans`,
  rendered as the `h1`.

## Generated ids

With the playbook's settings: lowercase, spaces become hyphens,
punctuation dropped, and a repeated id gets `-2`, `-3`
(`add-metadata-to-a-resource-2`): numbering starts at 2, where Docusaurus
and Starlight start at 1. Defaults: `_about_metadata`, `_2`.

## Table of contents

Built in the browser by the default UI's script: `h2` and `h3`
([browser check](../../results/browser-checks.txt)). The static HTML has
no entries.
