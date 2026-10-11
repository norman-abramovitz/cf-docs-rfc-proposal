"""Writes the variables files the macros extension reads, from the book's
template_variables.yml (../../source/): vars.yml for passthrough, the file
with its top key renamed to `vars`; vars-native.yml for native, the same
with every empty value written as "" (Jinja prints a null as "None") and
the key that is not a name left out."""
import re
import yaml

src = yaml.safe_load(open('../../source/template_variables.yml', encoding='utf-8'))['template_variables']
with open('vars.yml', 'w', encoding='utf-8') as f:
    yaml.safe_dump({'vars': src}, f, allow_unicode=True, sort_keys=False, width=1000)
native = {k: ('' if v is None else v) for k, v in src.items() if re.fullmatch(r'\w+', k)}
with open('vars-native.yml', 'w', encoding='utf-8') as f:
    yaml.safe_dump({'vars': native}, f, allow_unicode=True, sort_keys=False, width=1000)
