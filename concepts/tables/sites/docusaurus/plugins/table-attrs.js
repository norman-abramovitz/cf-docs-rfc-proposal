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
const COMMENT = /^\s*<!--\s*table:\s*(.*?)\s*-->\s*$/;

function attrs(spec) {
  const words = spec.split(/\s+/);
  const className = words.filter((w) => w.startsWith('.')).map((w) => w.slice(1));
  const id = words.find((w) => w.startsWith('#'))?.slice(1);
  return {...(className.length && {className}), ...(id && {id})};
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
        if (m) child.data = {...child.data, hProperties: {...child.data?.hProperties, ...attrs(m[1])}};
      }
      walk(child);
    });
  };
  walk(tree);
};
