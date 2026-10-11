// Writes one playbook per mode from antora-playbook.yml and the book's
// variables file (../../source/template_variables.yml).
//
// site-passthrough.yml: every key as an AsciiDoc attribute, its value as the
//   book writes it, except `title`: AsciiDoc reads an attribute of that name
//   as the document title, so with it every page's title becomes "Cloud
//   Foundry Documentation" (../../results/antora-title-key.txt). A reference
//   to a name that is not defined renders as nothing (attribute-missing:
//   drop), as in the book.
// site-native.yml: the values prepared for AsciiDoc, as the converter would
//   write them: Markdown in a value becomes HTML (attribute references are
//   replaced after AsciiDoc's inline formatting, so backticks and asterisks
//   in a value would stay as they are, while HTML passes through); an empty
//   value is ''; the key `title`, which is also AsciiDoc's own attribute for
//   the page title, and the key that is not a name are left out. Every name
//   is required: a reference to a name that is not defined is a warning
//   (attribute-missing: warn), and a warning fails the build
//   (runtime.log.failure_level: warn).
const fs = require('node:fs');
const yaml = require('js-yaml');
const base = yaml.load(fs.readFileSync('antora-playbook.yml', 'utf8'));
const vars = yaml.load(fs.readFileSync('../../source/template_variables.yml', 'utf8')).template_variables;

function write(file, mode, attributes, extra = {}) {
  const book = JSON.parse(JSON.stringify(base));
  book.content.sources[0].start_paths.push(`concepts/variables/sites/antora/${mode}`);
  Object.assign(book.asciidoc.attributes, attributes);
  Object.assign(book.runtime, extra);
  fs.writeFileSync(file, yaml.dump(book, {lineWidth: -1}));
}

// The Markdown the book's values use, as HTML: links, code, bold, emphasis,
// backslash escapes. Values with block Markdown (lists, fenced code) are
// left as they are; no test page uses one.
function inlineHtml(v) {
  if (typeof v !== 'string' || /^\s*([*+-]|\d+\.)\s|```/m.test(v)) return v;
  return v
    .replace(/`([^`]+)`/g, (m, c) => `<code>${c.replace(/\\_/g, '_')}</code>`)
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2">$1</a>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[\s(])_([^_]+)_(?=[\s.,;:)]|$)/g, '$1<em>$2</em>')
    .replace(/\\([_*\[\]])/g, '$1');
}

const {title, ...passthrough} = vars;
write('site-passthrough.yml', 'passthrough', {'attribute-missing': 'drop', ...passthrough});

const native = {};
for (const [k, v] of Object.entries(vars)) {
  if (!/^\w+$/.test(k) || k === 'title') continue;
  native[k] = v == null ? '' : inlineHtml(String(v));
}
write('site-native.yml', 'native', {'attribute-missing': 'warn', ...native}, {log: {failure_level: 'warn'}});
