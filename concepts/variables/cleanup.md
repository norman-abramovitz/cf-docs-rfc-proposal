# Cleanup list: undefined and empty variables

Status: draft, incomplete — covers what is known as of 2026-10-11.

Every place a page in the book prints a variable that has no value. A
**variable** is a name in `<%= vars.name %>` whose value comes from the
book's `config/template_variables.yml`. A name is **not defined** when no
key in that file carries it, and **empty** when its key has no value. Both
print nothing on the published pages today, and the build reports
neither ([survey](survey/README.md#variables-used-but-not-defined-or-empty)).
After conversion every tool fails or warns on them
([convention 3](results.md#conventions-to-record)).

Decision (Docs WG lead, 2026-10-11): the references are removed before
conversion, and this list stays with the Docs WG, which does the
conversion ([R-24](../../requirements/README.md#r-24) markup cleanup
before conversion; [convention 4](results.md#conventions-to-record)).
The empty keys are removed from `template_variables.yml` as well (Docs WG
lead, 2026-10-11): the 31 that the references use, and the 20 that no
page uses; see [Empty keys](#empty-keys).

**82 references, 59 names, 47 files, 9 repositories**: 38 references to
28 names that are not defined, 44 to 31 names that are empty. One
reference is in a partial (`_using-vol-services`). Links point at the
commits the survey read ([shas.txt](survey/shas.txt)).

How to read the tables:

- **Fix: delete the line** — the line holds only the reference, so the
  page loses nothing. 58 rows.
- **Fix: remove the reference** — the line has text around it; take out
  the `<%= vars.… %>` and keep the text. 24 rows.
- A page owner who knows what the text should say can add a value
  instead, and the row is dropped from the list.

Regenerate the tables with [survey/cleanup.py](survey/cleanup.py).

## docs-bbr

| File and line | Name | Kind | Line today | Fix |
|---|---|---|---|---|
| [index.html.md.erb L36](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/index.html.md.erb#L36) | `bbr_ert` | empty | `<%= vars.bbr_ert %>` | delete the line |
| [installing.html.md.erb L28](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/installing.html.md.erb#L28) | `bbr_space` | empty | `* Your jumpbox must have sufficient space for the backup. <%= vars.bbr_space %>` | remove the reference |

## docs-buildpacks

| File and line | Name | Kind | Line today | Fix |
|---|---|---|---|---|
| [java/getting-started-deploying-apps/gsg-grails.html.md.erb L6](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L6) | `GSG_intro_sentence` | not defined | `<%=vars.GSG_intro_sentence%>` | delete the line |
| [java/getting-started-deploying-apps/gsg-grails.html.md.erb L111](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L111) | `dev_console_1` | empty | `…ibes using the cf CLI to configure a ClearDB managed service instance for an app. <%=vars.dev_console_1%>` | remove the reference |
| [java/getting-started-deploying-apps/gsg-grails.html.md.erb L175](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L175) | `dev_console_5` | empty | `<%=vars.dev_console_5%>` | delete the line |
| [java/getting-started-deploying-apps/gsg-grails.html.md.erb L205](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L205) | `gen_GSG` | empty | `<%= vars.gen_GSG %>` | delete the line |
| [java/getting-started-deploying-apps/gsg-grails.html.md.erb L314](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L314) | `dev_console_4` | empty | `…nage Your Application with the cf CLI](#cli-manage) section for more information. <%=vars.dev_console_4%>` | remove the reference |
| [java/getting-started-deploying-apps/gsg-grails.html.md.erb L364](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-grails.html.md.erb#L364) | `dev_console_note` | empty | `<%=vars.dev_console_note%>` | delete the line |
| [java/getting-started-deploying-apps/gsg-ratpack.html.md.erb L6](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-ratpack.html.md.erb#L6) | `GSG_intro_sentence` | not defined | `<%=vars.GSG_intro_sentence%>` | delete the line |
| [java/getting-started-deploying-apps/gsg-ratpack.html.md.erb L95](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-ratpack.html.md.erb#L95) | `dev_console_1` | empty | `Learn how to use the CLI to configure a Redis managed service instance for an app. <%=vars.dev_console_1%>` | remove the reference |
| [java/getting-started-deploying-apps/gsg-ratpack.html.md.erb L163](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-ratpack.html.md.erb#L163) | `dev_console_5` | empty | `<%=vars.dev_console_5%>` | delete the line |
| [java/getting-started-deploying-apps/gsg-ratpack.html.md.erb L193](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-ratpack.html.md.erb#L193) | `gen_GSG` | empty | `<%=vars.gen_GSG%>` | delete the line |
| [java/getting-started-deploying-apps/gsg-ratpack.html.md.erb L285](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-ratpack.html.md.erb#L285) | `dev_console_4` | empty | `…nage Your Application with the cf CLI](#cli-manage) section for more information. <%=vars.dev_console_4%>` | remove the reference |
| [java/getting-started-deploying-apps/gsg-ratpack.html.md.erb L335](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-ratpack.html.md.erb#L335) | `dev_console_note` | empty | `<%=vars.dev_console_note%>` | delete the line |
| [java/getting-started-deploying-apps/gsg-spring.html.md.erb L8](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-spring.html.md.erb#L8) | `GSG_intro_sentence` | not defined | `<%=vars.GSG_intro_sentence%>` | delete the line |
| [java/getting-started-deploying-apps/gsg-spring.html.md.erb L165](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-spring.html.md.erb#L165) | `gen_GSG` | empty | `<%=vars.gen_GSG%>` | delete the line |
| [java/getting-started-deploying-apps/gsg-spring.html.md.erb L258](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-spring.html.md.erb#L258) | `dev_console_4` | empty | `See [Manage your application with the cf CLI](#cli-manage) for more information. <%=vars.dev_console_4%>` | remove the reference |
| [java/getting-started-deploying-apps/gsg-spring.html.md.erb L308](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/getting-started-deploying-apps/gsg-spring.html.md.erb#L308) | `dev_console_note` | empty | `<%=vars.dev_console_note%>` | delete the line |
| [ruby/gsg-ruby.html.md.erb L6](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/ruby/gsg-ruby.html.md.erb#L6) | `GSG_intro_sentence` | not defined | `<%=vars.GSG_intro_sentence%>` | delete the line |
| [ruby/gsg-ruby.html.md.erb L34](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/ruby/gsg-ruby.html.md.erb#L34) | `dev_console_1` | empty | `Use the cf CLI to configure a Redis Cloud managed service instance for an app. <%=vars.dev_console_1%>` | remove the reference |
| [ruby/gsg-ruby.html.md.erb L117](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/ruby/gsg-ruby.html.md.erb#L117) | `dev_console_5` | empty | `<%=vars.dev_console_5%>` | delete the line |
| [ruby/gsg-ruby.html.md.erb L148](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/ruby/gsg-ruby.html.md.erb#L148) | `gen_GSG` | empty | `<%=vars.gen_GSG%>` | delete the line |
| [ruby/gsg-ruby.html.md.erb L243](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/ruby/gsg-ruby.html.md.erb#L243) | `dev_console_4` | empty | `…nage Your Application with the cf CLI](#cli-manage) section for more information. <%=vars.dev_console_4%>` | remove the reference |
| [ruby/gsg-ruby.html.md.erb L256](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/ruby/gsg-ruby.html.md.erb#L256) | `dev_console_note` | empty | `<%=vars.dev_console_note%>` | delete the line |

## docs-cf-admin

| File and line | Name | Kind | Line today | Fix |
|---|---|---|---|---|
| [enabling_ipv6.html.md.erb L26](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/enabling_ipv6.html.md.erb#L26) | `custom_load_balancer` | empty | `1. Set up an external load balancer for your <%= vars.app_runtime_abbr %> deployment. <%=` | remove the reference |
| [listing-feature-flags.html.md.erb L70](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/listing-feature-flags.html.md.erb#L70) | `user_org_creation` | empty | `` * `user_org_creation`: Any user can create an org. <%= vars.user_org_creation %> Minimum CC API version: 2.12. `` | remove the reference |
| [metadata.html.md.erb L22](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/metadata.html.md.erb#L22) | `metadata_ref` | not defined | `<%= vars.metadata_ref %>` | delete the line |
| [notifications.html.md.erb L18](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/notifications.html.md.erb#L18) | `asg_notifications_prereq` | empty | `<%= vars.asg_notifications_prereq %>` | delete the line |
| [securing-traffic.html.md.erb L79](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/securing-traffic.html.md.erb#L79) | `ssl_cert_ert` | not defined | `<%= vars.ssl_cert_ert %>` | delete the line |
| [start-stop-vms.html.md.erb L14](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/start-stop-vms.html.md.erb#L14) | `bosh_cli_link` | not defined | `This procedure uses the BOSH Command Line Interface (BOSH CLI). <%= vars.bosh_cli_link %>` | remove the reference |
| [supporting-websockets.html.md.erb L19](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/supporting-websockets.html.md.erb#L19) | `or_apps_man2` | empty | `…ontroller to developers using the Cloud Foundry Command Line Interface (cf CLI) <%= vars.or_apps_man2 %>.` | remove the reference |
| [troubleshooting-router-error-responses.html.md.erb L29](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting-router-error-responses.html.md.erb#L29) | `gather_routing_logs` | not defined | `1. Gather the Gorouter logs and Diego Cell logs at the time of the incident. <%= vars.gather_routing_logs %>` | remove the reference |
| [troubleshooting_slow_requests.html.md.erb L257](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting_slow_requests.html.md.erb#L257) | `bosh_cli_link` | not defined | `` Where `ROUTER-GUID` is the unique identifier for the router VM. <%= vars.bosh_cli_link %> `` | remove the reference |
| [troubleshooting_slow_requests.html.md.erb L322](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting_slow_requests.html.md.erb#L322) | `bosh_cli_link` | not defined | `` Where `ROUTER-GUID` is the unique identifier for the router VM. <%= vars.bosh_cli_link %> `` | remove the reference |
| [troubleshooting_slow_requests.html.md.erb L367](https://github.com/cloudfoundry/docs-cf-admin/blob/13826fa7d93eee66902c4a2187a96b884137b58a/troubleshooting_slow_requests.html.md.erb#L367) | `bosh_cli_link` | not defined | `identifier for the router VM. <%= vars.bosh_cli_link %>` | remove the reference |

## docs-cloudfoundry-concepts

| File and line | Name | Kind | Line today | Fix |
|---|---|---|---|---|
| [architecture/garden.html.md.erb L35](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/architecture/garden.html.md.erb#L35) | `garden_runc` | not defined | `<%= vars.garden_runc %>` | delete the line |
| [architecture/index.html.md.erb L65](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/architecture/index.html.md.erb#L65) | `blobstore_kb` | empty | `…bstore as either an internal server or an external S3 or S3-compatible endpoint. <%= vars.blobstore_kb %>` | remove the reference |
| [asg.html.md.erb L130](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/asg.html.md.erb#L130) | `asg_note` | not defined | `<%= vars.asg_note %>` | delete the line |
| [diego/diego-architecture.html.md.erb L39](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/diego/diego-architecture.html.md.erb#L39) | `vm_note` | not defined | `<%= vars.vm_note %>` | delete the line |
| [diego/diego-architecture.html.md.erb L182](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/diego/diego-architecture.html.md.erb#L182) | `best_practices_link` | not defined | `… there might not be enough time to rotate the certificates before expiry. <%= vars.best_practices_link %>` | remove the reference |
| [high-availability.html.md.erb L48](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/high-availability.html.md.erb#L48) | `external_lb` | not defined | `<%= vars.external_lb %>` | delete the line |
| [high-availability.html.md.erb L100](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/high-availability.html.md.erb#L100) | `scaling_ert` | empty | `<%= vars.scaling_ert %>` | delete the line |
| [high-availability.html.md.erb L114](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/high-availability.html.md.erb#L114) | `om_resurrector_header` | empty | `<%= vars.om_resurrector_header %>` | delete the line |
| [high-availability.html.md.erb L116](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/high-availability.html.md.erb#L116) | `om_resurrector_text` | empty | `<%= vars.om_resurrector_text %>` | delete the line |
| [high-availability.html.md.erb L125](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/high-availability.html.md.erb#L125) | `pcf_pools` | not defined | `<%= vars.pcf_pools %>` | delete the line |
| [high-availability.html.md.erb L130](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/high-availability.html.md.erb#L130) | `scaling_ert_db` | empty | `backup and restore where possible. <%= vars.scaling_ert_db %>` | remove the reference |
| [maintaining-high-availability.html.md.erb L16](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/maintaining-high-availability.html.md.erb#L16) | `azs` | empty | `<%= vars.azs %>` | delete the line |
| [overview.html.md.erb L111](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/overview.html.md.erb#L111) | `ops_manager` | not defined | `…nts access to BOSH</li><li>Holds accounts for <%= vars.ops_manager %> operators who deploy runtimes, serv…` | remove the reference |
| [overview.html.md.erb L206](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/overview.html.md.erb#L206) | `concepts_sf_vs_full_header` | empty | `<%= vars.concepts_sf_vs_full_header %>` | delete the line |
| [overview.html.md.erb L208](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/overview.html.md.erb#L208) | `small_footprint_comparison` | empty | `<%= vars.small_footprint_comparison %>` | delete the line |
| [overview.html.md.erb L214](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/overview.html.md.erb#L214) | `concepts_product_model_header` | empty | `<%= vars.concepts_product_model_header %>` | delete the line |
| [overview.html.md.erb L219](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/overview.html.md.erb#L219) | `concepts_product_model_image` | empty | `<%= vars.concepts_product_model_image %>` | delete the line |
| [security.html.md.erb L146](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/security.html.md.erb#L146) | `console_links` | empty | `<%= vars.console_links %>` | delete the line |
| [security.html.md.erb L211](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/security.html.md.erb#L211) | `ipsec_note` | empty | `<%= vars.ipsec_note %>` | delete the line |
| [security.html.md.erb L213](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/security.html.md.erb#L213) | `compliance_links` | not defined | `<%= vars.compliance_links %>` | delete the line |
| [security.html.md.erb L222](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/security.html.md.erb#L222) | `app_svc_links` | not defined | `<%= vars.app_svc_links %>` | delete the line |

## docs-dev-guide

| File and line | Name | Kind | Line today | Fix |
|---|---|---|---|---|
| [capi/client-libraries.html.md.erb L13](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/capi/client-libraries.html.md.erb#L13) | `capi_link` | not defined | `<%= vars.capi_link %>` | delete the line |
| [deploy-apps/app-lifecycle.html.md.erb L49](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/app-lifecycle.html.md.erb#L49) | `app_graceful_shutdown_config` | not defined | `<%= vars.app_graceful_shutdown_config %>` | delete the line |
| [deploy-apps/app-ssh-overview.html.md.erb L9](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/app-ssh-overview.html.md.erb#L9) | `mutual_tls_ssh` | not defined | `<%= vars.mutual_tls_ssh %>` | delete the line |
| [deploy-apps/cf-networking.html.md.erb L14](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/cf-networking.html.md.erb#L14) | `app_traffic_logging` | not defined | `<%= vars.app_traffic_logging %>` | delete the line |
| [deploy-apps/cf-networking.html.md.erb L27](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/cf-networking.html.md.erb#L27) | `app_man_network` | not defined | `<%= vars.app_man_network %>` | delete the line |
| [deploy-apps/cf-scale.html.md.erb L17](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/cf-scale.html.md.erb#L17) | `autoscaler_note_dev_guide` | not defined | `<%=vars.autoscaler_note_dev_guide%>` | delete the line |
| [deploy-apps/deploy-app.html.md.erb L77](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/deploy-app.html.md.erb#L77) | `ssl` | empty | `<%= vars.ssl %>` | delete the line |
| [deploy-apps/push-docker.html.md.erb L27](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/push-docker.html.md.erb#L27) | `docker_auth1` | not defined | `* The location of the Docker image on Docker Hub or another Docker registry. <%= vars.docker_auth1 %>` | remove the reference |
| [deploy-apps/routes-domains.html.md.erb L836](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L836) | `domains_on_hosted` | not defined | `<%= vars.domains_on_hosted %>` | delete the line |
| [deploy-apps/routes-domains.html.md.erb L902](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/routes-domains.html.md.erb#L902) | `dns_warning` | not defined | `<%= vars.dns_warning %>` | delete the line |
| [deploy-apps/ssh-apps.html.md.erb L17](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/ssh-apps.html.md.erb#L17) | `mutual_tls_ssh` | not defined | `<%= vars.mutual_tls_ssh %>` | delete the line |
| [deploy-apps/ssh-services.html.md.erb L12](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/ssh-services.html.md.erb#L12) | `mutual_tls_ssh` | not defined | `<%= vars.mutual_tls_ssh %>` | delete the line |
| [deploy-apps/streaming-logs.html.md.erb L31](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/streaming-logs.html.md.erb#L31) | `human_readable_timestamp` | empty | `<%= vars.human_readable_timestamp %>` | delete the line |
| [index.html.md.erb L7](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/index.html.md.erb#L7) | `gsg_app_video_link` | not defined | `<%= vars.gsg_app_video_link %>` | delete the line |
| [services/_using-vol-services.html.md.erb L436](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/_using-vol-services.html.md.erb#L436) | `external_vol_smb_note` | empty | `<%= vars.external_vol_smb_note %>` | delete the line |
| [services/route-binding.html.md.erb L9](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/route-binding.html.md.erb#L9) | `route_services_appsman2` | empty | `<%= vars.route_services_appsman2 %>` | delete the line |
| [services/user-provided.html.md.erb L12](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/user-provided.html.md.erb#L12) | `user_provided_apps_man` | empty | `<%= vars.user_provided_apps_man %>` | delete the line |
| [using-tasks.html.md.erb L16](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/using-tasks.html.md.erb#L16) | `tasks_ai` | empty | `<%= vars.tasks_ai %>` | delete the line |

## docs-loggregator

| File and line | Name | Kind | Line today | Fix |
|---|---|---|---|---|
| [cli-plugin.html.md.erb L14](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/cli-plugin.html.md.erb#L14) | `configure_system_logging_link` | not defined | `<%= vars.configure_system_logging_link %>` | delete the line |
| [data-sources.html.md.erb L153](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/data-sources.html.md.erb#L153) | `custom_metrics_footnote` | not defined | `<%= vars.custom_metrics_footnote %>` | delete the line |
| [log-ops-guide.html.md.erb L100](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/log-ops-guide.html.md.erb#L100) | `configure_system_logging_link` | not defined | `…onfigure an aggregate log and metric drain for your foundation. <%= vars.configure_system_logging_link %>` | remove the reference |
| [nozzle-tutorial.html.md.erb L23](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/nozzle-tutorial.html.md.erb#L23) | `configure_system_logging_link` | not defined | `aggregate log and metric drain for your foundation. <%= vars.configure_system_logging_link %>` | remove the reference |

## docs-running-cf

| File and line | Name | Kind | Line today | Fix |
|---|---|---|---|---|
| [hm-notifications.html.md.erb L49](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/hm-notifications.html.md.erb#L49) | `email_notifications` | empty | `<%= vars.email_notifications %>` | delete the line |

## docs-services

| File and line | Name | Kind | Line today | Fix |
|---|---|---|---|---|
| [index.html.md.erb L13](https://github.com/cloudfoundry/docs-services/blob/ccb0036407e4c2eabbb61a3b3de008f821f41c5b/index.html.md.erb#L13) | `tiledev_link` | not defined | `<%= vars.tiledev_link %>` | delete the line |
| [overview.html.md.erb L110](https://github.com/cloudfoundry/docs-services/blob/ccb0036407e4c2eabbb61a3b3de008f821f41c5b/overview.html.md.erb#L110) | `cli_install_link` | not defined | `For information about downloading, installing, and uninstalling the cf CLI, see <%= vars.cli_install_link %>.` | remove the reference |

## docs-uaa

| File and line | Name | Kind | Line today | Fix |
|---|---|---|---|---|
| [uaa-user-management.html.md.erb L371](https://github.com/cloudfoundry/docs-uaa/blob/216c797cfa1a971cf0f9e53eb3e4803aaf914a94/uaa-user-management.html.md.erb#L371) | `pw_policy` | empty | `<%= vars.pw_policy %>` | delete the line |

## Empty keys

| Key | Line | References today |
|---|---|---|
| `product_link` | [L9](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L9) | none |
| `asg_notifications_prereq` | [L62](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L62) | 1 |
| `azs` | [L64](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L64) | 1 |
| `bbr_ert` | [L66](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L66) | 1 |
| `bbr_space` | [L67](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L67) | 1 |
| `bbr_rn_intro` | [L68](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L68) | none |
| `bbr_rn_compatibility` | [L69](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L69) | none |
| `blobstore_kb` | [L72](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L72) | 1 |
| `Cloud Foundry has used two architectures for managing application containers` | [L79](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L79) | none |
| `cloud_controller_dea_agent` | [L80](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L80) | none |
| `cloud_controller_dea_algorithm` | [L81](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L81) | none |
| `concepts_sf_vs_full_header` | [L84](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L84) | 1 |
| `concepts_product_model_header` | [L85](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L85) | 1 |
| `concepts_product_model_image` | [L86](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L86) | 1 |
| `small_footprint_comparison` | [L87](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L87) | 1 |
| `console_links` | [L90](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L90) | 1 |
| `contact_support` | [L91](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L91) | none |
| `cookies_shared_domain_1` | [L94](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L94) | none |
| `custom_load_balancer` | [L98](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L98) | 1 |
| `dea_diego_table_row` | [L102](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L102) | none |
| `dev_console_1` | [L145](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L145) | 3 |
| `dev_console_3` | [L147](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L147) | none |
| `dev_console_4` | [L148](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L148) | 4 |
| `dev_console_5` | [L149](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L149) | 3 |
| `dev_console_note` | [L150](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L150) | 4 |
| `domains_shared_domains` | [L159](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L159) | none |
| `email_notifications` | [L161](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L161) | 1 |
| `external_vol_smb_note` | [L175](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L175) | 1 |
| `gen_GSG` | [L178](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L178) | 4 |
| `ipsec_note` | [L188](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L188) | 1 |
| `log_management` | [L198](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L198) | none |
| `loggregator_log_cache_link` | [L203](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L203) | none |
| `om_resurrector_header` | [L216](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L216) | 1 |
| `om_resurrector_text` | [L217](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L217) | 1 |
| `or_apps_man2` | [L218](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L218) | 1 |
| `pw_policy` | [L226](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L226) | 1 |
| `route_services_apps_manager` | [L236](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L236) | none |
| `scaling_ert_db` | [L288](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L288) | 1 |
| `scaling_ert` | [L289](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L289) | 1 |
| `ssl` | [L298](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L298) | 1 |
| `tcp_port_review` | [L304](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L304) | none |
| `user_org_creation` | [L311](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L311) | 1 |
| `warden_garden` | [L313](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L313) | none |
| `ssl_haproxy` | [L320](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L320) | none |
| `tasks_ai` | [L321](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L321) | 1 |
| `isolation_segments_create` | [L323](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L323) | none |
| `ha_ert` | [L328](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L328) | none |
| `route_services_appsman1` | [L329](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L329) | none |
| `route_services_appsman2` | [L330](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L330) | 1 |
| `user_provided_apps_man` | [L331](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L331) | 1 |
| `human_readable_timestamp` | [L365](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L365) | 1 |
