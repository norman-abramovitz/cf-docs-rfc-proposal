// Remark plugin: a Markdown pipe table takes a class and an id from an HTML
// comment in the block just above it, or above the table's title (a
// paragraph that is one bold run):
//
//   <!-- table: .table-compact #label-requirements -->
//   **Label requirements**
//
//   | Part of Label | Length in characters |
//   | --- | --- |
//
// The parser drops comments, so the line is read from the page source.
//
// Hint classes, as Antora writes them, set the column hints: colN-key,
// colN-value, colN-prose (role) and colN-nowrap (wrap: avoid), N from 1.
// Their cells are marked as list-table marks them, and the table gets
// hinted-table.
const HINT = /^col([1-9][0-9]*)-(key|value|prose|nowrap)$/;
const COMMENT = /^\s*<!--\s*table:\s*(.*?)\s*-->\s*$/;

function attrs(spec) {
  const words = spec.split(/\s+/);
  const className = words.filter((w) => w.startsWith('.')).map((w) => w.slice(1));
  const id = words.find((w) => w.startsWith('#'))?.slice(1);
  return {...(className.length && {className}), ...(id && {id})};
}

// Mark each cell of a hinted column; wrap: avoid needs a box inside the cell.
function markColumns(table, classes) {
  const cols = [];
  for (const m of classes.map((c) => HINT.exec(c)).filter(Boolean)) {
    (cols[m[1] - 1] ||= []).push(m[2] === 'nowrap' ? 'wrap-avoid' : `role-${m[2]}`);
  }
  if (!cols.length) return classes;
  for (const row of table.children) {
    row.children.forEach((cell, c) => {
      const marks = cols[c];
      if (!marks) return;
      cell.data = {...cell.data, hProperties: {...cell.data?.hProperties, className: marks}};
      if (marks.includes('wrap-avoid')) cell.children = [{type: 'tableAttrsBox', data: {hName: 'div', hProperties: {className: ['wrap-avoid-box']}}, children: cell.children}];
    });
  }
  return ['hinted-table', ...classes];
}

const isTitle = (n) => n?.type === 'paragraph' && n.children.length === 1 && n.children[0].type === 'strong';

module.exports = () => (tree, file) => {
  const lines = String(file.value).split(/\r?\n/);
  // Index of the first non-blank line above a 1-based line number.
  const above = (line) => {
    let i = line - 2;
    while (i >= 0 && !lines[i].trim()) i--;
    return i;
  };
  const walk = (node) => {
    (node.children || []).forEach((child, k) => {
      if (child.type === 'table' && child.position) {
        let i = above(child.position.start.line);
        const prev = node.children[k - 1];
        if (!COMMENT.test(lines[i] ?? '') && isTitle(prev) && prev.position.end.line - 1 === i) i = above(prev.position.start.line);
        const m = i >= 0 && COMMENT.exec(lines[i]);
        if (m) {
          const a = attrs(m[1]);
          if (a.className) a.className = markColumns(child, a.className);
          child.data = {...child.data, hProperties: {...child.data?.hProperties, ...a}};
        }
      }
      walk(child);
    });
  };
  walk(tree);
};
