# Validation record — October 1, 2026

This record separates calculations and file checks from the native Desktop evidence. The analysis uses the committed January 2023–July 2026 snapshot.

## Data and source

- 172 records: 43 months × four geographies.
- Unique `(month, geography)` keys; each geography has the same consecutive January 2023–July 2026 series.
- No missing sales values in the selected series. Amounts are retained in source thousands of CAD; status codes are preserved.
- Selected source dimensions: `Retail trade [44-45]`, `Total retail sales`, `Unadjusted`.
- A fresh download of the Statistics Canada archive on October 1, 2026 matched all **172 sales values** in the committed CSV. This does not guarantee that later releases will remain unchanged.
- CSV SHA-256: `9225a9d7c80c4d16b5003ebad994fd40899035e55d72b02729d6e5b20a6425b3`.

## Calculations

The SQLite queries, CSV arithmetic, and native July report agree after display rounding:

| Measure | Exact input/result or rounded percentage |
| --- | ---: |
| Edmonton July 2026 sales, CAD | 3,583,120,000 |
| Edmonton July 2025 sales, CAD | 3,199,154,000 |
| Calgary July 2026 sales, CAD | 3,131,691,000 |
| Calgary July 2025 sales, CAD | 2,873,274,000 |
| Alberta July 2026 sales, CAD | 10,231,135,000 |
| Edmonton annual growth | 12.00% |
| Calgary annual growth | 8.99% |
| Edmonton share of Alberta | 35.02% |
| Edmonton June annual growth | 9.91% |

Run `python scripts/run_analysis.py` from the repository root to reproduce the SQL output. SQL's twelve-row lag is appropriate because every monthly series is consecutive. A first-year growth result is blank when the prior-year amount is absent.

## Native project files

- 34 schema-bound JSON definitions validated against Microsoft's PBIP/PBIR schemas; report theme validated against its theme schema.
- Embedded CSV decoded and compared with the exact committed snapshot.
- Twelve measures, report field references and visual roles checked; two pages and 26 visual containers, including titles and notes.
- Visual bounds checked against the 1280 × 720 report canvas.
- Project paths checked for the known Windows clone location; project definitions contain no machine-specific source CSV path.
- The project ZIP contains the `.pbip`, adjacent report/model folders, opening notes, and source CSV; archive integrity checked.

The format checks alone do not prove Power BI Desktop can execute or render a report. The Desktop evidence below supplies that additional check.

## Desktop evidence

- The eleven core measures applied in Desktop with zero reported problems before the prepared native layout was opened.
- The prepared `.pbip` opened and refreshed successfully on October 1, 2026.
- The unchanged [July screenshot](screenshots/retail-overview-july-2026.png) shows all five expected headline values, a populated Edmonton/Calgary trend, and the Alberta/Edmonton/Calgary comparison. Alberta's bar is approximately CAD 10.231 billion.
- The project owner confirmed the month-switching check worked: cards and comparison changed while the trend retained its history. This is owner confirmation; no June screenshot was supplied.
- The source page definitions and records were checked. Its native visual layout has not been evidenced by a supplied screenshot; review it before a live presentation.

## Delivery scope

The repository publishes a native Power BI **project** and a separate HTML demo. The earlier local `.pbix` has not been uploaded; a `.pbix` export is optional. No Power BI service deployment, scheduled cloud refresh, row-level security, commercial client outcome, or measured business savings is claimed.

The snapshot is fixed. Power BI Desktop **Refresh** loads the embedded records; it does not download new Statistics Canada data. The underlying figures are unadjusted and may be revised.
