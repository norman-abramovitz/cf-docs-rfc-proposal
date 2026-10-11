// Notes in the browser: for each page, the console errors and failed
// requests on load and, for each note, the label the reader sees (after CSS,
// so capitals made by text-transform show; in Antora also the colour of the
// mark the label sits on), the box's left border and background colours,
// and whether the note has a box at all (any border or background).
//
// Usage: node notes-browser.mjs URL...
// Needs Google Chrome installed; each site served (make serve).
import { chromium } from 'playwright-core'

const SELECTOR = [
  'p.note', 'div.note',                       // published book, passthrough
  'div.theme-admonition',                     // Docusaurus
  'div.admonition',                           // Zensical
  'aside.starlight-aside',                    // Starlight
  'div.admonitionblock'                       // Antora
].join(',')

function probe (selector) {
  const out = []
  for (const n of document.querySelectorAll(selector)) {
    if (n.parentElement.closest(selector)) continue
    let box = n
    let label = ''
    let mark = ''
    if (n.classList.contains('admonitionblock')) {
      // Antora's default UI: the label is the icon's title, shown by CSS
      // (::after { content: attr(title) }) on a coloured mark; the box is
      // the content cell
      const i = n.querySelector('td.icon i')
      const t = n.querySelector('td.content > .title')
      label = t ? t.innerText.trim() : (i ? i.getAttribute('title') : '')
      if (!t && i && getComputedStyle(i, '::after').textTransform === 'uppercase') label = label.toUpperCase()
      if (i) mark = getComputedStyle(i).backgroundColor
      box = n.querySelector('td.content') || n
    } else {
      const title = n.querySelector('.note__title, [class*="admonitionHeading"], .admonition-title, .starlight-aside__title')
      label = title ? title.innerText.trim() : ''
    }
    const cs = getComputedStyle(box)
    const border = ['Left', 'Top'].map((s) => cs[`border${s}Width`] !== '0px' && cs[`border${s}Style`] !== 'none' ? cs[`border${s}Color`] : '').filter(Boolean)[0] || ''
    const bg = cs.backgroundColor
    const boxed = !!border || (bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent')
    out.push({ cls: n.className, label: label.replace(/\s+/g, ' '), mark, border, bg, boxed, text: n.innerText.replace(/\s+/g, ' ').trim().slice(0, 50) })
  }
  return out
}

const browser = await chromium.launch({ channel: 'chrome' })
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } })
for (const url of process.argv.slice(2)) {
  const errors = []
  page.removeAllListeners('console')
  page.removeAllListeners('pageerror')
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text().split('\n')[0].slice(0, 160) + (m.location().url ? ` [${m.location().url}]` : '')) })
  page.on('pageerror', (e) => errors.push(String(e).split('\n')[0].slice(0, 160)))
  page.removeAllListeners('response')
  page.on('response', (r) => { if (r.status() >= 400) errors.push(`  (${r.status()} for ${r.url()})`) })
  await page.goto(url, { waitUntil: 'networkidle' })
  await page.waitForTimeout(500)
  // A missing favicon is the local server's, not the page's
  const shown = errors.filter((e) => !/favicon/.test(e))
  const notes = await page.evaluate(probe, SELECTOR)
  console.log(`\n${url}`)
  console.log(`  console errors: ${shown.length ? '' : 'none'}`)
  for (const e of shown) console.log(`    ${e}`)
  notes.forEach((n, i) => console.log(`  ${i + 1}. ${n.cls} | label "${n.label}"${n.mark ? ` on ${n.mark}` : ''} | ${n.boxed ? `box: border ${n.border || '-'}, background ${n.bg}` : 'no box'} | ${n.text}`))
}
await browser.close()
