# Starlight conventions for cross-repository links

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#starlight-0426). Pages are Markdoc (`.mdoc`),
headings follow the
[headings round's conventions](../../../headings/sites/starlight/CONVENTIONS.md)
(`## Text {% #id %}`).

```bash
make build            # install, then build every variant into dist/<variant>/ (logs in .check/)
make check            # links and outline checks: mono passthrough and native, linked native
make check-other      # the same checks on default-passthrough, which shows what breaks
make probe-broken     # a missing page and a missing anchor in another directory
make probe-depth      # links held in variables and in a partial, on pages at two depths
make probe-redirects  # old URLs with Astro's redirects
```

Each build starts without Astro's content cache (`.astro/`). The docs
collection is Astro's `glob()` loader over the variant's folder
([src/content.config.ts](src/content.config.ts)); Starlight's own
`docsLoader()` is the same loader over `src/content/docs/`
([`loaders.ts` L55-L58](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/loaders.ts#L55-L58)).

## Layout

| Variant | Layout | Pages | URLs |
|---|---|---|---|
| `mono-passthrough`, `mono-native` | one folder whose subfolders are the URL directories | `pages/passthrough`, `pages/native` | `.html` |
| `linked-native` | the same subfolders as symbolic links, as checkouts of separate repositories would be linked in | `linked/native` | `.html` |
| `default-passthrough` | mono | `pages/passthrough` | Astro's default |

- **Starlight reads one docs collection.** Separate repositories reach it
  as folders inside the collection's folder: checked out there (as
  submodules), or linked in. Linked folders build: `linked-native` passes
  every check ([check](../../results/starlight-check.txt)).
- **One edit link base for the whole site.** `editLink.baseUrl` plus the
  page's path
  ([configuration reference L80-L84](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/docs/src/content/docs/reference/configuration.mdx#L80-L84));
  a page's front matter can override it with `editUrl`
  ([frontmatter reference L38-L42](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/docs/src/content/docs/reference/frontmatter.md#L38-L42)),
  so a converter could write each page's own repository there. The site
  does not; every page links into one repository, with the path in this
  site ([edit links](../../results/edit-links.txt)).

## URLs

- **`build.format: 'file'` writes each page as `<path>.html`**, and
  Starlight writes its own links that way
  ([Astro `config.ts` L1307-L1313](https://github.com/withastro/astro/blob/3571e2d2e80a66764254fa9b7750704a150ca3f6/packages/astro/src/types/public/config.ts#L1307-L1313)).
  Decision (this round): the checked variants use it, with
  `trailingSlash: 'never'`.
- **A folder's index page becomes `<folder>.html`.** Starlight drops
  `/index` from a page's slug
  ([`slugs.ts` L44-L53](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/packages/starlight/src/utils/slugs.ts#L44-L53)),
  so `concepts/architecture/index.mdoc` is published as
  `concepts/architecture.html`, with `format: 'file'` and with
  `format: 'preserve'` alike (tried on 2026-10-11). A link written
  `architecture/index.html` finds no page: passthrough has 37 of 39 links
  as expected, the two misses being the links to folder index pages
  ([check](../../results/starlight-check.txt)). The old URL needs a
  redirect.
- **With the default URLs** (`<path>/index.html`) the passthrough pages
  find 13 of 39 links as expected
  ([check-other](../../results/starlight-check-other.txt)).

## Links

| Source | Passthrough | Native |
|---|---|---|
| `../adminguide/x.html#id` (another directory) | as written | `/adminguide/x.html#id`, root-relative |
| `architecture/index.html#routing` | as written | `/concepts/architecture.html#routing` |
| `https://docs.cloudfoundry.org/devguide/x.html` | as written | `/devguide/x.html` |
| `#id` | as written | as written |
| `<a href="../custom-ports.html">` | as written | a Markdown link, root-relative |

- **Starlight has no link to a source file.** A link is a URL, and
  Starlight writes it as it is. Decision (this round): the native link is
  the root-relative URL Starlight itself writes for the page under the
  chosen URL style, the form the book publishes for Markdown links today.
- **Passthrough keeps links page-relative**, and they resolve where the
  target's URL is unchanged.

## What the build reports

Nothing. A missing page and a missing anchor, in either form, build with
no message and exit status 0
([probe-broken](../../results/starlight-probe-broken.txt)). Link checking
needs a plugin; Starlight lists `starlight-links-validator`
([plugins page L35-L36](https://github.com/withastro/starlight/blob/afe57bbbc254b957b969d581d0f861925035bdcf/docs/src/content/docs/resources/plugins.mdx#L35-L36)),
which this round did not try.

## Links in variables and partials

From [probe-depth](../../results/starlight-probe-depth.txt), with Markdoc
variables that hold a parsed link (the variables round's native form) and
the partial tag, on a page one folder deep and one two folders deep:

| Link | One folder deep | Two folders deep |
|---|---|---|
| variable, relative URL | resolves | no page |
| variable, root-relative | resolves | resolves |
| partial, relative URL | resolves | no page |
| partial, root-relative | resolves | resolves |

The native form is root-relative, so it does not depend on depth.

## Old URLs

Astro's `redirects` setting writes, for a static build, a page with a meta
refresh at each old path
([`config.ts` L343](https://github.com/withastro/astro/blob/3571e2d2e80a66764254fa9b7750704a150ca3f6/packages/astro/src/types/public/config.ts#L343),
[`3xx.ts` L27](https://github.com/withastro/astro/blob/3571e2d2e80a66764254fa9b7750704a150ca3f6/packages/astro/src/core/routing/3xx.ts#L27)).
With `format: 'file'` both old URLs of the probe are written as
`….html` and lead to `routes-domains`; the page has no script, and its
refresh URL has no fragment, so nothing in it carries the old URL's
fragment on
([probe-redirects](../../results/starlight-probe-redirects.txt)).
