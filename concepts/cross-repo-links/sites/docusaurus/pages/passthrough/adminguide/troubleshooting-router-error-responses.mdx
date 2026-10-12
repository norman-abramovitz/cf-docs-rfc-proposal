---
title: "Troubleshooting router error responses in Cloud Foundry"
---


Are your 502 errors the result of your infrastructure, Cloud Foundry, or an app? This topic helps you understand and
debug these errors.

## Outer error responses overview {#overview}

In your deployment, 502 errors can come from any of the following:

- **Infrastructure**: issues with your load balancer or network can cause 502 errors.
- **Platform**: issues with Gorouter or Diego Cells can cause 502 errors.
See the following sections:
  - [Diagnose Gorouter Errors](#gorouter-errors)
  - [Diagnose Stale Routes in Gorouter](#diagnose-stale-routes)
  - [Gorouter Error Classification Table](#gorouter-error-classification)
- **App**: issues with an app's load or configuration can cause 502 errors.
See [Diagnose App Errors](#app-errors).

If you are unsure of the source of 502 errors, see [General Debugging Steps](#debugging-steps).

## General debugging steps {#debugging-steps}

Some general debugging steps for any issue resulting in 502 errors are as follows:

1. Gather the Gorouter logs and Diego Cell logs at the time of the incident.

1. Review the logs and consider the following:
    1. Which errors are the Gorouters returning?
    1. Is Gorouter's routing table accurate? Are the endpoints for the route as expected? For more information, see [Dynamic Routing Table](https://github.com/cloudfoundry/gorouter#dynamic-routing-table) in the Gorouter documentation on GitHub.
    1. Do the Diego Cell logs have anything interesting about unexpected app crashes or restarts?
    1. Is the app healthy and handling requests successfully? You can use request tracing headers to verify. For more information, see [HTTP Headers for Zipkin Tracing](../concepts/http-routing.html#zipkin-headers) in _HTTP Routing_.

1. Consider the following:
   - Does your load balancer log 502 errors, but Gorouter does not? This means that traffic is not reaching Gorouter.
   - Was there a recent platform change or upgrade that caused an increase in 502 errors?
   - Are there any suspicious [metrics](../running/all_metrics.html#routing) spiking? How is the CPU and memory utilization?

## Log formatting {#log-formatting}

### Levels {#levels}

### Message contents {#message-contents}

### Access logs {#access-logs}

For more information about identity-aware routing and how these fields are used for observability, see [Identity-aware routing](../concepts/identity-aware-routing.html).

## Diagnose Gorouter errors {#gorouter}

### Gorouter cannot connect to the app container {#cannot-connect}

### Gorouter errors after connecting {#connect-error}

- `read: connection reset by peer` errors.
When these errors occur, the Gorouter returns error to the client, marks backend ineligible, and does not retry another back end.
  - Only for idempotent requests and if [route-integrity](#tls-to-back-end) is enabled:

## Diagnose stale routes in Gorouter {#diagnose-stale-routes}

To disable this behavior, set `router.backends.enable_tls` to `false` as described in [TLS to apps and other back end services](../concepts/http-routing.html#tls-to-back-end) in _HTTP Routing_.

### Causes of stale routes {#stale-routes}

### How to locate stale routes {#stale-route-triage}

### How to fix stale routes {#stale-routes-fix}

The following procedure helps you fix stale routes:

1. Ensure that SSL verification is activated.
For more information, see [With TLS Enabled](../concepts/http-routing.html#with-tls) in _HTTP Routing_.

## Gorouter error classification table {#gorouter-error-classification}

## Diagnose app errors {#app-errors}

### Gorouter specific response headers {#gorouter-specific-response-headers}
