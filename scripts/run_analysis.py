"""Load the committed CSV into SQLite and execute the portfolio SQL analysis."""

import csv
import pathlib
import sqlite3

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "retail_sales_monthly.csv"
SQL = ROOT / "sql" / "analysis.sql"


def main():
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE retail_sales (month TEXT, geography TEXT, sales_cad_thousands INTEGER, quality_status TEXT, PRIMARY KEY (month, geography))")
    with DATA.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    connection.executemany(
        "INSERT INTO retail_sales VALUES (:month, :geography, :sales_cad_thousands, :quality_status)", rows
    )
    print(f"Loaded {len(rows)} monthly observations; amounts are CAD thousands.\n")
    # sqlite3 executescript cannot return result sets, so run each SELECT block separately.
    blocks = SQL.read_text(encoding="utf-8").split("-- QUERY: ")[1:]
    for block in blocks:
        title, statement = block.split("\n", 1)
        result = connection.execute(statement.strip().rstrip(";"))
        print(title.strip())
        print(" | ".join(column[0] for column in result.description))
        for row in result.fetchall():
            print(" | ".join(str(value) if value is not None else "NULL" for value in row))
        print()
    connection.close()


if __name__ == "__main__":
    main()
