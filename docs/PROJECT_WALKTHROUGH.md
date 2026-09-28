# Retail analytics project walkthrough

## Purpose

This independent portfolio exercise studies monthly retail sales in the Edmonton census metropolitan area and compares Edmonton with Calgary and Alberta. The dashboard answers three practical questions: how large Edmonton retail sales were in a selected month, how sales changed against the same month a year earlier, and how Edmonton compares with the Alberta total.

## Source and structure

The source is Statistics Canada table 20-10-0056-01. The committed snapshot covers January 2023 through July 2026: 43 months for Edmonton, Calgary, Alberta, and Canada, yielding 172 rows. It keeps total retail sales, retail trade [44-45], and unadjusted observations. Each row has a month, geography, sales amount in thousands of Canadian dollars, and source quality status.

The import into Power BI Desktop treats `month` as a Date, `sales_cad_thousands` as a Whole number, and the descriptive columns as Text. The separate `Report Month` table is a disconnected picker. It controls the headline measures without cutting the historical line chart down to a single month.

## Calculation logic

| Result | How it is calculated | July 2026 check |
| --- | --- | ---: |
| Edmonton sales | Edmonton row for the selected month, multiplied by 1,000 to convert source thousands to CAD | CAD 3.583 billion |
| Calgary sales | Calgary row for the selected month, same conversion | CAD 3.132 billion |
| Edmonton annual growth | (Edmonton sales in selected month ÷ Edmonton sales in the same month one year earlier) − 1 | 12.00% |
| Calgary annual growth | Same calculation for Calgary | 8.99% |
| Edmonton share of Alberta | Edmonton sales ÷ Alberta sales in the same month | 35.02% |

The SQL query in `sql/analysis.sql` independently computes annual growth with a 12-month lag within each geography. `scripts/run_analysis.py` runs that query against the committed CSV. The Power BI measures in `powerbi/retail-measures.tmdl` use the selected month and `EDATE(..., -12)` for the corresponding prior-year row. Results should agree after display rounding.

## Reading the visuals

The cards summarize the selected month. The line chart shows the Edmonton and Calgary annual growth series over time; 2023 has no growth values because the source snapshot does not include 2022. The source quality table preserves the Statistics Canada status codes. For July 2026, Edmonton and Alberta are marked A and Calgary is marked B in this snapshot.

## Limits and next questions

- The observations are **unadjusted**: a change between consecutive months may reflect seasonal patterns. Annual growth compares the same calendar month across years.
- Edmonton and Calgary refer to metropolitan areas; Alberta refers to the entire province. The Edmonton/Alberta ratio is a geographic share, not a company's market share.
- Statistics Canada can revise source figures. This repository preserves a dated snapshot for reproducibility; refreshing the source may change the results.
- Further analysis could investigate category-level retail sales or population-adjusted measures, if consistent public series are available and the geographic definitions align.

## Demonstration path

Open the interactive preview, change the month, and describe which cards change and which historical trend remains visible. Then open the native Power BI report once it has been completed and verified, show how the disconnected picker controls the headline measures, and compare the five July 2026 figures with the SQL output. Explain the conversion from thousands to dollars and the same-month-prior-year growth calculation.

Only present the native Power BI report as completed after it has been built and checked in Power BI Desktop.
