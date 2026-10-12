"""Markdown extension: a pipe table takes a class and an id from an HTML
comment in the block just above it, or above the table's title (a paragraph
that is one bold run):

    <!-- table: .table-compact #label-requirements -->
    **Label requirements**

    | Part of Label | Length in characters |
    | --- | --- |

A table given a class also gets `table`: the theme styles only tables
without a class, and the site's `table.table` rules give its look back.

A blank line is added after the comment, because inside a list item a
table must follow a blank line; this runs after fenced code is set aside
(priority 25) and before HTML blocks are (20), so code stays as written.
The comment is then raw HTML, kept aside with a placeholder in its own
paragraph, found after inline processing (20), when bold text is an element.
"""
import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
from markdown.util import HTML_PLACEHOLDER_RE

COMMENT = re.compile(r'^\s*<!--\s*table:\s*(.*?)\s*-->\s*$')


class BlankAfterComment(Preprocessor):
    def run(self, lines):
        out = []
        for line in lines:
            out += [line, ''] if COMMENT.match(line) else [line]
        return out


def is_title(el):
    """A paragraph whose whole content is one bold run."""
    return (el.tag == 'p' and len(el) == 1 and el[0].tag == 'strong'
            and not (el.text or '').strip() and not (el[0].tail or '').strip())


class TableAttrs(Treeprocessor):
    def spec(self, el):
        if el.tag != 'p' or len(el) or not el.text:
            return None
        m = HTML_PLACEHOLDER_RE.fullmatch(el.text.strip())
        raw = str(self.md.htmlStash.rawHtmlBlocks[int(m[1])]) if m else el.text
        return COMMENT.match(raw)

    def run(self, root):
        for parent in root.iter():
            kids = list(parent)
            for i, el in enumerate(kids):
                if el.tag != 'table' or i == 0:
                    continue
                spec = self.spec(kids[i - 1])
                if not spec and i > 1 and is_title(kids[i - 1]):
                    spec = self.spec(kids[i - 2])
                if not spec:
                    continue
                words = spec[1].split()
                classes = [w[1:] for w in words if w.startswith('.')]
                ids = [w[1:] for w in words if w.startswith('#')]
                if classes:
                    el.set('class', ' '.join(([] if 'table' in classes else ['table']) + classes))
                if ids:
                    el.set('id', ids[0])


class TableAttrsExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(BlankAfterComment(md), 'table_attrs', 22)
        md.treeprocessors.register(TableAttrs(md), 'table_attrs', 15)


def makeExtension(**kwargs):
    return TableAttrsExtension(**kwargs)
