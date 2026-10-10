// The default UI gives a table no box of its own, so a table wider than the
// article widens the page. Each table goes in a box that scrolls sideways.
document.querySelectorAll('.doc table').forEach(function (table) {
  var box = document.createElement('div')
  box.className = 'table-scroll'
  table.parentNode.insertBefore(box, table)
  box.appendChild(table)
})
