# Note survey

Status: draft, incomplete — covers what is known as of 2026-10-10.

This survey counts every note in the 15 `cloudfoundry/docs-*` repositories
and records how each one is written: its element, its kind, its title, what
it holds and where it sits. A note is a short passage set apart from the
text around it and headed Note, Important or Caution; the tools call it an
admonition ([glossary](../../../glossary.md#admonition)). The survey was
done on 2026-10-10 to choose the test pages of the notes round and to know
which patterns a conversion has to handle
([R-07](../../../requirements/README.md#r-07) notes and admonitions).

| File | What it is |
|---|---|
| [notes.csv](notes.csv) | The data: one row per note, 568 rows, each with a GitHub link to the note at the surveyed commit |
| [shas.txt](shas.txt) | The 15 repositories and the commit surveyed in each: the `docs-*` lines of the [table survey's list](../../tables/survey/shas.txt) |
| [survey.py](survey.py) | Finds the notes in a set of clones and writes `notes.csv` |
| [summary.py](summary.py) | Prints the counts below from `notes.csv` |

## Scope

- **Repositories.** The 15 `docs-*` repositories of the
  [table survey](../../tables/survey/README.md#scope), at the same commits.
  Decision (this round): the six tutorial repositories the table survey
  also read are left out, since the round's question is the book's notes;
  `docs-bosh`
  is counted, but apart, as the table survey did, because it builds
  bosh.io with MkDocs and the Material theme, not the book
  ([`mkdocs.yml`](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/mkdocs.yml#L319-L321)).
  "The book" below means the other 14.
- **Files.** The table survey's: `.md`, `.erb`, `.html`, `.haml`,
  `.markdown`, `.mdx` and `.adoc`, without `.git`, `node_modules` and
  `vendor` folders and without Markdown files at a repository's root, which
  no site publishes. Files in `archive/` folders are counted and flagged.
- **Variables.** The book's
  [`config/template_variables.yml`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml)
  is read too, for values that hold a note.
- **Source, not published pages.** A partial counts once however many pages
  include it.

## Method

[survey.py](survey.py) reads every file and finds five forms of note. Lines
inside fenced code blocks are skipped for every form; the Markdown forms
also skip lines inside `<pre>` blocks and inside HTML notes.

| Form | What is found |
|---|---|
| `html` | an HTML element whose class list holds the word `note`: `<p class="note">`, `<div class="note important">` and so on |
| `variable` | a value in `template_variables.yml` that holds such an element |
| `blockquote` | a Markdown blockquote (`> …`) whose text starts with a label such as `**Note**` or `Important:` |
| `label` | a paragraph or list item, outside any note element, that starts with a label: `**Note:**`, `<strong>Note</strong>`, `Note:`. "Note that …" and "Note the GUID …" are verbs and are not counted |
| `admonition` | a Python-Markdown admonition, `!!! note "Title"` |

For an HTML note it records the element and class as written, the quotes
around the class, the kind (the class after `note`, or `note`), whether a
`note__title` span is there and its text, what the note holds (lists, code,
code blocks, links, variables, partials, other ERB tags, images, tables),
Markdown syntax inside the HTML (backticks, `**`, `[text](url)`, list
lines), the indentation of the opening tag, whether it sits in a list (under
a Markdown list item, or inside an open `<li>`), in a table cell or in a
partial, and whether the element is closed. A `<p>` holds no block, so a
`<p class="note">` without `</p>` is taken to end where a browser or the
Markdown processor ends it: at the next `<p>` tag or blank line.

## Totals

| | HTML | Variable | Label | Blockquote | Admonition | All |
|---|---|---|---|---|---|---|
| Book (14 repositories) | 241 | 12 | 1 | 0 | 0 | 254 |
| bosh.io (`docs-bosh`) | 0 | 0 | 12 | 0 | 302 | 314 |
| **All** | **241** | **12** | **13** | **0** | **302** | **568** |

The 241 HTML notes are on 107 pages: `docs-dev-guide` 97, `docs-bbr` 38,
`docs-buildpacks` 22, `docs-deploying-cf` 22, `docs-cloudfoundry-concepts`
18, `docs-cf-admin` 15, `docs-running-cf` 12, `docs-cf-cli` 6,
`docs-loggregator` 6, `docs-credhub` 3, `docs-services` 2. `docs-uaa` and
`docs-dotnet-core-tutorial` have none, and `docs-book-cloudfoundry` has
notes only in its variables. Nine of the 241 are in `archive/` folders.

## The book's notes

**Elements and kinds.** Every note in the book is HTML; none is written as a
blockquote, and one is a label paragraph (`* Note:` in a list,
[`scaling-cloud-controller` L32](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/managing-cf/scaling-cloud-controller.html.md.erb#L32)).

| Element and class, as written | Notes | Variables |
|---|---|---|
| `<p class="note">` | 110 | 12 |
| `<p class="note important">` | 89 | |
| `<p class="note caution">` | 26 | |
| `<p class="note warning">` | 2 | |
| `<div class="note important">` | 9 | |
| `<div class="note">` | 4 | |
| `<div class="note caution">` | 1 | |

Every class is in straight quotes. No other class names a note: no
element has `class="tip"`, `class="warning"`, `class="alert"` or
`class="note breaking"`, though the book's stylesheet styles `.tip` and
`.note.breaking` (below). The two `note warning` notes are both in
`archive/` folders, as are 9 of the 11 notes without a title span.

**Titles.** 242 of the 253 notes in pages and variables open with
`<span class="note__title"><strong>Note</strong></span>` (or `Important`,
`Caution`), and every title matches its class: 120 Note, 95 Important, 27
Caution. The book's own script added the spans: it walks the content
repositories and inserts the span after each opening tag, the title chosen
by the class
([`scripts/add-note-titles.ps1` L46-L50](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/scripts/add-note-titles.ps1#L46-L50)).
Outside `archive/`, two notes have no span:
[`java-tips` L16](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/java-tips.html.md.erb#L16)
and
[`log-management` L172](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/log-management.html.md.erb#L172).

**What notes hold** (of the 253 in pages and variables; a note can hold
several): code 125, links 76, variables 18, lists 7, code blocks 3 (two in
`<pre>` inside a `<div class="note">`); 81 hold plain text only. No note
holds a partial, an image or a table. Every note in a page holds one
paragraph after its title, except the two `<div>` notes with a code block,
which hold two.

- **Lists** are always HTML `<ul>` or `<ol>`, and always in a `<div>`:
  [`cf-backup` L16](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/cf-backup.html.md.erb#L16),
  [`routes-domains` L234](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L234),
  [`manifest-attributes` L147](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/manifest-attributes.html.md.erb#L147).
- **Code blocks:**
  [`gsg-grails` L154](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L154),
  [`gsg-spring` L126](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-spring.html.md.erb#L126).
- **Variables** (`<%= vars.name %>` inside the note):
  [`routes-domains` L234](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L234),
  [`healthchecks` L186](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/healthchecks.html.md.erb#L186).
- **Markdown inside an HTML note:** two notes, both indented in a list
  step, write a code span with backticks
  ([`_using-vol-services` L266](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/_using-vol-services.html.md.erb#L266),
  [`custom-stack` L34](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/custom-stack.html.md.erb#L34)).
  On the published page the first renders as code
  ([published copy](../published/using-vol-services.html), line 786),
  because inside a list item the note is part of a paragraph and its text
  is read as Markdown. No note outside a list uses Markdown syntax.

**Where notes sit.** 35 notes are indented under a Markdown list item and 6
sit inside an HTML `<li>`; 5 sit in table cells (4 in
[`staticfile/index`](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/staticfile/index.html.md.erb#L107),
1 in
[`healthchecks` L146](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/healthchecks.html.md.erb#L146));
10 are in partials, one of which is a note and nothing else
([`_v3-note`](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/_v3-note.html.md.erb#L1)).

**Notes held in variables.** 12 values in `template_variables.yml` hold a
`<p class="note">`, written on one line with the title span. Seven are used
by pages at the surveyed commits (`external_vol_win_note`,
`billing_manager_role_note`, `cc_logging_default`, `mutual_tls_tcp`,
`isolation_segments_note`, `internal_domain_config`, `capi_sidecar_req`);
five are not used by any page (`ecr_support_cf_12_1`,
`enable_syslog_forwarding_link`, `link_adminguide_commands`,
`route_services`, `route_services_config`). One,
[`route_services_config`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L237),
holds a heading, text and a code block before its note.

**Markup defects** a browser repairs and a strict tool does not
([R-24](../../../requirements/README.md#r-24) markup cleanup before
conversion):

- 4 `<p class="note">` are never closed:
  [`cf-backup` L66](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/cf-backup.html.md.erb#L66)
  and
  [L109](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/cf-backup.html.md.erb#L109),
  [`node/index` L141](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/node/index.html.md.erb#L141),
  and one in `archive/` that ends with `<p>` where `</p>` was meant
  ([`azure` L108](https://github.com/cloudfoundry/docs-deploying-cf/blob/1113cfaf3626931c653c91dc8d537d7f181d6762/archive/azure.html.md.erb#L108)).
  The book's Markdown processor wraps each in a paragraph, and the
  browser ends it at the next block: the published page holds
  `<p><p class="note caution">` and the note's text
  ([published copy](../published/cf-backup.html), line 603).
- 2 notes close with `</p>` at the end of a text line; the book's own
  script moves such tags to a line of their own
  ([`scripts/fix-note-closing-tags.ps1`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/scripts/fix-note-closing-tags.ps1#L1-L3)).
  Both are the `note warning` notes in `archive/`.

## How the book styles notes today

The book's stylesheet has four rules
([`book-styles.scss` L229-L308](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/stylesheets/book-styles.scss#L229-L308)):

| Selector | Look | Used by |
|---|---|---|
| `.note` | pale yellow box (`#ffffed`), 1-pixel border `#ebebd3`, rounded corners, a lightbulb icon at the left | every note: 241 in pages, 12 in variables |
| `.note.warning` | pink box (`#fdd`, border `#fbb`), a warning-sign icon | 2 notes, both in `archive/` |
| `.note.breaking` | pink box, a broken-link icon | none |
| `.tip` | white box with a border, an icon | none |

There is no rule for `.note.important`, `.note.caution` or `.note__title`.
So every Important and Caution note looks exactly like a Note: the same
yellow box and lightbulb, told apart only by the bold title the span
holds. The stylesheet served on 2026-10-10
([`/stylesheets/all.css`](https://docs.cloudfoundry.org/stylesheets/all.css),
a built file, not pinned) has the same four rules and no others for notes.
A browser on the published pages confirms it: Caution, Important and Note
all get background `rgb(255, 255, 237)` and border `rgb(235, 235, 211)`
([browser checks](../results/browser-checks.txt)).

## bosh.io

`docs-bosh` writes notes as Python-Markdown admonitions, which its
`mkdocs.yml` turns on
([L367-L368](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/mkdocs.yml#L367-L368)):
302 on 128 pages, the count the table survey found. Types as written:
`note` 226, `warning` 35, `Note` 15, `tip` 12, `Warning` 4, `info` 3,
`Caveat` 2, and `danger`, `Info`, `Notice`, `Important`, `help` once each;
`!!!warning` without a space once. 17 carry a title in quotes
(`!!! warning "AWS IPv6 Prefix Limitation"`). 33 are indented in a list.
They hold code in 95, links in 75 and a list in 8. Twelve more notes are
label paragraphs (`**Note:** …`, `Note: …`), six of them in lists.

Python-Markdown lower-cases the type for the class and capitalizes it for
the default title, so `!!! Note` and `!!! note` make the same note
([`admonition.py` L176-L183](https://github.com/Python-Markdown/markdown/blob/0ffbf00cf667971d46f43aafba825e8d25098bc5/markdown/extensions/admonition.py#L176-L183),
version 3.11.0). Which of the other types the bosh.io theme styles was not
checked.

## How to rerun

Run from a working directory outside this repository, with `python3 -I`.
`SURVEY` stands for this folder, `concepts/notes/survey`. Each repository is
fetched at its commit, without history:

```sh
mkdir -p repos
git init -q repos/docs-bbr
git -C repos/docs-bbr fetch -q --depth 1 https://github.com/cloudfoundry/docs-bbr.git 51465950ce3a2196d66a9339086b94feed280c3e
git -C repos/docs-bbr checkout -q FETCH_HEAD
# … the same three lines for each repository in SURVEY/shas.txt

python3 -I SURVEY/survey.py repos SURVEY/shas.txt notes.csv
cmp notes.csv SURVEY/notes.csv
python3 -I SURVEY/summary.py SURVEY/notes.csv
```

`survey.py` prints the totals per form; `summary.py` prints every count on
this page. The scripts read files only; they run nothing from the clones.
