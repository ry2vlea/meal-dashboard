#!/usr/bin/env python3
"""Copy data/meals.json into the embedded fallback <script id="seed"> block in index.html.
Run after editing data/meals.json:  python3 scripts/embed.py"""
import json, re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root / "data/meals.json").read_text(encoding="utf-8"))
blob = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
html = (root / "index.html").read_text(encoding="utf-8")
pat = re.compile(r'(<script id="seed" type="application/json">\n).*?(\n</script>)', re.S)
if not pat.search(html):
    raise SystemExit("seed block not found in index.html")
html = pat.sub(lambda m: m.group(1) + blob + m.group(2), html, count=1)
(root / "index.html").write_text(html, encoding="utf-8")
print(f"embedded {len(data['entries'])} entries into index.html")
