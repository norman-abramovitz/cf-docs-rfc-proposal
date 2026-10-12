// The same pages as book-render.rb, read by a CommonMark parser: which code
// blocks a CommonMark tool finds where the book's Redcarpet finds others.
//
// Usage: node commonmark-render.mjs WORK_DIR COMMONMARK.csv
//   WORK_DIR is book-render.rb's: its md/<repo>/<file> tree holds each page's
//   Markdown after the ERB step. Writes one row per code block that
//   commonmark.js 0.31.2 (the reference parser of CommonMark 0.31.2) finds:
//   fenced or indented, its info string, its line count, its first line.
//   Raw HTML blocks such as <pre> are HTML in both parsers and are not rows.
//   (commonmark.js keeps whether a block is fenced in the node's _isFenced.)
import fs from 'node:fs'
import path from 'node:path'
import { Parser } from 'commonmark'

const [work, out] = process.argv.slice(2)
if (!work || !out) { console.error('usage: node commonmark-render.mjs WORK_DIR COMMONMARK.csv'); process.exit(2) }
const root = path.join(work, 'md')
const csv = (v) => /[",\n]/.test(String(v)) ? `"${String(v).replace(/"/g, '""')}"` : String(v)
const rows = [['repo', 'file', 'n', 'kind', 'info', 'lines', 'first_line']]

function* files(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    const p = path.join(dir, e.name)
    if (e.isDirectory()) yield* files(p)
    else yield p
  }
}

const parser = new Parser()
for (const f of files(root)) {
  const rel = path.relative(root, f).split(path.sep)
  const repo = rel.shift()
  const doc = parser.parse(fs.readFileSync(f, 'utf8'))
  const walker = doc.walker()
  let ev, n = 0
  while ((ev = walker.next())) {
    if (!ev.entering || ev.node.type !== 'code_block') continue
    const code = ev.node.literal || ''
    const first = (code.split('\n').map((l) => l.trim()).find(Boolean) || '').slice(0, 80)
    rows.push([repo, rel.join('/'), ++n, ev.node._isFenced ? 'fenced' : 'indented', ev.node.info || '',
      code.replace(/\n$/, '').split('\n').length, first])
  }
}
fs.writeFileSync(out, rows.map((r) => r.map(csv).join(',')).join('\n') + '\n')
console.log(`${rows.length - 1} code blocks found by commonmark.js`)
