# Zensical conventions for cross-repository links

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#zensical-0069). Headings follow the
[headings round's conventions](../../../headings/sites/zensical/CONVENTIONS.md)
(`## Text {#id}`).

```bash
make build            # install, then build every variant into site/<variant>/ (logs in .check/)
make check            # links and outline checks: mono, passthrough and native
make check-other      # the same checks on linked-native and default-passthrough, which show what breaks
make probe-broken     # a missing page and a missing anchor in another directory; as built and with --strict
make probe-depth      # links held in variables and in a partial, on pages at two depths
make probe-redirects  # old URLs with the redirects plugin
```

`make` writes one copy of [zensical.toml](zensical.toml) per variant,
`.zensical-<variant>.toml`, changing `docs_dir`, `site_dir` and
`use_directory_urls`. Zensical colours its messages; the Makefile strips
the colour codes from the logs.

## Layout

| Variant | Layout | `docs_dir` | URLs |
|---|---|---|---|
| `mono-passthrough`, `mono-native` | one folder whose subfolders are the URL directories | `pages/passthrough`, `pages/native` | `.html` |
| `linked-native` | the same subfolders as symbolic links, as docs-bosh links in a submodule's docs | `linked/native` | `.html` |
| `default-passthrough` | mono | `pages/passthrough` | Zensical's default |

- **Zensical reads one docs folder.** Separate repositories reach it as
  folders inside that folder: a git submodule checked out there is a plain
  folder, so it builds as mono does.
- **Folders that are symbolic links are not built.** `linked-native` builds
  the home page (a linked file) and no page of the linked folders: 0 of 4
  test pages ([check-other](../../results/zensical-check-other.txt)). The
  file walk of the
  [`zensical-watch` crate](https://github.com/zensical/zensical/tree/de3702c2df5257c42501163af0afbd765714824a/crates/zensical-watch)
  is set not to follow links (`follow_links(false)`, its `manager.rs`,
  lines 762-768).
  docs-bosh, built with MkDocs, mounts the bpm-release submodule's docs
  this way ([`content/bpm`](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/bpm)),
  so that layout would not carry over as it is.
- **One edit link base for the whole site.** `repo_url` and `edit_uri` are
  site settings, and the edit link is that base plus the page's path in the
  docs folder
  ([`page.rs` L305-L322](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/crates/zensical/src/structure/page.rs#L305-L322)).
  Every page links into one repository
  ([edit links](../../results/edit-links.txt)); the theme shows the link
  with the `content.action.edit` feature.

## URLs

- **`use_directory_urls = false` writes each page as `<path>.html`**; the
  default is `true`
  ([`config.py` L530](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/config.py#L530)).
  Decision (this round): the checked variants set it to `false`, so the
  book's URLs are files of the build. A folder's `index.md` is
  `<folder>/index.html`.
- **With the default**, every page is `<path>/index.html`, and Zensical
  rewrites a relative URL one folder deeper (`../adminguide/x.html` becomes
  `../../adminguide/x.html`), keeping `.html`. The passthrough pages then
  find 15 of 39 links as expected
  ([check-other](../../results/zensical-check-other.txt)).

## Links

| Source | Passthrough | Native |
|---|---|---|
| `../adminguide/x.html#id` (another directory) | as written | `../adminguide/x.md#id`, a file path |
| `troubleshoot-app-health.html#id` (same directory) | as written | `./troubleshoot-app-health.md#id` |
| `https://docs.cloudfoundry.org/devguide/x.html` | as written | a file path |
| `/concepts/http-routing.html#keepalive` (on that page) | as written | `#keepalive` |
| `#id` | as written | as written |
| `<a href="../custom-ports.html">` | as written | a Markdown link, file path |

- **A file path is the native link**, the same in both layouts. Zensical
  writes it as the target's URL (`../adminguide/x.html`), page-relative.
- **Passthrough builds unchanged**: `.html` links stay as written and
  resolve, 39 of 39 ([check](../../results/zensical-check.txt)).

## What the build reports

From [probe-broken](../../results/zensical-probe-broken.txt):

| Link | Native (`.md`) | Passthrough (`.html`) |
|---|---|---|
| missing page | "page does not exist", with file, line and column | nothing |
| missing anchor, another page | "anchor does not exist", with file, line and column | nothing |
| in-page id missing | "anchor does not exist" | "anchor does not exist" |

- Both checks are on by default (`invalid_links`, `invalid_link_anchors`,
  [`config.py` L748-L787](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/config.py#L748-L787)).
  They warn and the build succeeds; `zensical build --strict` stops with
  "Aborted because --strict flag is set" and exit status 1
  ([`main.py` L62-L67](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/main.py#L62-L67)).
- The five links already broken in the book are all reported in native,
  the three in-page ones in passthrough
  ([build warnings](../../results/zensical-build-warnings.txt)).

## Links in variables and partials

From [probe-depth](../../results/zensical-probe-depth.txt), with the
template engine's variables and include (the variables and partials
rounds' delimiters), on a page one folder deep and one two folders deep:

| Link | One folder deep | Two folders deep |
|---|---|---|
| variable, relative URL | resolves | no page |
| variable, root-relative | resolves | resolves |
| variable, file path | resolves | no page |
| partial, relative URL | resolves | no page |
| partial, root-relative | resolves | resolves |
| partial, file path | resolves | no page |

The template engine writes the value or the partial into the page before
Markdown reads it, so every relative path, a file path included, is read
from the including page.

## Old URLs

The `redirects` plugin, MkDocs's `redirect_maps`
([`config.py` L2032-L2044](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/python/zensical/config.py#L2032-L2044)),
writes a redirect page at each old path, with a meta refresh and a script
that keeps the fragment
([`output.rs` L37-L51](https://github.com/zensical/zensical/blob/de3702c2df5257c42501163af0afbd765714824a/crates/zensical/src/compat/mkdocs/plugin/redirects/output.rs#L37-L51);
the [probe](../../results/zensical-probe-redirects.txt) reports what the
script does with the fragment).
Both old URLs of the probe, one in another directory, get a page that leads
to `routes-domains`
([probe-redirects](../../results/zensical-probe-redirects.txt)). docs-bosh
uses the same plugin under MkDocs
([`mkdocs.yml` L362-L365](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/mkdocs.yml#L362-L365)).
