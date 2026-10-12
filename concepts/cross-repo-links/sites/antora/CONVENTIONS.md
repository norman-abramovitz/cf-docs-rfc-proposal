# Antora conventions for cross-repository links

The patterns that worked in this round. Results and evidence:
[results.md](../../results.md#antora-321). Pages are AsciiDoc; headings
follow the [headings round's conventions](../../../headings/sites/antora/CONVENTIONS.md)
(`[#id]` above the heading, `idprefix: ''`, `idseparator: '-'`).

```bash
make build            # install, then build every variant into site/<variant>/ (logs in .check/)
make check            # links and outline checks: split and mono, passthrough and native
make check-other      # the same checks on default-passthrough, which shows what breaks
make probe-broken     # a missing page and a missing anchor in another component or module
make probe-depth      # links held in attributes and in a partial, on pages at two depths
make probe-redirects  # old URLs with page aliases
```

`make` writes one playbook per mode from [antora-split.yml](antora-split.yml)
and [antora-mono.yml](antora-mono.yml) (`.playbook-<layout>-<mode>.yml`).
Every build runs with `CI=true`, so that the default UI uses each source's
`edit_url` for pages read from a worktree instead of a `file://` link
([content-edit-url.adoc L27-L31](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/docs/modules/playbook/pages/content-edit-url.adoc#L27-31)).

## Layout

| Variant | Layout | URLs |
|---|---|---|
| `split-passthrough`, `split-native` | one component per repository, named as its URL directory (`concepts`, `adminguide`, …), each its own content source; the book's start page in the component `ROOT` | `.html` |
| `mono-passthrough`, `mono-native` | one component named `ROOT`, one module per URL directory, the start page in the module `ROOT` | `.html` |
| `default-passthrough` | mono, with the `indexify` URL style | `<path>/index.html` |

- **Both layouts give the same URLs.** A versionless component named `ROOT`
  is published at the root of the site, and its `ROOT` module adds no
  segment
  ([component-name-key.adoc L60-L96](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/docs/modules/ROOT/pages/component-name-key.adoc#L60-96)).
  So the component `adminguide` (split) and the module `adminguide` of
  `ROOT` (mono) both publish `/adminguide/x.html`.
- **Each content source has its own edit link.** `edit_url` is set per
  source in the split playbook, so each page names its own repository
  ([content-edit-url.adoc L38-L46](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/docs/modules/playbook/pages/content-edit-url.adoc#L38-46);
  [edit links](../../results/edit-links.txt)). Here all sources are folders
  of this repository, so the path in each link is this repository's.
- **A content source is a git repository** (here, this repository's
  worktree, each start path standing for one repository). Antora reads the
  repositories itself; no checkout into one folder is needed.

## URLs

- **`html_extension_style: default` writes each page as `<path>.html`**
  ([how-antora-builds-urls.adoc L207-L212](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/docs/modules/ROOT/pages/how-antora-builds-urls.adoc#L207-212)),
  and a folder's `index.adoc` as `<folder>/index.html`: the book's URLs.
  The earlier rounds used `indexify`. Decision (this round): the checked
  variants use `default`.
- **With `indexify`** (`<path>/index.html`), the passthrough pages find 13
  of 39 links as expected
  ([check-other](../../results/antora-check-other.txt)).

## Links

| Source | Passthrough | Native, split | Native, mono |
|---|---|---|---|
| `../adminguide/x.html#id` (another repository) | `link:../adminguide/x.html#id[text]` | `xref:adminguide::x.adoc#id[text]` | `xref:adminguide:x.adoc#id[text]` |
| `troubleshoot-app-health.html#id` (same repository, `devguide/deploy-apps/`) | `link:…[text]` | `xref:deploy-apps/troubleshoot-app-health.adoc#id[text]` | the same |
| `https://docs.cloudfoundry.org/devguide/x.html` | `link:https://…[text]` | `xref:devguide::x.adoc[text]` | `xref:devguide:x.adoc[text]` |
| `#id` | `link:#id[text]` | `<<id,text>>` | `<<id,text>>` |

- **The xref names the target by component (split) or module (mono)**, and
  the file by its path from the `pages` folder, not from the current page
  ([resource-id-coordinates.adoc L135-L156](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/docs/modules/page/pages/resource-id-coordinates.adoc#L135-156)).
  The two layouts differ only in `::` against `:`.
- **Antora writes an xref as a page-relative `.html` URL**
  (`../adminguide/x.html#id`): every native link resolves, 39 of 39, in
  both layouts ([check](../../results/antora-check.txt)).
- **Passthrough writes every link with the `link:` macro** and the URL as
  written, since AsciiDoc has no raw HTML link. Decision (this round).

## What the build reports

From [probe-broken](../../results/antora-probe-broken.txt):

| Link | Native | Passthrough |
|---|---|---|
| missing page, another component or module | ERROR "target of xref not found", with the page | nothing |
| missing anchor, another page | nothing | nothing |
| in-page id missing (`<<id>>`) | INFO "possible invalid reference", at `--log-level=info` only | nothing |

- **The build succeeds** unless `--log-failure-level` (or
  `runtime.log.failure_level`) is set; Antora's default failure level is
  `fatal`, and when the level is met it exits with status 2
  ([runtime-log-failure-level.adoc L3-L14](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/docs/modules/playbook/pages/runtime-log-failure-level.adoc#L3-14)).
  With `--log-failure-level=error` the probe exits with status 2.
- **An xref whose page is missing is published as an in-page link** to an
  id named after the target (`#adminguide::no-such-page.adoc`).
- **Fragments of xrefs are not checked.** The two links already broken in
  the book that point at another page's id are not reported.

## Links in attributes and partials

From [probe-depth](../../results/antora-probe-depth.txt), with attributes
in the playbook and a partial of the `concepts` module included from a
page one folder deep and one two folders deep:

| Link | One folder deep | Two folders deep |
|---|---|---|
| attribute, `link:` relative | resolves | no page |
| attribute, `link:` root-relative | resolves | resolves |
| attribute, `xref:` | resolves | resolves |
| partial, `link:` relative | resolves | no page |
| partial, `link:` root-relative | resolves | resolves |
| partial, `xref:` | resolves | resolves |

An xref is resolved at the page that renders it, wherever its text came
from, and written as a URL relative to that page.

## Old URLs

`page-aliases` on the target page writes a redirect page at each old URL,
by default as a static HTML file
([page-aliases.adoc L1-L15](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/docs/modules/page/pages/page-aliases.adoc#L1-15),
[urls-redirect-facility.adoc L10](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/docs/modules/playbook/pages/urls-redirect-facility.adoc#L10));
`redirect_facility` can instead write rules for nginx, Apache httpd,
Netlify or GitLab Pages
([L29-L36](https://gitlab.com/antora/antora/-/blob/fcc5d507ecf5944a0ea3fc8048160cf4c26da7f7/docs/modules/playbook/pages/urls-redirect-facility.adoc#L29-36)).
An alias can name another component (split) or module (mono): both old
URLs of the probe, one in another repository's directory, lead to
`routes-domains`. The page's script sets the location without the old
URL's fragment
([probe-redirects](../../results/antora-probe-redirects.txt)).
