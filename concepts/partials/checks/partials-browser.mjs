// Partials in the browser: for each page, the console errors and failed
// requests on load, and the targets of the table-of-contents links after
// the page's scripts have run (Antora builds its table of contents in the
// browser, so the static HTML has none).
//
// Usage: node partials-browser.mjs URL...
// Needs Google Chrome installed; each site served (make serve).
import { chromium } from 'playwright-core'

const TOC = [
  'aside.toc a', '.toc-menu a',               // Antora default UI
  '.table-of-contents a',                     // Docusaurus
  'nav.md-nav--secondary a',                  // Zensical
  'starlight-toc a',                          // Starlight
  '.quick-links a'                            // published book
].join(',')

const browser = await chromium.launch({ channel: 'chrome' })
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } })
for (const url of process.argv.slice(2)) {
  const errors = []
  page.removeAllListeners('console')
  page.removeAllListeners('pageerror')
  page.removeAllListeners('response')
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text().split('\n')[0].slice(0, 160)) })
  page.on('pageerror', (e) => errors.push(String(e).split('\n')[0].slice(0, 160)))
  page.on('response', (r) => { if (r.status() >= 400) errors.push(`(${r.status()} for ${r.url()})`) })
  await page.goto(url, { waitUntil: 'networkidle' })
  await page.waitForTimeout(500)
  const toc = await page.evaluate((sel) => [...new Set([...document.querySelectorAll(sel)]
    .map((a) => a.getAttribute('href') || '').filter((h) => h.startsWith('#')).map((h) => h.slice(1)))], TOC)
  console.log(url)
  console.log('  console errors: ' + (errors.length ? '' : 'none'))
  for (const e of errors) console.log('    ' + e)
  console.log('  table of contents: ' + (toc.length ? toc.map((t) => '#' + t).join(' ') : 'none'))
}
await browser.close()
