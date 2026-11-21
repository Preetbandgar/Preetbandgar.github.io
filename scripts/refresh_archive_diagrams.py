#!/usr/bin/env python3
"""Update the two embedded archive diagrams from their PNG source files."""
from pathlib import Path
import base64, re
site = Path(__file__).resolve().parent.parent
index = site / "projects" / "index.html"
html = index.read_text(encoding="utf-8")
for name in ("Terraform-aws-eks", "FullStack-Blogging-App"):
    asset = f"../assets/projects/diagrams/{name}.png"
    data = base64.b64encode((site / "assets" / "projects" / "diagrams" / f"{name}.png").read_bytes()).decode("ascii")
    pattern = r'(src=")data:image/png;base64,[^"]+(" data-original-asset="' + re.escape(asset) + r'")'
    html, count = re.subn(pattern, lambda m: m.group(1) + "data:image/png;base64," + data + m.group(2), html)
    if count != 1:
        raise RuntimeError(f"Could not find embedded diagram for {name} in projects/index.html")
index.write_text(html, encoding="utf-8")
print("Updated both archive diagrams.")
