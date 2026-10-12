# Sphinx with MyST, the default theme, and the shared template variables.
import re
from pathlib import Path

from docutils import nodes

import yaml

project = "Tables round — Sphinx/MyST probe"
root_doc = "scale-table-host"
extensions = ["myst_parser"]
# attrs_inline: `/var/vcap/jobs/JOB`{.path} gives the code a class.
myst_enable_extensions = ["substitution", "attrs_inline"]
# Partials (_name.md) are included by a host page, not built as pages.
exclude_patterns = ["_build", "_*.md"]

# The source's vars.name becomes {{name}}.
_vars = Path(__file__).parent / "../../../source/template_variables.yml"
myst_substitutions = yaml.safe_load(_vars.read_text())["template_variables"]

html_static_path = ["_static"]
html_css_files = ["hints.css"]

# Hint classes on a table (colN-key, colN-value, colN-prose, colN-nowrap, N
# from 1) mark that column's cells, as the other sites' list tables do:
# role-key ... and wrap-avoid. One rule in hints.css then serves any column,
# and the table gets the hinted class. NOTE: rows below a cell that spans
# rows are not adjusted.
_HINT = re.compile(r"^col([1-9][0-9]*)-(key|value|prose|nowrap)$")


def _mark_columns(app, doctree):
    for table in doctree.findall(nodes.table):
        cols = {}
        for m in filter(None, map(_HINT.match, table["classes"])):
            mark = "wrap-avoid" if m[2] == "nowrap" else f"role-{m[2]}"
            cols.setdefault(int(m[1]) - 1, []).append(mark)
        if cols and "hinted" not in table["classes"]:
            table["classes"].append("hinted")
        for row in table.findall(nodes.row) if cols else ():
            col = 0
            for entry in row.children:
                entry["classes"] += cols.get(col, [])
                col += 1 + entry.get("morecols", 0)


def setup(app):
    app.connect("doctree-read", _mark_columns)
