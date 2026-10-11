# Sources

Verbatim copies of the test pages new in this round, taken on 2026-10-10 at
the commits the [table style survey](../../tables/survey/README.md) used.
Nothing in this directory is edited; every change lives in `../sites/`. Two
test pages were already copied for the tables round and are used from
there.

| File | Repository | Path | Commit | License |
|------|------------|------|--------|---------|
| `access-control.html.md.erb` | [cloudfoundry/docs-services](https://github.com/cloudfoundry/docs-services) | `access-control.html.md.erb` | `ccb0036407e4c2eabbb61a3b3de008f821f41c5b` | Apache-2.0 |
| `routes-domains.html.md.erb` | [cloudfoundry/docs-dev-guide](https://github.com/cloudfoundry/docs-dev-guide) | `deploy-apps/routes-domains.html.md.erb` | `9c8df63eb3823011e4e3aff9958c36e25d5190b7` | Apache-2.0 |
| `template_variables.yml` | [cloudfoundry/docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry) | `config/template_variables.yml` (excerpt) | `0f2d16e419498c84f304da96f3afc8fd9c689975` | Apache-2.0 |
| [`../../tables/source/metadata.html.md.erb`](../../tables/source/metadata.html.md.erb) | cloudfoundry/docs-cf-admin | `metadata.html.md.erb` | see [tables SOURCES](../../tables/source/SOURCES.md) | Apache-2.0 |
| [`../../tables/source/troubleshooting_slow_requests.html.md.erb`](../../tables/source/troubleshooting_slow_requests.html.md.erb) | cloudfoundry/docs-cf-admin | `troubleshooting_slow_requests.html.md.erb` | see [tables SOURCES](../../tables/source/SOURCES.md) | Apache-2.0 |

Links to the pages at those commits:
[access-control.html.md.erb](https://github.com/cloudfoundry/docs-services/blob/ccb0036407e4c2eabbb61a3b3de008f821f41c5b/access-control.html.md.erb),
[routes-domains.html.md.erb](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb),
[template_variables.yml](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/0f2d16e419498c84f304da96f3afc8fd9c689975/config/template_variables.yml).
Licenses: [docs-services LICENSE](https://github.com/cloudfoundry/docs-services/blob/ccb0036407e4c2eabbb61a3b3de008f821f41c5b/LICENSE),
[docs-dev-guide LICENSE](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/LICENSE).

## Notes

- **`routes-domains` is used as an excerpt.** The page has 42 headings
  over 962 lines. The sites convert only its front matter and its
  "Domains" section (lines 688–962, the end of the file): 17 headings that
  hold every case the page has (HTML `<h4>` tags next to Markdown `####`
  headings, and the page's only `#####` headings). The outline check
  compares only that section (`--section domains`), the way the tables
  round showed one section of `uaa-performance`.
- **Variables excerpt.** `template_variables.yml` keeps the
  `template_variables:` key and the variables the four pages use that the
  book defines, in their original order. It replaces the tables round's
  excerpt for this round; the two share `app_runtime_first` and
  `app_runtime_abbr`.
- **Variables used but not defined.** The excerpt of `routes-domains` uses
  `vars.domains_on_hosted` and `vars.dns_warning`; neither appears in the
  book's `template_variables.yml` at that commit, so the published page
  renders them as empty text, and so must a converted page. (The tables
  round recorded the same for `metadata_ref` and `bosh_cli_link`.)
- **Published pages.** [`../published/`](../published/) holds the four
  pages as docs.cloudfoundry.org served them on 2026-10-10, saved with
  `curl`, for the outline check to compare against:
  [metadata](https://docs.cloudfoundry.org/adminguide/metadata.html),
  [troubleshooting_slow_requests](https://docs.cloudfoundry.org/adminguide/troubleshooting_slow_requests.html),
  [access-control](https://docs.cloudfoundry.org/services/access-control.html),
  [routes-domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html).
  The published pages are built from whatever commit the book used last,
  not from the commits above; their heading trees match the copied sources
  ([results/published-outlines.txt](../results/published-outlines.txt)).

## Verify

Every copy matches its upstream commit. Run from this directory, with the
repositories cloned next to `cf-docs-rfc-proposal` (`../../../..` is the
directory holding it). No output means every file matches.

```bash
R=../../../..
git -C $R/docs-services show ccb0036407e4c2eabbb61a3b3de008f821f41c5b:access-control.html.md.erb | diff - access-control.html.md.erb
git -C $R/docs-dev-guide show 9c8df63eb3823011e4e3aff9958c36e25d5190b7:deploy-apps/routes-domains.html.md.erb | diff - routes-domains.html.md.erb
git -C $R/docs-book-cloudfoundry show 0f2d16e419498c84f304da96f3afc8fd9c689975:config/template_variables.yml | grep -xF -f <(grep -v '^#' template_variables.yml) | diff - <(grep -v '^#' template_variables.yml)
```
