"""Writes vars.yml, the variables file the macros extension reads: the
round's excerpt of the book's template_variables.yml (../../source/) with
its top key renamed to `vars`."""
import yaml

src = yaml.safe_load(open('../../source/template_variables.yml', encoding='utf-8'))['template_variables']
with open('vars.yml', 'w', encoding='utf-8') as f:
    yaml.safe_dump({'vars': src}, f, allow_unicode=True, sort_keys=False, width=1000)
