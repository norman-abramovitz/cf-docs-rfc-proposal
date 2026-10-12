# Cleanup list: partial names held in variables

Status: draft, incomplete — covers what is known as of 2026-10-11.

A **partial** is a file whose name starts with `_` and whose text a page
includes with `<%= partial 'name' %>`. Ten keys in the book's
`config/template_variables.yml` hold a partial's name, so that a page
could include `<%= partial vars.key %>` and each edition's book could
pick its own partial. No page does that any more: the pages that include
these partials name them directly
([survey](survey/README.md#partial-names-held-in-variables)).

Decision (Docs WG lead, 2026-10-11): partial names in variables are not
needed, and the ten keys are removed before conversion
([R-24](../../requirements/README.md#r-24) markup cleanup before
conversion; [recommendation](results.md#are-partial-names-in-variables-still-needed)).
The one remaining mention, an ERB comment, goes with them.

## Keys to remove from template_variables.yml

| Variable | Value | Partial | Line |
|---|---|---|---|
| `concepts_product_model_text` | `"./overview_model"` | `_overview_model` (concepts) | [L88](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L88) |
| `roles_table` | `"_oss_roles_table"` | `_oss_roles_table` (concepts) | [L231](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L231) |
| `scale_table` | `"oss_scale_table"` | `_oss_scale_table` (concepts) | [L287](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L287) |
| `suspended_roles_table` | `"_suspended_org_roles_table"` | `_suspended_org_roles_table` (concepts) | [L301](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L301) |
| `tcp_port` | `"../adminguide/tcp_modify_ports"` | `_tcp_modify_ports` (cf-admin) | [L305](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L305) |
| `zipkin_enable` | `zipkin_oss_config` | `_zipkin_oss_config` (cf-admin) | [L314](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L314) |
| `gorouter_client_cert` | `"gorouter_client_cert_oss"` | `_gorouter_client_cert_oss` (cf-admin) | [L344](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L344) |
| `ssl_termin_gorouter` | `"ssl_termin_gorouter_oss"` | `_ssl_termin_gorouter_oss` (cf-admin) | [L345](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L345) |
| `ssl_termin_lb_only` | `"ssl_termin_lb_only_oss"` | `_ssl_termin_lb_only_oss` (cf-admin) | [L346](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L346) |
| `ssl_termin_gorouter_lb` | `"ssl_termin_gorouter_lb_oss"` | `_ssl_termin_gorouter_lb_oss` (cf-admin) | [L347](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L347) |

## Comment to remove

| File and line | Line today | Fix |
|---|---|---|
| [overview.html.md.erb L216](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/overview.html.md.erb#L216) (docs-cloudfoundry-concepts) | `<%# partials for vars.concepts_product_model_text %>` | delete the line |
