# Links already broken today

Status: draft, incomplete — covers what is known as of 2026-10-10.

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
