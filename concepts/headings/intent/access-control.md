# Intent: `access-control`

- Source: [`../source/access-control.html.md.erb`](../source/access-control.html.md.erb)
- Published: <https://docs.cloudfoundry.org/services/access-control.html>
  (copy: [`../published/access-control.html`](../published/access-control.html))
- Anchors file: [`access-control.anchors`](access-control.anchors)

## Cases this page covers

- **Skipped levels.** `## Enabling access to Service Plans` is followed by
  `#### Enabling access to a subset of users`, with no `###` between them;
  the same happens under "Deactivating access". The section then closes
  with `### Limitations`, one level up from the `####` headings before it.
  A heading scan made for this round, over 11 of the book's repositories at
  the table survey's commits, found no other page whose headings skip a
  level after the first heading (the scan is not committed; see
  [results](../results.md#not-yet-written)).
- **Headings with no explicit id.** The three `####` headings and
  `### Limitations` have no `<a id>`. The only ids they have are the ones
  the published page generates from their text.
- **Anchors written with no space before the text**
  (`## <a id='prerequisites'></a>Prerequisites`), so the published page's
  generated id has no leading hyphen. For "Prerequisites" the generated id
  and the explicit one are the same word, so the published page has the id
  `prerequisites` twice.

## Heading tree to keep

```
h1 Managing access to Service Plans
  h2 Prerequisites                                          #prerequisites
  h2 Service Plan access                                    #display-access
  h2 Enabling access to Service Plans                       #enable-access
      h4 Enabling access to a subset of users               (generated) #enabling-access-to-a-subset-of-users
  h2 Deactivating access to Service Plans                   #disable-access
      h4 Deactivating access to all plans for all users     (generated) #deactivating-access-to-all-plans-for-all-users
      h4 Deactivating access for specific orgs or plans     (generated) #deactivating-access-for-specific-orgs-or-plans
    h3 Limitations                                          (generated) #limitations
```

**The skipped levels are kept.** Decision (this round): the outline is
preserved as written, so a conversion does not renumber the `####`
headings to `###`. Renumbering would be a deliberate restructuring and
would be recorded as a deviation; it is a question for the page's owner,
not for a converter.

## Anchors to keep

The four explicit ids, then the four generated ids of the headings that
have no explicit one, listed in [`access-control.anchors`](access-control.anchors).
Decision (this round): a generated id is kept when its heading has no
explicit id, because it is the only address that heading has.

### Links from other pages

| Anchor | Linked from |
|--------|-------------|
| `#enable-access` | [docs-services `managing-service-brokers.html.md.erb` L56](https://github.com/cloudfoundry/docs-services/blob/ccb0036407e4c2eabbb61a3b3de008f821f41c5b/managing-service-brokers.html.md.erb#L56), and at least 16 files in other repositories, most of them service broker READMEs, for example [cloudfoundry-samples/github-service-broker-ruby](https://github.com/cloudfoundry-samples/github-service-broker-ruby/blob/557463abd1c346c8b88b9175d9997a6587427b8f/README.md) and [cloudfoundry-community/elasticache-broker](https://github.com/cloudfoundry-community/elasticache-broker/blob/d0a66eab280793e3d2f342996e6c16a5cc6f9c8f/README.md) |
| `#disable-access` | [yugrinov/spring-cloud-services `installation.html.md.hbs`](https://github.com/yugrinov/spring-cloud-services/blob/c82e9572134b35e3af28d406593f1a9b11740feb/installation.html.md.hbs) |

**Already broken on the published page:** `#make-plans-public`, linked
from two repositories
([full list](../broken-links.md#access-control)):
[IronFoundry/if-service-broker](https://github.com/IronFoundry/if-service-broker/blob/fdc97f9ec8f21f5b3f820d9b03250b2c60c08f62/README.md)
and [teddyking/mongodb_broker](https://github.com/teddyking/mongodb_broker/blob/3e036673a9cd68c1b0eeb8bc2c1ff17453d825b2/README.md).
No heading on the current page has that id.

## Deviations

None. Body changes a tool needs (terminal blocks, see the results) are
recorded per tool.

## Checks

```bash
python3 -I ../checks/outline.py ../published/access-control.html BUILT.html --anchors access-control.anchors
```
