# Link survey

Status: draft, incomplete — covers what is known as of 2026-10-11.

This survey lists every link in the 15 `cloudfoundry/docs-*` repositories
and in the book's own repository, and resolves each one the way the book's
build and server do. A **link** here is an `<a href>`, an `<img src>` or a
Markdown link, image or reference definition, in a page, a partial, a
variable's value, the subnav or a layout. For each link it records how the
URL is written, which page and id it reaches, whether that page lives in
another repository, and whether the link works today. The survey was done
on 2026-10-11 to choose the test pages of the cross-repository links round
and to give data to [R-08](../../../requirements/README.md#r-08)
cross-repository links, [R-15](../../../requirements/README.md#r-15) URL
identifies the source and [R-16](../../../requirements/README.md#r-16) old
URLs keep working.

| File | What it is |
|---|---|
| [links.csv](links.csv) | One row per link and per page it renders on, 4,903 rows: where it is written, the URL, its kind, the page and id it reaches, the repositories at both ends, its status, the `href` the book publishes, and a GitHub link to the line at the surveyed commit |
| [redirects.csv](redirects.csv) | One row per rule in the book's `redirects.rb`, 85 rows, with whether its target exists |
| [shas.txt](shas.txt) | The 15 repositories and the commit surveyed in each: the partials survey's list |
| [survey.py](survey.py) | Finds and resolves the links in a set of clones; writes both CSV files |
| [summary.py](summary.py) | Prints the counts below from the two CSV files |
| [ids.py](ids.py), [ids.txt](ids.txt) | Checks the survey's model of generated heading ids against 18 published pages |
| [published.py](published.py), [published.txt](published.txt) | Checks the survey's predicted `href` values against the same 18 published pages |
| [spot-check.txt](spot-check.txt) | Live requests that check some of the survey's results, 2026-10-11 |

Terms used below:

- **Page-relative**: a URL resolved against the page's own address
  (`../adminguide/x.html`, `x.html`). **Root-relative**: a URL that starts
  with `/` (`/devguide/x.html`). **Absolute**: a URL with a host. **In-page**:
  a URL that is only a fragment (`#id`). A **fragment** or **anchor** is the
  part after `#`, the id of an element on the target page.
- **Section**: one entry of the book's `config.yml`, which names a
  repository and the URL **directory** its pages are published under
  ([`config.yml` L9-L90](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config.yml#L9-L90)):
  docs-cf-admin is `adminguide/`, docs-dev-guide `devguide/`, and so on.
- **Crosses a repository boundary**: the link renders on a page of one
  repository and reaches a page of another. For a link in a partial or a
  variable, the page it renders on counts.

## Scope

- **Repositories.** The 15 `docs-*` repositories of the
  [partials survey](../../partials/survey/README.md#scope), at the same
  commits, and the book repository: its `master_middleman/source/` (home
  page, subnav, layouts), `config/template_variables.yml` and
  `redirects.rb`. The layouts that only the Bookbinder gem provides are read
  from `pivotal-cf/bookbinder` at the `v9.12.0` tag
  ([`f608a44`](https://github.com/pivotal-cf/bookbinder/commit/f608a441572def7787361842f05e42d163d78d54)),
  as in the partials survey.
- **Files.** The partials survey's: `.md`, `.erb`, `.html`, `.haml`,
  `.markdown`, `.mdx` and `.adoc`, without `.git`, `node_modules` and
  `vendor` folders and without Markdown files at a repository's root.
- **Two MkDocs sites.** docs-bosh builds bosh.io/docs and
  docs-dotnet-core-tutorial a tutorial, both with MkDocs, not the book
  ([docs-bosh `mkdocs.yml` L3-L10](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/mkdocs.yml#L3-L10)).
  Their links are resolved within each site (a relative `.md` file, or a
  URL below the site's root) and counted apart.
- **Source, not published pages.** Links are counted where they are
  written; a link in a partial or a variable is counted once for each page
  it renders on.

## How the book builds a link

The book pins `bookbindery` 9.12.1, which runs Middleman 3.4 with Redcarpet
([partials survey](../../partials/survey/README.md#how-the-book-resolves-a-partial)).
Four layers touch a link:

1. **Markdown links are rewritten.** Bookbinder's Middleman settings turn on
   Redcarpet's `autolink` and set `relative_links` to false
   ([`config.rb` L11-L16, L24](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/config.rb#L11-L24)).
   Middleman renders each Markdown link through its `link_to` helper
   ([`redcarpet.rb` L70-L75](https://github.com/middleman/middleman/blob/37845e89c0c4e84bbab9b202cf21e0c02c84d398/middleman-core/lib/middleman-core/renderers/redcarpet.rb#L70-L75)),
   which looks a relative path up in its sitemap, from the current page's
   folder, and when it finds the page writes the page's root-relative URL
   ([`util.rb` L172-L185](https://github.com/middleman/middleman/blob/37845e89c0c4e84bbab9b202cf21e0c02c84d398/middleman-core/lib/middleman-core/util.rb#L172-L185)).
   So `../adminguide/securing-traffic.html` on `concepts/http-routing` is
   published as `/adminguide/securing-traffic.html`, and
   `architecture/index.html#routing` as `/concepts/architecture/#routing`
   ([published copy, line 564](../published/http-routing.html)). A Markdown
   link the sitemap does not hold, and every HTML `<a>`, is published as
   written.
2. **Partials and variables are rendered into the page first**, so their
   relative links are resolved from the page that includes them
   ([partials survey, step 6](../../partials/survey/README.md#how-the-book-resolves-a-partial)).
   A value with a relative link works only at one folder depth. The book
   has two variables for the same sentence and link, one for each depth:
   `port_limitations` with `../../adminguide/supporting-websockets.html`
   and `port_limitations_1` with `../adminguide/supporting-websockets.html`
   ([`template_variables.yml` L222-L223](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/config/template_variables.yml#L222-L223)).
3. **The server answers with redirects and folders.** The book's app runs
   `redirects.rb` through Rack::Rewrite before serving files
   ([`rack_app.rb` L38-L51](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/template_app/rack_app.rb#L38-L51)).
   A path with no dot is redirected to the same path with a slash, which
   is served only when it is a folder with an `index.html`
   ([`server.rb` L26-L37](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/template_app/lib/server.rb#L26-L37)):
   `/devguide/deploy-apps/routes-domains` without `.html` ends in a 404
   ([spot check](spot-check.txt)).
4. **Bookbinder checks links after each build, without fragments or
   absolute URLs.** Its link checker skips `http:` and `https:` URLs, counts
   a page as present when a redirect rule matches it, and splits off the
   fragment without checking it
   ([`link_checker.rb` L15, L79-L97](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/lib/bookbinder/postprocessing/link_checker.rb#L15-L97)).
   `bind` returns 1 when it finds a broken link
   ([`bind.rb` L76-L82](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/lib/bookbinder/commands/bind.rb#L76-L82)).
   Whether the book's publishing pipeline stops on that status is
   unverified: no public pipeline definition was found.

The page's "View the source for this page in GitHub" link is Bookbinder's
repo link
([`bookbinder_helpers.rb` L72-L76](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/bookbinder_helpers.rb#L72-L76));
on the published pages it names the repository and file
([published copy, `repo-link`](../published/http-routing.html)).

## Method

[survey.py](survey.py) builds a model of the site the book serves: each
section's repository mounted under its directory, Middleman's rule for the
output path of each file, the partial lookup of the partials survey, and
the variables file. Then it reads every file and finds the links:
Markdown inline links and images, reference definitions, HTML `<a href>`,
`<img src>` and `<area href>`, `<http://…>` autolinks and bare URLs (which
the book's `autolink` setting makes links), outside fenced code and inline
code. A variable used as a URL is replaced by its value. Each link is
resolved as a browser and the book's server would: joined to the page's URL,
looked up as a built page or file, a folder's `index.html`, or else a rule
of `redirects.rb` (up to five hops); then the fragment is looked up among
the target page's ids: `id` and `<a name>` attributes in the page and in the
partials it includes, the layouts' ids, and the id the book generates for
each Markdown heading. The model of generated ids is "the heading's text
with tags removed and variables replaced, lowercased, each space a hyphen".
Links on docs.cloudfoundry.org under `/api/` are the UAA and CredHub API
references, published there by their own builds
([R-29](../../../requirements/README.md#r-29)); they are not checked. Links
to bosh.io/docs are resolved against the docs-bosh clone. Other hosts are
not checked.

**Checks of the model.** On the 18 published pages saved by the earlier
rounds and this one:

- every one of their 233 heading ids is made by the model
  ([ids.txt](ids.txt));
- 250 of the 251 links the survey predicts are on the pages with the
  predicted `href` ([published.txt](published.txt)). The one missing is a
  bare `www.` address inside an HTML table, which the book's Markdown does
  not turn into a link. Cloudflare, in front of the site, adds links to
  `/cdn-cgi/l/email-protection` in place of e-mail addresses in the text
  ([published copy](../../headings/published/routes-domains.html)); they
  are not in the source and are left out.

Live requests on 2026-10-11 agree with the survey on every URL and id tried
([spot-check.txt](spot-check.txt)).

## Totals

| | Rows | As written |
|---|---|---|
| Book: pages, partials and variable values, as rendered | 2,892 | 2,863 |
| Book: subnav (rendered on every page) and layouts | 269 | 269 |
| Book: variable values no page uses, partials no page includes | 49 | 49 |
| bosh.io (docs-bosh) | 1,676 | |
| .NET Core tutorial (docs-dotnet-core-tutorial) | 17 | |

The 2,892 rows in content, by kind: page-relative 1,126 (153 of them
images), to other hosts 1,013, in-page 448, root-relative 252, absolute to
docs.cloudfoundry.org 50, a variable as the whole URL 3.

## Findings

**Links between repositories.** 594 rows in content cross a repository
boundary, 572 as written, from 142 files. They are page-relative 329,
root-relative 231, absolute to docs.cloudfoundry.org 32, and a variable 2.
Every page-relative one goes up with `../` (165 one level, 150 two, 14
three) and then names the other section's directory, so it works only
while that directory name and the page's depth stay as they are. 221 of
the 231 root-relative ones are on the book's home page
([`index.html.md.erb`](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/index.html.md.erb)).
The subnav adds 264 root-relative links from the book repository to every
section. The repositories linked to most are docs-dev-guide (179 rows),
docs-cloudfoundry-concepts (92) and docs-buildpacks (66);
[summary.py](summary.py) prints the whole matrix.

**Links that name their own directory.** Eight links in three repositories go
up out of their own section and back in through its directory name, for
example `../concepts/asg.html` on `concepts/security`
([L218](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/security.html.md.erb#L218)).
Like the partial call `../adminguide/tcp_modify_ports`
([partials survey](../../partials/survey/README.md#findings)), they work
only because the book names the directory so.

**Folder index pages.** 135 internal links reach a folder's `index.html`;
120 write `…/index.html`, 5 write the folder with a trailing `/`. The book
publishes the Markdown ones as the folder (`/concepts/architecture/`), so
both forms are URLs in use.

**What the book publishes.** 758 of the 761 page-relative Markdown links
(not images) are published root-relative, because Middleman found their
page; the other three reach their page by a redirect or are empty. The 212
page-relative HTML `<a>` links are published as written.

**Links in variables.** 92 values hold a link; 48 of them are used on a
page. 27 used values hold page-relative links, rendered 42 times; each works
only at its pages' depth. All 42 reach their page today, 2 of them by a
redirect.

**Links in partials.** 71 rows; 19 are page-relative and are resolved from
the including page. No partial is included from pages at two depths today.

**Links already broken.** 55 rows in content do not reach their target: 50
point at an id the target page does not have (23 in-page, 27 to another
page), 3 are absolute links whose redirect leads to a missing page
(`/adminguide/trusted-system-certificates.html`), and 2 point at an id
bosh.io does not have. 18 of the 55 cross a repository boundary. They are
in 41 files of 12 repositories. Examples: 15 links to ids on
`devguide/deploy-apps/manifest.html` (`env-block` 6 times, `start-commands`,
`services-block`, `minimal-manifest`, `routes`) that are now on
`manifest-attributes.html`, for example
[L708](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/deploy-apps/manifest-attributes.html.md.erb#L708);
the [headings round's](../../headings/broken-links.md) two in-page links on
`routes-domains`. None of the 55 is reported by the book's link checker,
which checks neither fragments nor absolute URLs.

**Absolute links to docs.cloudfoundry.org.** 50 rows in content: 38 reach a
page, 2 by redirect, 7 go to the API references, and 3 reach a redirect
whose target is gone. The book's link checker skips all of them.

**`redirects.rb`.** 85 rules (84 permanent, 1 temporary; 6 regular
expressions). 40 targets exist (2 with a fragment the target lacks), 30 do
not, 3 redirect again, and 12 leave the site. One rule's source holds a
fragment, `/devguide/deploy-apps/manifest.html#deprecated`
([L48](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/redirects.rb#L48)).
A browser never sends the fragment to the server
([RFC 3986 §3.5](https://www.rfc-editor.org/rfc/rfc3986#section-3.5)), so
that rule cannot match. Live, a missing target answers 404 after the
redirect, for example `/deploying/ec2/…` → `/deploying/aws/index.html`
([spot check](spot-check.txt)).

**bosh.io.** The book's pages link to bosh.io 59 times: 48 reach a
docs-bosh page, 2 an id that page lacks, and 9 go to bosh.io's release,
job and stemcell pages, outside its docs. 26 of the book's bosh.io links
write `….html`, which bosh.io redirects to the folder URL
([spot check](spot-check.txt)). docs-bosh itself already combines two
repositories: a git submodule, `external/bpm-release`, whose `docs` folder a
symbolic link mounts as `content/bpm`
([`.gitmodules`](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/.gitmodules),
[`content/bpm`](https://github.com/cloudfoundry/docs-bosh/blob/20a41223a7ba87700424634c42e94a22a669b45e/content/bpm)).
13 of its links lead into that submodule, which this survey did not fetch.

## How to rerun

Run from a working directory outside this repository, with `python3 -I`.
`SURVEY` stands for this folder. The clones are fetched as in the
[partials survey](../../partials/survey/README.md#how-to-rerun), and
Bookbinder at its `v9.12.0` tag:

```sh
git clone -q https://github.com/pivotal-cf/bookbinder.git bookbinder
git -C bookbinder checkout -q f608a441572def7787361842f05e42d163d78d54

python3 -I SURVEY/survey.py repos SURVEY/shas.txt links.csv redirects.csv bookbinder
cmp links.csv SURVEY/links.csv && cmp redirects.csv SURVEY/redirects.csv
python3 -I SURVEY/summary.py SURVEY/links.csv SURVEY/redirects.csv

# The checks of the model, on the published pages saved in this evaluation
python3 -I SURVEY/ids.py repos SURVEY/../../*/published/*.html
python3 -I SURVEY/published.py SURVEY/links.csv SURVEY/../../*/published/*.html
```

The scripts read files only; they run nothing from the clones.
