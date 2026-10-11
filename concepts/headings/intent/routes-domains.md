# Intent: `routes-domains` (Domains section)

- Source: [`../source/routes-domains.html.md.erb`](../source/routes-domains.html.md.erb), lines 688–962
- Published: <https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html>
  (copy: [`../published/routes-domains.html`](../published/routes-domains.html))
- Anchors file: [`routes-domains.anchors`](routes-domains.anchors)

## Cases this section covers

- **HTML heading tags in an ERB page.** Five of the section's `####`
  headings are written as HTML, `<h4><a id='create-shared-domain'></a> Create a shared domain</h4>`,
  next to Markdown `####` headings at the same level ("Delete a private
  domain"). The page as a whole has 15 such `<h4>` tags.
- **The deepest level in the test set**: two `#####` headings under
  "DNS for domains", which give the section four levels (`##` to `#####`).
- **Ids that links point to**, from this page and from other repositories
  (below).

## Heading tree to keep

Only the Domains section is converted (see [SOURCES](../source/SOURCES.md#notes));
the outline check compares the page title and that section
(`--section domains`).

```
h1 Configuring routes and domains
  h2 Domains                                                     #domains
    h3 List domains for an org                                   #list-domains
    h3 HTTP versus TCP domains                                   #http-vs-tcp-domains
    h3 Shared domains                                            #shared-domains
      h4 Create a shared domain           (HTML <h4> in source)  #create-shared-domain
      h4 Delete a shared domain           (HTML <h4> in source)  #delete-shared-domain
      h4 Internal domain                  (HTML <h4> in source)  #internal-domains
    h3 Private domains                                           #private-domains
      h4 Create a private domain          (HTML <h4> in source)  #create-private-domain
      h4 Sharing a private domain with one or more orgs  (HTML <h4> in source)  #sharing-private-domains
      h4 Delete a private domain                                 #delete-private-domain
    h3 Requirements for parent and child domains                 #parent-child-domains
    h3 DNS for domains                                           #domains-dns
      h4 Mapping Domains to your custom domain                   #subdomain-dns
        h5 Mapping a single domain to your custom domain         #single-mapping
        h5 Mapping multiple subdomains to your custom domain     #wildcard-mapping
      h4 Configuring DNS for your registered root domain         #root-domain-dns
```

**An HTML heading and a Markdown heading are the same heading.** Decision
(this round): the outline counts both, and a native conversion writes both
as the tool's own heading syntax. On the published page they differ in two
ways that a reader can see: an HTML heading gets no generated id, and the
page's quick links (its table of contents) list only `##` and `###`
headings that start with an `<a id>`, so neither kind of `####` appears
there. Bookbinder's quick-links code:
[`quicklinks_renderer.rb`](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/quicklinks_renderer.rb#L24-L26)
(tag v9.12.0; the book's Gemfile pins
[`bookbindery` 9.12.1](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/Gemfile#L3),
which has no tag on GitHub; the file is the same in the 9.12.1 gem
published on rubygems.org).

## Anchors to keep

The 17 explicit ids above, listed in [`routes-domains.anchors`](routes-domains.anchors).

### Links from other pages

Links into the Domains section, found in the clones of the docs
repositories and by GitHub code search on 2026-10-10. Code search counts
are lower bounds.

| Anchor | Linked from |
|--------|-------------|
| `#domains` | [docs-cf-admin `enabling-tcp-routing.html.md.erb` L72](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/enabling-tcp-routing.html.md.erb#L72); [SAP-docs/btp-cloud-platform](https://github.com/SAP-docs/btp-cloud-platform/blob/32010e1ff2f76d2f80517ba81b0dcca46c057a38/docs/10-concepts/supported-and-unsupported-cloud-foundry-features-f8a351c.md); [vmware-tanzu/tanzu-dev-portal](https://github.com/vmware-tanzu/tanzu-dev-portal/blob/9862e10d630d65c7515312f532b30df5d6876e4e/content/learningpaths/cloud-native-development-in-practice/route-naming.md); two more |
| `#private-domains` | three pages in [SAP-docs/btp-cloud-platform](https://github.com/SAP-docs/btp-cloud-platform/blob/32010e1ff2f76d2f80517ba81b0dcca46c057a38/docs/50-administration-and-ops/create-routes-9fddeea.md), [sap-tutorials/btp-foundation](https://github.com/sap-tutorials/btp-foundation/blob/d35b4782a244377121ab64084fe70f2c5afd4070/tutorials/btp-cockpit-cf-managing-routes/btp-cockpit-cf-managing-routes.md), two more; this page |
| `#shared-domains` | [SAP-docs/btp-custom-domain-service](https://github.com/SAP-docs/btp-custom-domain-service/blob/4819e96c8e2db303d77523f296112fc5884a851b/docs/cd-cli/20-Configuration/sharing-custom-domains-8ecabca.md); [pivotal/blog](https://github.com/pivotal/blog/blob/32d0162eaf90e137e4c1138583dddcabf55c3068/content/post/pws-io-domain-failure.md); this page |
| `#domains-dns` | [swisscom/docs-appcloud-devguide](https://github.com/swisscom/docs-appcloud-devguide/blob/05d27c0e9ac4c44a7c2aadf68d3f4b14f37940a2/deploy-apps/certificates.html.md.erb); one more; this page |

The rest of the page (the Routes section) is linked more: `#internal-routes`,
`#map-route`, `#routes`, `#surgical-routing`, `#http-vs-tcp-routes`,
`#create-route` and others, from CF repositories such as
[docs-cf-admin](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/enabling-tcp-routing.html.md.erb#L25)
and from outside them. They are outside the excerpt.

**Already broken on the published page** (none of these ids is on the
page; the first four point into the Routes section; full list with causes:
[broken-links.md](../broken-links.md#routes-domains)). Two of them are
also linked from this page's own source: `#create-route-w-port`
([L394](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L394))
and `#http-vs-tcp-shared-domains`
([L62](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L62)).

- `#create-route-w-port`, from [docs-dev-guide `services/fluentd.html.md.erb` L36](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/fluentd.html.md.erb#L36):
  the id is `create-route-with-port`.
- `#-create-a-tcp-route-with-a-port` and `#-http-vs.-tcp-routes`, from
  [cloudfoundry/cf-networking-onboarding](https://github.com/cloudfoundry/cf-networking-onboarding/blob/5f1ba8ec5e8f03bec98b9ca47864ae9edec29eb7/tcp-routes/010-user-workflow.markdown):
  ids generated from older headings. The first heading is now an HTML
  `<h4>`, which gets no generated id at all; the second was reworded.
- `#-create-an-http-route-with-a-path`, from
  [textbook/textbook.github.io](https://github.com/textbook/textbook.github.io/blob/660b0381bfc6e37a2a896d9ee09f54c05cbe4f50/content/development/spa-config.md):
  same cause, an HTML `<h4>` now.
- `#http-vs-tcp-shared-domains`, from
  [pivotal-cf/docs-overops-application-reliability](https://github.com/pivotal-cf/docs-overops-application-reliability/blob/a5c002b2f47ee43f5607a74bbf9047a63eed1240/docs-content/using.html.md.erb):
  no such id on the page.

## Deviations

None in the headings. The body needed tool-specific changes for variables
in code (see the results).

## Checks

```bash
python3 -I ../checks/outline.py ../published/routes-domains.html BUILT.html --anchors routes-domains.anchors --section domains
```
