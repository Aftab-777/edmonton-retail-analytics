"""Embed the committed retail CSV in a self-contained, offline HTML dashboard."""

import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "dashboard" / "template.html"
OUTPUT = ROOT / "dashboard" / "index.html"

with (ROOT / "data" / "retail_sales_monthly.csv").open(encoding="utf-8", newline="") as source:
    rows = list(csv.DictReader(source))
records = [
    [row["month"], row["geography"], int(row["sales_cad_thousands"]), row["quality_status"]]
    for row in rows
]
if len(records) != 172 or len({(row[0], row[1]) for row in records}) != 172:
    raise ValueError("The dashboard requires the complete, unique 172-row source snapshot")

html = TEMPLATE.read_text(encoding="utf-8").replace("__EMBEDDED_DATA__", json.dumps(records, separators=(",", ":")))
OUTPUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUTPUT} with {len(records)} embedded observations")
