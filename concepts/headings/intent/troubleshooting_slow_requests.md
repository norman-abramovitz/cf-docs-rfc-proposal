# Intent: `troubleshooting_slow_requests`

- Source: [`../../tables/source/troubleshooting_slow_requests.html.md.erb`](../../tables/source/troubleshooting_slow_requests.html.md.erb)
- Published: <https://docs.cloudfoundry.org/adminguide/troubleshooting_slow_requests.html>
  (copy: [`../published/troubleshooting_slow_requests.html`](../published/troubleshooting_slow_requests.html))
- Anchors file: [`troubleshooting_slow_requests.anchors`](troubleshooting_slow_requests.anchors)

## Cases this page covers

- **A variable in a heading:**
  `### <a id="app_logs"></a> Use app logs to locate delays in <%= vars.app_runtime_abbr %>`
  (source line 422). The heading text, its table-of-contents entry and any
  id made from the text must show the value ("Cloud Foundry"), not the
  expression.
- **Ids that links on the same page point to.** Tables 5 and 6 link to
  `#gorouter-latency`, `#ops-recommendations` and `#total-latency`; the
  prose links to `#app_logs` and `#within-cf`.
- **Anchor with and without a space before the text.**
  `## <a id="overview"></a>App requests overview` has none; the other
  headings have one. On the published page this decides whether the
  generated id starts with a hyphen (`app-requests-overview` against
  `-find-the-cause-of-latency`).
- **An underscore in an id** (`app_logs`).

## Heading tree to keep

```
h1 Troubleshooting slow requests in Cloud Foundry
  h2 App requests overview                                       #overview
  h2 Find the cause of latency                                   #cause
    h3 Experiment 1: Measure total round-trip app requests       #total-latency
    h3 Experiment 2: View request time in access logs            #within-cf
    h3 Experiment 3: Duplicate latency on another endpoint       #duplicate-latency
    h3 Experiment 4: Remove the load balancer from request path  #remove-the-load-balancer
    h3 Experiment 5: Remove Gorouter from request path           #remove-the-gorouter
    h3 Experiment 6: Test the network between the router and the app   #test-internal-network
  h2 Investigate or address latency                              #next
    h3 Use app logs to locate delays in Cloud Foundry            #app_logs
    h3 Causes for Gorouter latency                               #gorouter-latency
    h3 Operations recommendations                                #ops-recommendations
```

## Anchors to keep

Every explicit id above (12), listed in
[`troubleshooting_slow_requests.anchors`](troubleshooting_slow_requests.anchors).
The published page's generated ids (`-experiment-1:-measure-total-round-trip-app-requests`)
are not kept (same decision as [metadata](metadata.md#anchors-to-keep)).

### Links from other pages

None found in the clones of the docs repositories or by GitHub code search
on 2026-10-10. The five links on the page itself are the ones that matter.

## Deviations

None. The body is the tables round's native conversion of the page; only
the heading lines differ between modes.

## Checks

```bash
python3 -I ../checks/outline.py ../published/troubleshooting_slow_requests.html BUILT.html --anchors troubleshooting_slow_requests.anchors
```
