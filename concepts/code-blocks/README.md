# Concept: Code blocks

Status: **draft, incomplete — covers what is known as of 2026-10-11.**
The survey, the conversions and the checks are done; the conventions are
proposals for review. Results: [results.md](results.md).

This round asks whether the book's code blocks survive conversion into
each hands-on tool: their text exactly, their type with matching
highlighting, and a copy button
([R-06](../../requirements/README.md#r-06) typed code blocks). It takes
up what earlier rounds left to it: `<pre>` blocks that MDX and Markdoc
read as Markdown (tables round), code blocks in notes (notes round),
fences that only the book's Markdown engine closes (headings survey) and
variables inside code (variables round). It adds a code-block check
beside the outline, notes, variables and partials checks.

Terms used below:

- **Code block.** Text set apart from the page and shown as written, in a
  fixed-width font, with its line breaks kept: commands, their output,
  configuration files. On a built page it is a `<pre>` element.
- **Fence.** The Markdown way to write one: a line of three or more
  backticks, the code, and a closing line. The **info string** after the
  opening backticks (```` ```console ````) names the block's **type**,
  its language.
- **`<pre>` block.** A code block written in HTML: `<pre class="terminal">`
  (the book's terminal sessions), `<pre>` or `<pre><code>`.
- **Highlighting.** Colouring a block's words by their role with a
  **lexer** for its type. **Copy button**: a button on the block that
  puts its text on the clipboard.
- **Prompt.** The `$ ` before a command in a terminal session. A
  **console** block holds commands with prompts and their output; a
  **bash** block holds commands or a script without prompts.
- **Redcarpet** is the book's Markdown engine; **CommonMark** is the
  specification most other Markdown tools follow. They read some fences
  differently. **MDX** is Docusaurus's page format (Markdown with JSX);
  **Markdoc** is the format the Starlight sites use, as in the earlier
  rounds.
- **Modes.** *passthrough*: each code block as the book writes it,
  fences with their info string or none, `<pre>` blocks as HTML;
  *native*: every block the tool's own code block with a type, the
  published page's defects fixed. Everything outside code blocks is the
  same in both modes and follows the earlier rounds' native conventions
  (headings, notes, variables). Docusaurus and Starlight also have a
  *raw* check of the forms whose build fails; Docusaurus a probe of its
  CommonMark format.

## Progress

- [x] **Survey.** Every code block in the 15 `docs-*` repositories and
  the book repository at the partials survey's commits: 1,777 in the book
  (1,132 fences, 592 `<pre>` blocks, 47 indented, 6 fences shown as text)
  and 1,180 in bosh.io. How the book renders them (Redcarpet 3.2.3 and
  Rouge 1.11.1 through middleman-syntax, no copy button), with pinned
  source lines; a model of that renderer that matches 20 of 20 published
  pages; and the 14 files where Redcarpet and CommonMark find different
  code blocks. Scripts, data and write-up: [survey/](survey/README.md).
- [x] **Test pages chosen and copied**, verbatim at the survey's commits:
  [source/SOURCES.md](source/SOURCES.md), with the published pages as
  served on 2026-10-11 in [published/](published/).
- [x] **Intent written.** For each page, every code block's text, type,
  section and place, and what the published page gets wrong:
  [intent/](intent/), with a code file per page that the check reads.
- [x] **Code-block check written**: [checks/codeblocks.py](checks/codeblocks.py),
  with [checks/check-site.sh](checks/check-site.sh) and a browser check,
  [checks/codeblocks-browser.mjs](checks/codeblocks-browser.mjs).
- [x] **Converted and built** in all four hands-on tools, passthrough and
  native, plus the raw checks and probes. Every block passes in native
  mode in every tool, 53 of 53: [results.md](results.md#summary).
- [ ] **Conventions reviewed.** The eight proposals and four questions in
  [results.md](results.md#conventions-to-record).

## Test pages

| Page | Repository | Blocks | Cases |
|------|------------|--------|-------|
| [`routes-domains`](intent/routes-domains.md), Create a route | cloudfoundry/docs-dev-guide (the headings, notes, variables and partials rounds' page) | 9 | `console` fences with prompts and output; `<pre><code>` with variables and `<span>@</span>`; a fence indented after a list item |
| [`troubleshooting_slow_requests`](intent/troubleshooting_slow_requests.md), whole page | cloudfoundry/docs-cf-admin (the headings and tables rounds' page) | 11 | unlabelled fences; `<pre class="terminal">` with blank lines and `*/*`; a terminal block with a blank line in a list item |
| [`gsg-grails`](intent/gsg-grails.md), Step 5 | cloudfoundry/docs-buildpacks | 5 | a `<pre>` in a note; `console` without prompts; a YAML file in a terminal block; e-mail addresses in code |
| [`backup`](intent/backup.md), Connect to your jumpbox | cloudfoundry/docs-bbr | 4 | a fence right after text; a fence closed by ```` ```<br> ````; nested lists |
| [`backup-clean`](intent/backup.md), Clean up after a failed backup | cloudfoundry/docs-bbr | 4 | four backticks closed by three; backslash continuations |
| [`nginx`](intent/nginx.md), Create the nginx.conf file | cloudfoundry/docs-buildpacks | 13 | `{{…}}` template syntax in code and prose; `&lt;file&gt;` in a fence; untyped NGINX configuration |
| [`multiple-processes`](intent/multiple-processes.md), whole page | cloudfoundry/docs-dev-guide | 7 | a fence the published page shows as text; a terminal block with blank lines and `&#35;` before a note in a list item |

**How they were chosen.** Decision (this round): from the survey's rows,
few pages that together hold the common forms (unlabelled fences,
`console` fences, `<pre class="terminal">`, `<pre><code>`), the places
(top level, list item, note) and every pattern the earlier rounds handed
on: `<pre>` text that MDX and Markdoc read as Markdown, a code block in a
note, the two fences in `backup` that only the book closes, and
variables in code. Two pages come from earlier rounds; `routes-domains`
holds this round's variables in code. Three cases the survey found were
added for what they test: a fence right after text (`backup`), a fence
the published page shows as text (`multiple-processes`), and template
syntax and character references in fences (`nginx`). What no test page
holds is under [Not yet written](results.md#not-yet-written).

## Code-block check

[checks/codeblocks.py](checks/codeblocks.py) reads a built HTML page and
checks its code blocks against a code file. It needs only Python 3.

```bash
# The page's code blocks: type, place, highlighting, copy button, section, first line
python3 -I checks/codeblocks.py published/nginx.html

# The blocks of some sections in the code-file format, to start a code file
python3 -I checks/codeblocks.py published/nginx.html --emit --section Port

# A built page against its code file, requiring a type on every block
python3 -I checks/codeblocks.py BUILT.html --expect intent/nginx.code --require type

# Every check on every page of one site (run from sites/<tool>, after make build)
../../checks/check-site.sh site note=note,important=important,caution=caution type
```

What it does:

- **Finds every code block**, each outermost `<pre>` in the content area,
  and matches it to the code file's blocks in order, within the sections
  the file names. A block the file does not have, or a block it misses,
  fails.
- **Compares the text exactly.** The normalisation: line breaks read from
  `<br>` and line elements, copy buttons and line numbers left out,
  character references decoded, trailing white space on each line and
  blank lines at the ends dropped. Indentation, tabs, quotes and inner
  blank lines must match. The published site's hidden e-mail addresses
  are decoded as its script decodes them.
- **Fails on what leaked**: ERB, Markdoc or MDX variable syntax, AsciiDoc
  attribute references, HTML tags, character references or fence lines in
  the text where the code file has none; and block elements (`<p>`,
  `<hr>`, list items) inside the block, the sign that a tool read its text
  as Markdown.
- **Checks the section and the place**: body, list item, note or table
  cell.
- **Reads the type, the highlighting and the copy button**, and with
  `--require type,highlight,copy` fails a block that lacks one. Types a
  tool spells differently count as one (`console`, `shell-session`,
  `shellsession`; `bash`, `sh`; `yaml`, `yml`; `text`, `plaintext`).
- **Reads what the copy button copied**, from the attribute the browser
  check writes (or Expressive Code's `data-code`), and says whether it is
  the block's text or its commands without prompts.

`make check` in each site runs it with the outline check and, on the
four pages with notes, the notes check; native mode requires a type.
`make check-browser` serves the site, loads every page in Chrome through
[codeblocks-browser.mjs](checks/codeblocks-browser.mjs), clicks every copy
button, saves each page as the browser holds it, and runs the same checks
on the saved pages, requiring a type and a copy button in native mode.
Run on the published pages, the check fails on 10 blocks of five pages,
the book's own defects ([published check](results/published-check.txt)).

## Method

1. **Survey** every code block, how the book renders it, and where the
   book's Markdown engine and CommonMark disagree.
2. **Choose pages** that hold the patterns, preferring pages already
   converted.
3. **Write the intent**: each block's text, type, section and place, from
   the published page with its defects fixed.
4. **Convert by hand** into each tool, in both modes; the content outside
   code blocks follows the earlier rounds' native conventions. The
   mechanical part (heading ids, notes, variables, and for Antora a first
   draft with pandoc) was done with scratch scripts; every page was then
   reviewed and edited by hand.
5. **Build and check** with the code-block, outline and notes checks, in
   the static pages and in a browser; probe what each tool does with
   `console` and with the book's forms where the build fails.
6. **Record conventions** per tool ([sites/](sites/)`<tool>/CONVENTIONS.md`).

Each tool keeps the version of the earlier rounds. Two settings are new:
Zensical turns on its copy button (`content.code.copy`), and Starlight
draws fences with the code component of its Markdoc preset. Docusaurus
adds Prism grammars and a `console` alias.

## Layout

```
concepts/code-blocks/
├── README.md          this file
├── results.md         results per tool, cases across tools, conventions, questions
├── survey/            survey.py, book-render.rb, commonmark-render.mjs, summary.py, compare-published.py, the CSV files, README
├── source/            new test pages and the variables excerpt, verbatim, plus SOURCES.md
├── published/         the four new published pages, as served on 2026-10-11
├── intent/            per page: <page>.md, <page>.code (what the check compares), <page>.anchors; four .notes
├── checks/            codeblocks.py, check-site.sh, codeblocks-browser.mjs
├── sites/             docusaurus/, zensical/, starlight/, antora/: pages per mode, config, Makefile, CONVENTIONS.md
└── results/           check output per tool (static and browser), build warnings, probes, raw checks, published check
```

Each site builds with `make build` and checks with `make check` and `make
check-browser`; `make probe` and `make check-raw` run the probes and the
raw checks where a site has them. Sites serve on ports 4101–4104. Build
output and installed packages are ignored by git; the results in
[results/](results/) were produced from the sites built in place.

Decision (this round): the saved published pages stay in the repository
so the checks can be rerun after the live site changes. They, and the
rest of this round's working files, can be removed once the conversion is
complete.
