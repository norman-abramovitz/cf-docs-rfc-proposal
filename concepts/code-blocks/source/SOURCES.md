# Sources

Verbatim copies of the test pages new in this round, taken on 2026-10-11 at
the commits the [code-block survey](../survey/README.md) read (the
partials survey's commits). Nothing in this directory is edited; every
change lives in `../sites/`. Two pages were copied in earlier rounds and
are used from there.

| File | Repository | Path | Commit | License |
|------|------------|------|--------|---------|
| `gsg-grails.html.md.erb` | [cloudfoundry/docs-buildpacks](https://github.com/cloudfoundry/docs-buildpacks) | `java/getting-started-deploying-apps/gsg-grails.html.md.erb` | `239e5c8676200914c4d386970f9989e46de9e969` | Apache-2.0 |
| `nginx-index.html.md.erb` | cloudfoundry/docs-buildpacks | `nginx/index.html.md.erb` | `239e5c8676200914c4d386970f9989e46de9e969` | Apache-2.0 |
| `backup.html.md.erb` | [cloudfoundry/docs-bbr](https://github.com/cloudfoundry/docs-bbr) | `backup.html.md.erb` | `51465950ce3a2196d66a9339086b94feed280c3e` | Apache-2.0 |
| `multiple-processes.html.md.erb` | [cloudfoundry/docs-dev-guide](https://github.com/cloudfoundry/docs-dev-guide) | `multiple-processes.html.md.erb` | `9c8df63eb3823011e4e3aff9958c36e25d5190b7` | Apache-2.0 |
| `template_variables.yml` | [cloudfoundry/docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry) | `config/template_variables.yml` (excerpt: the three keys the test pages use inside code blocks) | `30dfa57692253a6ae1b3df0726444b1e32852c91` | Apache-2.0 |
| [`../../headings/source/routes-domains.html.md.erb`](../../headings/source/routes-domains.html.md.erb) | cloudfoundry/docs-dev-guide | `deploy-apps/routes-domains.html.md.erb` | see [headings SOURCES](../../headings/source/SOURCES.md) | Apache-2.0 |
| [`../../tables/source/troubleshooting_slow_requests.html.md.erb`](../../tables/source/troubleshooting_slow_requests.html.md.erb) | cloudfoundry/docs-cf-admin | `troubleshooting_slow_requests.html.md.erb` | see [tables SOURCES](../../tables/source/SOURCES.md) | Apache-2.0 |

`nginx-index.html.md.erb` is renamed from `index.html.md.erb` so that its
name says which page it is.

Links to the files at those commits:
[gsg-grails](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb),
[nginx/index](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/nginx/index.html.md.erb),
[backup](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb),
[multiple-processes](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/multiple-processes.html.md.erb),
[template_variables.yml](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml)
(L55, L224, L339).
Licenses:
[docs-buildpacks LICENSE](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/LICENSE),
[docs-bbr LICENSE](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/LICENSE),
[docs-dev-guide LICENSE](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/LICENSE),
[docs-book-cloudfoundry LICENSE](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/LICENSE).

## Notes

**Excerpts.** The sites convert one section of four pages and two whole
pages; `backup` gives two sections, built as two pages:

| Test page | Source | Lines |
|-----------|--------|-------|
| `routes-domains` | the Create a route section | [L106-L265](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L106-L265) |
| `troubleshooting_slow_requests` | the whole page | [all 481 lines](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting_slow_requests.html.md.erb) |
| `gsg-grails` | Step 5 | [L109-L186](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L109-L186) |
| `backup` | Connect to your jumpbox | [L18-L111](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L18-L111) |
| `backup-clean` | Clean up after a failed backup | [L350-L400](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L350-L400) |
| `nginx` | Create the nginx.conf file, with its subsections | [L39-L229](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/nginx/index.html.md.erb#L39-L229) |
| `multiple-processes` | the whole page | [all 129 lines](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/multiple-processes.html.md.erb) |

**Variables outside code blocks** follow the variables round's accepted
conventions: product names (`app_runtime_abbr`, `app_runtime_first`,
`recommended_by`) are written as "Cloud Foundry"; references to names
with no value or no key (`dev_console_1`, `dev_console_5`,
`bosh_cli_link`) are removed. The three domain names stay variables,
in prose and in code.
