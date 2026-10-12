# Concepts

The migration is worked one documentation concept at a time. For each concept,
real pages are converted by hand into each candidate tool, the conventions that
work are recorded, and those conventions later drive the `scan` and
`convert` commands of `cf-docs-migrate`, a migration tool still to be
written.

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
| [Tables](tables/) | Done, with open items: [results](tables/results.md#summary) | Complex HTML tables (widths, spans, lists and paragraphs in cells, variables in cells) are the main reason the content is not plain Markdown today |
| [Copyright and build-time values](build-time-values/) | Conventions for review, year rule open: [results](build-time-values/results.md#summary) | The footer year and "Page last updated" are computed at build; comparisons must mask them, and converted pages need dates that survive conversion. Whether the year should follow content changes is an open question for the RFC. |
| [Headings](headings/) | Done, with open items: [results](headings/results.md#not-yet-written) | Simplest concept; establishes the outline check |
| [Variables](variables/) | Done, with open items: [results](variables/results.md#not-yet-written) | `<%= vars.* %>` from `template_variables.yml`; some values contain HTML or Markdown |
| [Partials](partials/) | Done, with open items: [results](partials/results.md#not-yet-written) | `<%= partial '...' %>`; some partial names are themselves stored in variables |
| [Notes and admonitions](notes/) | Done, with open items: [results](notes/results.md#not-yet-written) | `<p class="note">` with `note__title` spans |
| Code blocks | Proposed | Shell, console, JSON, YAML; copy button |
| Cross-repository links | Proposed | Links between content repositories must survive conversion |
