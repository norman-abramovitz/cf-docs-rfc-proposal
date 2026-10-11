// Writes the value of `{vars.name}` into each heading before Docusaurus
// makes the table of contents, so the generated one shows the value, not
// the expression's source. Runs as a beforeDefaultRemarkPlugin. Text
// values only: a name with no text value stops the build, as the
// variables module does.
const vars = require('./vars.json');

const EXPR = /^\s*vars\.([A-Za-z_][A-Za-z0-9_]*)\s*$/;

function replace(node, file) {
  for (const child of node.children ?? []) {
    if (child.type === 'mdxTextExpression') {
      const m = EXPR.exec(child.value);
      if (!m) continue;
      const value = vars[m[1]];
      if (typeof value !== 'string') {
        throw new Error(`Variable not defined as text: vars.${m[1]} in ${file.path}`);
      }
      child.type = 'text';
      child.value = value;
      delete child.data;
    } else {
      replace(child, file);
    }
  }
}

module.exports = function headingVars() {
  return (tree, file) => {
    (function walk(node) {
      if (node.type === 'heading') return replace(node, file);
      for (const child of node.children ?? []) walk(child);
    })(tree);
  };
};
