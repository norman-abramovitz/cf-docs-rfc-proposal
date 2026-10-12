// Code blocks in the browser: loads each page, lets its scripts run (some
// tools add copy buttons and highlighting there), clicks each code block's
// copy button, and saves the page as the browser then holds it, with what
// each button copied written on its <pre> as data-copied-text. codeblocks.py
// then checks the saved page. Console errors, failed requests and responses
// of 400 or more are printed.
//
// Usage: node codeblocks-browser.mjs OUT_DIR URL...
//   Each page is saved as OUT_DIR/<last two path segments, joined by ->.html
//   (passthrough/routes-domains/ -> passthrough-routes-domains.html).
//   A block's copy button is a button whose title, label or class mentions
//   copy or clipboard, in the <pre> or its wrappers that hold no other <pre>.
// Needs Google Chrome installed; each site served from its build folder.
//
// What a click copies is caught where the page hands it to the browser:
// navigator.clipboard.writeText (Docusaurus, Starlight, Antora) and the
// copy event that document.execCommand('copy') fires (clipboard.js, which
// Zensical's theme uses). Nothing is read back from the system clipboard.
import fs from 'node:fs'
import path from 'node:path'
import { chromium } from 'playwright-core'

const [out, ...urls] = process.argv.slice(2)
if (!out || !urls.length) { console.error('usage: node codeblocks-browser.mjs OUT_DIR URL...'); process.exit(2) }
fs.mkdirSync(out, { recursive: true })

const CAPTURE = () => {
  window.__copied = null
  const orig = navigator.clipboard && navigator.clipboard.writeText
  if (orig) {
    navigator.clipboard.writeText = function (t) { window.__copied = String(t); return orig.call(this, t).catch(() => {}) }
  }
  document.addEventListener('copy', () => {
    const a = document.activeElement
    const t = a && (a.tagName === 'TEXTAREA' || a.tagName === 'INPUT') ? a.value.slice(a.selectionStart, a.selectionEnd) : String(document.getSelection())
    window.__copied = t
  }, true)
}

const browser = await chromium.launch({ channel: 'chrome' })
let fail = 0
for (const url of urls) {
  const context = await browser.newContext()
  await context.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: new URL(url).origin })
  await context.addInitScript(CAPTURE)
  const page = await context.newPage()
  const errors = []
  page.on('console', (m) => { if (m.type() === 'error' && !m.text().startsWith('Failed to load resource')) errors.push('console: ' + m.text().slice(0, 160)) })
  page.on('pageerror', (e) => errors.push('page error: ' + String(e.message).slice(0, 160)))
  page.on('requestfailed', (r) => errors.push('request failed: ' + r.url()))
  page.on('response', (r) => { if (r.status() >= 400 && !/favicon\.(svg|ico)$/.test(r.url())) errors.push(`response ${r.status()}: ${r.url()}`) })
  await page.goto(url, { waitUntil: 'networkidle' })
  await page.waitForTimeout(800)
  const n = await page.evaluate(() => document.querySelectorAll('pre').length)
  let clicked = 0
  for (let i = 0; i < n; i++) {
    const has = await page.evaluate((i) => {
      const pre = document.querySelectorAll('pre')[i]
      let s = pre
      for (let k = 0; k < 5 && s && (s === pre || s.querySelectorAll('pre').length === 1); k++, s = s.parentElement) {
        const b = [...s.querySelectorAll('button')].find((b) => /copy|clipboard/i.test([b.title, b.getAttribute('aria-label'), b.className].join(' ')))
        if (b) { window.__copied = null; b.click(); return true }
      }
      return false
    }, i)
    if (!has) continue
    await page.waitForTimeout(150)
    await page.evaluate((i) => {
      const pre = document.querySelectorAll('pre')[i]
      if (window.__copied !== null) pre.setAttribute('data-copied-text', window.__copied)
    }, i)
    clicked++
  }
  const name = new URL(url).pathname.split('/').filter(Boolean).slice(-2).join('-') || 'index'
  fs.writeFileSync(path.join(out, name + '.html'), await page.content())
  console.log(`== ${url}`)
  console.log(`   ${n} pre elements, ${clicked} copy buttons clicked; saved ${name}.html`)
  for (const e of errors) console.log(`   ${e}`)
  if (errors.length) fail = 1
  await context.close()
}
await browser.close()
process.exit(fail)
