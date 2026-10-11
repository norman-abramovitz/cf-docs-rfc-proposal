# Intent: `app-ssh-overview`

- Source: [`../source/app-ssh-overview.html.md.erb`](../source/app-ssh-overview.html.md.erb)
  (cloudfoundry/docs-dev-guide, whole page)
- Published: <https://docs.cloudfoundry.org/devguide/deploy-apps/app-ssh-overview.html>
  (copy: [`../published/app-ssh-overview.html`](../published/app-ssh-overview.html))
- Variables file (what the check compares): [`app-ssh-overview.vars`](app-ssh-overview.vars);
  anchors: [`app-ssh-overview.anchors`](app-ssh-overview.anchors)

## Cases this page covers

- **An HTML value used inside a sentence, in an HTML table cell**:
  `config_ssh_link` holds a sentence with an `<a>`. 28 of the book's 49
  uses of an HTML value sit inside a sentence
  ([survey](../survey/README.md#values-that-hold-markup-and-where-they-are-used)).
- **A Markdown value as a paragraph of its own**: `platform_ssh_configuration`
  holds a sentence with a Markdown link. Pages use Markdown values 48
  times.
- **A variable in a heading** that has an explicit id. 27 headings in the
  book hold a variable, all with an `<a id>`.
- **A variable that is not defined**: `mutual_tls_ssh`, one of 28 such
  names.
- **The tag written without spaces**, `<%=vars.config_ssh_link%>`; ERB
  reads it the same.
- **Links in values relative to the page**: both values link to
  `../../running/config-ssh.html`, which is right only from a page two
  folders deep.

## Variables to keep

| # | Variable | Value ([file](../source/template_variables.yml)) | Place | Renders as | Source |
|---|----------|-------|-------|------------|--------|
| 1 | `mutual_tls_ssh` | not defined | a paragraph of its own, after the opening | nothing | [L9](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/app-ssh-overview.html.md.erb#L9) |
| 2 | `app_runtime_abbr` | `Cloud Foundry` ([L25](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L25)) | text, "SSH access control hierarchy" | Cloud Foundry | [L19](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/app-ssh-overview.html.md.erb#L19) |
| 3 | `config_ssh_link` | `For more information, see <a href="../../running/config-ssh.html">Configuring SSH Access for Cloud Foundry</a>.` ([L326](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L326)) | end of the `Operator` row's last cell, after the cell's text | the sentence, with a link to `../../running/config-ssh.html` | [L31](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/app-ssh-overview.html.md.erb#L31) |
| 4 | `app_runtime_full` | `Cloud Foundry` ([L23](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L23)) | the heading `## <a id="platform-ssh-config"></a> Configuring SSH access for …` | Configuring SSH access for Cloud Foundry | [L64](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/app-ssh-overview.html.md.erb#L64) |
| 5 | `platform_ssh_configuration` | three sentences, the last with `[Configuring SSH Access](../../running/config-ssh.html)` ([L220](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L220)) | a paragraph of its own, the page's last | a paragraph with a link | [L66](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/app-ssh-overview.html.md.erb#L66) |

## What a conversion must keep

- **Each value's text in its place**, and its markup as markup: the link in
  the table cell and the link in the last paragraph are links
  ([published copy](../published/app-ssh-overview.html), lines 549 and
  585).
- **The heading's text with the value**, in the heading and in the table
  of contents, and its id `platform-ssh-config`.
- **Nothing where the undefined variable is**, and no variable syntax
  anywhere on the page.

## Cleanup and deviations

- **Link targets.** The published page writes the Markdown value's link as
  `/running/config-ssh.html` and the HTML value's as
  `../../running/config-ssh.html`. The check accepts any link whose target
  ends in `running/config-ssh.html`; where the target page lives after
  conversion is the cross-repository links concept's question
  ([R-08](../../../requirements/README.md#r-08) cross-repository links).
- **The undefined variable.** Decision (this round): native mode removes
  the reference, which renders as nothing today, so that the tool can
  require every name; passthrough keeps it, to show what each tool does
  with it.
- **The image** path becomes `images/ssh-app-access.png` (or the tool's
  image folder), because the test page sits in one folder.
- **No deviation** from the published text.
