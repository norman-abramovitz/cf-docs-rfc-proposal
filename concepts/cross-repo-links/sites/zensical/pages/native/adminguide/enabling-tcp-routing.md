---
title: "Enabling and configuring TCP routing in Cloud Foundry"
---


You can enable TCP routing in Cloud Foundry. Learn about TCP routing and go through the steps of enabling and configuring it.

## TCP routing overview {#overview}

## TCP routing architecture {#architecture}

The following example workflow ships with route ports, back end ports, and app ports:

1. You create a TCP route for your app based on a TCP domain and a route port, and
map this route to one or more apps. See [Create a Route](../devguide/deploy-apps/routes-domains.md#create-route) in _Configuring Routes and Domains_.

1. By default, the Diego Cell only routes requests to port `8080`, the app port, on the app
container internal interface. The app port is the port on which apps must listen. Developers
can use the Cloud Controller API to update the ports an app can receive requests on.

    For more
information, see [Configuring Apps to Listen on Custom Ports (Beta)](../devguide/custom-ports.md).

## Prerequisites for activating TCP routing {#prerequisites}

To set up networking
requirements:

1. Choose a domain from which you can create TCP routes for your apps. For
example, create a domain which is similar to your app domain but prefixed by the TCP subdomain,
such as `tcp.APP-DOMAIN.com`, where `APP-DOMAIN` is the name of your app domain.

1. Configure DNS to resolve this domain name to the IP address of a highly available load
balancer that can forward traffic for the domain to the TCP routers. For more information,
see [Domains](../devguide/deploy-apps/routes-domains.md#domains) in _Configuring Routes
and Domains_. If you are operating an environment that does not require high availability,
configure DNS to resolve the TCP domain name you have chosen directly to a single instance
of the TCP router.

### TLS for TCP Routing {#tls-tcp-routes}

#### Disabling TLS for TCP Routing {#disabling-tls-for-tcp-routing}

## Configure TCP routing after deploying Cloud Foundry {#post-deploy}

After you activate TCP routing and deploy Cloud Foundry, you must add the TCP
shared domain and configure org quotas that allow you to create TCP routes. To do this,
you must use the Cloud Foundry Command Line Interface (cf CLI) and have an admin user account.

For more information about the cf CLI, see [Using the Cloud Foundry Command Line Interface
(cf CLI)](../cf-cli/index.md).

### Configure Cloud Foundry with your TCP Domain {#configure-domain}

After you deploy Cloud Foundry, you must configure Cloud Foundry
with the domain that you configured in [Prerequisites for Enabling TCP Routing](#prerequisites).

### Configure a quota for TCP routes {#configure-quota}

For more information, see
[Creating and Modifying Quota Plans](./quota-plans.md).

## Create a TCP route {#create-tcp-route}

For information about creating a TCP route, see [Create a TCP Route with a Port](../devguide/deploy-apps/routes-domains.md#create-route-with-port) in _Configuring Routes
and Domains_.

## Modify TCP port reservations {#modify-ports}
