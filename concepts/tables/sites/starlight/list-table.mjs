// Table hints for Markdoc tables. Adds attributes to Markdoc's own table
// node, so authors write them on the built-in {% table %} tag:
//
//   {% table widths="25 75" header-rows=1 stub-columns=1 roles="key prose" title="..." %}
//   * Key
//   * Value
//   ---
//   * `alpha`
//   * One paragraph.
//   {% /table %}
//
// Option names follow MyST's list-table where one exists (widths,
// header-rows, stub-columns) and add the hints from the tables concept
// (roles, wrap, title), as in the other sites. A table without hints renders
// as Markdoc renders it.
import Markdoc from '@markdoc/markdoc';

const {Tag} = Markdoc;
const words = (v) => (v ? String(v).trim().split(/\s+/) : []);
const hints = ['widths', 'header-rows', 'stub-columns', 'roles', 'wrap', 'title'];

export const table = {
  render: 'table',
  attributes: {
    widths: {type: String},
    'header-rows': {type: Number},
    'stub-columns': {type: Number},
    roles: {type: String},
    wrap: {type: String},
    title: {type: String},
  },
  transform(node, config) {
    const a = node.attributes;
    const [thead, tbody] = node.transformChildren(config);
    if (!hints.some((h) => h in a)) return new Tag('table', {}, [thead, tbody]);

    const widths = words(a.widths);
    const roles = words(a.roles);
    const wrap = words(a.wrap);
    const stubColumns = a['stub-columns'] || 0;
    // Markdoc puts the first row in thead; header-rows moves more rows there.
    const extra = Math.max((a['header-rows'] ?? 1) - 1, 0);
    thead.children.push(...tbody.children.splice(0, extra));

    const classesFor = (col) => {
      const role = roles[col];
      const w = wrap[col] || (role === 'key' ? 'avoid' : '');
      return [role && `role-${role}`, w === 'avoid' && 'wrap-avoid'].filter(Boolean);
    };
    const decorate = (row, header) => {
      row.children.forEach((cell, c) => {
        const classes = classesFor(c);
        if (!header && c < stubColumns) {
          cell.name = 'th';
          cell.attributes.scope = 'row';
        }
        if (classes.length) cell.attributes.class = classes.join(' ');
        // wrap: avoid needs a box inside the cell: a cell's own width cannot cap its no-wrap width.
        if (classes.includes('wrap-avoid')) cell.children = [new Tag('div', {class: 'wrap-avoid-box'}, cell.children)];
      });
    };
    thead.children.forEach((row) => decorate(row, true));
    tbody.children.forEach((row) => decorate(row, false));

    if (a.title) {
      const span = thead.children[0]?.children.length || 1;
      thead.children.unshift(new Tag('tr', {}, [new Tag('th', {colspan: span, scope: 'colgroup'}, [a.title])]));
    }
    const children = [thead, tbody];
    if (widths.length) {
      const cols = widths.map((w) => new Tag('col', w === 'auto' ? {} : {style: `width:${w}%`}));
      children.unshift(new Tag('colgroup', {}, cols));
    }
    return new Tag('table', {class: 'hinted-table'}, children);
  },
};
