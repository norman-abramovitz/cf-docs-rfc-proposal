# Version survey

Status: draft, incomplete — covers what is known as of 2026-10-16.

This survey counts every version the book's pages write as text or in a
link, and sorts each into a category: a version that must stay as written,
one that should follow the release the docs describe, and versions that
are not release versions at all. It was done on 2026-10-16 to decide where
**version values** would be used and to choose the test pages of a
version-values round. The variables round
([variables survey](../../variables/survey/README.md)) surveyed the
variables the book defines; this survey looks at the versions it writes
as text.

Terms used below:

- **Version mention.** A version written in a page: a token such as
  `v1.2`, `v263`, `1.2.3` or `1.2.3-rc.1` in the text, or a link whose
  path names a version (`/releases/tag/v38.0.0`, `?v=0.6.1`,
  `/version/3.169.0/`) or a branch (`/blob/main/`).
- **Version value.** A value the build supplies in place of a version
  written by hand, such as the version of `capi-release` in the
  cf-deployment release the docs describe. The book has no such values
  today; its variables file holds versions as text
  ([`hash_routing_version`, L181](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L181)).
- **Fixed** and **floating.** A fixed version must not change when the
  docs move to a newer release ("Available in bosh-release v267+").
  A floating version should ("install cf CLI v8").

