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
//
// A style other than the standard one is a class, written with Markdoc's
// class shorthand: {% table .table-media %}.
//
// Hint classes, as Antora writes them, set the column hints on a table
// without hint attributes: colN-key, colN-value, colN-prose (role) and
// colN-nowrap (wrap: avoid), N from 1. A pipe table takes them from the
// table comment (table-attrs.mjs): <!-- table: .col1-key .col1-nowrap -->.
import Markdoc from '@markdoc/markdoc';

const {Tag} = Markdoc;
const words = (v) => (v ? String(v).trim().split(/\s+/) : []);
// Markdoc keeps the class shorthand as an object ({'table-media': true}).
const className = (v) => (v && typeof v === 'object' ? Object.keys(v).filter((k) => v[k]).join(' ') : v || '');
const hints = ['widths', 'header-rows', 'stub-columns', 'roles', 'wrap', 'title'];
const HINT = /^col([1-9][0-9]*)-(key|value|prose|nowrap)$/;

function mark(cell, classes) {
  if (!classes?.length) return;
  cell.attributes.class = classes.join(' ');
  // wrap: avoid needs a box inside the cell: a cell's own width cannot cap its no-wrap width.
  if (classes.includes('wrap-avoid')) cell.children = [new Tag('div', {class: 'wrap-avoid-box'}, cell.children)];
}

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
    const cls = className(a.class);
    // The id shorthand ({% table #name %}) names the table, as an HTML table's id does.
    const id = a.id ? {id: a.id} : {};
    const style = cls ? {...id, class: cls} : id;
    if (!hints.some((h) => h in a)) {
      const cols = [];
      for (const m of words(cls).map((c) => HINT.exec(c)).filter(Boolean)) {
        (cols[m[1] - 1] ||= []).push(m[2] === 'nowrap' ? 'wrap-avoid' : `role-${m[2]}`);
      }
      if (!cols.length) return new Tag('table', style, [thead, tbody]);
      [...thead.children, ...tbody.children].forEach((row) => row.children.forEach((cell, c) => mark(cell, cols[c])));
      return new Tag('table', {...id, class: `hinted-table ${cls}`}, [thead, tbody]);
    }

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
        mark(cell, classes);
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
    return new Tag('table', {...id, class: ['hinted-table', cls].filter(Boolean).join(' ')}, children);
  },
};
