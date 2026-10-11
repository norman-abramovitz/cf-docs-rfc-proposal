# Intent: `metadata`

- Source: [`../../tables/source/metadata.html.md.erb`](../../tables/source/metadata.html.md.erb)
- Published: <https://docs.cloudfoundry.org/adminguide/metadata.html>
  (copy: [`../published/metadata.html`](../published/metadata.html))
- Anchors file: [`metadata.anchors`](metadata.anchors)

## Cases this page covers

- **Deep tree.** 32 headings over three levels (`##` to `####`), under a
  title that comes from the front matter (`title:`), not from an `# H1`.
- **Every heading has an explicit id**, written as an empty anchor at the
  start of the heading: `### <a id="add-cli"></a> Add metadata to a resource`.
- **Repeated heading text.** Five headings appear twice, once under
  "cf CLI procedures" and once under "API procedures": "Add metadata to a
  resource", "Add a label", "Update metadata for a resource", "Remove
  metadata from a resource", "View metadata for a resource". The explicit
  ids keep them apart (`add-cli` and `add`); an id made from the text
  would repeat.

## Heading tree to keep

The tree is the published page's, read by the outline check:
[`../results/published-outlines.txt`](../results/published-outlines.txt).
Levels and text must match in order; the page title is the `h1`.

```
h1 Using metadata in Cloud Foundry
  h2 About metadata                                  #about
    h3 Methods of adding metadata                    #methods
    h3 Types of metadata                             #types
      h4 Annotations sent to service brokers         #annotations
    h3 Metadata Requirements                         #reqs
      h4 Requirements for labels                     #reqs-labels
      h4 Requirements for annotations                #reqs-annotations
    h3 Metadata key prefixes                         #prefix
  h2 cf CLI procedures                               #cf-cli-procedures
    h3 Add metadata to a resource                    #add-cli
      h4 Add a label                                 #add-label-cli
    h3 Update metadata for a resource                #update-cli
    h3 Remove metadata from a resource               #remove-cli
      h4 Remove a label                              #remove-label-cli
    h3 View metadata for a resource                  #view-cli
      h4 View labels                                 #view-label-cli
      h4 Select resources by labels                  #select-resources-cli
  h2 API procedures                                  #api-procedures
    h3 Add metadata to a resource                    #add
      h4 Add a label                                 #add-label
      h4 Add an annotation                           #annotation
    h3 Update metadata for a resource                #update
    h3 Remove metadata from a resource               #remove
    h3 View metadata for a resource                  #view
    h3 List resources by querying labels             #query
      h4 Selector requirement reference              #requirements-reference
  h2 Example: Label resources with a git commit      #example
    h3 Manually label resources                      #manual
    h3 Automate labeling resources                   #example-script
      h4 Prerequisite                                #example-prerequisite
      h4 Example script                              #script
  h2 Example: Add custom tags to log and metric envelopes   #example-custom-tags
```

## Anchors to keep

Every explicit id above (32), listed in [`metadata.anchors`](metadata.anchors).

The published page also gives each heading a second id made from its text,
with a leading hyphen (`-about-metadata`), because the empty anchor and the
space after it are part of the heading text when the id is made. Two
headings get the same second id each time the text repeats
(`-add-metadata-to-a-resource` twice). Decision (this round): those
generated ids are not kept. They repeat, they start with a hyphen, and no
link that works today points at one (below).

### Links from other pages

Found by searching the clones of the docs repositories and GitHub code
search on 2026-10-10.

| Anchor | Linked from |
|--------|-------------|
| `#types` | [docs-dev-guide `deploy-apps/manifest-attributes.html.md.erb` L441](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/manifest-attributes.html.md.erb#L441) |
| `#query` | [cloud_controller_ng `docs/v3/source/includes/concepts/_metadata.md.erb`](https://github.com/cloudfoundry/cloud_controller_ng/blob/6cd32c7e5ca241c139f07c35ba5a55a3eb6f003a/docs/v3/source/includes/concepts/_metadata.md.erb) (the v3 API docs) |
| `#reqs` | [orange-cloudfoundry/osb-cmdb `CfAnnotationValidator.java`](https://github.com/orange-cloudfoundry/osb-cmdb/blob/e860dc361002de290e5ff3666c104eb1dbfe3851/osb-cmdb/src/main/java/com/orange/oss/osbcmdb/metadata/CfAnnotationValidator.java) |
| `#requirements-reference` | [orange-cloudfoundry/cf-cli-cmdb-scripts `cf-cli-cmdb-functions.bash`](https://github.com/orange-cloudfoundry/cf-cli-cmdb-scripts/blob/313efdad8eede088d0bb50196cb1e0e82141fe93/cf-cli-cmdb-functions.bash) |

**Already broken on the published page:** `#-view-metadata-for-an-object`,
a generated id from an older heading text, is linked from 19 files (38 links) in
[cloudfoundry/terraform-provider-cloudfoundry](https://github.com/cloudfoundry/terraform-provider-cloudfoundry/blob/a10579a0544dd0a55535bf051a0c3559c9a3c6e7/docs/resources/app.md)
(for example `docs/resources/app.md`) and 9 files (34 links) in
[SAP/crossplane-provider-cloudfoundry](https://github.com/SAP/crossplane-provider-cloudfoundry/blob/750b2f0b6be5e4a6488e7d209035dac5e9cc0613/apis/resources/v1alpha1/resource.go).
The heading is now "View metadata for a resource", twice, so no id on the
page matches. This is a finding for
[R-16](../../../requirements/README.md#r-16) old URLs keep working: links
to generated ids break when a heading is reworded.

## Deviations

None. The body is the tables round's native conversion of the page; only
the heading lines differ between modes.

## Checks

```bash
python3 -I ../checks/outline.py ../published/metadata.html BUILT.html --anchors metadata.anchors
```
