# Links already broken today

Status: draft, incomplete — covers what is known as of 2026-10-10. Updated
2026-10-11 with the links the [cross-repository links survey](#found-by-the-cross-repository-links-survey-2026-10-11)
found across the book, and the redirect rules whose target is gone.
Updated 2026-10-12 with [one anchor used four times](#one-anchor-used-four-times-uaa-performance-2026-10-12)
and [one id on two tables](#one-id-on-two-tables-roles-2026-10-12).

Links to the four test pages of the Headings round that point at a heading
anchor which is not on today's published page. They are broken before any
migration, so keeping ids during conversion cannot repair them; each needs
its link fixed at the source, or a redirect or added anchor
([R-16](../../requirements/README.md#r-16) old URLs keep working).
Decision (Docs WG lead, 2026-10-10): they are listed here for fixing.

Searched on 2026-10-10 against the pages as served that day
([published/](published/)); every `id=` and `name=` attribute on each
page, in either quote style, counts as present.

What was searched:

- **All 17 `cloudfoundry/docs-*` repositories**, shallow clones of the
  default branch on 2026-10-10, for absolute and relative links to the
  four pages with a fragment.
- **The published pages themselves**, for in-page `href="#…"` links.
- **GitHub code search** (default branches only), 17 queries: the four
  page paths with and without `docs.cloudfoundry.org/`, the two old
  paths that `docs-book-cloudfoundry/redirects.rb` sends to
  `routes-domains` (`deploy-apps/domains-routes.html`,
  `adminguide/manage-domains-routes.html`), and each known broken
  fragment on its own. 364 files came back; each was fetched at its
  repository's default-branch head and scanned.
- **Full clones** of the seven repositories with broken links, to make
  their counts complete rather than search-limited.

Code search sees default branches only, mostly skips forks and does
not index large files, so every count outside the clones is a lower
bound. Pinned links use the default-branch head on 2026-10-10. No
source repository is archived.

Causes, with the change that broke each link, are from the history of
`docs-dev-guide`, `docs-services` and `docs-cf-admin`.

## metadata

Page: <https://docs.cloudfoundry.org/adminguide/metadata.html>

`#-view-metadata-for-an-object` is the id the site generated for the
heading "View Metadata for an Object", whose own id was `view`. The
heading became "View metadata for a resource" in August 2019
([docs-cf-admin history](https://github.com/cloudfoundry/docs-cf-admin/commits/master/metadata.html.md.erb)),
and today it appears twice, as `view-cli` (cf CLI) and `view` (API).
The old heading was the API one, so the intended id is `view`. Every
link's text reads "Add as described here" about labels and annotations,
so `add-cli` or `add` may suit the reader better.

Each repository has two hand-written lines; the other files are
generated from them, so fixing the two source lines and regenerating
fixes the rest.

| Fragment | Source (repo, linked file:line pinned) | Archived? | Cause | Intended id |
|----------|----------------------------------------|-----------|-------|-------------|
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `cloudfoundry/provider/utils.go` [L52](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/cloudfoundry/provider/utils.go#L52), [L63](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/cloudfoundry/provider/utils.go#L63) | no | Id generated from older heading text; hand-written source | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/data-sources/buildpacks.md` [L45](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/data-sources/buildpacks.md#L45), [L47](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/data-sources/buildpacks.md#L47) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/data-sources/service_broker.md` [L33](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/data-sources/service_broker.md#L33), [L34](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/data-sources/service_broker.md#L34) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/data-sources/service_brokers.md` [L45](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/data-sources/service_brokers.md#L45), [L46](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/data-sources/service_brokers.md#L46) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/data-sources/service_route_binding.md` [L33](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/data-sources/service_route_binding.md#L33), [L34](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/data-sources/service_route_binding.md#L34) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/data-sources/service_route_bindings.md` [L41](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/data-sources/service_route_bindings.md#L41), [L42](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/data-sources/service_route_bindings.md#L42) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/app.md` [L138](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/app.md#L138), [L153](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/app.md#L153) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/buildpack.md` [L35](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/buildpack.md#L35), [L37](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/buildpack.md#L37) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/domain.md` [L31](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/domain.md#L31), [L33](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/domain.md#L33) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/isolation_segment.md` [L30](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/isolation_segment.md#L30), [L31](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/isolation_segment.md#L31) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/org.md` [L41](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/org.md#L41), [L42](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/org.md#L42) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/route.md` [L45](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/route.md#L45), [L48](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/route.md#L48) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/service_broker.md` [L35](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/service_broker.md#L35), [L36](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/service_broker.md#L36) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/service_credential_binding.md` [L45](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/service_credential_binding.md#L45), [L47](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/service_credential_binding.md#L47) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/service_instance.md` [L112](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/service_instance.md#L112), [L114](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/service_instance.md#L114) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/service_route_binding.md` [L35](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/service_route_binding.md#L35), [L36](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/service_route_binding.md#L36) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/space.md` [L34](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/space.md#L34), [L36](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/space.md#L36) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/user.md` [L34](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/user.md#L34), [L38](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/user.md#L38) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | cloudfoundry/terraform-provider-cloudfoundry, `docs/resources/user_cf.md` [L34](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/user_cf.md#L34), [L36](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/user_cf.md#L36) | no | Id generated from older heading text; generated page, fixed by the `utils.go` lines | `view` |
| `#-view-metadata-for-an-object` | SAP/crossplane-provider-cloudfoundry, `apis/resources/v1alpha1/resource.go` [L17](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/apis/resources/v1alpha1/resource.go#L17), [L21](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/apis/resources/v1alpha1/resource.go#L21) | no | Id generated from older heading text; hand-written source | `view` |
| `#-view-metadata-for-an-object` | SAP/crossplane-provider-cloudfoundry, `package/crds/cloudfoundry.crossplane.io_apps.yaml` [L87](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_apps.yaml#L87), [L137](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_apps.yaml#L137), [L628](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_apps.yaml#L628), [L645](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_apps.yaml#L645) | no | Id generated from older heading text; generated CRD, fixed by the `resource.go` lines | `view` |
| `#-view-metadata-for-an-object` | SAP/crossplane-provider-cloudfoundry, `package/crds/cloudfoundry.crossplane.io_domains.yaml` [L87](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_domains.yaml#L87), [L105](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_domains.yaml#L105), [L310](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_domains.yaml#L310), [L329](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_domains.yaml#L329) | no | Id generated from older heading text; generated CRD, fixed by the `resource.go` lines | `view` |
| `#-view-metadata-for-an-object` | SAP/crossplane-provider-cloudfoundry, `package/crds/cloudfoundry.crossplane.io_organizations.yaml` [L87](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_organizations.yaml#L87), [L94](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_organizations.yaml#L94), [L202](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_organizations.yaml#L202), [L216](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_organizations.yaml#L216) | no | Id generated from older heading text; generated CRD, fixed by the `resource.go` lines | `view` |
| `#-view-metadata-for-an-object` | SAP/crossplane-provider-cloudfoundry, `package/crds/cloudfoundry.crossplane.io_routes.yaml` [L87](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_routes.yaml#L87), [L186](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_routes.yaml#L186), [L392](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_routes.yaml#L392), [L444](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_routes.yaml#L444) | no | Id generated from older heading text; generated CRD, fixed by the `resource.go` lines | `view` |
| `#-view-metadata-for-an-object` | SAP/crossplane-provider-cloudfoundry, `package/crds/cloudfoundry.crossplane.io_servicecredentialbindings.yaml` [L96](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_servicecredentialbindings.yaml#L96), [L189](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_servicecredentialbindings.yaml#L189), [L426](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_servicecredentialbindings.yaml#L426), [L440](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_servicecredentialbindings.yaml#L440) | no | Id generated from older heading text; generated CRD, fixed by the `resource.go` lines | `view` |
| `#-view-metadata-for-an-object` | SAP/crossplane-provider-cloudfoundry, `package/crds/cloudfoundry.crossplane.io_serviceinstances.yaml` [L92](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_serviceinstances.yaml#L92), [L132](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_serviceinstances.yaml#L132), [L523](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_serviceinstances.yaml#L523), [L546](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_serviceinstances.yaml#L546) | no | Id generated from older heading text; generated CRD, fixed by the `resource.go` lines | `view` |
| `#-view-metadata-for-an-object` | SAP/crossplane-provider-cloudfoundry, `package/crds/cloudfoundry.crossplane.io_serviceroutebindings.yaml` [L96](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_serviceroutebindings.yaml#L96), [L103](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_serviceroutebindings.yaml#L103), [L379](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_serviceroutebindings.yaml#L379), [L393](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_serviceroutebindings.yaml#L393) | no | Id generated from older heading text; generated CRD, fixed by the `resource.go` lines | `view` |
| `#-view-metadata-for-an-object` | SAP/crossplane-provider-cloudfoundry, `package/crds/cloudfoundry.crossplane.io_spaces.yaml` [L92](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_spaces.yaml#L92), [L104](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_spaces.yaml#L104), [L293](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_spaces.yaml#L293), [L312](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/package/crds/cloudfoundry.crossplane.io_spaces.yaml#L312) | no | Id generated from older heading text; generated CRD, fixed by the `resource.go` lines | `view` |

## troubleshooting_slow_requests

Page: <https://docs.cloudfoundry.org/adminguide/troubleshooting_slow_requests.html>

No broken links found. All in-page links (13 distinct fragments) resolve, and no link from
another page or repository carries a fragment to this page.

## access-control

Page: <https://docs.cloudfoundry.org/services/access-control.html>

`#make-plans-public` was an explicit `<a id>` on this page until
September 2014, when the section was rewritten as "Enable Access to
Service Plans" with id `enable-access`
([docs-services d0744fa](https://github.com/cloudfoundry/docs-services/commit/d0744fa441c38bb57a8f4623009111263e60e7ea)).
The same id still exists on another page,
`services/managing-service-brokers.html#make-plans-public`, which is
also a valid target for these links.

| Fragment | Source (repo, linked file:line pinned) | Archived? | Cause | Intended id |
|----------|----------------------------------------|-----------|-------|-------------|
| `#make-plans-public` | IronFoundry/if-service-broker, `README.md` [L36](https://github.com/IronFoundry/if-service-broker/blob/fdc97f9ec8f21f5b3f820d9b03250b2c60c08f62/README.md#L36) | no | Explicit id removed when the section was rewritten (2014) | `enable-access` |
| `#make-plans-public` | teddyking/mongodb_broker, `README.md` [L16](https://github.com/teddyking/mongodb_broker/blob/3e036673a9cd68c1b0eeb8bc2c1ff17453d825b2/README.md#L16) | no | Explicit id removed when the section was rewritten (2014) | `enable-access` |

## routes-domains

Page: <https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html>

Two of the broken links are on the page itself: its source links to
`#http-vs-tcp-shared-domains` and `#create-route-w-port`, and the
published page shows both as dead in-page links.

| Fragment | Source (repo, linked file:line pinned) | Archived? | Cause | Intended id |
|----------|----------------------------------------|-----------|-------|-------------|
| `#create-route-w-port` | cloudfoundry/docs-dev-guide, `deploy-apps/routes-domains.html.md.erb` [L394](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L394) (in-page link) | no | Typo of an existing id. The link read `#create-route-with-port` until a 2023-07-28 style edit ([8ceabb1](https://github.com/cloudfoundry/docs-dev-guide/commit/8ceabb14db63a87f0b08650936d4edd2dc225c55)) shortened it; the id was never `create-route-w-port` | `create-route-with-port` |
| `#create-route-w-port` | cloudfoundry/docs-dev-guide, `services/fluentd.html.md.erb` [L36](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/fluentd.html.md.erb#L36) | no | Same typo, introduced by the same commit | `create-route-with-port` |
| `#http-vs-tcp-shared-domains` | cloudfoundry/docs-dev-guide, `deploy-apps/routes-domains.html.md.erb` [L62](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L62) (in-page link) | no | Explicit id renamed. `<a id='http-vs-tcp-shared-domains'>` became `http-vs-tcp-domains` in the same 2023-07-28 edit ([8ceabb1](https://github.com/cloudfoundry/docs-dev-guide/commit/8ceabb14db63a87f0b08650936d4edd2dc225c55)); the in-page link was not updated | `http-vs-tcp-domains` |
| `#http-vs-tcp-shared-domains` | pivotal-cf/docs-overops-application-reliability, `docs-content/using.html.md.erb` [L15](https://github.com/pivotal-cf/docs-overops-application-reliability/blob/a5c002b2f47ee43f5607a74bbf9047a63eed1240/docs-content/using.html.md.erb#L15) | no | Explicit id renamed (as above) | `http-vs-tcp-domains` |
| `#-create-a-tcp-route-with-a-port` | cloudfoundry/cf-networking-onboarding, `tcp-routes/010-user-workflow.markdown` [L125](https://github.com/cloudfoundry/cf-networking-onboarding/blob/5f1ba8ec5e8f03bec98b9ca47864ae9edec29eb7/tcp-routes/010-user-workflow.markdown#L125) | no | Heading is now an HTML `<h4>` with no generated id ([8239f0a](https://github.com/cloudfoundry/docs-dev-guide/commit/8239f0a4af67a4a4c54eb2a7f5a1bbd2ad0eb7b1), 2025-04-11); the generated id was also from older heading text ("Create a TCP Route with a Port") | `create-route-with-port` |
| `#-create-an-http-route-with-a-path` | textbook/textbook.github.io, `content/development/spa-config.md` [L237](https://github.com/textbook/textbook.github.io/blob/660b0381bfc6e37a2a896d9ee09f54c05cbe4f50/content/development/spa-config.md#L237) | no | Heading is now an HTML `<h4>` with no generated id ([8239f0a](https://github.com/cloudfoundry/docs-dev-guide/commit/8239f0a4af67a4a4c54eb2a7f5a1bbd2ad0eb7b1), 2025-04-11) | `create-route-w-path` |
| `#-http-vs.-tcp-routes` | cloudfoundry/cf-networking-onboarding, `tcp-routes/010-user-workflow.markdown` [L124](https://github.com/cloudfoundry/cf-networking-onboarding/blob/5f1ba8ec5e8f03bec98b9ca47864ae9edec29eb7/tcp-routes/010-user-workflow.markdown#L124) | no | Id generated from older heading text. "HTTP vs. TCP routes" became "HTTP versus TCP routes" in 2023 ([8ceabb1](https://github.com/cloudfoundry/docs-dev-guide/commit/8ceabb14db63a87f0b08650936d4edd2dc225c55)); its generated id is now `-http-versus-tcp-routes` | `http-vs-tcp-routes` |

## Totals

| Page | Fragment | Links | Files | Repositories |
|------|----------|-------|-------|--------------|
| metadata | `#-view-metadata-for-an-object` | 72 | 28 | 2 (terraform provider: 38 links in 19 files; crossplane provider: 34 links in 9 files) |
| troubleshooting_slow_requests | none | 0 | 0 | 0 |
| access-control | `#make-plans-public` | 2 | 2 | 2 |
| routes-domains | `#create-route-w-port` | 2 | 2 | 1 (docs-dev-guide) |
| routes-domains | `#http-vs-tcp-shared-domains` | 2 | 2 | 2 |
| routes-domains | `#-create-a-tcp-route-with-a-port` | 1 | 1 | 1 |
| routes-domains | `#-http-vs.-tcp-routes` | 1 | 1 (same file as above) | 1 |
| routes-domains | `#-create-an-http-route-with-a-path` | 1 | 1 | 1 |
| **All** | 7 fragments | **81** | **35** | **8** |

The repositories are cloudfoundry/terraform-provider-cloudfoundry,
SAP/crossplane-provider-cloudfoundry, IronFoundry/if-service-broker,
teddyking/mongodb_broker, cloudfoundry/docs-dev-guide,
pivotal-cf/docs-overops-application-reliability,
cloudfoundry/cf-networking-onboarding and textbook/textbook.github.io.

Thirteen hand-written lines cover all 81 links: the 4
source lines in the two providers (the other 68 provider links follow by
regeneration) and the 9 links outside the providers.

## Same fragments on other hosts (not counted)

These links use a fragment that is not on today's page, but they point
at older or vendor hosts, not docs.cloudfoundry.org:

- `#make-plans-public` on `docs.gopivotal.com/pivotalcf/services/access-control.html`:
  [ephoning/sample-service-broker `README.md` L18](https://github.com/ephoning/sample-service-broker/blob/ba777f1eae2e4c00e4b3eb05549e765871027c27/README.md#L18),
  [IronFoundry/ironfoundry.github.io `help/how_services_and_service-brokers_are_used_in_cloud_foundry.md` L20](https://github.com/IronFoundry/ironfoundry.github.io/blob/d6af26e8ec7a115ee83124495c1d909073a878a5/help/how_services_and_service-brokers_are_used_in_cloud_foundry.md#L20).
- `#http-vs.-tcp-routes` on `docs.run.pivotal.io/devguide/deploy-apps/routes-domains.html`:
  three README files in apigeekdemos/apigee-s1p-labs.

One link that looks related is valid:
`docs.cloudfoundry.org/services/managing-service-brokers.html#make-plans-public`
(Infra-Red/postgresql-service-broker-boshrelease), since that page
still has the id.

## Searches not completed

- None of the 17 code-search queries hit the rate limit or the
  1000-result cap, and none reported incomplete results.
- Two extra queries, `"access-control.html#"` and `"metadata.html#"`,
  were dropped: code search ignores the punctuation, so they returned
  5,088 and 164,864 unrelated files. The path queries above cover the
  same links.
- Relative links were checked only inside the `cloudfoundry/docs-*`
  repositories. Copies of these pages on other sites, such as forks of
  `docs-dev-guide`, were not searched.

## Found by the cross-repository links survey (2026-10-11)

The [cross-repository links survey](../cross-repo-links/survey/README.md)
resolved every link in the content of the 15 repositories the book
collects, pages and partials, against a model of the book's site, at the
commits in its [shas.txt](../cross-repo-links/survey/shas.txt). 55 links
in content do not reach their target: 50 point at an id the target page
does not have, 3 reach a redirect whose target is gone, and 2 point at an
id bosh.io does not have. Two of them, the in-page links on
`routes-domains`, are listed above and left out below.

Decision (Docs WG lead, 2026-10-11): these links are fixed at the source
before conversion, and the redirect rules whose target is gone are
dropped or retargeted
([R-24](../../requirements/README.md#r-24) markup cleanup before
conversion; [cross-repository links convention 5](../cross-repo-links/results.md#conventions-to-record)).

A **suggested fix** comes from the site model and needs checking before
use: an id on the same page whose spelling is close (it may be a
different section), the pages that now carry the id, or for a redirect
rule the pages with the same file name. "Target page" is the page the
link resolves to; a link in a partial is listed once.

Regenerate the tables with
[cleanup.py](../cross-repo-links/survey/cleanup.py) from a run of the
survey.

### Links, by repository

#### docs-bbr

| Source | Link as written | Target page | Problem | Suggested fix |
|---|---|---|---|---|
| [backup.html.md.erb L313](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L313) | `#what-to-do-with-artifact` | `/bbr/backup.html` | no such id on the target page | no similar id found; remove the fragment or pick a heading |

#### docs-book-cloudfoundry

| Source | Link as written | Target page | Problem | Suggested fix |
|---|---|---|---|---|
| [master_middleman/source/contribute.html.md.erb L22](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/contribute.html.md.erb#L22) | `#raise-issue` | `/contribute.html` | no such id on the target page | `#issue` on the same page (similar id) |

#### docs-buildpacks

| Source | Link as written | Target page | Problem | Suggested fix |
|---|---|---|---|---|
| [dotnet-core/index.html.md.erb L157](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/dotnet-core/index.html.md.erb#L157) | `../../devguide/deploy-apps/manifest.html#env-block` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |
| [go/index.html.md.erb L231](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/go/index.html.md.erb#L231) | `https://docs.cloudfoundry.org/adminguide/trusted-system-certificates.html` | `/` | redirects to a page that is gone | the redirect's target is gone; link to the page that now covers it |
| [hwc/extension-buildpack.html.md.erb L170](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/hwc/extension-buildpack.html.md.erb#L170) | `../../devguide/deploy-apps/manifest.html#start-commands` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |
| [java/java-tips.html.md.erb L462](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/java-tips.html.md.erb#L462) | `../../devguide/deploy-apps/manifest.html#env-block` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |
| [php/gsg-php-composer.html.md.erb L74](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/php/gsg-php-composer.html.md.erb#L74) | `../../devguide/deploy-apps/manifest.html#env-block` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |
| [php/gsg-php-newrelic.html.md.erb L23](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/php/gsg-php-newrelic.html.md.erb#L23) | `../../devguide/deploy-apps/manifest.html#env-block` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |
| [php/gsg-php-usage.html.md.erb L174](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/php/gsg-php-usage.html.md.erb#L174) | `../../devguide/deploy-apps/manifest.html#env-block` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |
| [php/index.html.md.erb L106](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/php/index.html.md.erb#L106) | `https://docs.cloudfoundry.org/adminguide/trusted-system-certificates.html` | `/` | redirects to a page that is gone | the redirect's target is gone; link to the page that now covers it |
| [python/index.html.md.erb L81](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/python/index.html.md.erb#L81) | `../../devguide/deploy-apps/manifest.html#start-commands` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |
| [python/index.html.md.erb L220](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/python/index.html.md.erb#L220) | `https://docs.cloudfoundry.org/adminguide/trusted-system-certificates.html` | `/` | redirects to a page that is gone | the redirect's target is gone; link to the page that now covers it |
| [r/index.html.md.erb L44](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/r/index.html.md.erb#L44) | `../../devguide/deploy-apps/manifest.html#start-commands` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |
| [ruby/gsg-ror.html.md.erb L25](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/ruby/gsg-ror.html.md.erb#L25) | `../../devguide/deploy-apps/manifest.html#minimal-manifest` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |
| [ruby/sample-ror.html.md.erb L24](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/ruby/sample-ror.html.md.erb#L24) | `../../devguide/deploy-apps/manifest.html#minimal-manifest` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |

#### docs-cf-admin

| Source | Link as written | Target page | Problem | Suggested fix |
|---|---|---|---|---|
| [cli-user-management.html.md.erb L106](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/cli-user-management.html.md.erb#L106) | `../cf-cli/getting-started.html#multi-origin` | `/cf-cli/getting-started.html` | no such id on the target page | the id is on `/concepts/managing-roles.html` |
| [cli-user-management.html.md.erb L145](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/cli-user-management.html.md.erb#L145) | `../cf-cli/getting-started.html#multi-origin` | `/cf-cli/getting-started.html` | no such id on the target page | the id is on `/concepts/managing-roles.html` |
| [quota-plans.html.md.erb L22](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/quota-plans.html.md.erb#L22) | `../devguide/deploy-apps/cf-networking.html#policy-quotas` | `/devguide/deploy-apps/cf-networking.html` | no such id on the target page | no similar id found; remove the fragment or pick a heading |
| [troubleshooting-router-error-responses.html.md.erb L17](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb#L17) | `#gorouter-errors` | `/adminguide/troubleshooting-router-error-responses.html` | no such id on the target page | `#diagnose-gorouter-errors` on the same page (similar id) |
| [troubleshooting-router-error-responses.html.md.erb L204](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb#L204) | `#tls-to-back-end` | `/adminguide/troubleshooting-router-error-responses.html` | no such id on the target page | the id is on `/concepts/http-routing.html` |
| [troubleshooting-router-error-responses.html.md.erb L291](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb#L291) | `../concepts/http-routing.html#with-tls` | `/concepts/http-routing.html` | no such id on the target page | `#without-tls` on the same page (similar id) |

#### docs-cloudfoundry-concepts

| Source | Link as written | Target page | Problem | Suggested fix |
|---|---|---|---|---|
| [architecture/index.html.md.erb L83](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/architecture/index.html.md.erb#L83) | `../diego/diego-architecture.html#bbs` | `/concepts/diego/diego-architecture.html` | no such id on the target page | the id is on `/concepts/architecture/index.html`, `/running/all_metrics.html` |
| [architecture/index.html.md.erb L85](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/architecture/index.html.md.erb#L85) | `../diego/diego-architecture.html#bbs` | `/concepts/diego/diego-architecture.html` | no such id on the target page | the id is on `/concepts/architecture/index.html`, `/running/all_metrics.html` |
| [asg.html.md.erb L109](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/asg.html.md.erb#L109) | `#unbinding-asgs` | `/concepts/asg.html` | no such id on the target page | `#-binding-asgs` on the same page (similar id) |
| [contribute.html.md.erb L22](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/contribute.html.md.erb#L22) | `#github-issue` | `/concepts/contribute.html` | no such id on the target page | `#-raising-a-github-issue` on the same page (similar id) |
| [contribute.html.md.erb L22](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/contribute.html.md.erb#L22) | `#github-pr` | `/concepts/contribute.html` | no such id on the target page | `#non-github` on the same page (similar id) |
| [roles.html.md.erb L60](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/roles.html.md.erb#L60) | `./architecture/uaa.html#scopes` | `/concepts/architecture/uaa.html` | no such id on the target page | the id is on `/uaa/uaa-concepts.html`, `/uaa/uaa-deploy.html` |

#### docs-credhub

| Source | Link as written | Target page | Problem | Suggested fix |
|---|---|---|---|---|
| [hsm-config.html.md.erb L383](https://github.com/cloudfoundry/docs-credhub/blob/21b0448736435cec0f5a1491e0b40bda9c4307eb/hsm-config.html.md.erb#L383) | `#establish-network-trust-link` | `/credhub/hsm-config.html` | no such id on the target page | `#network-trust-link` on the same page (similar id) |
| [hsm-config.html.md.erb L385](https://github.com/cloudfoundry/docs-credhub/blob/21b0448736435cec0f5a1491e0b40bda9c4307eb/hsm-config.html.md.erb#L385) | `#establish-network-trust-link` | `/credhub/hsm-config.html` | no such id on the target page | `#network-trust-link` on the same page (similar id) |

#### docs-deploying-cf

| Source | Link as written | Target page | Problem | Suggested fix |
|---|---|---|---|---|
| [cf-deployment/gcp.html.md.erb L53](https://github.com/cloudfoundry/docs-deploying-cf/blob/1113cfaf3626931c653c91dc8d537d7f181d6762/cf-deployment/gcp.html.md.erb#L53) | `https://bosh.io/docs/cli-v2.html#install` | `/content/cli-v2.md` | no such id on bosh.io | check bosh.io for the heading's current id |
| [common/aws.html.md.erb L50](https://github.com/cloudfoundry/docs-deploying-cf/blob/1113cfaf3626931c653c91dc8d537d7f181d6762/common/aws.html.md.erb#L50) | `https://bosh.io/docs/cli-v2.html#install` | `/content/cli-v2.md` | no such id on bosh.io | check bosh.io for the heading's current id |

#### docs-dev-guide

| Source | Link as written | Target page | Problem | Suggested fix |
|---|---|---|---|---|
| [deploy-apps/_c2c_oss_logging.html.md.erb L4](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/_c2c_oss_logging.html.md.erb#L4) | `#iaas` | `/devguide/deploy-apps/cf-networking.html` | no such id on the target page | no similar id found; remove the fragment or pick a heading |
| [deploy-apps/_c2c_oss_logging.html.md.erb L23](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/_c2c_oss_logging.html.md.erb#L23) | `#iaas` | `/devguide/deploy-apps/cf-networking.html` | no such id on the target page | no similar id found; remove the fragment or pick a heading |
| [deploy-apps/_c2c_oss_logging.html.md.erb L42](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/_c2c_oss_logging.html.md.erb#L42) | `#iaas` | `/devguide/deploy-apps/cf-networking.html` | no such id on the target page | no similar id found; remove the fragment or pick a heading |
| [deploy-apps/_c2c_oss_logging.html.md.erb L52](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/_c2c_oss_logging.html.md.erb#L52) | `#iaas` | `/devguide/deploy-apps/cf-networking.html` | no such id on the target page | no similar id found; remove the fragment or pick a heading |
| [deploy-apps/deploy-app.html.md.erb L51](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/deploy-app.html.md.erb#L51) | `#custom-route` | `/devguide/deploy-apps/deploy-app.html` | no such id on the target page | `#custom-push` on the same page (similar id) |
| [deploy-apps/deploy-app.html.md.erb L132](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/deploy-app.html.md.erb#L132) | `#custom-route` | `/devguide/deploy-apps/deploy-app.html` | no such id on the target page | `#custom-push` on the same page (similar id) |
| [deploy-apps/environment-variable.html.md.erb L8](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/environment-variable.html.md.erb#L8) | `./manifest.html#env-block` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |
| [deploy-apps/manifest-attributes.html.md.erb L506](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/manifest-attributes.html.md.erb#L506) | `../../cf-cli/getting-started.html#find-app` | `/cf-cli/getting-started.html` | no such id on the target page | no similar id found; remove the fragment or pick a heading |
| [deploy-apps/routes-domains.html.md.erb L388](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L388) | `#create-route-w-port` | `/devguide/deploy-apps/routes-domains.html` | no such id on the target page | `#create-route-with-port` on the same page (similar id) |
| [deploy-apps/routes-domains.html.md.erb L397](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L397) | `../deploy-apps/manifest.html#routes` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html`, `/devguide/deploy-apps/routes-domains.html` |
| [deploy-apps/ssh-apps.html.md.erb L11](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/ssh-apps.html.md.erb#L11) | `../../cf-cli/http-proxy.html#v3-ssh-socks5` | `/cf-cli/http-proxy.html` | no such id on the target page | no similar id found; remove the fragment or pick a heading |
| [services/_using-vol-services.html.md.erb L48](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/_using-vol-services.html.md.erb#L48) | `../deploy-apps/manifest.html#services-block` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |
| [services/application-binding.html.md.erb L213](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/application-binding.html.md.erb#L213) | `../deploy-apps/manifest.html#services-block` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |
| [services/managing-services.html.md.erb L213](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/managing-services.html.md.erb#L213) | `../deploy-apps/manifest.html#services-block` | `/devguide/deploy-apps/manifest.html` | no such id on the target page | the id is on `/devguide/deploy-apps/manifest-attributes.html` |

#### docs-loggregator

| Source | Link as written | Target page | Problem | Suggested fix |
|---|---|---|---|---|
| [container-metrics.html.md.erb L143](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/container-metrics.html.md.erb#L143) | `#cpu-mem-disk` | `/loggregator/container-metrics.html` | no such id on the target page | `#cf-mem-disk` on the same page (similar id) |
| [log-ops-guide.html.md.erb L81](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/log-ops-guide.html.md.erb#L81) | `../running/managing-cf/logging-config.html#scaling` | `/running/managing-cf/logging-config.html` | no such id on the target page | the id is on `/devguide/deploy-apps/rolling-deploy.html`, `/devguide/services/oms-nozzle.html`, `/loggregator/log-ops-guide.html` |
| [opentelemetry.html.md.erb L123](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/opentelemetry.html.md.erb#L123) | `#logging-and-metrics` | `/loggregator/opentelemetry.html` | no such id on the target page | no similar id found; remove the fragment or pick a heading |

#### docs-running-cf

| Source | Link as written | Target page | Problem | Suggested fix |
|---|---|---|---|---|
| [metrics/_cloud_controller.html.md.erb L4](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/metrics/_cloud_controller.html.md.erb#L4) | `#cc_worker` | `/running/all_metrics.html` | no such id on the target page | no similar id found; remove the fragment or pick a heading |

#### docs-services

| Source | Link as written | Target page | Problem | Suggested fix |
|---|---|---|---|---|
| [binding-credentials.html.md.erb L15](https://github.com/cloudfoundry/docs-services/blob/ccb0036407e4c2eabbb61a3b3de008f821f41c5b/binding-credentials.html.md.erb#L15) | `../devguide/services/managing-services.html#use` | `/devguide/services/managing-services.html` | no such id on the target page | the id is on `/adminguide/stack-auditor.html` |

#### docs-uaa

| Source | Link as written | Target page | Problem | Suggested fix |
|---|---|---|---|---|
| [uaa-concepts.html.md.erb L12](https://github.com/cloudfoundry/docs-uaa/blob/216c797cfa1a971cf0f9e53eb3e4803aaf914a94/uaa-concepts.html.md.erb#L12) | `#user-groups` | `/uaa/uaa-concepts.html` | no such id on the target page | `#-user-groups` on the same page (similar id) |
| [uaa-concepts.html.md.erb L88](https://github.com/cloudfoundry/docs-uaa/blob/216c797cfa1a971cf0f9e53eb3e4803aaf914a94/uaa-concepts.html.md.erb#L88) | `#shadow` | `/uaa/uaa-concepts.html` | no such id on the target page | `##shadow` on the same page (similar id) |
| [uaa-deploy.html.md.erb L30](https://github.com/cloudfoundry/docs-uaa/blob/216c797cfa1a971cf0f9e53eb3e4803aaf914a94/uaa-deploy.html.md.erb#L30) | `#local` | `/uaa/uaa-deploy.html` | no such id on the target page | `#demo-local` on the same page (similar id) |

### Redirect rules whose target is gone

30 of the 85 rules in the book's
[`redirects.rb`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb)
send a reader to a page that no longer exists. A static host writes each
rule as a page, so each is dropped or given a new target before
conversion
([R-16](../../requirements/README.md#r-16) old URLs keep working).
Rule [L48](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L48)
can never match, because its source holds a `#` part, which browsers do
not send; it does nothing and can go with them.

| Rule | From | To (missing) | Suggested target |
|---|---|---|---|
| [L7](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L7) | `/console/cf-api-endpoint.html` | `/running/cf-api-endpoint.html` | `/running/archive/cf-api-endpoint.html` |
| [L9](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L9) | `%r{/deploying/ec2/.*}` | `/deploying/aws/index.html` | `/deploying/common/aws.html` |
| [L11](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L11) | `/deploying/openstack/deploying_bosh.html` | `/deploying/openstack/index.html` | none by file name; drop the rule or pick a page |
| [L12](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L12) | `/deploying/openstack/deploying_microbosh.html` | `/deploying/openstack/index.html` | none by file name; drop the rule or pick a page |
| [L13](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L13) | `/deploying/openstack/uploading_bosh_stemcell.html` | `/deploying/openstack/index.html` | none by file name; drop the rule or pick a page |
| [L15](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L15) | `/deploying/vsphere/bosh-example-manifest.html` | `/deploying/vsphere/index.html` | none by file name; drop the rule or pick a page |
| [L16](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L16) | `/deploying/vsphere/deploying_bosh_with_micro_bosh.html` | `/deploying/vsphere/index.html` | none by file name; drop the rule or pick a page |
| [L17](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L17) | `/deploying/vsphere/deploying_micro_bosh.html` | `/deploying/vsphere/index.html` | none by file name; drop the rule or pick a page |
| [L18](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L18) | `/deploying/vsphere/install-and-prepare-vsphere.html` | `/deploying/vsphere/index.html` | none by file name; drop the rule or pick a page |
| [L20](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L20) | `/deploying/vcloud/bosh-example-manifest.html` | `/deploying/vcloud/index.html` | none by file name; drop the rule or pick a page |
| [L21](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L21) | `/deploying/vcloud/deploying_bosh_with_micro_bosh.html` | `/deploying/vcloud/index.html` | none by file name; drop the rule or pick a page |
| [L22](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L22) | `/deploying/vcloud/deploying_micro_bosh.html` | `/deploying/vcloud/index.html` | none by file name; drop the rule or pick a page |
| [L23](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L23) | `/deploying/vcloud/micro-bosh-example-manifest.html` | `/deploying/vcloud/index.html` | none by file name; drop the rule or pick a page |
| [L25](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L25) | `/deploying/boshlite/deploy_cf_boshlite.html` | `/deploying/boshlite/index.html` | none by file name; drop the rule or pick a page |
| [L27](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L27) | `/deploying/cf-stub-aws.html` | `/deploying/aws/cf-stub.html` | none by file name; drop the rule or pick a page |
| [L28](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L28) | `/deploying/cf-stub-openstack.html` | `/deploying/openstack/cf-stub.html` | none by file name; drop the rule or pick a page |
| [L29](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L29) | `/deploying/cf-stub-vsphere.html` | `/deploying/common/vsphere-vcloud-cf-stub.html` | none by file name; drop the rule or pick a page |
| [L30](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L30) | `/deploying/cf-stub-vcloud.html` | `/deploying/common/vsphere-vcloud-cf-stub.html` | none by file name; drop the rule or pick a page |
| [L40](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L40) | `/devguide/deploy-apps/api-endpoint.html` | `/running/cf-api-endpoint.html` | `/running/archive/cf-api-endpoint.html` |
| [L43](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L43) | `%r{/devguide/installcf/(.*)}` | `/cf-cli/$1` | none by file name; drop the rule or pick a page |
| [L44](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L44) | `%r{/devguide/cf-cli/(.*)}` | `/cf-cli/$1` | none by file name; drop the rule or pick a page |
| [L57](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L57) | `/running/api/version.html` | `/running/cf-api-endpoint.html` | `/running/archive/cf-api-endpoint.html` |
| [L78](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L78) | `/services/volume-services-v2.10.html` | `/devguide/services/volume-services.html` | none by file name; drop the rule or pick a page |
| [L79](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L79) | `/services/volume-services-v2.9.html` | `/devguide/services/volume-services.html` | none by file name; drop the rule or pick a page |
| [L85](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L85) | `/adminguide/trusted-system-certificates.html` | `/running/trusted-system-certificates.html` | `/devguide/deploy-apps/trusted-system-certificates.html`, `/running/archive/trusted-system-certificates.html` |
| [L86](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L86) | `/adminguide/deploy-vol-services.html` | `/running/deploy-vol-services.html` | `/running/archive/deploy-vol-services.html` |
| [L95](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L95) | `/deploying/aws/setup_aws.html` | `/deploying/aws/setup_bosh_aws.html` | none by file name; drop the rule or pick a page |
| [L97](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L97) | `/concepts/architecture/execution-agent.html` | `/concepts/diego/dea-vs-diego.html` | none by file name; drop the rule or pick a page |
| [L98](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L98) | `/concepts/architecture/dea-algorithm.html` | `/concepts/diego/dea-vs-diego.html` | none by file name; drop the rule or pick a page |
| [L99](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L99) | `/concepts/architecture/warden.html` | `/concepts/diego/dea-vs-diego.html` | none by file name; drop the rule or pick a page |

## One anchor used four times: uaa-performance (2026-10-12)

Page: <https://docs.cloudfoundry.org/running/uaa-performance.html>

Found while linking the tables test pages to their tables on the
published page. The source gives the headings of all four sections the
same anchor, `<a id='client-credentials'></a>`, so `#client-credentials`
reaches only the first section; the other three cannot be linked by an
anchor of their own. Each heading also lacks the space after `###`, so
the published page gives it a second, generated id that starts with a
hyphen (`-password-grant-type`).

| Source (docs-running-cf, pinned) | Heading | Ids on the published page | Suggested fix (to check) |
|---|---|---|---|
| [L84](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/uaa-performance.html.md.erb#L84) | Client credentials grant type | `client-credentials`, `-client-credentials-grant-type` | keep `client-credentials`; add the space after `###` |
| [L169](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/uaa-performance.html.md.erb#L169) | Password grant type | `client-credentials` (again), `-password-grant-type` | a new id such as `password`; add the space |
| [L254](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/uaa-performance.html.md.erb#L254) | Authorization code grant type | `client-credentials` (again), `-authorization-code-grant-type` | a new id such as `authorization-code`; add the space |
| [L305](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/uaa-performance.html.md.erb#L305) | Implicit grant type | `client-credentials` (again), `-implicit-grant-type` | a new id such as `implicit`; add the space |

Links to the hyphen-prefixed ids were not searched for; adding the space
changes those ids, so a search should come before the fix.

## One id on two tables: roles (2026-10-12)

Page: <https://docs.cloudfoundry.org/concepts/roles.html>

Found while adding the roles table as a test page. Two partials included by
`roles.html.md.erb` open their table with the same id, so the published
page has `oss-roles-permissions` twice; `#oss-roles-permissions` reaches
only the first table, and the second has no id of its own.

| Source (docs-cloudfoundry-concepts, pinned) | Table | Suggested fix (to check) |
|---|---|---|
| [`_oss_roles_table.html.md.erb` L1](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/_oss_roles_table.html.md.erb#L1) | Roles and permissions for active orgs | keep `oss-roles-permissions` |
| [`_suspended_org_roles_table.html.md.erb` L1](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/_suspended_org_roles_table.html.md.erb#L1) | Roles and permissions for suspended orgs | a new id such as `oss-suspended-org-roles-permissions`, in the pattern of the suspended spaces table's `oss-suspended-space-roles-permissions` |

Links to `#oss-roles-permissions` were not searched for.
