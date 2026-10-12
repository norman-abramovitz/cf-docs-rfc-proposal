# Docusaurus conventions for cross-repository links

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#docusaurus-3102). Headings follow the
[headings round's conventions](../../../headings/sites/docusaurus/CONVENTIONS.md)
(`## Text {#id}`); pages are `.mdx`, as in the earlier rounds.

```bash
make build            # install, then build every variant into build/<variant>/ (logs in .check/)
make check            # links and outline checks: split and mono, passthrough and native
make check-other      # the same checks on split-filelinks and default-passthrough, which show what breaks
make probe-broken     # a missing page and a missing anchor in another content source; warn and throw
make probe-depth      # links held in variables and in a partial, on pages at two depths
make probe-redirects  # old URLs with the client-redirects plugin
```

Each variant is a whole site served at `/`, picked by environment
variables in [docusaurus.config.js](docusaurus.config.js): `LAYOUT`,
`PAGES` and `URLS`. Each build starts without `.docusaurus/` and
`node_modules/.cache/`: files generated for another variant's plugins made
the next build fail ("Cannot read properties of undefined (reading
'length')" in `DocItemFooter`, then "Can't resolve
'@site/.docusaurus/docusaurus-plugin-content-pages/…'").

## Layout

| Variant | Layout | Pages | URLs |
|---|---|---|---|
| `split-passthrough`, `split-native` | one docs plugin instance per repository, `routeBasePath` its URL directory (`concepts`, `adminguide`, `devguide`, `running`, `cf-cli`) | `pages/passthrough`, `pages/native-split` | `.html` |
| `mono-passthrough`, `mono-native` | one docs instance at `/` over one folder whose subfolders are the URL directories | `pages/passthrough`, `pages/native-mono` | `.html` |
| `split-filelinks` | split | `pages/native-mono` (file links across instances) | `.html` |
| `default-passthrough` | mono | `pages/passthrough` | Docusaurus's default |

- **Separate content sources are docs plugin instances.** Each has its own
  `id`, `path` and `routeBasePath`
  ([multi-instance guide](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/website/docs/guides/docs/docs-multi-instance.mdx)).
  A repository checked out into `pages/…/<dir>` (as a submodule or by the
  build) is one instance. Both layouts give the same URLs.
- **The home page.** In split, the book repository's start page is a page
  of the pages plugin; in mono, a docs page with `slug: /`.
- **One edit link per repository, in both layouts.** `editUrl` takes a
  function of the doc's path
  ([`plugin-content-docs.mdx` L37](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/website/docs/api/plugins/plugin-content-docs.mdx#L37));
  the site's function names the repository from the instance (split) or
  from the first folder (mono), and the source file with `.html.md.erb`
  ([edit links](../../results/edit-links.txt)).

## URLs

- **`trailingSlash: false` writes each page as `<path>.html`** and links to
  it as `<path>`
  ([`docusaurus.config.js.mdx` L138-L146](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/website/docs/api/docusaurus.config.js.mdx#L138-L146)).
  The book's URL `/concepts/http-routing.html` is then a file of the build,
  and GitHub Pages also serves `/concepts/http-routing` from it
  ([spot check of this repository's own site](../../survey/spot-check.txt)).
  Decision (this round): every checked variant uses it.
- **A folder's index page keeps `…/index.html` only with `slug: index`.**
  Without it, `concepts/architecture/index.mdx` becomes
  `concepts/architecture.html`, and a link written
  `architecture/index.html` finds no page.
- **With the default URLs** (`<path>/index.html`) the passthrough pages'
  `.html` links find no page: 13 of 39 links as expected
  ([check-other](../../results/docusaurus-check-other.txt)).

## Links

| Source | Passthrough | Native, mono | Native, split |
|---|---|---|---|
| `../adminguide/x.html#id` (another repository) | as written | `../adminguide/x.mdx#id`, a file path | `/adminguide/x#id`, the URL |
| `troubleshoot-app-health.html#id` (same repository) | as written | `./troubleshoot-app-health.mdx#id` | `./troubleshoot-app-health.mdx#id` |
| `https://docs.cloudfoundry.org/devguide/x.html` | as written | a file path | the URL `/devguide/x` |
| `#id` | as written | as written | as written |
| `<a href="../custom-ports.html">` | as written | a Markdown link, file path | a Markdown link, file path |

- **A file path works only within one docs plugin instance.** Docusaurus
  says so
  ([`markdown-features-links.mdx` L54](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/website/docs/guides/markdown-features/markdown-features-links.mdx#L54)),
  and the code looks the path up in the instance's own map of source files
  ([`plugin-content-docs/src/index.ts` L160-L170](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/packages/docusaurus-plugin-content-docs/src/index.ts#L160-L170)).
  In `split-filelinks` all 19 file links between instances stay as
  `….mdx` URLs and find no page; Docusaurus warns about each one
  ([build warnings](../../results/docusaurus-build-warnings.txt)).
  Decision (this round): in split, a link to another instance is the
  target's root-relative URL without extension.
- **Docusaurus rewrites relative URL links to root-relative**, from the
  page's URL: `../concepts/http-routing.html#zipkin-headers` is published as
  `/concepts/http-routing.html#zipkin-headers`, as the book does. An HTML
  `<a>` is left as written.
- **Passthrough works, and the build calls it broken.** Every `.html` link
  resolves in the built site (39 of 39), but Docusaurus reports 24 of them
  as broken links, since it knows its routes without `.html`
  ([build warnings](../../results/docusaurus-build-warnings.txt)). It does
  not check links written as HTML `<a>`.

## What the build reports

From [probe-broken](../../results/docusaurus-probe-broken.txt):

| Link | Native | Passthrough |
|---|---|---|
| missing page, another source | broken link | broken link |
| missing anchor, another source | broken anchor | broken link (the `.html` URL) |
| missing page, file path (mono) | "Markdown link … couldn't be resolved", then a broken link | — |
| in-page id missing | broken anchor | broken anchor |

- `onBrokenLinks` defaults to `throw` and `onBrokenAnchors` to `warn`
  ([`docusaurus.config.js.mdx` L395-L413](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/website/docs/api/docusaurus.config.js.mdx#L395-L413)).
  The sites set both to `warn` so the logs hold every message; with `throw`
  the build exits with status 1 and lists the broken links (it stops before
  the anchors).
- Each message names the page's route and the link, not the source file
  and line, except the Markdown-link message, which names both.
- The five links already broken in the book are all reported in native,
  three in passthrough (the two to other pages are reported as broken
  links instead).

## Links in variables and partials

From [probe-depth](../../results/docusaurus-probe-depth.txt), a page one
folder deep and one two folders deep:

| Link | One folder deep | Two folders deep |
|---|---|---|
| variable (JSX `<a>`), relative | resolves | no page |
| variable, root-relative | resolves | resolves |
| variable, `<Link to="/adminguide/x">` | resolves | resolves |
| partial, relative URL | resolves | no page |
| partial, root-relative | resolves | resolves |
| partial, file path from the partial's folder | resolves | resolves |

A file path in an imported partial is resolved from the partial's own file
(when the partial is inside the docs folder, so the docs plugin compiles
it). A relative URL is resolved from the page.

## Old URLs

`@docusaurus/plugin-client-redirects` writes a page that redirects with
JavaScript (keeping the query and fragment) and a meta refresh
([`plugin-client-redirects.mdx` L10-L12](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/website/docs/api/plugins/plugin-client-redirects.mdx#L10-L12)).
From [probe-redirects](../../results/docusaurus-probe-redirects.txt):

- `from: '/devguide/deploy-apps/domains-routes'` is written as
  `…/domains-routes/index.html`, even with `trailingSlash: false`, so the
  old URL `…/domains-routes.html` is not covered.
- With the default URLs, `fromExtensions: ['html']`
  ([L44](https://github.com/facebook/docusaurus/blob/f37f9035584917a97a260b91fc2842cba4f8b94f/website/docs/api/plugins/plugin-client-redirects.mdx#L44))
  writes `concepts/http-routing.html/index.html`, a folder named like the
  old file; a host that adds the slash to a folder serves it. Links through
  it reach a redirect page, whose script passes the fragment on.
