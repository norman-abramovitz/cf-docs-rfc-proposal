# Middleman without Bookbinder

**Question.** What is the smallest change that removes Bookbinder and keeps
the pages' ERB and HTML as they are?

**Answer.** A short Middleman configuration file and a small layout. The
five test pages build unchanged, and every table matches the published page
cell for cell. Bookbinder adds nothing the tables need.

## What was done

- **Middleman 4.6.3 on Ruby 4.0.7**, with Redcarpet, the Markdown engine the
  published book uses. Pinned in [Gemfile.lock](Gemfile.lock).
- **The pages are the source files themselves.** `source/` links to the five
  files in [`../../source/`](../../source/) and its `images/`; nothing is
  copied or edited.
- **[config.rb](config.rb)** sets the Markdown engine with the book's options
  (tables, autolink, smartypants, fenced code, heading ids, no intra-word
  emphasis) and a `vars` helper. The helper reads
  `../../source/template_variables.yml` into an `OpenStruct`, as Bookbinder's
  own `vars` helper does.
- **The partial** uses Middleman's own `partial`:
  [scale-table-host.html.md.erb](source/scale-table-host.html.md.erb) holds
  `<%= partial 'oss_scale_table' %>`, as `high-availability.html.md.erb` does.
- **[The layout](source/layouts/layout.erb)** prints the page title and the
  page inside `<article>`. It has none of the book's navigation, quick links,
  "Page last updated" line or GitHub link.
- [variable-checks.html.md.erb](source/variable-checks.html.md.erb) tests a
  defined, an undefined and an HTML-valued variable.

`make check` builds the site and runs the spot checks; `make serve` serves it
on port 8005.

## Results

- **Every table is identical to the published page.** Rows, cells, cell text
  and code spans match for all thirteen tables, compared with
  [tables.py](../../checks/tables.py) against the pages saved from
  docs.cloudfoundry.org.
- **The text matches too.** A word-by-word comparison
  ([text-diff.py](../../checks/text-diff.py)) differs only where the layout
  leaves things out: the quick links at the top, "Page last updated", and the
  GitHub link. Quotes come out curly, as on the published page (smartypants).
- **Spot checks: 33 of 36 pass.** The three that fail test the intent files'
  cleanup, which this probe does not apply: the curly-quoted
  `class=“table”` in `credential-types`, and the backslashes in
  `\[a-z0-9A-Z\]` in `metadata`. The published page shows the same three.
- **Variables behave as in the book.** An undefined variable
  (`vars.metadata_ref`) renders as nothing; an HTML-valued one
  (`vars.route_services`) renders as markup, not escaped. ERB's `<%=` does not
  escape here.
- **The partial renders inside its host page**, and `&ge;` renders as ≥.
- **No build warnings.**

## Ruby 4.0.7

Middleman 4.6.3 runs on Ruby 4.0.7. One change is needed and two problems
came from this machine, not from Middleman:

- **`ostruct` must be in the Gemfile.** Since Ruby 4.0 it is no longer a
  default gem, and without it `require 'ostruct'` fails:
  `cannot load such file -- ostruct (LoadError)`. Bookbinder's `vars` helper
  uses it the same way.
- **This machine's Bundler was shadowed.** Ruby 4.0.7 brings Bundler 4.0.20,
  but an older copy (4.0.19) in Homebrew's `site_ruby` loaded first, and
  `bundle install` stopped with "The running version of Bundler (4.0.19) does
  not match the version of the specification installed for it (4.0.20)". The
  Makefile installs the locked Bundler into `vendor/bundler` and runs that one.
- **`sassc` did not compile.** Middleman depends on `sassc` 2.4.0, which builds
  C++ code; this machine's compiler found no C++ standard headers
  (`'vector' file not found`). The Makefile points it at the SDK's headers.

No older Ruby was needed.
