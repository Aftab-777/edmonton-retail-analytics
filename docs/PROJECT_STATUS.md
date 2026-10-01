# Project checkpoint — October 1, 2026

## Published deliverables

- A 172-row Statistics Canada snapshot for January 2023–July 2026: Edmonton, Calgary, Alberta, and Canada.
- Reproducible Python extraction, SQLite analysis, and an annual growth chart.
- An interactive [web demo](https://aftab-777.github.io/edmonton-retail-analytics/) using the same snapshot.
- A native [Power BI project](../powerbi/project/) with two pages, twelve measures, five headline cards, a month selector, a city annual-growth chart, a selected-month sales comparison, and source records/calculation notes.
- A [complete project ZIP](../powerbi/Edmonton-Retail-Pulse-Project.zip), [opening instructions](../powerbi/OPEN_PROJECT.md), [walkthrough](PROJECT_WALKTHROUGH.md), and [validation record](VALIDATION.md).
- An unchanged [native Desktop screenshot](screenshots/retail-overview-july-2026.png) showing the July overview.

## Verification completed

On October 1, 2026, the prepared `.pbip` project opened in Power BI Desktop and refreshed successfully. The supplied native screenshot shows all five July headline values and both populated charts. The July cards match the CSV and SQL: Edmonton CAD 3.583 billion, Edmonton annual growth 12.00%, Edmonton share of Alberta 35.02%, Calgary CAD 3.132 billion, and Calgary annual growth 8.99%. The comparison chart shows Alberta CAD 10.231 billion.

The project owner confirmed the month-switching check worked after selecting June: the cards and comparison changed, while the trend retained its history. This confirmation is distinct from the supplied July screenshot; a June screenshot was not supplied.

The native project passed Microsoft JSON schema and theme validation, embedded-snapshot integrity checks, visual field-reference and layout-bound checks, and Windows path-length checks. A fresh Statistics Canada archive download on October 1 matched all 172 committed sales values. See [VALIDATION.md](VALIDATION.md) for the scope of each check.

## Optional next improvements

1. Before a live presentation, open **Source data & notes**, check its labels, and take a second native screenshot. Its definitions and records have been checked, but no native screenshot of that page has been supplied.
2. Save an optional **Power BI file (.pbix)** from Desktop if a recruiter wants a single-file copy. The earlier locally saved `.pbix` is not part of this published repository.
3. Practise explaining the source units, twelve measures, disconnected month selector, SQL validation, and data limitations.
4. For a future release, review revised source values and rebuild the snapshot, web demo, and native project together.

The published `.pbip` and its adjacent folders are the native Power BI deliverable. GitHub Pages hosts the separate HTML demo. The embedded snapshot is fixed; Desktop **Refresh** does not download newer source data. Power BI service deployment and scheduled cloud refresh are outside the current project.
