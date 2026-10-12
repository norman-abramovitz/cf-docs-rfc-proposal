# Cleanup list: code blocks the parsers read differently

Status: draft, incomplete — covers what is known as of 2026-10-11.

Code blocks whose source two Markdown parsers read differently: the
book's engine (Redcarpet, through the survey's model of it) and
commonmark.js, which stands in for the parsers the four tools use. In 14
files the two find different code blocks
([survey](survey/README.md#fences-only-the-books-engine-closes-and-other-disagreements)).
A **fence** is a code block between lines of three backticks; an
**indented block** is code marked only by four spaces of indent.

Decision (Docs WG lead, 2026-10-11): these are repaired at the source
before conversion, so that every tool reads the block the way the
published page shows it, or the way the author meant it where the
published page is wrong
([R-24](../../requirements/README.md#r-24) markup cleanup before
conversion; [convention 5](results.md#conventions-to-record)). The
three `<pre>` tags with curly quotes go in the same pass.

Line links point at the commits the survey read
([shas.txt](survey/shas.txt)).

## Fences right after a line of text

The book makes inline code of these; CommonMark makes a code block. The
published `backup` page shows L64-L66 as one `<code>` element running
over three lines. Fix: **add a blank line before the fence.**

| File | Lines |
|---|---|
| docs-bbr `backup.html.md.erb` | [L64-L66](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L64-L66), [L74-L77](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L74-L77) |
| docs-dev-guide `services/_using-vol-services.html.md.erb` | [L66-L68](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/_using-vol-services.html.md.erb#L66-L68) |
| docs-loggregator `opentelemetry.html.md.erb` | [L184-L211](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/opentelemetry.html.md.erb#L184-L211) |
| docs-deploying-cf `archive/azure.html.md.erb` | [L179-L181](https://github.com/cloudfoundry/docs-deploying-cf/blob/1113cfaf3626931c653c91dc8d537d7f181d6762/archive/azure.html.md.erb#L179-L181) |
| docs-book-cloudfoundry `docker/README.md` (not a page of the site) | [L6-L9](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/docker/README.md#L6-L9) |

## Fences closed only the book's way

| File | Lines | Fix |
|---|---|---|
| docs-bbr `backup.html.md.erb` | [L76](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L76) closes with `` ```<br> ``, which closes nothing | **make the line a plain closing fence** |
| docs-bbr `backup.html.md.erb` | [L359-L365](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/backup.html.md.erb#L359-L365) opens with four backticks and closes with three | **close with four backticks** (or open with three) |

## Fences indented four or more spaces deeper than their list item's text

One parser reads a fence, the other an indented block that shows the
fence lines as text. Fix: **indent the fence to the list item's text.**

| File | Lines | Published page today |
|---|---|---|
| docs-dev-guide `multiple-processes.html.md.erb` | [L20-L31](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/multiple-processes.html.md.erb#L20-L31) | shows the fence lines inside the block |
| docs-buildpacks `hwc/web-config-transform-buildpack.html.md.erb` | [L66-L73](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/hwc/web-config-transform-buildpack.html.md.erb#L66-L73) | right; CommonMark shows the fence lines |
| docs-buildpacks `java/java-tips.html.md.erb` | [L152-L160](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/java/java-tips.html.md.erb#L152-L160) | right; CommonMark shows the fence lines |

## Text indented four spaces

One parser reads an indented block, the other a paragraph or list item.

| File | Lines | Book | Fix |
|---|---|---|---|
| docs-buildpacks `hwc/index.html.md.erb` | [L141-L143](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/hwc/index.html.md.erb#L141-L143) | code | **write it as a fence with a type** |
| docs-buildpacks `upgrading_dependency_versions.html.md.erb` | [L135-L140](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/upgrading_dependency_versions.html.md.erb#L135-L140) | code | **write it as a fence with a type** |
| docs-bbr `bbr-devguide.html.md.erb` | [L186-L187](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/bbr-devguide.html.md.erb#L186-L187) | text | **remove the indent** |
| docs-bbr `external-blobstores.html.md.erb` | [L61-L62](https://github.com/cloudfoundry/docs-bbr/blob/51465950ce3a2196d66a9339086b94feed280c3e/external-blobstores.html.md.erb#L61-L62) | text | **remove the indent** |

## HTML indented four spaces

CommonMark reads an indented block that shows the HTML as text. Fix:
**indent the `<pre>` to its list item's text** (five spaces) in
`application-binding`, and **remove the indent** on the home page.

| File | Lines |
|---|---|
| docs-dev-guide `services/application-binding.html.md.erb` | [L253-L255](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/application-binding.html.md.erb#L253-L255), [L259-L261](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/application-binding.html.md.erb#L259-L261): `<pre class="terminal">` indented four spaces under list items whose text starts at column 5 |
| docs-book-cloudfoundry `master_middleman/source/index.html.md.erb` | [L42](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/index.html.md.erb#L42) onward: the book's home page, 785 lines that CommonMark reads as one code block |

## `<pre>` tags with curly quotes

`class=‘terminal’` uses curly quotes, so the class is not `terminal`.
Fix: **straight quotes**, `class="terminal"`.

| File | Lines |
|---|---|
| docs-running-cf `managing-cf/audit-events.html.md.erb` | [L42](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/managing-cf/audit-events.html.md.erb#L42) |
| docs-running-cf `managing-cf/usage-events.html.md.erb` | [L31](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/managing-cf/usage-events.html.md.erb#L31), [L102](https://github.com/cloudfoundry/docs-running-cf/blob/956acc86445d2f3cb29f031294f86f37f515b471/managing-cf/usage-events.html.md.erb#L102) |

## Not needed

Two files in `docs-dotnet-core-tutorial` (`docs/deploy-app.md`,
`docs/scale-vertical.md`) differ only in a block's trailing blank line.
The block's text is the same, so nothing needs fixing.
