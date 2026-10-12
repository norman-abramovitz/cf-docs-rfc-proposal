# Sources

Verbatim copies of the files new in this round, taken on 2026-10-11 at the
commits the [link survey](../survey/README.md) read (the partials survey's
commits, [survey/shas.txt](../survey/shas.txt)). Nothing in this directory is
edited; every change lives in `../sites/`. Three test pages and one partial
were copied in earlier rounds and are used from there.

| File | Repository | Path | Commit | License |
|------|------------|------|--------|---------|
| `http-routing.html.md.erb` | [cloudfoundry/docs-cloudfoundry-concepts](https://github.com/cloudfoundry/docs-cloudfoundry-concepts) | `http-routing.html.md.erb` | `97e0d0b25f059c06edd25e30355d26eb93dc560a` | Apache-2.0 |
| `redirects.rb` | [cloudfoundry/docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry) | `redirects.rb` | `30dfa57692253a6ae1b3df0726444b1e32852c91` | Apache-2.0 |
| [`../../variables/source/troubleshooting-router-error-responses.html.md.erb`](../../variables/source/troubleshooting-router-error-responses.html.md.erb) | cloudfoundry/docs-cf-admin | `troubleshooting-router-error-responses.html.md.erb` | see [variables SOURCES](../../variables/source/SOURCES.md) | Apache-2.0 |
| [`../../partials/source/enabling-tcp-routing.html.md.erb`](../../partials/source/enabling-tcp-routing.html.md.erb) | cloudfoundry/docs-cf-admin | `enabling-tcp-routing.html.md.erb` | see [partials SOURCES](../../partials/source/SOURCES.md) | Apache-2.0 |
| [`../../headings/source/routes-domains.html.md.erb`](../../headings/source/routes-domains.html.md.erb) | cloudfoundry/docs-dev-guide | `deploy-apps/routes-domains.html.md.erb` | see [headings SOURCES](../../headings/source/SOURCES.md) | Apache-2.0 |
| [`../../partials/source/_routing_conflict.html.md.erb`](../../partials/source/_routing_conflict.html.md.erb) | cloudfoundry/docs-dev-guide | `deploy-apps/_routing_conflict.html.md.erb` | see [partials SOURCES](../../partials/source/SOURCES.md) | Apache-2.0 |
| [`../../variables/source/template_variables.yml`](../../variables/source/template_variables.yml) | cloudfoundry/docs-book-cloudfoundry | `config/template_variables.yml` (the whole file) | see [variables SOURCES](../../variables/source/SOURCES.md) | Apache-2.0 |

The earlier rounds' copies are identical to the files at the survey's
commits (checked with `diff` on 2026-10-11 against the clones the survey
read).

Links to the files at those commits:
[http-routing.html.md.erb](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/http-routing.html.md.erb),
[redirects.rb](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb).
Licenses:
[docs-cloudfoundry-concepts LICENSE](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/LICENSE),
[docs-book-cloudfoundry LICENSE](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/LICENSE).

## Notes

- **Excerpts.** The sites keep every heading of each test page, with its id,
  so the outline check compares whole pages; under the headings they keep
  the lines that hold the links under test. The line numbers are those of
  the source files:
  - `http-routing`: 6–9, 43–44, 65, 70–72, 167, 352, 354–358, 370, 403,
    455, 491–492.
  - `troubleshooting-router-error-responses`: 7–8, 12–23, 27–40, 173,
    202–204, 234, 288–291 (the note under step 1 of "How to fix stale
    routes" is left out).
  - `enabling-tcp-routing`: 6, 22–25, 50–55, 63–75, 116–121, 125–126,
    160–161, 222–223.
  - `routes-domains`: 6–8, 49, 54, 62, 66, 402, 406–408.
  Decision (this round): bodies outside the links are left out; notes,
  tables, code blocks and images are other rounds' questions.
- **Partials and variables in the test pages are written in place**, as the
  book renders them: the two partials of `http-routing` that hold one
  heading each (`_oss_xfcc_loadbalancer`, `_oss_xfcc_router`) become that
  heading; `_routing_conflict` on `routes-domains` becomes its text and its
  link. Variables that print a product name become the name (variables
  round, accepted convention); variables whose value holds a link become
  their value; `gather_routing_logs`, used on
  `troubleshooting-router-error-responses` but not defined in the book's
  file, is removed (variables round, accepted answer 2). Decision (this
  round): the test pages carry no includes or variables, so that every link
  is one the tool's link handling sees; the [depth probe](../results.md#links-in-variables-and-partials)
  tests links held in variables and partials.
- **Stub pages.** Pages that the test pages link to but that are not test
  pages are stubs in each site: the target's title, one sentence naming its
  source file, and a heading for each id the test pages link to, with that
  heading's text. Decision (this round): the stubs sit at their target's
  path in their target's content source, so a link resolves only if the
  tool gets the path across sources right.
- **`redirects.rb`** is the book's list of old URLs and where they now
  lead. The survey reads it from the clone; the redirect probe uses two of
  its rules (L38 and L115).
- **Published pages.** [`../published/`](../published/) holds
  `http-routing` as docs.cloudfoundry.org served it on 2026-10-11, saved
  with `curl`:
  [http-routing](https://docs.cloudfoundry.org/concepts/http-routing.html).
  The other three test pages are compared with the variables, partials and
  headings rounds' copies, saved on 2026-10-10 and 2026-10-11.

## Verify

Run from this directory, with the repositories cloned next to
`cf-docs-rfc-proposal` (`../../../..` is the directory holding it). No
output means every file matches.

```bash
R=../../../..
git -C $R/docs-cloudfoundry-concepts show 97e0d0b25f059c06edd25e30355d26eb93dc560a:http-routing.html.md.erb | diff - http-routing.html.md.erb
git -C $R/docs-book-cloudfoundry show 30dfa57692253a6ae1b3df0726444b1e32852c91:redirects.rb | diff - redirects.rb
```