| File | What it is |
|---|---|
| [mentions.csv](mentions.csv) | One row per version mention (1,661 rows), each with a GitHub link at the surveyed commit: the token, the link, the rule that sorted it, its category, and its place and the elements around it as the variables survey records them |
| [sample.csv](sample.csv) | 80 mentions read by hand, with the category each was given and why (below, [Hand-read sample](#hand-read-sample)) |
| [survey.py](survey.py) | Finds the mentions and sorts them; writes `mentions.csv` |
| [sources.py](sources.py) | For the links of categories 3 and 4: where a build could take the version from |

## Scope

- **Repositories and files** as in the
  [variables survey](../../variables/survey/README.md#scope): the 15
  `docs-*` repositories at the same commits
  ([shas.txt](../../variables/survey/shas.txt)), the same file types, and
  the book's `config/template_variables.yml`. `docs-bosh` (bosh.io) and
  `docs-dotnet-core-tutorial` are counted apart in `site`.
- **Not counted:** IP addresses (709) and numbers with two parts and no
  name before them, such as `1.5` (566). A two-part number counts when a
  name or word comes before it: `Ubuntu 22.04`, `JDK 1.7`, `version 2.33`.
- **Text inside ERB tags** is not read (the variables survey counts
  those).

## Method

[survey.py](survey.py) finds each version token in the text and each
link, and gives each the first rule that applies. Places (`place`,
`table`, `note`, `list`, `html`) come from the variables survey's
`place_of` and `containers`, which `survey.py` loads from
[../../variables/survey/survey.py](../../variables/survey/survey.py)
rather than repeating them.

| Rule | Found in | What it matches | Category |
|---|---|---|---|
| `bound` | text, value | a limit in the same sentence: "or later", `v263+`, "available in", "introduced in", "requires", "since", "until", "before", "from v…", "between … and", a range `v26~v35.1.0`, "bump to" | 1 |
| `name-fact` | text | a version after "Ubuntu": the version names the Ubuntu release | 8 |
| `history-page` | text | a page in `archive/`, release notes, changelog | 1 |
| `code-command` | text | a code line that installs or fetches: `bosh upload-release`, `gem install`, `curl`, `wget`, `docker pull`, … | 2 |
| `docs-version-pin` | link | `/version/N/` (the CC API, UAA and CredHub references) | 3 |
| `release-tag` | link | `/releases/tag/`, `/tree/vN`, `/blob/vN`, `.git#vN` | 3 |
| `bosh-io-version` | link | bosh.io with `?v=` or `version=` | 3 |
| `download` | link | an archive or binary file with a version | 3 |
| `third-party-docs-version` | link | another project's docs at a version (vSphere 6.7, MySQL 5.7) | 3 |
| `branch-link` | link, value | GitHub `blob`, `tree`, `raw` or `edit` at `master`, `main` or `develop` | 4 |
| `code-other` | text | any other version in a code block | 6 |
| `not-release` | text | after TLS, HTTP, SAML, OSBAPI, cgroup, UUID…; `vN` next to API, endpoint, format, manifest, schema | 7 |
| `api-path`, `page-name`, `local-host`, `site-asset` | link | `/v3/apps`, `cli-v2.md`, `0.0.0.0:6868`, a pinned CDN script | 7 |
| `prose`, `value`, `link-other` | | none of the above | undecided |

The rules were written from the source, in passes: each pass, a sample of
each rule's rows was read and the rule changed where it was wrong. The
patterns are in `survey.py`.

## Categories and counts

Categories 1 to 5 were proposed on 2026-10-15; 6 and 7 came out of the
first pass over the source and were accepted on 2026-10-16. Category 8
came out of the hand-read sample and was accepted on 2026-10-16.

| # | Category | Fixed or floating | Mentions | Example |
|---|---|---|---|---|
| 1 | **Version bound or history**: a release where something starts, stops or happened | fixed | 491 | [bosh.io `cloud-config` L252](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/cloud-config.md#L252): "Available in bosh-release v267+" |
| 2 | **Current version** in prose or commands | floating | 1 by rule, more in the undecided rows | [bosh.io `cpi-api-v2-migration-guide` L100](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/cpi-api-v2-migration-guide.md#L100): `gem install bosh_cpi -v 2.5.0`; [`sidecars` L13](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/sidecars.html.md.erb#L13): "The latest supported cf CLI release is cf CLI v8" |
| 3 | **Version in a URL** | floating, unless the text is about that release | 189 | [`security` L128](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/security.html.md.erb#L128): `v3-apidocs.cloudfoundry.org/version/3.0.0/` |
| 4 | **Branch link** | floats today without anyone choosing it; should name the release | 292 | [`deploy-cf` L40](https://github.com/cloudfoundry/docs-deploying-cf/blob/1113cfaf3626931c653c91dc8d537d7f181d6762/cf-deployment/deploy-cf.html.md.erb#L40): `cf-deployment/blob/main/operations/windows2019-cell.yml` |
| 5 | **The docs' own version** | floating, from the build | 0 in text; 2 in ERB | the stacks pages print `v<%= vars.current_major_version %>`, `10-0` ([`stacks` L11](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/stacks.html.md.erb#L11)), a value left from a commercial book |
| 6 | **Captured output and sample data**: command output, dependency files, sample manifests | fixed; never a value | 179 | [`java-tips` L58](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/java-tips.html.md.erb#L58): staging output "Installing tomcat 10.1.60" |
| 7 | **Not a release version**: API, protocol and format versions, page names, hosts | not a version value | 157 | [`securing-traffic` L151](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/securing-traffic.html.md.erb#L151): "TLS v1.2" |
| 8 | **Fact tied to a name**: the version belongs to the name before it, not to the release the docs describe | fixed | 33 by rule, more in the undecided rows | [`stacks` L31](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/stacks.html.md.erb#L31): "`cflinuxfs4` (default), derived from Ubuntu 22.04 LTS" |
| | **Undecided by rule** | | 319 | |
| | **Total** | | 1,661 | |

By site: bosh.io holds 350 of the 491 in category 1 and 103 of the 189 in
category 3. The variables file holds 12 bounds, among them
`hash_routing_version` ("Available from cf-deployment v55.2.0, together
with cf CLI 8.10.0 and later", used 6 times), and 13 branch links. 21
mentions are in `archive/` folders.

## Hand-read sample

80 mentions were drawn at random (seed `20261016`) and read: 60 of the
rows the rules had left undecided, and 20 `code-other` rows to check that
rule. The draw was made before the last rule changes, from 404 undecided
rows; 17 of the 60 have since been sorted by a rule, all 17 as they were
read by hand.

| Pool | Read | 1 fixed | 2 current | 6 sample | 7 not a release | 8 fact tied to a name |
|---|---|---|---|---|---|---|
| still undecided | 43 | 10 | 7 | 7 | 18 | 1 |
| sorted by a later rule | 17 | 10 | 0 | 0 | 2 | 5 |
| `code-other` | 20 | | | 19 | 1 | |

What the reading shows:

- **Current versions are few, and look like names.** The seven are
  "cf CLI v8" four times, supported JDKs twice and one tooling README.
  "cf CLI v8" reads like a fixed name ("BOSH CLI v2" is one: v2 is the
  only BOSH CLI), but it becomes wrong when cf CLI v9 ships. No rule can
  tell the two apart; a writer can.
- **Fixed facts that are not bounds.** "cflinuxfs4, derived from Ubuntu
  22.04" and "the stemcell's system Python is 3.14" are fixed: the
  version belongs to the name before it. They are category 8. A rule
  finds those after "Ubuntu"; the others, such as the Python one, are
  left undecided.
- **Samples that pin a release.** 3 of the 20 `code-other` rows are
  manifest snippets with a release and its version
  (`credhub-release?v=0.6.1`). They are samples, but a reader may copy
  them, and a writer may want the current version there.

## Where a build could take the versions from

From [sources.py](sources.py), for the links of categories 3 and 4, with
cf-deployment's manifest at
[v60.10.0](https://github.com/cloudfoundry/cf-deployment/blob/6087d6187ff113882a0a3dd4cda3455cbef4d1e2/cf-deployment.yml)
(31 releases and one stemcell):

| Source | 3 version in a URL | 4 branch link |
|---|---|---|
| a release in `cf-deployment.yml` | 19 | 78 |
| the stemcell in `cf-deployment.yml` | 9 | |
| cf-deployment's own tag | 1 | 49 |
| the CC API, UAA and CredHub versions their releases ship | 29 | |
| the OSBAPI spec version Cloud Controller supports | 24 | 1 |
| another CF repository (BOSH, CPIs, `bosh-deployment`, tools) | 63 | 136 |
| outside the CF organizations (vSphere and MySQL docs, downloads) | 44 | 26 |
| a docs repository | | 3 |

About a third of these links could take their version from one file,
cf-deployment's manifest at the release the docs describe. BOSH's links
need a second source (`bosh-deployment` or the BOSH release). The links
outside the CF organizations have no source a build can read.

The CC API reference is the clearest case of drift: pages link to ten
different versions of it, from 3.0.0 to 3.169.0.

## Not yet done

- Most of the 319 undecided rows are not sorted; the sample above
  describes them.
- `component` (the name before a token) is a guess from the text and is
  not checked.
- Category 3 links were not checked to see if they still resolve, and
  category 4 links were not checked against the tags.
- The values the versions would come from were not built.

## How to rerun

Fetch the repositories as in the
[variables survey](../../variables/survey/README.md#how-to-rerun), into
`repos/`, then:

```sh
python3 -I SURVEY/survey.py repos VARS/shas.txt mentions.csv
cmp mentions.csv SURVEY/mentions.csv
gh api 'repos/cloudfoundry/cf-deployment/contents/cf-deployment.yml?ref=v60.10.0' \
  -H 'Accept: application/vnd.github.raw' > cf-deployment.yml
python3 -I SURVEY/sources.py SURVEY/mentions.csv cf-deployment.yml
```

`SURVEY` is this folder and `VARS` is `concepts/variables/survey`.
`survey.py` loads the variables survey's `survey.py` from beside this
folder, so the two folders must stay side by side. The scripts read files
only; they run nothing from the clones.
