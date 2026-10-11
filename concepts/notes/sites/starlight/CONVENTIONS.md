# Starlight conventions for notes

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#starlight-0426). Pages and variables follow
the [tables round's conventions](../../../tables/sites/starlight/CONVENTIONS.md),
headings the [headings round's](../../../headings/sites/starlight/CONVENTIONS.md)
(`## Text {% #id %}`).

```bash
make build      # install, generate vars.json, build the site (log in .check/build.log)
make serve      # serve dist/ at http://localhost:4321
make check      # build, then the outline and notes checks on every page, passthrough and native
make check-raw  # Markdoc's errors on the raw page that stops the build, and the checks on the rest
```

## Passthrough

The HTML notes stay; Markdoc reads the text inside HTML as Markdown, which
forces three changes, as the tables round found for table cells:

| Source | Passthrough | Why |
|--------|-------------|-----|
| a note's text over several lines | the text on one line | the space next to an inline tag on the second line is dropped: `with the<code>cf set-health-check</code>command` |
| a variable, then a space and an inline tag, on the same line | the space written `&#32;` | the same space is dropped: `type to<code>http</code>` |
| `<code>>= v7.1.48</code>` | `<code>&gt;= v7.1.48</code>` | `>` at the start of the text is read as a blockquote: `<code><blockquote><p>= v7.1.48</p></blockquote></code>` |
| a `<p class="note">` without `</p>` | the note closed | the build stops: "Node 'html-tag' is missing closing" |
| `<%= vars.external_vol_win_note %>` | `{% rawhtml value=$vars.external_vol_win_note /%}` | the tables round's tag for an HTML-valued variable |

Evidence: [raw check](../../results/starlight-raw-check.txt),
[built HTML](../../results/raw-html-excerpts.txt). The notes check finds
the dropped spaces; nothing in the build reports them. The theme gives
HTML notes no box ([browser check](../../results/browser-checks.txt)).

## Native

The `aside` tag of Starlight's own Markdoc preset, `@astrojs/starlight-markdoc`
0.7.0, which renders Starlight's `Aside` component:

```markdown
{% aside type="caution" title="Important" %}

The health check configuration that you provide with
`cf push` overrides any configuration in the app manifest.

{% /aside %}
```

- **Only the preset's `aside` tag is taken**
  ([markdoc.config.mjs](markdoc.config.mjs)). Extending the whole preset
  would also replace Markdoc's code blocks with Starlight's, and change
  pages the earlier rounds converted. Decision (this round): add the one
  tag.
- **The types are `note`, `tip`, `caution` and `danger`**
  ([preset L67-L85](https://github.com/withastro/starlight/blob/fe11bb470d2177a3696ddeac7379a9625b9f987b/packages/markdoc/index.mjs#L67-L85)).
  There is no `important`. Decision (this round): all three kinds are
  mapped by severity, with the source's title: `note` → `type="note"`,
  `important` → `type="caution" title="Important"`, `caution` →
  `type="danger" title="Caution"`. Caution does not keep Starlight's
  `caution` type, so that Important and Caution stay two different boxes.
  With no title, the aside shows the type's name ("Note").
- **Markdown inside is read**, variables as `{% $vars.name %}`. The text
  inside the tag is Markdown, not HTML, so the whitespace and `>` problems
  of passthrough do not arise.
- **In a list** the tag is indented under its item; **in an HTML table
  cell** it works with blank lines around it.
- **A note held in a variable becomes a partial**, `_external_vol_win_note.mdoc`,
  included with `{% partial file="./_external_vol_win_note.mdoc" /%}`.
- **No link check** runs at build time, as in the earlier rounds.

## How a note reads in the source

```markdown
{% aside type="danger" title="Caution" %}

Selective backups increase your overall recovery time. …

{% /aside %}
```

The tag syntax is longer than the other tools' but says what it does; the
body needs no indentation.
