// Variables in the browser: for each page, the console errors and failed
// requests on load, and responses of 400 or more (a React hydration error
// shows here, and nowhere in the static HTML), and, after the page's scripts have run, any variable syntax
// left in the page's text or in its table of contents.
//
// Usage: node vars-browser.mjs URL...
// Needs Google Chrome installed; each site served from its build folder.
import { chromium } from 'playwright-core'

const LEFTOVER = /<%|%>|\{\s*vars\.|\bvars\.[a-z_]\w*|\{%|\$vars\.|\{\{\s*[A-Za-z_]/
const TOC = [
  '.table-of-contents a',          // Docusaurus
  '.md-nav--secondary a',          // Zensical
  'starlight-toc a',               // Starlight
  'aside.toc a'                    // Antora
].join(',')

const browser = await chromium.launch({ channel: 'chrome' })
let fail = 0
for (const url of process.argv.slice(2)) {
  const page = await browser.newPage()
  const errors = []
  page.on('console', (m) => { if (m.type() === 'error' && !m.text().startsWith('Failed to load resource')) errors.push('console: ' + m.text().slice(0, 160)) })
  page.on('pageerror', (e) => errors.push('page error: ' + String(e.message).slice(0, 160)))
  page.on('requestfailed', (r) => errors.push('request failed: ' + r.url()))
  page.on('response', (r) => { if (r.status() >= 400 && !r.url().endsWith('/favicon.svg') && !r.url().endsWith('/favicon.ico')) errors.push(`response ${r.status()}: ${r.url()}`) })
  await page.goto(url, { waitUntil: 'networkidle' })
  await page.waitForTimeout(500)
  const text = await page.evaluate(() => document.body.innerText)
  const toc = await page.evaluate((sel) => [...document.querySelectorAll(sel)].map((a) => a.innerText.trim()).filter(Boolean), TOC)
  const left = text.split('\n').filter((l) => LEFTOVER.test(l))
  console.log(`== ${url}`)
  console.log(`   title: ${await page.title()}`)
  console.log(`   table of contents: ${[...new Set(toc)].join(' | ') || '(none)'}`)
  for (const e of errors) console.log(`   ${e}`)
  for (const l of left) console.log(`   variable syntax in the text: ${l.trim().slice(0, 140)}`)
  if (errors.length || left.length) fail = 1
  else console.log('   ok: no errors, no variable syntax')
  await page.close()
}
await browser.close()
process.exit(fail)
