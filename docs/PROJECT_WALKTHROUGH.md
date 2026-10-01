# Edmonton Retail Pulse: project walkthrough

## Purpose

This independent portfolio study answers three main questions: the size of Edmonton monthly retail sales, growth against the same month a year earlier, and Edmonton's share of Alberta sales. Calgary provides a city comparison, and the trend chart shows whether the headline results fit the longer history.

## From source to report

1. **Select the public series.** Use Statistics Canada table 20-10-0056-01, total retail sales, retail trade [44-45], unadjusted observations, January 2023–July 2026.
2. **Create the snapshot.** `scripts/build_dataset.py` downloads the original CSV archive and keeps Edmonton, Calgary, Alberta, and Canada. The resulting CSV has 172 rows: 43 consecutive months × four geographies.
3. **Check the data.** Confirm a unique month/geography key, complete months, nonmissing sales, source units, and retained quality codes. The 2023 rows supply the prior-year values needed for 2024 growth.
4. **Calculate independently in SQL.** `scripts/run_analysis.py` loads the committed CSV into SQLite and executes `sql/analysis.sql`. The queries calculate latest sales, annual growth, Edmonton's provincial share, and a 12-month growth series.
5. **Build the Power BI model.** Import the snapshot with a Date month, Whole number sales, and Text geography/status. A disconnected `Report Month` table provides the month selector. Twelve explicit DAX measures supply the report.
6. **Build and check the visuals.** Five headline cards, a month dropdown, a two-city growth line chart, a three-geography sales bar chart, and a source/notes page form the native report. The July Desktop screenshot and owner-confirmed month switching record its working behavior.
7. **Publish reproducible deliverables.** GitHub holds the CSV, SQL, scripts, native definitions, documentation, and screenshot. GitHub Pages hosts a separate HTML demo generated from the same data.

## Data dictionary

| Field | Meaning and Power BI type |
| --- | --- |
| `month` | Monthly reference period. CSV uses `YYYY-MM`; Power BI uses a Date on the first day of that month. |
| `geography` | Edmonton metropolitan area, Calgary metropolitan area, Alberta, or Canada; Text. |
| `sales_cad_thousands` | Source retail sales in thousands of Canadian dollars; Whole number. Multiply by 1,000 for CAD. |
| `quality_status` | Source status code retained as Text. Consult Statistics Canada metadata before interpreting the codes. |

There is no customer-level data, transaction table, or company revenue in this dataset. The province and country totals include the city observations, so the four geography series are not additive.

## Model and filter choices

The fact table is `retail_sales_monthly`. `Report Month` is `DISTINCT(retail_sales_monthly[month])` with **no relationship** to the fact table. Headline measures explicitly read the picker and filter the appropriate month. This makes one month drive the cards and comparison while the line chart still shows history.

`SELECTEDVALUE` reads a single selected month; `COALESCE` falls back to the latest snapshot month when it is not uniquely selected. Fixed-city headline measures clear fact-table filters and apply the chosen city/month. The comparison measure preserves the geography axis. The trend measure removes only the month filter when finding the prior year's amount, preserving the city context.

## Twelve measures

| Measure | Role |
| --- | --- |
| `Retail Sales CAD` | Convert source thousands to CAD. |
| `Selected Month` | Single chosen month, with a latest-month fallback. |
| `Edmonton Sales CAD` | Edmonton amount for the chosen month. |
| `Calgary Sales CAD` | Calgary amount for the chosen month. |
| `Alberta Sales CAD` | Alberta amount for the chosen month. |
| `Edmonton Sales Last Year CAD` | Edmonton amount 12 months earlier. |
| `Calgary Sales Last Year CAD` | Calgary amount 12 months earlier. |
| `Edmonton YoY %` | Edmonton same-month annual percentage change. |
| `Calgary YoY %` | Calgary same-month annual percentage change. |
| `Edmonton Share of Alberta %` | Edmonton amount divided by Alberta amount for the same month. |
| `Trend YoY %` | Annual change for each month/city on the trend chart. |
| `Selected Month Sales CAD` | Selected-month amount that preserves the comparison's geography axis. |

The eleven core measures are in `powerbi/retail-measures.tmdl`. The native builder adds the twelfth comparison measure. The native table definitions use self-contained expressions for several calculations, preserving the same logic and verified results.

## Calculate and interpret July 2026

| Result | Calculation | Verified result |
| --- | --- | ---: |
| Edmonton sales | 3,583,120 source thousands × 1,000 | CAD 3,583,120,000 |
| Edmonton annual growth | (3,583,120 − 3,199,154) ÷ 3,199,154 | 12.00% |
| Calgary annual growth | (3,131,691 − 2,873,274) ÷ 2,873,274 | 8.99% |
| Edmonton share of Alberta | 3,583,120 ÷ 10,231,135 | 35.02% |

Because numerator and denominator use the same units, converting thousands to CAD does not change the percentages. Edmonton grew faster than Calgary by about 3.01 percentage points. This describes a value change; it does not demonstrate the cause, changes in real sales volume, or a company's market share.

SQL uses `LAG(sales_cad_thousands, 12) OVER (PARTITION BY geography ORDER BY month)`. A twelve-row lag corresponds to a year only because the monthly series is complete. For sparse monthly records, use a calendar/date join instead.

## Demonstrate the project

1. Open the GitHub README and explain the business questions, source, and available deliverables.
2. Show the native July screenshot or open the `.pbip` in Power BI Desktop and refresh it.
3. Explain the five cards, then compare the two cities' annual growth and the province/city bars.
4. Switch to June. The headlines and bars change; the trend keeps its history. Edmonton June growth is 9.91%.
5. Open **Source data & notes** and explain the units, geographic overlap, status codes, and dated snapshot. Check this page's readability before a live demonstration.
6. Show the SQL query and DAX measure behind one percentage. Explain how their agreement validates the result.

## Concise project explanation

“Edmonton Retail Pulse is my portfolio project using Statistics Canada's monthly retail sales. It combines Python data preparation, SQLite analysis, and a Power BI report to compare Edmonton with Calgary and Alberta. I used a disconnected month selector so the cards change while the historical trend remains visible, and checked the results against SQL. In July 2026, Edmonton sales were CAD 3.583 billion, up 12.00% year over year, and represented 35.02% of Alberta sales. The repository includes the data, queries, native report definitions, and verification evidence.”

## Limits and future improvements

- The data is unadjusted and is not deflated by this project. Same-month annual comparison is useful but does not remove all seasonal or price effects.
- Statistical revisions may change past values. The fixed snapshot matched a fresh download on October 1, 2026.
- Desktop refresh loads the embedded snapshot; automatic source updates and Power BI service deployment are not implemented.
- Future improvements could add a maintained calendar, category detail, population-adjusted comparisons, or a reviewed update pipeline, using compatible sources.
- The native overview was checked in Desktop; a source-page screenshot and a `.pbix` export are optional additional deliverables, not prerequisites for using the published native `.pbip` project.

Source: [Statistics Canada table 20-10-0056-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2010005601), accessed September 27, 2026, reused under its [Open Licence](https://www.statcan.gc.ca/en/terms-conditions/open-licence). This independent project is not endorsed by Statistics Canada.
