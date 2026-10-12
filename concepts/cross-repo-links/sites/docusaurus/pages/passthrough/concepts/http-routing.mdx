---
title: "HTTP routing"
---


This topic tells you how the Gorouter, the main component in the Cloud Foundry routing tier, routes HTTP traffic within
Cloud Foundry.

For more information about routing, see [Routing](architecture/index.html#routing) in _Cloud Foundry Components_.

## HTTP headers {#http-headers}

### Header size limit {#header-size-limit}

### X-Forwarded Proto {#X-Forwarded-Proto}

### X-Forwarded-For {#X-Forwarded-For}

If your load balancer terminates TLS on the client side of the Gorouter, it must append these headers to requests forwarded to the Gorouter.
For more information, see [Securing Traffic into Cloud Foundry](../adminguide/securing-traffic.html).

### HTTP headers for Zipkin tracing {#zipkin-headers}

For more information about Zipkin tracing, see [Enabling Zipkin Tracing](../adminguide/zipkin_tracing.html).

### HTTP headers for W3C tracing {#w3c-headers}

When W3C tracing is enabled in Cloud Foundry, the Gorouter generates W3C HTTP headers unless they are provided
by the client, as described in [Unique trace identification](../adminguide/distributed-tracing.html#unique-trace-id).

### HTTP headers for app instance routing {#app-instance-routing}

### HTTP headers for process instance routing {#process-instance-routing}

Apps that have <a href="https://docs.cloudfoundry.org/devguide/multiple-processes.html">multiple processes</a> or apps that have been pushed with the rolling or canary deployment strategies cannot be reliably routed to using the <code>X-Cf-App-Instance</code> header. Users who wish to route to a specific instance of these apps should use the <code>X-Cf-Process-Instance</code> header.

### Forwarding client certificate to apps {#forward-client-cert}

#### Terminating TLS for the First Time at the Load Balancer {#forward-mtls}

#### Terminating TLS for the First Time at the Gorouter {#xfcc_router_tls}

## Client-Side TLS {#client-side-tls}

## TLS to apps and other back end services {#tls-to-back-end}

## Preventing mis-routes {#consistency}

### Without TLS to back ends enabled {#without-tls}

### Consistency mode can differ by instance group {#config-by-instance-group}

### Configuring validation of app instance identity with TLS {#app-valid-tls-config}

## Router balancing algorithm {#balancing-algorithm}

As an application developer, you can configure the load balancing algorithm by following the guide [Configuring per-route options](../devguide/custom-per-route-options.html) which describes how to specify load balancing algorithms scoped at the application level.

The possible options:

* `round-robin`. For more information, see [Round-Robin Load Balancing](#round-robin).

* `least-connection`. For more information, see [Least-Connection Load Balancing](#least-connection).

By default, the Gorouter's balancing algorithm availability zone preference is None. We do not recommend changing this value. For more information about these values, see [Load Balancing AZ Preference](#balancing-algorithm-az-preference).

### Round robin load balancing {#round-robin}

### Least connection load balancing {#least-connection}

### Load balancing availability zone preference {#balancing-algorithm-az-preference}

## WebSockets {#sockets}

To support WebSockets, the operator must configure the load balancer correctly. Depending on the configuration, clients may have to use a different port for WebSocket connections, such as port 4443, or a different domain name. For more information, see [Supporting WebSockets](../adminguide/supporting-websockets.html).

## Session affinity {#sessions}

## Keep alive connections {#keepalive}

### Front end clients {#front-end}

### Back end servers {#back-end}

For more information, see [Keep alive connections](/concepts/http-routing.html#keepalive) in _HTTP Routing_.

## Transparent retries {#retry}

In all cases, if the app still does not respond to the request, the Gorouter returns a `502` error. For more
information, see [Troubleshooting Router Error Responses](../adminguide/troubleshooting-router-error-responses.html).
