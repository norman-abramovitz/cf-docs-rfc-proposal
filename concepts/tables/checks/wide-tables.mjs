// Wide tables: a table wider than the content column scrolls sideways inside
// its own box, and the page never scrolls sideways because of a table.
// Each table in turn gets an unbreakable 200-character line in its first
// cell; the check passes when the page is no wider than before and a box
// between the table and the article scrolls. A table-media table is checked
// as it is: its images shrink, so it must fit the column.
//
// Usage: node wide-tables.mjs URL-PATTERN MODE...
//   URL-PATTERN holds %m (mode) and %p (page), e.g. http://localhost:8001/%m/%p/
// Needs the site served (make serve) and Google Chrome installed.
import { chromium } from 'playwright-core'

const PAGES = ['scale-table-host', 'credential-types', 'metadata',
  'troubleshooting_slow_requests', 'uaa-concepts', 'uaa-performance']
const [pattern, ...modes] = process.argv.slice(2)

function probe () {
  const root = document.querySelector('article, main, .doc')
  const doc = document.documentElement
  const out = []
  for (const t of root.querySelectorAll('table')) {
    if (t.parentElement.closest('table')) continue
    const n = out.length + 1
    if (t.classList.contains('table-media')) {
      const fits = t.getBoundingClientRect().right <= root.getBoundingClientRect().right + 1
      out.push({ n, ok: fits, why: fits ? 'media grid fits the column' : 'media grid wider than the column' })
      continue
    }
    const before = doc.scrollWidth
    const cell = t.querySelector('tbody td, tbody th, td, th')
    const line = document.createElement('code')
    line.style.whiteSpace = 'nowrap'
    line.textContent = 'x'.repeat(200)
    cell.appendChild(line)
    let box = null
    for (let a = t; a && a !== root; a = a.parentElement) {
      const cs = getComputedStyle(a)
      if (/auto|scroll/.test(cs.overflowX) && !/table/.test(cs.display) && a.scrollWidth > a.clientWidth + 1) { box = a; break }
    }
    const widened = doc.scrollWidth > before + 1
    line.remove()
    out.push({ n, ok: box && !widened, why: widened ? 'the page widens' : box ? 'scrolls in its own box' : 'no scroll box (clipped)' })
  }
  return out
}

const browser = await chromium.launch({ channel: 'chrome' })
const page = await browser.newPage()
let ok = 0, fail = 0
for (const width of [1280, 390]) {
  await page.setViewportSize({ width, height: 900 })
  for (const m of modes) {
    for (const p of PAGES) {
      const url = pattern.replace('%m', m).replace('%p', p)
      const res = await page.goto(url, { waitUntil: 'load' })
      if (!res || !res.ok()) { console.log(`FAIL  ${width}px ${m}/${p}: HTTP ${res ? res.status() : 'error'}`); fail++; continue }
      for (const r of await page.evaluate(probe)) {
        if (r.ok) ok++
        else { console.log(`FAIL  ${width}px ${m}/${p} table ${r.n}: ${r.why}`); fail++ }
      }
    }
  }
}
await browser.close()
console.log(`== wide tables: ${ok} passed, ${fail} failed`)
process.exit(fail ? 1 : 0)
