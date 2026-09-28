"""Render an optional chart from the committed dataset (requires matplotlib)."""

import csv
import pathlib

import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
with (ROOT / "data" / "retail_sales_monthly.csv").open(encoding="utf-8", newline="") as source:
    rows = list(csv.DictReader(source))

fig, ax = plt.subplots(figsize=(10.4, 4.9), layout="constrained")
for city, colour in (("Edmonton, Alberta", "#1457a3"), ("Calgary, Alberta", "#d97732")):
    city_rows = [r for r in rows if r["geography"] == city]
    months = [r["month"] for r in city_rows]
    amounts = [int(r["sales_cad_thousands"]) for r in city_rows]
    annual_change = [100 * (amounts[i] / amounts[i-12] - 1) for i in range(12, len(amounts))]
    ax.plot(months[12:], annual_change, label=city.split(",")[0], color=colour, linewidth=2.3)

ax.axhline(0, color="#596579", linewidth=0.8, linestyle="--")
ax.set_title("Retail sales growth: Edmonton and Calgary", loc="left", fontsize=15, fontweight="bold")
ax.set_ylabel("Year-over-year change (%)")
ax.set_xlabel("Month (unadjusted sales, same month one year earlier)", labelpad=12)
ax.set_xticks(months[12::4])
ax.tick_params(axis="x", rotation=30)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.2)
ax.legend(frameon=False, loc="upper left", ncol=2)
fig.text(0.99, -0.055, "Source: Statistics Canada, table 20-10-0056-01 · snapshot: 24 Sep 2026", ha="right", fontsize=8, color="#525f70")
target = ROOT / "docs" / "retail_growth.svg"
target.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(target, format="svg", bbox_inches="tight")
print(target)
