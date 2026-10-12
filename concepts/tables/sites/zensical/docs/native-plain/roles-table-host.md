---
title: Roles table host
---

Host page for the `_oss_roles_table` partial, standing in for
`roles.html.md.erb`, which includes it with
an ERB `partial 'oss_roles_table'` call.

The following table describes the default permissions for various <%= vars.app_runtime_abbr %> roles in active orgs.

<% include "native-plain/_oss_roles_table.md" %>
