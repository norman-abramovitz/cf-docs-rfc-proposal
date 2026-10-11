# Zensical conventions for variables

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#zensical-0069). Pages follow the earlier
rounds' conventions: headings as the
[headings round's native mode](../../../headings/sites/zensical/CONVENTIONS.md)
writes them (`## Text {#id}`), notes as the
[notes round's native mode](../../../notes/sites/zensical/CONVENTIONS.md)
writes them.

```bash
make build      # install, write vars.yml and vars-native.yml, build both modes into site/
make serve      # serve site/ at http://localhost:8001
make check      # build, then the variables, outline and notes checks on every page, passthrough and native
make check-raw  # all_metrics exactly as written, with its ERB code line
make probe      # what each on_undefined setting does with an undefined and an empty name
```

## The mechanism

Zensical has a built-in macros extension, a port of the MkDocs plugin: it
renders each page as a Jinja template before Python-Markdown reads it
([`macros.py`](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/extensions/macros.py#L281-L299),
v0.0.69). A site turns it on with `[project.plugins.macros]`, which
Zensical maps onto the extension
([`config.py` L1146-L1151](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/config.py#L1146-L1151)).
`include_yaml` loads a YAML file as variables, and the `j2_*` settings
change Jinja's delimiters.

## Passthrough

The earlier rounds' site, unchanged: ERB delimiters (`<%=`, `%>`, `<%`,
`<%#`), the book's file loaded with its top key renamed to `vars`, and
`on_undefined = "silent"`.

- **Every `<%= vars.name %>` builds as written**, in text, inline code,
  fenced code, HTML table cells, headings, link text and link targets
  (Markdown and HTML), on every page
  ([check](../../results/zensical-check.txt)): 85 of 85 values in place.
- **Values that hold markup render as markup**: the page is rendered
  before Python-Markdown reads it, so an HTML value is HTML and a Markdown
  value is Markdown, as in the book. A Markdown value inside an HTML block
  stays as written, also as in the book.
- **A heading with a variable** shows the value in the heading and the
  table of contents ([browser check](../../results/browser-checks.txt));
  the headings round found the generated id uses it too.
- **The title can hold a variable.** The extension renders a front
  matter `title` that holds its delimiters
  ([`macros.py` L492-L521](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/extensions/macros.py#L492-L521)),
  so `title: <%= vars.app_runtime_abbr %> Component Metrics` works. The
  book's ERB code line that sets the title is not Jinja and stops the
  build: "TemplateSyntaxError: Encountered unknown tag 'current_page'"
  ([raw check](../../results/zensical-raw-check.txt)); the converter writes
  the variable into the front matter instead. A front matter `description`
  is not rendered.
- **Relative links in values** are rewritten one folder deeper, because
  each page is served as a folder (`../../running/config-ssh.html` becomes
  `../../../running/config-ssh.html`); HTML and Markdown links alike.
- **A name that is not defined renders as nothing**, and the build says
  nothing.
- **An empty value prints "None".** The book's file has 51 keys with no
  value, a YAML null; Jinja prints a null as `None`, where the book prints
  nothing ([probe](../../results/zensical-probe.txt)). 44 uses on the
  book's pages read such a key; none is on a test page.

## Native

The same extension and delimiters, with every name required:

- **`on_undefined = "strict"`** with `on_error_fail = true`: a name that is
  not defined stops the build. The message names the variable but not the
  page: "RuntimeError: Python error: UndefinedError: 'dict object' has no
  attribute 'no_such_name'" ([probe](../../results/zensical-probe.txt)).
  With `on_error_fail = false` the build passes, logs "Macro rendering
  failed in probe.md: …", and replaces the page with an error page. The
  other settings: `silent` and `lax` print nothing, `keep` prints
  `{{ no such element: dict object['no_such_name'] }}` on the page
  ([`macros.py` L546-L551](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/extensions/macros.py#L545-L550)).
- **vars-native.yml** is the book's file with empty values written as
  `""`, so they print nothing, and without the key that is not a name
  ([vars.py](vars.py)).
- **References to names that are not defined are removed** from the pages
  (they render as nothing today).
- **Why the ERB delimiters and not Jinja's own.** Decision (this round):
  keep `<%= %>`. With Jinja's `{{ }}`, `{% %}` and `{# #}`
  ([probe](../../results/zensical-probe.txt)):
  - a heading id written `{#id}`, the headings round's form, opens a Jinja
    comment and stops the build: "TemplateSyntaxError: Missing end of
    comment tag"; `{ #id }` would avoid it;
  - the book's own `{{port}}` and `{{.Subject}}` examples (12 lines on 2
    pages) become variables: with `silent` the nginx example's
    `listen {{port}};` builds as `listen ;`, and with `strict` the build
    stops.

  The ERB form is also what writers know today.

## Values that hold markup

Nothing to do: Python-Markdown reads the value as part of the page. A
value that is a whole note becomes a partial, as the notes round decided;
the macros extension's `include` reads it.

## How a variable reads in the source

```markdown
## Configuring SSH access for <%= vars.app_runtime_full %> {#platform-ssh-config}

<td>Configure the deployment to allow or prohibit SSH access (one-time). <%= vars.config_ssh_link %></td>

- Are there any suspicious [metrics](<%= vars.gorouter_metrics_link %>) spiking?
```

The page reads as the book's does.
