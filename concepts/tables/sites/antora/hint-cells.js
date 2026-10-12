// Asciidoctor tree processor: hint classes on a table (colN-key, colN-value,
// colN-prose, colN-nowrap, N from 1) mark that column's cells, as the other
// sites' list tables do: role-key ... and wrap-avoid. One rule in hints.css
// then serves any column, and the table gets the hinted role.
//
// The HTML converter writes a cell's class from its alignment only
// ("tableblock halign-X valign-Y") and has no cell role, so the marks are
// appended to the cell's valign attribute and reach the class through it.
// NOTE: this depends on that string; `make check` fails if the marks are lost.
const HINT = /^col([1-9][0-9]*)-(key|value|prose|nowrap)$/;

module.exports.register = function (registry) {
  registry.treeProcessor(function () {
    this.process((doc) => {
      for (const table of doc.findBy({context: 'table'})) {
        const cols = [];
        for (const m of table.getRoles().map((r) => HINT.exec(r)).filter(Boolean)) {
          (cols[m[1] - 1] ||= []).push(m[2] === 'nowrap' ? 'wrap-avoid' : `role-${m[2]}`);
        }
        if (!cols.length) continue;
        table.addRole('hinted');
        const rows = table.getRows();
        for (const row of [...rows.getHead(), ...rows.getBody(), ...rows.getFoot()]) {
          // A cell's own column ignores the spans before it, so count them.
          // NOTE: rows below a cell that spans rows are not adjusted.
          let col = 0;
          for (const cell of row) {
            const marks = cols[col];
            if (marks) cell.setAttribute('valign', `${cell.getAttribute('valign')} ${marks.join(' ')}`);
            col += cell.getColumnSpan() || 1;
          }
        }
      }
      return doc;
    });
  });
};
