---
title: Variable checks
---

# Variable checks

How this site handles the variable and partial cases the test pages need.

<p><span id="defined">Defined: <%= vars.platform_name %></span></p>

<p><span id="undefined">Undefined: <%= vars.metadata_ref %></span></p>

<div id="html-raw"><%= vars.route_services %></div>

<% include "_check_partial.md" %>
