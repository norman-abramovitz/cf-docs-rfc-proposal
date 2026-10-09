# Concepts

The migration is worked one documentation concept at a time. For each concept,
real pages are converted by hand into each candidate tool, the conventions that
work are recorded, and those conventions later drive the `cf-docs-migrate`
`scan` and `convert` commands.

## Principles

- **Content and document outline are preserved ideally.** The words, code,
  links, heading tree, and order of sections should survive conversion. A
  conversion may restructure content when the source structure was chosen for
  formatting reasons (for example, short phrases set as a list where sentences
  would read better as paragraphs). Every such change is deliberate and
  recorded as a deviation.
- **Everything else is a hint.** Column widths, alignment, wrapping, and
  similar presentation details express author intent, not exact values. Each
  tool and template honors hints as well as it can. Hints are tool-neutral.
  The first ones are drafted in [Tables](tables/README.md#hints-for-tables) and
  move to a shared `hints.md` once a second concept needs them.
- **Appearance is not compared.** Fonts, colors, and heading styles belong to
  the site template. A converted page can look different from the published
  page and still be correct.
- **The source format is open.** Markdown is one candidate, not a requirement.
  HTML passthrough and tool extensions are first-class options. Formats are
  judged by whether they meet the requirements of each user group.
- **Open source only.** Every tool in the evaluation is open source.

## Candidate tools

| Tier | Tools | Work |
|------|-------|------|
| Hands-on | Zensical, Docusaurus, Astro/Starlight, Antora | Each concept converted by hand, conventions recorded |
| Probe | Eleventy (EJS variables), Sphinx/MyST (directive hints), Middleman without Bookbinder (minimal-change baseline) | One page per probe |
| On paper | Hugo, VitePress | Capability check against requirements |

## Concepts

| Concept | Status | Why it matters |
|---------|--------|----------------|
| [Tables](tables/) | Done: [results](tables/results.md#summary) | Complex HTML tables (widths, spans, lists and paragraphs in cells, variables in cells) are the main reason the content is not plain Markdown today |
| Copyright and build-time values | Proposed | The published footer renders `&copy; <%= Time.now.year %> Cloud Foundry Foundation` from `docs-book-cloudfoundry/master_middleman/source/layouts/_book-footer.erb`, so the year changes on every build whether or not any content changed. Conversion is mostly a formatting change, which may not warrant a new copyright year. Open question for the RFC: should the year follow content changes (for example, the last commit that changed a page's content) rather than the build date? Either way, page comparisons must treat build-time values as expected differences. |
| Headings | Proposed | Simplest concept; establishes the outline check |
| Variables | Proposed | `<%= vars.* %>` from `template_variables.yml`; some values contain HTML or Markdown |
| Partials | Proposed | `<%= partial '...' %>`; some partial names are themselves stored in variables |
| Notes and admonitions | Proposed | `<p class="note">` with `note__title` spans |
| Code blocks | Proposed | Shell, console, JSON, YAML; copy button |
| Cross-repository links | Proposed | Links between content repositories must survive conversion |
