# Recreate the report in Power BI Desktop

This project includes a clean CSV and SQL analysis, **not** a `.pbix` file. These steps describe how to build the Power BI report yourself and verify it against the published SQL results.

1. Choose **Get data → Text/CSV** and import `data/retail_sales_monthly.csv`.
2. In Power Query, set `geography` and `quality_status` to text, `sales_cad_thousands` to whole number, and add a `month_date` column with `Date.FromText([month] & "-01")`. Set `month_date` to Date. Select **Close & Apply**.
3. In **Modeling → New table**, create a calendar and relate its `Date` column (one) to `retail_sales_monthly[month_date]` (many). Mark the calendar as a date table using `Date`.

```DAX
Calendar = CALENDAR ( DATE ( 2023, 1, 1 ), DATE ( 2026, 7, 31 ) )

Retail Sales CAD =
SUM ( retail_sales_monthly[sales_cad_thousands] ) * 1000

Retail Sales Last Year =
CALCULATE ( [Retail Sales CAD], DATEADD ( 'Calendar'[Date], -1, YEAR ) )

YoY % =
DIVIDE ( [Retail Sales CAD] - [Retail Sales Last Year], [Retail Sales Last Year] )

Edmonton Share of Alberta % =
DIVIDE (
    CALCULATE ( [Retail Sales CAD], retail_sales_monthly[geography] = "Edmonton, Alberta" ),
    CALCULATE ( [Retail Sales CAD], retail_sales_monthly[geography] = "Alberta" )
)
```

4. Format `[Retail Sales CAD]` as currency with billions or millions display units; format the two percentage measures as percentages with two decimal places. In **View → Themes → Browse for themes**, import [`retail-theme.json`](retail-theme.json) to match the dashboard preview palette.
5. Use the [interactive dashboard preview](../dashboard/index.html) as a visual reference: a month slicer across the top; four cards (Edmonton sales, Edmonton YoY, Edmonton share of Alberta, Calgary sales); a two-city annual growth line chart; and a selected-month sales comparison for Edmonton, Calgary, and Alberta. For the growth line chart, put `Calendar[Date]` by month on the x-axis, `YoY %` on the y-axis, and `geography` in the legend; select Edmonton and Calgary. Use a table visual to show source quality status. Set the page to the latest month to check the cards.
6. Check July 2026 against `python scripts/run_analysis.py`: Edmonton **CAD 3.583 billion**, Calgary **CAD 3.132 billion**, Edmonton **12.00% YoY**, Calgary **8.99% YoY**, and Edmonton share of Alberta **35.02%**. Display rounding may differ slightly.

The values are unadjusted monthly sales. Use the same month in the previous year for growth; avoid presenting consecutive-month changes as seasonally adjusted trends. The snapshot can be revised in later Statistics Canada releases. The status column contains source data quality indicators and should remain available to readers.
