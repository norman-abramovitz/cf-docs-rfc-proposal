"""Markdown extension: a `list-table` block that turns a nested list into an
HTML table, so cells can hold lists and paragraphs. Options follow MyST's
list-table where one exists (widths, header-rows, stub-columns) and add the
table hints from the tables concept (roles, wrap, title). A title is a header
row spanning every column, above the column headers.

    /// list-table
        widths: 25 75
        header-rows: 1
        stub-columns: 1
        roles: key prose
        title: ...

    -   - Key
        - Value
    -   - `alpha`
        - One paragraph.
    ///

The table sits in a `div.hinted-table`: the theme styles only tables without
a class, so the hook goes on the wrapper.
"""
import xml.etree.ElementTree as etree

from pymdownx.blocks import BlocksExtension
from pymdownx.blocks.block import Block, type_integer, type_string


def words(value):
    return str(value).split() if value else []


class ListTable(Block):
    NAME = 'list-table'
    ARGUMENT = None
    OPTIONS = {
        'widths': ('', type_string),
        'header-rows': (0, type_integer),
        'stub-columns': (0, type_integer),
        'roles': ('', type_string),
        'wrap': ('', type_string),
        'title': ('', type_string),
    }

    def on_create(self, parent):
        return etree.SubElement(parent, 'div', {'class': 'hinted-table'})

    def classes_for(self, col):
        roles, wrap = words(self.options['roles']), words(self.options['wrap'])
        role = roles[col] if col < len(roles) else ''
        w = wrap[col] if col < len(wrap) else ('avoid' if role == 'key' else '')
        return [c for c in (role and f'role-{role}', w == 'avoid' and 'wrap-avoid') if c]

    def cell(self, item, tag, col, scope=None):
        el = etree.Element(tag)
        classes = self.classes_for(col)
        if classes:
            el.set('class', ' '.join(classes))
        if scope:
            el.set('scope', scope)
        children = list(item)
        # A cell holding a single paragraph renders its text directly, as an HTML cell would.
        if not (item.text or '').strip() and len(children) == 1 and children[0].tag == 'p':
            src = children[0]
        else:
            src = item
        # wrap: avoid needs a box inside the cell: a cell's own width cannot cap its no-wrap width.
        target = etree.SubElement(el, 'div', {'class': 'wrap-avoid-box'}) if 'wrap-avoid' in classes else el
        target.text = src.text
        target.extend(list(src))
        return el

    def on_end(self, block):
        rows = block.find('ul')
        if rows is None:
            raise ValueError('list-table needs a list of rows')
        header_rows = self.options['header-rows']
        stubs = self.options['stub-columns']
        table_rows = []
        for r, row in enumerate(rows.findall('li')):
            cells = row.find('ul')
            if cells is None:
                raise ValueError(f'list-table row {r + 1} has no cell list')
            tr = etree.Element('tr')
            for c, item in enumerate(cells.findall('li')):
                header = r < header_rows
                stub = not header and c < stubs
                tr.append(self.cell(item, 'th' if header or stub else 'td', c, 'row' if stub else None))
            table_rows.append(tr)

        block.remove(rows)
        table = etree.SubElement(block, 'table')
        widths = words(self.options['widths'])
        if widths:
            colgroup = etree.SubElement(table, 'colgroup')
            for w in widths:
                etree.SubElement(colgroup, 'col', {} if w == 'auto' else {'style': f'width:{w}%'})
        head = table_rows[:header_rows]
        if self.options['title']:
            span = len(table_rows[0]) if table_rows else 1
            tr = etree.Element('tr')
            th = etree.SubElement(tr, 'th', {'colspan': str(span), 'scope': 'colgroup'})
            th.text = self.options['title']
            head.insert(0, tr)
        if head:
            etree.SubElement(table, 'thead').extend(head)
        etree.SubElement(table, 'tbody').extend(table_rows[header_rows:])


class ListTableExtension(BlocksExtension):
    def extendMarkdownBlocks(self, md, block_mgr):
        block_mgr.register(ListTable, self.getConfigs())


def makeExtension(*args, **kwargs):
    return ListTableExtension(*args, **kwargs)
