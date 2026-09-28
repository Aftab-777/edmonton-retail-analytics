"""Download and extract a reproducible subset of Statistics Canada table 20-10-0056-01."""

import csv
import io
import pathlib
import urllib.request
import zipfile

SOURCE_URL = "https://www150.statcan.gc.ca/n1/tbl/csv/20100056-eng.zip"
GEOGRAPHIES = ("Edmonton, Alberta", "Calgary, Alberta", "Alberta", "Canada")
START_MONTH = "2023-01"
END_MONTH = "2026-07"  # Snapshot limit: data available on September 24, 2026.
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "retail_sales_monthly.csv"


def build():
    request = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "PortfolioDataStudy/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        archive_bytes = response.read()
    rows = []
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        with archive.open("20100056.csv") as source:
            reader = csv.DictReader(io.TextIOWrapper(source, encoding="utf-8-sig", newline=""))
            for row in reader:
                if not (START_MONTH <= row["REF_DATE"] <= END_MONTH):
                    continue
                if row["GEO"] not in GEOGRAPHIES:
                    continue
                if row["North American Industry Classification System (NAICS)"] != "Retail trade [44-45]":
                    continue
                if row["Sales"] != "Total retail sales" or row["Adjustments"] != "Unadjusted":
                    continue
                if not row["VALUE"]:
                    raise ValueError(f"Missing value for {row['GEO']} {row['REF_DATE']}")
                rows.append((row["REF_DATE"], row["GEO"], int(float(row["VALUE"])), row["STATUS"]))

    rows.sort(key=lambda item: (item[0], GEOGRAPHIES.index(item[1])))
    expected_months = 43  # January 2023 through July 2026 inclusive.
    if len(rows) != len(GEOGRAPHIES) * expected_months:
        raise ValueError(f"Expected {len(GEOGRAPHIES) * expected_months} rows, got {len(rows)}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.writer(destination)
        writer.writerow(("month", "geography", "sales_cad_thousands", "quality_status"))
        writer.writerows(rows)
    print(f"Wrote {len(rows)} observations to {OUTPUT}")


if __name__ == "__main__":
    build()
