# Sources

Verbatim copies of the test pages, taken from each repository's `master`
branch on 2026-10-08. Nothing in this directory is edited; every change lives
in `../sites/` and `../probes/`.

| File | Repository | Path | Commit | License |
|------|------------|------|--------|---------|
| `_oss_scale_table.html.md.erb` | [cloudfoundry/docs-cloudfoundry-concepts](https://github.com/cloudfoundry/docs-cloudfoundry-concepts) | `_oss_scale_table.html.md.erb` | `4ac2fb19a0a44534a8469de100af7dd91706e9b7` | Apache-2.0 |
| `_oss_roles_table.html.md.erb` | [cloudfoundry/docs-cloudfoundry-concepts](https://github.com/cloudfoundry/docs-cloudfoundry-concepts) | `_oss_roles_table.html.md.erb` | `97e0d0b25f059c06edd25e30355d26eb93dc560a` | Apache-2.0 |
| `metadata.html.md.erb` | [cloudfoundry/docs-cf-admin](https://github.com/cloudfoundry/docs-cf-admin) | `metadata.html.md.erb` | `19b0c9c5fabd93b33ba184c6eb541f3cafd3a1b9` | Apache-2.0 |
| `troubleshooting_slow_requests.html.md.erb` | [cloudfoundry/docs-cf-admin](https://github.com/cloudfoundry/docs-cf-admin) | `troubleshooting_slow_requests.html.md.erb` | `19b0c9c5fabd93b33ba184c6eb541f3cafd3a1b9` | Apache-2.0 |
| `uaa-concepts.html.md.erb` | [cloudfoundry/docs-uaa](https://github.com/cloudfoundry/docs-uaa) | `uaa-concepts.html.md.erb` | `0f43fb93af5aa378f940dd19fec7ee54c2c01ccd` | Apache-2.0 (stated in the repository's `NOTICE` file; no `LICENSE` file) |
| `credential-types.html.md.erb` | [cloudfoundry/docs-credhub](https://github.com/cloudfoundry/docs-credhub) | `credential-types.html.md.erb` | `e074f74717422c0082ca24a2a6da7fbbf8114999` | Apache-2.0 |
| `uaa-performance.html.md.erb` | [cloudfoundry/docs-running-cf](https://github.com/cloudfoundry/docs-running-cf) | `uaa-performance.html.md.erb` | `956acc86445d2f3cb29f031294f86f37f515b471` | Apache-2.0 |
| `images/request_lifecycle.png` | [cloudfoundry/docs-cf-admin](https://github.com/cloudfoundry/docs-cf-admin) | `images/request_lifecycle.png` | `45ab3458ddb3e06bd85f948c88c1f7675ee0ecba` | Apache-2.0 |
| `images/client-creds-threads-{1,2,4}.png`, `images/client-creds-throughput-{1,2,4}.png` | [cloudfoundry/docs-running-cf](https://github.com/cloudfoundry/docs-running-cf) | same paths | `54bf79ad1a5f83e4f9c0f68d13ed70c1f7de1e95` | Apache-2.0 |
| `template_variables.yml` | [cloudfoundry/docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry) | `config/template_variables.yml` (excerpt) | `0f2d16e419498c84f304da96f3afc8fd9c689975` | Apache-2.0 |
| `bosh-networks.md` | [cloudfoundry/docs-bosh](https://github.com/cloudfoundry/docs-bosh) | `content/networks.md` | `20a41223a7ba87700424634c42e94a22a669b45e` | Apache-2.0 |
| `bosh-cpi-api-v2.md` | [cloudfoundry/docs-bosh](https://github.com/cloudfoundry/docs-bosh) | `content/cpi-api-v2.md` | `20a41223a7ba87700424634c42e94a22a669b45e` | Apache-2.0 |
| `bosh-director-tasks.md` | [cloudfoundry/docs-bosh](https://github.com/cloudfoundry/docs-bosh) | `content/director-tasks.md` | `20a41223a7ba87700424634c42e94a22a669b45e` | Apache-2.0 |
| `bpm-config.md` | [cloudfoundry/bpm-release](https://github.com/cloudfoundry/bpm-release) | `docs/config.md` | `6b9988a0271aefc2e0cd6444ad4f8d562f46b06e` | Apache-2.0 |

## Notes

- **The partial and its host.** `_oss_scale_table` is not a page on its own.
  `high-availability.html.md.erb` in docs-cloudfoundry-concepts includes it at
  line 108 with `<%= partial 'oss_scale_table' %>`. The book also maps
  `scale_table: "oss_scale_table"` as a variable. Each site in this round
  includes the partial from a small host page instead of copying the whole
  host page.
- **The roles table, added 2026-10-12** as the seventh test page: a wide
  table, 12 columns, wider than the content column. `_oss_roles_table` is
  also a partial; `roles.html.md.erb` includes it at line 115 with
  `<%= partial 'oss_roles_table' %>`, and each site shows it in a host page,
  `roles-table-host`, as for the scale table. Copied from the clone at that
  commit on 2026-10-12.
- **Image.** `troubleshooting_slow_requests` shows one image, copied to
  `images/` so pages can keep its relative path `./images/request_lifecycle.png`.
- **Variables excerpt.** `template_variables.yml` keeps only the
  `template_variables:` key and the variables the test pages use, in their
  original order, plus `route_services` (a value that is HTML, used to check
  that a site does not escape HTML-valued variables) and `scale_table`. The
  full file has 272 variables at that commit.
- **Variables used but not defined.** `metadata.html.md.erb` uses
  `vars.metadata_ref`, and `troubleshooting_slow_requests.html.md.erb` uses
  `vars.bosh_cli_link` (three times). Neither appears in the book's
  `template_variables.yml`, so the published pages render them as empty text.
  A converted page must render them as empty too, not as an error or as
  literal text.

- **The media-grid page.** `uaa-performance` was added after the round, as
  the example for a second table style (`table-media`). It has twelve tables
  of chart thumbnails; the sites convert only its first section (the
  "Client credentials grant type" heading, the endpoint line and table 1)
  and its six images, the way the scale table is shown in a small host page.
  The page loads jQuery and a lightbox script (fancybox) from CDNs; the
  converted pages leave them out, so a thumbnail link opens the full image.
  Copied on 2026-10-09, a day after the other pages.

- **The bosh.io pages, added 2026-10-12** as test input for the candidate
  hints (row group, row emphasis, table notes) and the `table-output` and
  `table-compact` styles. They are Markdown pages built by bosh.io with
  MkDocs and Material for MkDocs, not ERB, and use no variables. Each file
  is the whole upstream page, copied with `git show` at the commit in the
  table (docs-bosh `master` on 2026-10-10, the commit the
  [survey](../survey/README.md#boshio) read); the prefix `bosh-` or `bpm-`
  keeps the names apart from the other test pages. As for `uaa-performance`,
  the sites convert only the section that holds the tables:
  - `bosh-networks.md`: "CPI Limitations", [lines 485–521](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/networks.md#L485-L521),
    survey tables T3 and T4 (table notes; row groups; a `table-compact`
    candidate).
  - `bosh-cpi-api-v2.md`: "Reference Table", [lines 46–61](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/cpi-api-v2.md#L46-L61),
    survey table T14 (row emphasis; a table note; the
    `*full agent settings**` defect; a `table-compact` candidate).
  - `bosh-director-tasks.md`: "Currently active tasks", [lines 22–37](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/director-tasks.md#L22-L37),
    survey table T18 (`table-output`).
  - `bpm-config.md`: "Job Configuration", [lines 24–89](https://github.com/cloudfoundry/bpm-release/blob/6b9988a0271aefc2e0cd6444ad4f8d562f46b06e/docs/config.md#L24-L89),
    the six schema tables B1–B6, B2 (`process`) foremost (`wrap: avoid`
    on identifiers, which the published page breaks). The commit is the one
    docs-bosh pins as its `external/bpm-release` submodule at `20a4122`,
    not bpm-release's `master`, which has moved on.

## Verify

Every copy matches its upstream commit. Run from this directory, with the
repositories cloned next to this one (`../../../..` is the directory holding
`cf-docs-rfc-proposal`). No output means every file matches.

```bash
R=../../../..
git -C $R/docs-cloudfoundry-concepts show 4ac2fb19a0a44534a8469de100af7dd91706e9b7:_oss_scale_table.html.md.erb | diff - _oss_scale_table.html.md.erb
git -C $R/docs-cf-admin show 19b0c9c5fabd93b33ba184c6eb541f3cafd3a1b9:metadata.html.md.erb | diff - metadata.html.md.erb
git -C $R/docs-cf-admin show 19b0c9c5fabd93b33ba184c6eb541f3cafd3a1b9:troubleshooting_slow_requests.html.md.erb | diff - troubleshooting_slow_requests.html.md.erb
git -C $R/docs-uaa show 0f43fb93af5aa378f940dd19fec7ee54c2c01ccd:uaa-concepts.html.md.erb | diff - uaa-concepts.html.md.erb
git -C $R/docs-credhub show e074f74717422c0082ca24a2a6da7fbbf8114999:credential-types.html.md.erb | diff - credential-types.html.md.erb
git -C $R/docs-cf-admin show 45ab3458ddb3e06bd85f948c88c1f7675ee0ecba:images/request_lifecycle.png | cmp - images/request_lifecycle.png
git -C $R/docs-running-cf show 956acc86445d2f3cb29f031294f86f37f515b471:uaa-performance.html.md.erb | diff - uaa-performance.html.md.erb
for f in images/client-creds-{threads,throughput}-{1,2,4}.png; do git -C $R/docs-running-cf show 54bf79ad1a5f83e4f9c0f68d13ed70c1f7de1e95:$f | cmp - $f; done
for f in networks cpi-api-v2 director-tasks; do git -C $R/docs-bosh show 20a41223a7ba87700424634c42e94a22a669b45e:content/$f.md | diff - bosh-$f.md; done
git -C $R/bpm-release show 6b9988a0271aefc2e0cd6444ad4f8d562f46b06e:docs/config.md | diff - bpm-config.md
git -C $R/docs-book-cloudfoundry show 0f2d16e419498c84f304da96f3afc8fd9c689975:config/template_variables.yml | grep -xF -f <(grep -v '^#' template_variables.yml) | diff - <(grep -v '^#' template_variables.yml)
```

The last line checks that every line of the excerpt (apart from the comment
header) appears verbatim, in order, in the upstream file.
