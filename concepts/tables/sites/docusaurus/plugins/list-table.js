// Remark plugin: turns a `:::list-table{...}` container directive into an HTML
// table. The directive holds one list item per row, each holding one list item
// per cell, so cells can contain lists and paragraphs. Options follow MyST's
// list-table where one exists (widths, header-rows, stub-columns) and add the
// table hints from the tables concept (roles, wrap, caption, title). A title is
// a header row spanning every column, above the column headers.
//
//   :::list-table{widths="25 75" header-rows="1" stub-columns="1" roles="key prose" title="..."}
//   - - Key
//     - Value
//   - - `alpha`
//     - One paragraph.
//   :::

const words = (v) => (v ? String(v).trim().split(/\s+/) : []);

function cellNode(item, tag, classes, scope) {
  let children = item.children;
  // A cell holding a single paragraph renders its text directly, as an HTML cell would.
  if (children.length === 1 && children[0].type === 'paragraph') children = children[0].children;
  // wrap: avoid needs a box inside the cell: a cell's own width cannot cap its no-wrap width.
  if (classes.includes('wrap-avoid')) children = [{type: 'listTableBox', data: {hName: 'div', hProperties: {className: ['wrap-avoid-box']}}, children}];
  const hProperties = {};
  if (scope) hProperties.scope = scope;
  if (classes.length) hProperties.className = classes;
  return {type: 'listTableCell', data: {hName: tag, hProperties}, children};
}

function toTable(node, file) {
  const a = node.attributes || {};
  const list = node.children.find((c) => c.type === 'list');
  if (!list) {
    file.fail('list-table needs a list of rows', node);
  }
  const widths = words(a.widths);
  const roles = words(a.roles);
  const wrap = words(a.wrap);
  const headerRows = Number(a['header-rows'] || 0);
  const stubColumns = Number(a['stub-columns'] || 0);

  const classesFor = (col) => {
    const role = roles[col];
    const w = wrap[col] || (role === 'key' ? 'avoid' : '');
    return [role && `role-${role}`, w === 'avoid' && 'wrap-avoid'].filter(Boolean);
  };

  const rows = list.children.map((rowItem, r) => {
    const cells = rowItem.children.find((c) => c.type === 'list');
    if (!cells) file.fail(`list-table row ${r + 1} has no cell list`, rowItem);
    const header = r < headerRows;
    return {
      type: 'listTableRow',
      data: {hName: 'tr'},
      children: cells.children.map((cellItem, c) => {
        const stub = !header && c < stubColumns;
        return cellNode(cellItem, header || stub ? 'th' : 'td', classesFor(c), stub ? 'row' : undefined);
      }),
    };
  });

  const children = [];
  if (a.caption) children.push({type: 'listTableCaption', data: {hName: 'caption'}, children: [{type: 'text', value: a.caption}]});
  if (widths.length) {
    children.push({
      type: 'listTableColgroup',
      data: {hName: 'colgroup'},
      children: widths.map((w) => ({
        type: 'listTableCol',
        data: {hName: 'col', hProperties: w === 'auto' ? {} : {style: `width:${w}%`}},
        children: [],
      })),
    });
  }
  const head = rows.slice(0, headerRows);
  if (a.title) {
    const span = rows[0] ? rows[0].children.length : 1;
    const th = {type: 'listTableCell', data: {hName: 'th', hProperties: {colSpan: span, scope: 'colgroup'}}, children: [{type: 'text', value: a.title}]};
    head.unshift({type: 'listTableRow', data: {hName: 'tr'}, children: [th]});
  }
  if (head.length) children.push({type: 'listTableSection', data: {hName: 'thead'}, children: head});
  children.push({type: 'listTableSection', data: {hName: 'tbody'}, children: rows.slice(headerRows)});

  node.data = {hName: 'table', hProperties: {className: ['hinted-table']}};
  node.children = children;
}

function walk(node, file) {
  if (node.type === 'containerDirective' && node.name === 'list-table') toTable(node, file);
  (node.children || []).forEach((c) => walk(c, file));
}

module.exports = () => (tree, file) => walk(tree, file);
