// Screenshots of every table on a page, as the comparison pages show them:
// a 1280-pixel window, each table with a 4-pixel margin (published pages: none), JPEG.
// A table wider than its scroll box gets two: what the reader sees (the box,
// with its scrollbar) as OUT-t<N>.jpg, and the whole table as OUT-t<N>-full.jpg,
// taken with the box's clipping switched off for the moment (no splicing).
//
// Usage: node screenshots.mjs URL OUT [--hide CSS-SELECTOR] [--margin PIXELS]
//   OUT is a path prefix, e.g. ../../../poc/compare/img/zensical-native-roles-table-host
//   --hide hides page furniture first, any CSS selector list (docs.cloudfoundry.org:
//   'header.header', and a[title="back to top"] for a table as wide as the window; Starlight: '.right-sidebar-container', whose sticky contents
//   would cover a full table that runs under them; Zensical: 'header.md-header' and
//   Docusaurus: '.navbar, [class*="skipToContent"]', sticky bars that would cover the
//   table's header row, and a skip link that shows in captures wider than the window)
//   --margin is 4 by default; the published screenshots use 0
// Needs Google Chrome installed.
import { chromium } from 'playwright-core'

const [url, out, ...rest] = process.argv.slice(2)
const opt = (name, dflt) => { const i = rest.indexOf(name); return i < 0 ? dflt : rest[i + 1] }
const hide = opt('--hide', null)
const m = +opt('--margin', 4)
if (!url || !out) { console.error('usage: node screenshots.mjs URL OUT [--hide CSS-SELECTOR] [--margin PIXELS]'); process.exit(2) }

// Each top-level table in the content, and its scroll box if it overflows one: the
// table itself (Starlight shows tables as blocks that scroll) or an element around it
function find () {
  const root = document.querySelector('article, main, .doc') || document.body
  return [...root.querySelectorAll('table')].filter(t => !t.parentElement.closest('table')).map((t, i) => {
    let box = null
    for (let a = t; a && a !== root; a = a.parentElement) {
      const cs = getComputedStyle(a)
      if (/auto|scroll|hidden/.test(cs.overflowX) && !/^table/.test(cs.display) && a.scrollWidth > a.clientWidth + 1) { box = a; break }
    }
    t.dataset.shot = i + 1
    if (box) box.dataset.shotBox = i + 1
    return !!box
  })
}

function rect ([sel, full]) {
  const el = document.querySelector(sel)
  el.scrollIntoView()
  const r = el.getBoundingClientRect()
  // with its clipping off, a table that is its own scroll box keeps its box width: use what it holds
  return { x: r.left + scrollX, y: r.top + scrollY, w: full ? Math.max(r.width, el.scrollWidth) : r.width, h: r.height }
}

const clip = b => ({ x: Math.floor(b.x) - m, y: Math.floor(b.y) - m, width: Math.ceil(b.w) + 2 * m, height: Math.ceil(b.y + b.h) - Math.floor(b.y) + 2 * m - (m ? 1 : 0) })

const browser = await chromium.launch({ channel: 'chrome' })
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } })
const res = await page.goto(url, { waitUntil: 'networkidle' })
if (!res || !res.ok()) { console.error(`HTTP ${res ? res.status() : 'error'}: ${url}`); process.exit(1) }
if (hide) await page.addStyleTag({ content: `${hide} { display: none !important }` })
await page.evaluate(() => document.fonts.ready)
const boxed = await page.evaluate(find)
for (const [i, wide] of boxed.entries()) {
  const n = i + 1
  const seen = await page.evaluate(rect, [wide ? `[data-shot-box="${n}"]` : `[data-shot="${n}"]`, false])
  await page.screenshot({ path: `${out}-t${n}.jpg`, type: 'jpeg', quality: 90, fullPage: true, clip: clip(seen) })
  let line = `${out}-t${n}.jpg ${Math.round(seen.w)}x${Math.round(seen.h)}`
  if (wide) {
    await page.evaluate(n => { document.querySelector(`[data-shot-box="${n}"]`).style.overflow = 'visible' }, n)
    const full = await page.evaluate(rect, [`[data-shot="${n}"]`, true])
    await page.screenshot({ path: `${out}-t${n}-full.jpg`, type: 'jpeg', quality: 90, fullPage: true, clip: clip(full) })
    await page.evaluate(n => { document.querySelector(`[data-shot-box="${n}"]`).style.overflow = '' }, n)
    line += `; full table ${Math.round(full.w)}x${Math.round(full.h)} in -t${n}-full.jpg`
  }
  console.log(line)
}
await browser.close()
