'use strict'

// Asciidoctor extension: header-rows=N on a table puts its first N rows in the
// table head. An AsciiDoc table has one header row, so a title row above the
// column headers needs two.
//
//   [%header,header-rows=2]
//   |===
//   2+^|Title
//   |Key |Value
//
//   |alpha |One
//   |===
module.exports.register = function (registry) {
  registry.treeProcessor(function () {
    this.process((doc) => {
      for (const table of doc.findBy({ context: 'table' })) {
        const n = parseInt(table.getAttribute('header-rows'), 10)
        const rows = table.getRows()
        if (n > rows.head.length) rows.head.push(...rows.body.splice(0, n - rows.head.length))
      }
      return doc
    })
  })
}
