# Zensical conventions for headings

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#zensical-0069). Pages and variables follow
the [tables round's conventions](../../../tables/sites/zensical/CONVENTIONS.md).

```bash
make build  # install, generate vars.yml, build the site
make serve  # serve site/ at http://localhost:8001
make check  # build, then run the outline check on every page and mode
```

## Headings

- **The source headings build as written.** `## <a id="about"></a> About metadata`
  works: the `<a id>` stays inside the heading, links to `#about` work,
  and the build's anchor check accepts them. The heading also gets a
  generated id (`about-metadata`), and the table of contents links to that
  one, not to `#about`.
- **Native: an attribute list on the heading.** `## About metadata {#about}`
  (the `attr_list` extension, on by default) puts the id on the heading;
  the table of contents then links to `#about`.
- **An HTML heading (`<h4><a id="x"></a>Text</h4>`) builds as written but
  is left out of the table of contents**; Python-Markdown passes raw HTML
  through without reading it. Native writes it as `#### Text {#x}`.
- **Variables in headings work in every mode.** The ERB tag is rendered
  before the page is read as Markdown, so the heading, the generated id
  (`use-app-logs-to-locate-delays-in-cloud-foundry`) and the table of
  contents all show the value.
- **Skipped levels stay as written**, with no warning.
- **The page title is the front matter's `title`.** The theme shows it as
  the `h1` because the pages have no `#` heading.

## Generated ids

Lowercase, spaces become hyphens, punctuation dropped, the `<a id>` and the
space after it ignored (`about-metadata`, no leading hyphen). A repeated id
gets `_1`, `_2` (`add-metadata-to-a-resource_1`): an underscore, where the
other tools use a hyphen.

## Table of contents

Every level from `h2` down (here `h2` to `h5`), Markdown headings only
([toc](../../results/zensical-toc.txt)).

## Anchor check

The build reports each link whose anchor does not exist on the target
page, with file, line and column
([build warnings](../../results/zensical-build-warnings.txt)). It counts
ids from `<a id>` and from attribute lists.
