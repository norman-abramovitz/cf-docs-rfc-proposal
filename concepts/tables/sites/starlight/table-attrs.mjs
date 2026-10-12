// A Markdown pipe table takes a class and an id from an HTML comment in the
// block just above it, or above the table's title (a paragraph that is one
// bold run):
//
//   <!-- table: .table-compact #label-requirements -->
//   **Label requirements**
//
//   | Part of Label | Length in characters |
//   | --- | --- |
//
// The comment is a node of its own before the table. The document transform
// moves its class and id onto the table, where the table node
// (list-table.mjs) renders them.
import Markdoc from '@markdoc/markdoc';

const {Tag} = Markdoc;
const COMMENT = /^table:\s*(.*)$/;

const spec = (n) => n?.type === 'comment' && COMMENT.exec(n.attributes.content.trim());
const isTitle = (n) =>
  n?.type === 'paragraph' && n.children.length === 1 && n.children[0].type === 'inline' &&
  n.children[0].children.length === 1 && n.children[0].children[0].type === 'strong';

function walk(node) {
  node.children.forEach((child, i) => {
    const [prev, prev2] = [node.children[i - 1], node.children[i - 2]];
    const m = child.type === 'table' && (spec(prev) || (isTitle(prev) && spec(prev2)));
    if (m) {
      const words = m[1].split(/\s+/);
      const classes = words.filter((w) => w.startsWith('.')).map((w) => w.slice(1));
      const id = words.find((w) => w.startsWith('#'))?.slice(1);
      if (classes.length) child.attributes.class = classes.join(' ');
      if (id) child.attributes.id = id;
    }
    walk(child);
  });
}

export const document = {
  ...Markdoc.nodes.document,
  transform(node, config) {
    walk(node);
    return new Tag('article', node.transformAttributes(config), node.transformChildren(config));
  },
};
