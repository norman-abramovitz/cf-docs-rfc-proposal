# Intent: `architecture`

- Source: [`../source/architecture.html.md.erb`](../source/architecture.html.md.erb)
  and its partials [`_log_cache`](../source/_log_cache.html.md.erb) and
  [`_syslog_agents`](../source/_syslog_agents.html.md.erb), cloudfoundry/docs-loggregator
- Excerpt: "Architecture reference diagrams" up to "System Metrics Agents
  architecture" (lines 12–94), without its two diagrams
- Published: <https://docs.cloudfoundry.org/loggregator/architecture.html>
  (copy: [`../published/architecture.html`](../published/architecture.html))
- Partials file: [`architecture.partials`](architecture.partials);
  anchors: [`architecture.anchors`](architecture.anchors)

## Cases this page covers

- **A partial after text in a list item.** `* **Log Cache:** <%= partial 'log_cache' %>`
  ([L59](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/architecture.html.md.erb#L59),
  L83, L89): the three calls of this kind in the book.
- **The same partial twice on one page** (`_log_cache`, L59 and L89).
- **Variables in a partial** (`_syslog_agents`: `platform_name`,
  `app_runtime_abbr`).

## What a conversion must keep

| # | Partial | Section | Place | After the host's words | Before the host's words |
|---|---|---|---|---|---|
| 1 | `_log_cache` | Loggregator Firehose architecture | list | "Log Cache:" | "Log Cache Syslog Server:" |
| 2 | `_syslog_agents` | Shared-nothing architecture | list | "Syslog Agent:" | "Syslog Binding Cache" |
| 3 | `_log_cache` | Shared-nothing architecture | list | "Log Cache:" | "Log Cache Syslog Server:" |

- **Each partial inside its list item**, right after the item's bold label,
  and the label not lost. `_log_cache`'s text appears exactly twice.
- **How it looks today.** The book renders the partial to HTML before the
  page's Markdown reads it, so the published item is
  `<p><strong>Log Cache:</strong> <p>Log Cache allows …</p></p>`
  ([published copy](../published/architecture.html), line 586). A browser
  ends the outer paragraph at the inner one, so readers see the label on a
  line of its own and the partial's text as a paragraph below it.

## Cleanup and deviations

- **Decision (this round):** where a tool cannot put a block partial after
  text on the same line, the label stays as the item's first paragraph and
  the partial follows as a block of the same item. That is how the
  published page already looks; the words are the same.
- **The diagrams** and their "View a larger version" links are left out of
  the excerpt; the text that mentions "the previous diagram" stays.
