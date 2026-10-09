# Sphinx with MyST, the default theme, and the shared template variables.
from pathlib import Path

import yaml

project = "Tables round — Sphinx/MyST probe"
root_doc = "scale-table-host"
extensions = ["myst_parser"]
myst_enable_extensions = ["substitution"]
# Partials (_name.md) are included by a host page, not built as pages.
exclude_patterns = ["_build", "_*.md"]

# The source's vars.name becomes {{name}}.
_vars = Path(__file__).parent / "../../../source/template_variables.yml"
myst_substitutions = yaml.safe_load(_vars.read_text())["template_variables"]

html_static_path = ["_static"]
html_css_files = ["hints.css"]
