# Sources

Verbatim copies of the test pages new in this round, taken on 2026-10-11 at
the commits the [variable survey](../survey/README.md) read (the notes
survey's commits). Nothing in this directory is edited; every change lives
in `../sites/`. One test page was copied in the headings round and is used
from there.

| File | Repository | Path | Commit | License |
|------|------------|------|--------|---------|
| `app-ssh-overview.html.md.erb` | [cloudfoundry/docs-dev-guide](https://github.com/cloudfoundry/docs-dev-guide) | `deploy-apps/app-ssh-overview.html.md.erb` | `9c8df63eb3823011e4e3aff9958c36e25d5190b7` | Apache-2.0 |
| `images/ssh-app-access.png` | cloudfoundry/docs-dev-guide | `images/ssh-app-access.png` | `9c8df63eb3823011e4e3aff9958c36e25d5190b7` | Apache-2.0 |
| `troubleshooting-router-error-responses.html.md.erb` | [cloudfoundry/docs-cf-admin](https://github.com/cloudfoundry/docs-cf-admin) | `troubleshooting-router-error-responses.html.md.erb` | `13826fa7d93eee66902c4a2187a96b884137b58a` | Apache-2.0 |
| `container-security.html.md.erb` | [cloudfoundry/docs-cloudfoundry-concepts](https://github.com/cloudfoundry/docs-cloudfoundry-concepts) | `container-security.html.md.erb` | `97e0d0b25f059c06edd25e30355d26eb93dc560a` | Apache-2.0 |
| `all_metrics.html.md.erb` | [cloudfoundry/docs-running-cf](https://github.com/cloudfoundry/docs-running-cf) | `all_metrics.html.md.erb` | `956acc86445d2f3cb29f031294f86f37f515b471` | Apache-2.0 |
| `template_variables.yml` | [cloudfoundry/docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry) | `config/template_variables.yml` (the whole file) | `30dfa57692253a6ae1b3df0726444b1e32852c91` | Apache-2.0 |
| [`../../headings/source/routes-domains.html.md.erb`](../../headings/source/routes-domains.html.md.erb) | cloudfoundry/docs-dev-guide | `deploy-apps/routes-domains.html.md.erb` | see [headings SOURCES](../../headings/source/SOURCES.md) | Apache-2.0 |

Links to the files at those commits:
[app-ssh-overview.html.md.erb](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/app-ssh-overview.html.md.erb),
[ssh-app-access.png](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/images/ssh-app-access.png),
[troubleshooting-router-error-responses.html.md.erb](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb),
[container-security.html.md.erb](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/container-security.html.md.erb),
[all_metrics.html.md.erb](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/all_metrics.html.md.erb),
[template_variables.yml](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml).
Licenses:
[docs-dev-guide](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/LICENSE),
[docs-cf-admin](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/LICENSE),
[docs-cloudfoundry-concepts](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/LICENSE),
[docs-running-cf](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/LICENSE),
[docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/LICENSE).

## Notes

- **`app-ssh-overview` is a whole page**, with its one image, copied so
  each site can show it.
- **Three pages are converted in part.** Every heading is kept, so the
  outline check compares whole pages, but only some sections keep their
  bodies; the others are empty in every site:
  - `troubleshooting-router-error-responses`: the opening (lines 7–8),
    "General debugging steps" (lines 25–40), "Levels" with its table cut
    to the header row and the `fatal` row (lines 44–62), and "Gorouter
    error classification table" with its table cut to the header row and
    the last row (lines 302–321 and 381–391).
  - `container-security`: the opening (lines 6–17), the introduction of
    "Inbound and outbound traffic" (lines 149–150), "Network traffic rules"
    (lines 177–183) and the list of "Container security" (lines 187–193).
  - `all_metrics`: everything but the eight lines that include the metric
    tables as partials (`<%= partial './metrics/cloud_controller' %>` and
    seven more), which belong to the partials round.
- **`routes-domains` is the headings round's excerpt**, its Domains
  section, as the notes round converted it: headings and notes in each
  tool's own syntax. Its variables are this round's.
- **The variables file is copied whole**, so that each site reads every
  key, as the book does, and the checks can name every variable.
- **Published pages.** [`../published/`](../published/) holds the new pages
  as docs.cloudfoundry.org served them on 2026-10-11, saved with `curl`:
  [app-ssh-overview](https://docs.cloudfoundry.org/devguide/deploy-apps/app-ssh-overview.html),
  [troubleshooting-router-error-responses](https://docs.cloudfoundry.org/adminguide/troubleshooting-router-error-responses.html),
  [container-security](https://docs.cloudfoundry.org/concepts/container-security.html),
  [all_metrics](https://docs.cloudfoundry.org/running/all_metrics.html),
  and two pages the survey cites,
  [configure-lb-healthcheck](https://docs.cloudfoundry.org/adminguide/configure-lb-healthcheck.html)
  and [stacks](https://docs.cloudfoundry.org/devguide/deploy-apps/stacks.html).
  `routes-domains` is compared with the headings round's copy. The
  published pages are built from whatever commit the book used last, not
  from the commits above; their variables' text matches the copied
  sources (the intent files list it).

## Verify

Every copy matches its upstream commit. Run from this directory, with the
repositories cloned next to `cf-docs-rfc-proposal` (`../../../..` is the
directory holding it). No output means every file matches.

```bash
R=../../../..
git -C $R/docs-dev-guide show 9c8df63eb3823011e4e3aff9958c36e25d5190b7:deploy-apps/app-ssh-overview.html.md.erb | diff - app-ssh-overview.html.md.erb
git -C $R/docs-dev-guide show 9c8df63eb3823011e4e3aff9958c36e25d5190b7:images/ssh-app-access.png | cmp - images/ssh-app-access.png
git -C $R/docs-cf-admin show 13826fa7d93eee66902c4a2187a96b884137b58a:troubleshooting-router-error-responses.html.md.erb | diff - troubleshooting-router-error-responses.html.md.erb
git -C $R/docs-cloudfoundry-concepts show 97e0d0b25f059c06edd25e30355d26eb93dc560a:container-security.html.md.erb | diff - container-security.html.md.erb
git -C $R/docs-running-cf show 956acc86445d2f3cb29f031294f86f37f515b471:all_metrics.html.md.erb | diff - all_metrics.html.md.erb
git -C $R/docs-book-cloudfoundry show 30dfa57692253a6ae1b3df0726444b1e32852c91:config/template_variables.yml | diff - template_variables.yml
```
