# Code-block survey

Status: draft, incomplete — covers what is known as of 2026-10-11.

This survey counts every code block in the 15 `cloudfoundry/docs-*`
repositories and in the book's own repository, and records how each one is
written, where it sits, what it holds, and what the book renders from it.
It was done on 2026-10-11 to choose the test pages of the code blocks
round ([R-06](../../../requirements/README.md#r-06) typed code blocks).

Terms used below:

- **Code block.** Text set apart from the page and shown as written, in a
  fixed-width font, with its line breaks kept: commands, their output,
  configuration files. On a built page it is a `<pre>` element.
- **Fence.** The Markdown way to write one: a line of three or more
  backticks (or tildes), the code, and a closing line of the same kind.
  The **info string** is the word after the opening backticks
  (```` ```console ````); it names the block's **type**, its language.
- **Indented code block.** The older Markdown way: lines indented four
  spaces after a blank line.
- **`<pre>` block.** A code block written in HTML, `<pre>…</pre>`, often
  `<pre class="terminal">`; with `<code>` inside, a `<pre><code>` block.
- **Highlighting.** Colouring a block's words by their role (command,
  option, string) with a **lexer**, the part of a highlighter that knows
  one language. The book's highlighter is Rouge.
- **Prompt.** The `$ ` before a command in a terminal session. A
  **console** block holds commands with prompts and their output; a
  **shell** block holds commands only.
- **Redcarpet** is the Markdown engine the book's build uses;
  **CommonMark** is the Markdown specification that most other tools
  follow.
- **ERB** is the Ruby template language the book's pages are written in;
  `<%= vars.name %>` puts in a variable's value before Markdown is read.
  **Bookbinder** and **Middleman** are the programs that build the book
  ([partials survey](../../partials/survey/README.md#how-the-book-resolves-a-partial)).

| File | What it is |
|---|---|
| [blocks.csv](blocks.csv) | One row per code block, 2,957 rows: its form, info string, place, how it closes, what it holds, what the book and a CommonMark parser make of it, with a GitHub link to the block at the surveyed commit |
| [rendered.csv](rendered.csv) | One row per code block the book's renderer finds (1,170), with the Rouge lexer it gets: the output of `book-render.rb` |
| [commonmark.csv](commonmark.csv) | One row per code block a CommonMark parser finds in the same pages (1,180): the output of `commonmark-render.mjs` |
| [shas.txt](shas.txt) | The 15 repositories and the commit surveyed in each: the partials survey's list |
| [survey.py](survey.py) | Finds the code blocks in a set of clones and writes `blocks.csv` |
| [book-render.rb](book-render.rb) | A model of the book's renderer: each Markdown page through Redcarpet and Rouge as the book's build runs them |
| [commonmark-render.mjs](commonmark-render.mjs), [package.json](package.json) | The same pages through commonmark.js 0.31.2, the CommonMark reference parser |
| [compare-published.py](compare-published.py), [published-pairs.txt](published-pairs.txt), [model-check.txt](model-check.txt) | The model's `<pre>` elements compared with 20 published pages: all the same |
| [summary.py](summary.py) | Prints the counts below from the three CSV files |

```bash
# from concepts/code-blocks/survey, with the clones in REPOS
GEM_HOME=GEMS ruby book-render.rb REPOS shas.txt rendered.csv WORK      # needs redcarpet 3.2.3, rouge 1.11.1
npm ci && node commonmark-render.mjs WORK commonmark.csv
python3 -I survey.py REPOS shas.txt rendered.csv commonmark.csv blocks.csv
python3 -I summary.py blocks.csv rendered.csv commonmark.csv
python3 -I compare-published.py WORK published-pairs.txt
```

## Scope

- **Repositories.** The 15 `docs-*` repositories of the
  [partials survey](../../partials/survey/README.md#scope), at the same
  commits ([shas.txt](shas.txt)), and the book repository,
  docs-book-cloudfoundry. `docs-bosh` builds bosh.io with MkDocs, not the
  book; its blocks are counted apart, as earlier surveys did. "The book"
  below means the other 14 repositories.
- **Files.** The earlier surveys': `.md`, `.erb`, `.html`, `.haml`,
  `.markdown`, `.mdx` and `.adoc`, without `.git`, `node_modules` and
  `vendor` folders and without Markdown files at a repository's root.
  Blocks in `archive/` folders (58) and in partials (61) are counted and
  flagged. One file no site publishes is counted:
  [`docker/README.md`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/docker/README.md)
  in the book repository.
- **Source, not published pages.** A block in a partial counts once.

## How the book renders a code block

The book pins `bookbindery` 9.12.1, which runs Middleman 3.4
([partials survey](../../partials/survey/README.md#how-the-book-resolves-a-partial)).
Lines are cited at Bookbinder's `v9.12.0` tag
([`f608a44`](https://github.com/pivotal-cf/bookbinder/commit/f608a441572def7787361842f05e42d163d78d54)),
as the partials survey does.

1. **Markdown engine and options.** Bookbinder's Middleman config loads
   `middleman-syntax`, sets Redcarpet with `tables`, `autolink`,
   `smartypants` and `fenced_code_blocks`, and activates the syntax
   extension
   ([`config.rb` L2, L11-L16, L32](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/config.rb#L11-L16)).
   Bookbinder requires `middleman-syntax ~> 2.0`, `rouge != 1.9.1` and
   `redcarpet ~> 3.2.3`
   ([`bookbinder.gemspec` L22-L24](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/bookbinder.gemspec#L22-L24)),
   and middleman-syntax 2.1.0 requires `rouge ~> 1.0`
   ([gemspec L19](https://github.com/middleman/middleman-syntax/blob/3f23e8a5fae7b24a60a4acb8db2208b8dcfac947/middleman-syntax.gemspec#L19)).
   The newest releases those allow are middleman-syntax 2.1.0, Rouge
   1.11.1 and Redcarpet 3.2.3
   ([RubyGems: middleman-syntax](https://rubygems.org/gems/middleman-syntax/versions),
   [rouge](https://rubygems.org/gems/rouge/versions),
   [redcarpet](https://rubygems.org/gems/redcarpet/versions)). The book
   has no `Gemfile.lock`, so which releases its build installs is not
   recorded; the published pages match these (the model, below).
2. **Every Markdown code block goes to Rouge.** middleman-syntax replaces
   Redcarpet's `block_code`, for fenced and indented blocks alike
   ([`redcarpet_code_renderer.rb` L6-L8](https://github.com/middleman/middleman-syntax/blob/3f23e8a5fae7b24a60a4acb8db2208b8dcfac947/lib/middleman-syntax/redcarpet_code_renderer.rb#L6-L8)).
   It finds a lexer with `Rouge::Lexer.find_fancy(language, code)`, falls
   back to plain text, and writes the class `highlight` plus the lexer's
   tag
   ([`highlighter.rb` L7-L16](https://github.com/middleman/middleman-syntax/blob/3f23e8a5fae7b24a60a4acb8db2208b8dcfac947/lib/middleman-syntax/highlighter.rb#L7-L16)).
   Rouge's formatter writes `<pre class="highlight TAG"><code>…</code></pre>`
   ([`html.rb` L48-L52](https://github.com/rouge-ruby/rouge/blob/e83a35a78dfb24d8412fac6383e9ef677bd8948f/lib/rouge/formatters/html.rb#L48-L52),
   Rouge 1.11.1).
3. **A block with no info string gets a guessed lexer.** `find_fancy`
   with no language asks Rouge to guess from the code
   ([`lexer.rb` L48-L66](https://github.com/rouge-ruby/rouge/blob/e83a35a78dfb24d8412fac6383e9ef677bd8948f/lib/rouge/lexer.rb#L48-L66)),
   and an unknown name finds no lexer, so plain text. Names are matched
   as written: `SQL` and `JSON` find no lexer.
4. **`console` is Rouge 1's `shell_session` lexer**, which also answers to
   `terminal`
   ([`shell_session.rb` L5-L25](https://github.com/rouge-ruby/rouge/blob/e83a35a78dfb24d8412fac6383e9ef677bd8948f/lib/rouge/lexers/shell_session.rb#L5-L25)).
   It colours a line that starts with `$ ` or `# `: the prompt, the
   command, its arguments. Every other line is plain text.
5. **`<pre>` blocks are HTML** and reach the page as written, after ERB
   has put in any variables. SmartyPants, the step that turns straight
   quotes into typographic ones, leaves the text inside `<pre>`,
   `<code>` and four other tags alone
   ([`html_smartypants.c` L327-L329](https://github.com/vmg/redcarpet/blob/c56a6d6d99fc930516631e81a112ae9a1fb9922d/ext/redcarpet/html_smartypants.c#L327-L329)).
   Bookbinder's stylesheet colours `.terminal` blocks
   ([`base.scss` L333-L337](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/source/stylesheets/base.scss#L333-L337))
   and holds the highlighting rules, among them `pre .gp` for a prompt
   ([`_syntax-highlight.scss` L19](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/source/stylesheets/partials/_syntax-highlight.scss#L19)).
6. **No copy button.** The layout loads one script, `all.js`
   ([`layout.erb` L21](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/layout.erb#L21)),
   made of Bookbinder's `bookbinder.js` and the book's `book.js`
   ([`all.js` L1-L2](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/source/javascripts/all.js#L1-L2)).
   Neither touches code blocks
   ([`book.js`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/javascripts/book.js),
   [`bookbinder.js`](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/source/javascripts/bookbinder.js));
   `book.js` also loads Mermaid for diagrams. The `all.js` that
   docs.cloudfoundry.org served on 2026-10-11 holds no call to the
   clipboard, and the four pages saved in [published/](../published/)
   hold no `<button>`.

**A model of the book's renderer.** [book-render.rb](book-render.rb) runs
each Markdown page through Redcarpet 3.2.3 and Rouge 1.11.1 the way points
1–3 describe. ERB is replaced, not run: a `<%= vars.name %>` becomes its
value, every other tag nothing. The model adds one option no source line
sets, Redcarpet's `no_intra_emphasis`: without it the model made
`cell_id … exit_description` emphasis inside a `<pre>` in a list item
where the published pages do not. Which layer of the real build sets it
was not traced, as the headings round could not trace heading ids
([headings results](../../headings/results.md#not-yet-written)).

With that option, the model's `<pre>` elements are the same, character for
character, as the published ones on all 20 pages compared, 186 `<pre>`
elements ([model-check.txt](model-check.txt)), once e-mail addresses are
decoded (below). Eight more pages fetched from docs.cloudfoundry.org on
2026-10-11 and not saved gave the same result, among them
[`web-config-transform-buildpack`](https://docs.cloudfoundry.org/buildpacks/hwc/web-config-transform-buildpack.html),
[`java-tips`](https://docs.cloudfoundry.org/buildpacks/java/java-tips.html),
[`application-binding`](https://docs.cloudfoundry.org/devguide/services/application-binding.html)
and [`opentelemetry`](https://docs.cloudfoundry.org/loggregator/opentelemetry.html)
(as served that day; not pinned). The published classes confirm Rouge 1:
`<pre class="highlight shell_session">`, with the prompt in a `w` span
([saved `routes-domains`](../../headings/published/routes-domains.html),
line 846). From Rouge 2.1.0 the lexer is named `console`
([`console.rb` L6-L7](https://github.com/rouge-ruby/rouge/blob/b63fc1705975b3adcf6ce1e23c165d53385b7924/lib/rouge/lexers/console.rb#L6-L7)),
and the class would read `highlight console`.

**The published HTML hides e-mail addresses.** Inside code blocks too,
`user@example.com` reaches the page as a link reading "[email protected]",
which a Cloudflare script turns back into the address in the browser
([saved `gsg-grails`](../published/gsg-grails.html), the script tag
`email-decode.min.js`). Some sources write `username<span>@</span>example.com`
to prevent it
([`routes-domains` L150](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L150)).
The code-block check decodes such links as the script does.

**Where the book's Markdown engine differs from CommonMark.** Redcarpet
3.2.3 reads fences more loosely than CommonMark:

- **Any bare fence line closes a block**: three or more backticks *or*
  tildes, of any length, with nothing after them
  ([`markdown.c` L1751-L1755](https://github.com/vmg/redcarpet/blob/c56a6d6d99fc930516631e81a112ae9a1fb9922d/ext/redcarpet/markdown.c#L1751-L1755)).
  CommonMark wants the opening character and at least the opening length.
- **A block in a list item ends with the item.** Any fence line, even
  ```` ```<br> ````, toggles the item's "inside a fence" state
  ([L1876-L1878](https://github.com/vmg/redcarpet/blob/c56a6d6d99fc930516631e81a112ae9a1fb9922d/ext/redcarpet/markdown.c#L1876-L1878)),
  so the item ends at the next item, and a block left open ends there too.
- **A fence cannot start right after a line of text.** Without the
  `lax_spacing` option, which the book does not set, a paragraph runs
  until a blank line
  ([L1658-L1677](https://github.com/vmg/redcarpet/blob/c56a6d6d99fc930516631e81a112ae9a1fb9922d/ext/redcarpet/markdown.c#L1658-L1677));
  the backticks then make an inline code span. In CommonMark a fence
  interrupts a paragraph.
- **A fence line needs no more than three spaces** before it, relative to
  its list item
  ([L1356-L1366](https://github.com/vmg/redcarpet/blob/c56a6d6d99fc930516631e81a112ae9a1fb9922d/ext/redcarpet/markdown.c#L1356-L1366));
  deeper, it is part of an indented code block. List items measure that
  indentation differently in the two.

## Method

[survey.py](survey.py) reads every file and finds three forms:

| Form | What is found |
|---|---|
| `fence`, `fence-tilde` | a line of three or more backticks or tildes, any indentation, and an optional info string; it ends as Redcarpet ends it (above), and the row says whether CommonMark ends it at the same line |
| `pre`, `pre-code` | an HTML `<pre>` element, without or with `<code>` inside |
| `indented`, `fence-as-text` | a block that only the two parsers' output shows: an indented code block, or one whose first line is a fence (a fence read as text) |

For each block it records the info string or the `<pre>` attributes, the
indentation, how it closes, and where it sits: at the top level, in a
Markdown list item, in an HTML list item, in a note, in a table cell, in a
blockquote. It records what the block holds: variables (`<%= vars.x %>`)
and other ERB, character references (`&lt;`), HTML elements inside a
`<pre>`, blank lines, braces, `{{`, `{%` and `{#` (template delimiters in
Zensical, Markdoc and Jinja), Markdown characters inside a `<pre>`
(`*`, `_`, backticks), tabs, and whether its first line starts with a
prompt (`$ `, `# `, `> `).

Then it joins each block with the two parsers' rows by its first line, in
document order, and records the kind each parser makes of it (fenced,
indented, HTML, or nothing) and, for the book, the Rouge lexer. Lines in
front matter and HTML comments are skipped. The join is approximate where
the two parsers pair fences differently; the file-level comparison in
[summary.py](summary.py) is exact.

## Totals

| | Code blocks | Files |
|---|---|---|
| The book (14 repositories and the book repository) | 1,777 | 205 |
| bosh.io (`docs-bosh`) | 1,180 | — |

The book's 1,777: fences 1,132 (1,110 with backticks, 22 with tildes),
`<pre>` blocks 592 (573 `<pre>`, 19 `<pre><code>`), indented blocks 47,
and 6 fences that the book shows as text. By repository: docs-dev-guide
524, docs-buildpacks 404, docs-cf-admin 227, docs-running-cf 89,
docs-deploying-cf 83, docs-uaa 81, docs-loggregator 77, docs-credhub 61,
docs-cloudfoundry-concepts 58, docs-bbr 57, docs-cf-cli 54, docs-services
34, docs-dotnet-core-tutorial 21, docs-book-cloudfoundry 7. The book's
model finds 1,170 blocks in Markdown (fenced and indented); commonmark.js
finds 1,180.

## Findings

**Most fences name no type.** 807 of the 1,132 fences (71%) have no info
string. Rouge guessed plain text for 788 of them, JSON for 11 (among them
`{{module "…"}}` lines in an NGINX file), and shell for 2; 6 are not code
blocks in the book at all (below). The 325 with an info string: `console`
196, `yaml` 51, `bash` 17, `json` 10, `xml` 8, `shell` 7, `java` 6, `ruby`
6, `text` 4, `csharp` 4, `script` 4, `path` 2, `go` 2, and one each of
`ssh`, `toml`, `c#`, `SQL`, `javascript`, `python`, `jq`, `yml`. Rouge
found no lexer for `script`, `path`, `ssh`, `jq`, `SQL` and `JSON`.

**`console` usually holds commands without prompts.** 164 of the 196
`console` fences start without `$ `, for example
[`cf marketplace`](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L124-L126).
Rouge 1's `shell_session` shows such a line as plain text, so on the
published pages these blocks are not coloured. Terminal sessions are
mostly `<pre class="terminal">`: 413 of its 554 uses start with `$ `, and
188 hold a prompt and output lines.

**`<pre>` blocks are a third of the book's code.** 592 blocks: `class="terminal"`
546, `class='terminal'` 5, no attribute 19, `<pre><code>` 19, and 3 with
typographic quotes, `class=‘terminal’`, which browsers read as the class
`‘terminal’`
([`audit-events` L42](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/managing-cf/audit-events.html.md.erb#L42),
[`usage-events` L31](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/managing-cf/usage-events.html.md.erb#L31),
L102). What their text holds matters to tools that read the text of
HTML as Markdown (results: Docusaurus and Starlight):

- a blank line: 106 blocks, 26 of them in a list item;
- characters Markdown reads, `*`, `_` or backticks: 24, such as
  `Accept: */*`
  ([`troubleshooting_slow_requests` L40-L60](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting_slow_requests.html.md.erb#L40-L60));
- braces `{` or `}`: 56 (JSON);
- a first line `---` (a YAML file): 7, such as
  [`gsg-grails` L179-L185](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L179-L185);
- HTML elements other than the `<code>` wrapper: 58 (`<strong>`, `<span>`,
  links);
- character references: 22, such as `routing&#95;api` and `&minus;` in
  [`_tcp_modify_ports` L3-L8](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/_tcp_modify_ports.html.md.erb#L3-L8),
  where `&minus;` shows U+2212, not a hyphen, in a YAML list.

**Where blocks sit.** In a Markdown list item: 619 fences (556 indented
four spaces, 47 eight, 10 six, 9 two) and 242 `<pre>` blocks; at the top
level 513 fences and 334 `<pre>` blocks. In an HTML list item 8, in a
table cell 6 (four in
[`_c2c_oss_enable`](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/_c2c_oss_enable.html.md.erb#L19-L23),
two in
[`oms-nozzle`](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/oms-nozzle.html.md.erb#L87-L94)),
and in a note 2, the notes round's open item:
[`gsg-grails` L158-L162](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L158-L162)
and
[`gsg-spring` L130-L134](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-spring.html.md.erb#L130-L134).

**Variables inside code.** 64 blocks hold 136 variable uses: 43 fences,
15 `<pre>`, 6 `<pre><code>`; docs-dev-guide 42 blocks, docs-cf-admin 10,
docs-loggregator 8. No block holds other ERB, and none writes `<%%` (ERB's
way to show a literal `<%`). Six blocks hold `{{`, five of them NGINX
buildpack templates
([`nginx/index` L52-L56](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/nginx/index.html.md.erb#L52-L56)),
one a `uaac` command whose JSON holds Go template fields,
`{{.Subject}}`
([`notifications` L109-L112](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/notifications.html.md.erb#L109-L112)).

**Character references inside fences are shown as written.** In a fence,
`&lt;file&gt;` is text, so the published page shows `&lt;file&gt;`
([`nginx/index` L147-L149](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/nginx/index.html.md.erb#L147-L149),
L167; and two YAML blocks in
[`manifest-attributes` L97](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/manifest-attributes.html.md.erb#L97-L110),
L847).

**Tabs**: 73 blocks hold a tab character (44 fences, 16 `<pre>`, 13
indented).

### Fences only the book's engine closes, and other disagreements

The headings survey found two fences in `backup` that only the book closes
([headings survey](../../headings/survey/README.md#fences-closed-the-books-way)).
Comparing the book's model with commonmark.js over every page finds 14
files where the two find different code blocks, and 2 more where they
differ only in a block's trailing blank line (`docs-dotnet-core-tutorial`).
By cause:

- **A fence right after a line of text** (6 fences): the book makes inline
  code of it, CommonMark a code block.
  [`backup` L64-L66](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L64-L66),
  [L74-L77](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L74-L77),
  [`_using-vol-services` L66-L68](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/_using-vol-services.html.md.erb#L66-L68),
  [`opentelemetry` L184-L211](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/opentelemetry.html.md.erb#L184-L211),
  [`archive/azure` L179-L181](https://github.com/cloudfoundry/docs-deploying-cf/blob/1113cfaf3626931c653c91dc8d537d7f181d6762/archive/azure.html.md.erb#L179-L181),
  and `docker/README.md`. The published `backup` shows L64-L66 as a
  `<code>` element running over three lines inside a list item.
- **A fence closed only the book's way** (2): `backup` L76 closes with
  ```` ```<br> ````, which closes nothing in either; the book ends the
  block with its list item. L359 opens with four backticks and closes with
  three
  ([L359-L365](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L359-L365)).
  In CommonMark the second block runs to the end of its list item and
  swallows the `<pre>` after it.
- **A fence indented four or more spaces deeper than its list item's
  text** (3 files): one parser reads a fence, the other an indented block
  that shows the fence lines.
  [`multiple-processes` L20-L31](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/multiple-processes.html.md.erb#L20-L31)
  is a YAML block in CommonMark, but the published page shows
  ```` ```yaml ```` and ```` ``` ```` inside the block;
  [`web-config-transform-buildpack` L66-L73](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/hwc/web-config-transform-buildpack.html.md.erb#L66-L73)
  and
  [`java-tips` L152-L160](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/java-tips.html.md.erb#L152-L160)
  are the other way round.
- **Text indented four spaces** (4 files): one parser reads an indented
  code block where the other reads a paragraph or list item.
  [`hwc/index` L141-L143](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/hwc/index.html.md.erb#L141-L143)
  and
  [`upgrading_dependency_versions` L135-L140](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/upgrading_dependency_versions.html.md.erb#L135-L140)
  are code in the book;
  [`bbr-devguide` L186-L187](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/bbr-devguide.html.md.erb#L186-L187)
  and
  [`external-blobstores` L61-L62](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/external-blobstores.html.md.erb#L61-L62)
  are code in CommonMark.
- **An indented `<pre>`** (1 file, 2 blocks): CommonMark reads an indented
  code block that shows the `<pre class="terminal">` tag as text
  ([`application-binding` L18-L25](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/application-binding.html.md.erb#L18-L25),
  L168).
- **The book's home page** is HTML indented four spaces: CommonMark reads
  all 785 lines as one code block
  ([`index.html.md.erb` L42](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/index.html.md.erb#L42)).

A conversion has to repair these before or while it converts, reading each
block the way the published page shows it or the way the author meant it
([R-24](../../../requirements/README.md#r-24) markup cleanup before
conversion). The test pages hold four of them (`backup` ×3,
`multiple-processes`).

### bosh.io

`docs-bosh` writes 1,180 fences, almost all typed: `shell` 504, `yaml`
430, `json` 96, `text` 94, `bash` 18, `ruby` 15, `powershell` 6, and a few
others; 2 have no info string. It writes no `<pre>` block. Its blocks were
counted, not converted.

## Not covered

- **Code in other forms.** Inline code, and commands written as inline
  code with `<br>` between steps
  ([`gsg-grails` L325-L352](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L325-L352)),
  were not counted. Three Mermaid diagrams written with the
  `mermaid_diagram` helper
  ([`bbr-devguide` L255](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/bbr-devguide.html.md.erb#L255);
  [helper](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/bookbinder_helpers.rb#L79-L83))
  are diagrams, not code blocks. No page uses Bookbinder's
  `yield_for_code_snippet`, which pulls code from another repository.
- **The model's limits.** It replaces ERB rather than running it and
  renders partials apart from their pages, so blocks in a partial are
  compared on the partial; pages in other formats (`.html.erb`) are not
  rendered.
