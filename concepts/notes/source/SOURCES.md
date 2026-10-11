# Sources

Verbatim copies of the test pages new in this round, taken on 2026-10-10 at
the commits the [note survey](../survey/README.md) read (the table survey's
commits). Nothing in this directory is edited; every change lives in
`../sites/`. One test page was copied in the headings round and is used
from there.

| File | Repository | Path | Commit | License |
|------|------------|------|--------|---------|
| `cf-backup.html.md.erb` | [cloudfoundry/docs-bbr](https://github.com/cloudfoundry/docs-bbr) | `cf-backup.html.md.erb` | `51465950ce3a2196d66a9339086b94feed280c3e` | Apache-2.0 |
| `healthchecks.html.md.erb` | [cloudfoundry/docs-dev-guide](https://github.com/cloudfoundry/docs-dev-guide) | `deploy-apps/healthchecks.html.md.erb` | `9c8df63eb3823011e4e3aff9958c36e25d5190b7` | Apache-2.0 |
| `using-vol-services.html.md.erb` | cloudfoundry/docs-dev-guide | `services/using-vol-services.html.md.erb` | `9c8df63eb3823011e4e3aff9958c36e25d5190b7` | Apache-2.0 |
| `_using-vol-services.html.md.erb` | cloudfoundry/docs-dev-guide | `services/_using-vol-services.html.md.erb` | `9c8df63eb3823011e4e3aff9958c36e25d5190b7` | Apache-2.0 |
| `template_variables.yml` | [cloudfoundry/docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry) | `config/template_variables.yml` (excerpt) | `30dfa57692253a6ae1b3df0726444b1e32852c91` | Apache-2.0 |
| [`../../headings/source/routes-domains.html.md.erb`](../../headings/source/routes-domains.html.md.erb) | cloudfoundry/docs-dev-guide | `deploy-apps/routes-domains.html.md.erb` | see [headings SOURCES](../../headings/source/SOURCES.md) | Apache-2.0 |

Links to the files at those commits:
[cf-backup.html.md.erb](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/cf-backup.html.md.erb),
[healthchecks.html.md.erb](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/healthchecks.html.md.erb),
[using-vol-services.html.md.erb](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/using-vol-services.html.md.erb),
[_using-vol-services.html.md.erb](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/_using-vol-services.html.md.erb),
[template_variables.yml](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml).
Licenses:
[docs-bbr LICENSE](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/LICENSE),
[docs-dev-guide LICENSE](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/LICENSE),
[docs-book-cloudfoundry LICENSE](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/LICENSE).

## Notes

- **`using-vol-services` is a host page and a partial.** The page itself is
  front matter and `<%= partial 'using-vol-services' %>`; the content is in
  `_using-vol-services`. The sites convert one page made of the host's front
  matter and two parts of the partial: its opening (lines 1–8, which hold
  the note kept in a variable) and the "Create and use NFS volume services"
  section up to "Migrate nfs-legacy services to nfs" (lines 225–279). The
  outline check compares the page title and that section
  (`--section nfs --until migrate`). How partials are converted is the
  partials concept's question.
- **`routes-domains` is the headings round's excerpt**, its Domains section,
  and its converted pages are the headings round's native pages. Their
  notes were left as HTML in that round, so they are this round's
  passthrough pages as they are.
- **`cf-backup` and `healthchecks` are whole pages.**
- **Variables excerpt.** `template_variables.yml` keeps the
  `template_variables:` key and the variables the four pages use, in their
  original order: the headings round's five, plus `company_name`, `admin`,
  `app_healthcheck_timeout` and `external_vol_win_note`, the note held in a
  variable. The headings round's five have the same values at this commit
  as at the one that round copied.
- **Published pages.** [`../published/`](../published/) holds the three new
  pages as docs.cloudfoundry.org served them on 2026-10-10, saved with
  `curl`:
  [cf-backup](https://docs.cloudfoundry.org/bbr/cf-backup.html),
  [healthchecks](https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html),
  [using-vol-services](https://docs.cloudfoundry.org/devguide/services/using-vol-services.html).
  `routes-domains` is compared with the headings round's copy. The
  published pages are built from whatever commit the book used last, not
  from the commits above; their notes match the copied sources (the
  intent files list them).

## Verify

Every copy matches its upstream commit. Run from this directory, with the
repositories cloned next to `cf-docs-rfc-proposal` (`../../../..` is the
directory holding it). No output means every file matches.

```bash
R=../../../..
git -C $R/docs-bbr show 51465950ce3a2196d66a9339086b94feed280c3e:cf-backup.html.md.erb | diff - cf-backup.html.md.erb
git -C $R/docs-dev-guide show 9c8df63eb3823011e4e3aff9958c36e25d5190b7:deploy-apps/healthchecks.html.md.erb | diff - healthchecks.html.md.erb
git -C $R/docs-dev-guide show 9c8df63eb3823011e4e3aff9958c36e25d5190b7:services/using-vol-services.html.md.erb | diff - using-vol-services.html.md.erb
git -C $R/docs-dev-guide show 9c8df63eb3823011e4e3aff9958c36e25d5190b7:services/_using-vol-services.html.md.erb | diff - _using-vol-services.html.md.erb
git -C $R/docs-book-cloudfoundry show 30dfa57692253a6ae1b3df0726444b1e32852c91:config/template_variables.yml | grep -xF -f <(grep -v '^#' template_variables.yml) | diff - <(grep -v '^#' template_variables.yml)
```
