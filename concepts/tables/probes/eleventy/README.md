# Eleventy probe

**Question.** Does Eleventy 3.1.6 render a page with ERB variables unchanged,
when the `<%= vars.name %>` tags are left as they are and read as EJS? EJS
uses the same tag syntax, but `<%=` escapes its output, where ERB in
Middleman does not. How does Eleventy's `include` compare with ERB `partial`?

**Answer.** Yes, for the tables. `uaa-concepts` builds with its text
unchanged, and its two tables come out byte for byte as written, with only
the variables filled in. Its variables hold plain text, so the escaping
makes no difference there. An HTML-valued variable does not survive: with
`<%=` it shows as escaped text, so a conversion has to write `<%-` for it.
An include needs `<%-` for the same reason, plus the full file name.

## What was done

- **Page.** [`uaa-concepts`](../../source/uaa-concepts.html.md.erb), copied
  unchanged into `src/uaa-concepts.md`; only the file name changes, so
  Eleventy reads it as Markdown. `markdownTemplateEngine: "ejs"` runs EJS
  over each Markdown page before markdown-it.
- **Scale table.** A host page includes
  [`_oss_scale_table`](../../source/_oss_scale_table.html.md.erb), also copied
  unchanged, with `<%- include('/_oss_scale_table.md') %>`.
- **Variables.** [`src/_data/vars.js`](src/_data/vars.js) reads
  `template_variables` from the variables excerpt, so pages use `vars.name`
  as in the source.
- **Escaping.** [`src/escaping.md`](src/escaping.md) writes the HTML-valued
  `route_services` with both tags.

`make check` builds and runs the spot checks for the two pages. With
`PUBLISHED=<dir of saved published pages>`, it also runs the word-by-word
comparison for `uaa-concepts`.

## Findings

1. **EJS is a plugin.** Since Eleventy 3.0, EJS is not part of the core;
   `@11ty/eleventy-plugin-ejs` 1.0.0 adds it (with `ejs` 3.1.10).
2. **The tables are unchanged.** Both `uaa-concepts` tables and the scale
   table match the source byte for byte after the variables are filled in.
   markdown-it leaves HTML blocks alone, so no cleanup is needed to build.
   The `implicit` row's stray `</td>` stays, and the browser repairs it as
   on the published page. All 11 spot checks for the two pages pass.
3. **The text matches as on the other sites.** The word-by-word comparison
   shows only the differences every site has:
   - the section links at the top of the page;
   - straight quotes where the published page has curly ones;
   - the GitHub line.
4. **`<%=` escapes.** EJS's `<%=` escapes `<`, `>`, `&` and quotes; ERB's
   `<%=` in Middleman outputs the value as is. Plain-text variables look the
   same either way. `route_services` holds a `<p class="note">`, and with
   `<%=` the page shows the tags as text; with `<%-` it renders the note. A
   conversion has to change `<%=` to `<%-` at least for every HTML-valued
   variable, and for every helper call that returns HTML.
5. **Includes differ from partials.**
   - **The tag:** ERB writes `<%= partial 'oss_scale_table' %>`, and
     Middleman finds the leading underscore and the extension itself.
     EJS needs `<%- include('/_oss_scale_table.md') %>`: the full file
     name, with the path from `_includes` (leading `/`) or from the
     page. With `<%=` the whole table shows as escaped text (checked).
   - **What the included file sees:** it gets the page's data, so its
     own `vars` tags work.
   - **How it is rendered:** as EJS only. The page's Markdown pass then
     covers it.
6. **A literal `<%` is a tag.** In EJS, as in ERB, `<%` in prose or a code
   span starts a tag, so it must be written `<%%`. None of the test pages
   has one.
7. **Copied pages that git ignores are skipped.** By default Eleventy does
   not build files that `.gitignore` lists. The copies in `src/` are
   ignored, so the config turns that off (`setUseGitIgnore(false)`).
8. **No heading IDs are made.** markdown-it adds no IDs to headings. The
   page's own `<a id>` anchors work. Two of them are written `id="#shadow"`
   and `id="#user-groups"` in the source, so their links have no target,
   here as on the published page.

Not covered: Middleman helpers other than `partial` (`image_tag`,
`link_to`), which have no EJS counterpart; the other three test pages.
