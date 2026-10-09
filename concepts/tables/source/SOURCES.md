# Sources

Verbatim copies of the test pages, taken from each repository's `master`
branch on 2026-10-08. Nothing in this directory is edited; every change lives
in `../sites/` and `../probes/`.

| File | Repository | Path | Commit | License |
|------|------------|------|--------|---------|
| `_oss_scale_table.html.md.erb` | [cloudfoundry/docs-cloudfoundry-concepts](https://github.com/cloudfoundry/docs-cloudfoundry-concepts) | `_oss_scale_table.html.md.erb` | `4ac2fb19a0a44534a8469de100af7dd91706e9b7` | Apache-2.0 |
| `metadata.html.md.erb` | [cloudfoundry/docs-cf-admin](https://github.com/cloudfoundry/docs-cf-admin) | `metadata.html.md.erb` | `19b0c9c5fabd93b33ba184c6eb541f3cafd3a1b9` | Apache-2.0 |
| `troubleshooting_slow_requests.html.md.erb` | [cloudfoundry/docs-cf-admin](https://github.com/cloudfoundry/docs-cf-admin) | `troubleshooting_slow_requests.html.md.erb` | `19b0c9c5fabd93b33ba184c6eb541f3cafd3a1b9` | Apache-2.0 |
| `uaa-concepts.html.md.erb` | [cloudfoundry/docs-uaa](https://github.com/cloudfoundry/docs-uaa) | `uaa-concepts.html.md.erb` | `0f43fb93af5aa378f940dd19fec7ee54c2c01ccd` | Apache-2.0 (stated in the repository's `NOTICE` file; no `LICENSE` file) |
| `credential-types.html.md.erb` | [cloudfoundry/docs-credhub](https://github.com/cloudfoundry/docs-credhub) | `credential-types.html.md.erb` | `e074f74717422c0082ca24a2a6da7fbbf8114999` | Apache-2.0 |
| `uaa-performance.html.md.erb` | [cloudfoundry/docs-running-cf](https://github.com/cloudfoundry/docs-running-cf) | `uaa-performance.html.md.erb` | `956acc86445d2f3cb29f031294f86f37f515b471` | Apache-2.0 |
| `images/request_lifecycle.png` | [cloudfoundry/docs-cf-admin](https://github.com/cloudfoundry/docs-cf-admin) | `images/request_lifecycle.png` | `45ab3458ddb3e06bd85f948c88c1f7675ee0ecba` | Apache-2.0 |
| `images/client-creds-threads-{1,2,4}.png`, `images/client-creds-throughput-{1,2,4}.png` | [cloudfoundry/docs-running-cf](https://github.com/cloudfoundry/docs-running-cf) | same paths | `54bf79ad1a5f83e4f9c0f68d13ed70c1f7de1e95` | Apache-2.0 |
| `template_variables.yml` | [cloudfoundry/docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry) | `config/template_variables.yml` (excerpt) | `0f2d16e419498c84f304da96f3afc8fd9c689975` | Apache-2.0 |

## Notes

- **The partial and its host.** `_oss_scale_table` is not a page on its own.
  `high-availability.html.md.erb` in docs-cloudfoundry-concepts includes it at
  line 102 with `<%= partial 'oss_scale_table' %>`. The book also maps
  `scale_table: "oss_scale_table"` as a variable. Each site in this round
  includes the partial from a small host page instead of copying the whole
  host page.
- **Image.** `troubleshooting_slow_requests` shows one image, copied to
  `images/` so pages can keep its relative path `./images/request_lifecycle.png`.
- **Variables excerpt.** `template_variables.yml` keeps only the
  `template_variables:` key and the variables the test pages use, in their
  original order, plus `route_services` (a value that is HTML, used to check
  that a site does not escape HTML-valued variables) and `scale_table`. The
  full file has about 290 variables.
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
git -C $R/docs-book-cloudfoundry show 0f2d16e419498c84f304da96f3afc8fd9c689975:config/template_variables.yml | grep -xF -f <(grep -v '^#' template_variables.yml) | diff - <(grep -v '^#' template_variables.yml)
```

The last line checks that every line of the excerpt (apart from the comment
header) appears verbatim, in order, in the upstream file.
