#!/usr/bin/env python3
"""Assemble editable HTML sections into a GitHub Pages-ready index.html."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / '_includes/home.template').read_text(encoding='utf-8')
def insert(match):
    name=match.group(1)
    if name not in {'hero.html','about.html','projects.html','stack.html','research.html','education.html','contact.html'}:
        raise ValueError(f'Unexpected include: {name}')
    return (ROOT / '_includes' / name).read_text(encoding='utf-8')
output = re.sub(r'<!-- INCLUDE ([\w.]+) -->', insert, source)
(ROOT/'index.html').write_text(output, encoding='utf-8')
print('Built index.html')
