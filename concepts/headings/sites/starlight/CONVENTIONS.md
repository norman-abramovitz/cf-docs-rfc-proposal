# Starlight conventions for headings

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#starlight-0426). Pages and variables follow
the [tables round's conventions](../../../tables/sites/starlight/CONVENTIONS.md).

```bash
make build  # install, generate vars.json, build the site (log in .check/build.log)
make serve  # serve dist/ at http://localhost:4321
make check  # build, then run the outline check on every page and mode
```

## Headings

- **Native: Markdoc's id annotation.** `## <a id="about"></a> About metadata`
  becomes `## About metadata {% #about %}`; the id goes on the heading and
  the table of contents links to it.
- **The source headings also build as written.** The `<a id>` stays inside
  the heading and links to it work; the heading gets a generated id with a
  leading hyphen (`-about-metadata`) and the table of contents links to
  that one.
- **An HTML heading (`<h4><a id="x"></a>Text</h4>`) builds as written but is
  not in the table of contents.** Native writes it as `#### Text {% #x %}`.
- **Variables in headings work in every mode.**
  `### Use app logs to locate delays in {% $vars.app_runtime_abbr %}` shows
  the value in the heading, the generated id and the table of contents.
- **Skipped levels stay as written**, with no warning.
- **The page title is the front matter's `title`**, rendered as the `h1`
  with the id `_top`; the table of contents starts with an "Overview" entry
  that links to it.

## Generated ids

Lowercase, spaces become hyphens, punctuation dropped, a repeated id gets
`-1`, `-2`, as in Docusaurus. A space at the start of the heading text
gives a leading hyphen.

## Table of contents

`h2` and `h3` (the default), plus "Overview"
([toc](../../results/starlight-toc.txt)).

## Anchor check

None: the build does not check links or anchors.

## Body changes the new pages needed

Not headings; they belong to the variables and code blocks concepts:

| Source | Starlight |
|--------|-----------|
| a variable in a fenced code block | `<pre><code>$ cf create-shared-domain {% $vars.app_domain %}</code></pre>`. Correction (2026-10-11): a fence renders the variable; Markdoc processes tags inside fences. Rebuilt with this site's configuration and package lock, the value appears in a fence with no language, with `console`, and in a list step. The `<pre>` form was not needed ([variables round](../../../variables/results.md#starlight-0426)) |
| a variable in inline code | `<code>{% $vars.app_domain %}</code>`, for the same reason |
| line breaks inside `<pre>` (code blocks above, and `<pre class="terminal">`) | written `&#10;`, the block on one line; Markdoc reads the text inside HTML as Markdown, so it joins the lines and turns blank lines into paragraphs |
