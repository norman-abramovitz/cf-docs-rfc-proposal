# Sources

Verbatim copies, taken on 2026-10-11, of the four test pages and of the
book and Bookbinder files that print build-time values. Nothing in this
directory is edited; the converted pages live in `../sites/`, written by
[`../helpers/pages.py`](../helpers/pages.py). The pages are at the commits
the [partial survey](../../partials/survey/shas.txt) read, which this
round's [survey](../survey/README.md) reads too.

| File | Repository | Path | Commit | License |
|------|------------|------|--------|---------|
| `access-control.html.md.erb` | [cloudfoundry/docs-services](https://github.com/cloudfoundry/docs-services) | `access-control.html.md.erb` | `ccb0036407e4c2eabbb61a3b3de008f821f41c5b` | Apache-2.0 |
| `architecture.html.md.erb` | [cloudfoundry/docs-loggregator](https://github.com/cloudfoundry/docs-loggregator) | `architecture.html.md.erb` | `8e027bac1099b737afe56afa1606b4fcf9d06c94` | Apache-2.0 |
| `using-vol-services.html.md.erb` | [cloudfoundry/docs-dev-guide](https://github.com/cloudfoundry/docs-dev-guide) | `services/using-vol-services.html.md.erb` | `9c8df63eb3823011e4e3aff9958c36e25d5190b7` | Apache-2.0 |
| `high-availability.html.md.erb` | [cloudfoundry/docs-cloudfoundry-concepts](https://github.com/cloudfoundry/docs-cloudfoundry-concepts) | `high-availability.html.md.erb` | `97e0d0b25f059c06edd25e30355d26eb93dc560a` | Apache-2.0 |
| `_book-footer.erb` | [cloudfoundry/docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry) | `master_middleman/source/layouts/_book-footer.erb` | `30dfa57692253a6ae1b3df0726444b1e32852c91` | Apache-2.0 |
| `_pre-content.erb` | cloudfoundry/docs-book-cloudfoundry | `master_middleman/source/layouts/_pre-content.erb` | `30dfa57692253a6ae1b3df0726444b1e32852c91` | Apache-2.0 |
| `book-layout.erb` | cloudfoundry/docs-book-cloudfoundry | `master_middleman/source/layouts/layout.erb` (renamed here, to tell it from Bookbinder's) | `30dfa57692253a6ae1b3df0726444b1e32852c91` | Apache-2.0 |
| `bookbinder_helpers.rb` | [pivotal-cf/bookbinder](https://github.com/pivotal-cf/bookbinder) | `master_middleman/bookbinder_helpers.rb` | `f608a441572def7787361842f05e42d163d78d54` (tag `v9.12.0`) | MIT |
| `git_accessor.rb` | pivotal-cf/bookbinder | `lib/bookbinder/ingest/git_accessor.rb` | `f608a441572def7787361842f05e42d163d78d54` | MIT |
| `bookbinder.js` | pivotal-cf/bookbinder | `master_middleman/source/javascripts/bookbinder.js` | `f608a441572def7787361842f05e42d163d78d54` | MIT |

Links to the files at those commits:
[access-control](https://github.com/cloudfoundry/docs-services/blob/ccb0036407e4c2eabbb61a3b3de008f821f41c5b/access-control.html.md.erb),
[architecture](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/architecture.html.md.erb),
[using-vol-services](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/services/using-vol-services.html.md.erb),
[high-availability](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/high-availability.html.md.erb),
[_book-footer.erb](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/_book-footer.erb),
[_pre-content.erb](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/_pre-content.erb),
[layout.erb](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/master_middleman/source/layouts/layout.erb),
[bookbinder_helpers.rb](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/bookbinder_helpers.rb),
[git_accessor.rb](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/lib/bookbinder/ingest/git_accessor.rb),
[bookbinder.js](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/master_middleman/source/javascripts/bookbinder.js).
Licenses:
[docs-services LICENSE](https://github.com/cloudfoundry/docs-services/blob/ccb0036407e4c2eabbb61a3b3de008f821f41c5b/LICENSE),
[docs-loggregator LICENSE](https://github.com/cloudfoundry/docs-loggregator/blob/8e027bac1099b737afe56afa1606b4fcf9d06c94/LICENSE),
[docs-dev-guide LICENSE](https://github.com/cloudfoundry/docs-dev-guide/blob/9c8df63eb3823011e4e3aff9958c36e25d5190b7/LICENSE),
[docs-cloudfoundry-concepts LICENSE](https://github.com/cloudfoundry/docs-cloudfoundry-concepts/blob/97e0d0b25f059c06edd25e30355d26eb93dc560a/LICENSE),
[docs-book-cloudfoundry LICENSE](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/LICENSE),
Bookbinder's MIT license ([gemspec L13](https://github.com/pivotal-cf/bookbinder/blob/f608a441572def7787361842f05e42d163d78d54/bookbinder.gemspec#L13)).

## Notes

- **The Bookbinder files match the gem the book uses.** The book pins
  `bookbindery` 9.12.1
  ([Gemfile L3](https://github.com/cloudfoundry/docs-book-cloudfoundry/blob/30dfa57692253a6ae1b3df0726444b1e32852c91/Gemfile#L3)).
  The 9.12.1 gem from [RubyGems](https://rubygems.org/gems/bookbindery/versions/9.12.1)
  and the repository's `v9.12.0` tag differ in two files only
  (`code_example_reader.rb`, `preprocessor.rb`; compared with `diff` on
  2026-10-11, as the partials round did), neither of them copied here.
- **Earlier rounds' copies.** `access-control` is also in the
  [headings round's sources](../../headings/source/SOURCES.md),
  `architecture` and `high-availability` in the
  [partials round's](../../partials/source/SOURCES.md), and
  `using-vol-services` in the [notes round's](../../notes/source/SOURCES.md);
  the files here are byte-for-byte the same (compared with `cmp`).
- **Excerpts.** Only `access-control` is converted whole. The other three
  converted pages hold the published title and first paragraph: the
  round tests the frame around the content
  ([README](../README.md#test-pages)).
