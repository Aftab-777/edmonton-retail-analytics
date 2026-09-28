# Build the retail report in Power BI Desktop

The repository includes source data, checked calculations, a theme, and a browser preview. The native report (`.pbix`) must still be built and checked in Power BI Desktop.

## Import and select a month

Download the repository ZIP from GitHub and extract it. In Power BI Desktop choose **Get data → Text/CSV** and select `data/retail_sales_monthly.csv`. Choose **Transform Data**. Set `geography` and `quality_status` to Text and `sales_cad_thousands` to Whole number. Add a custom column `month_date` with `Date.FromText([month] & "-01")` and set its type to Date. Choose **Close & Apply**. Confirm 172 rows: 43 months × four geographies.

Under **Modeling → New table** add a disconnected month picker. Do not relate it to the source table: the selected month should control the cards while the trend chart displays the whole series.

```DAX
Report Month = DISTINCT ( retail_sales_monthly[month_date] )
```

Place `Report Month[month_date]` in a slicer. Set **Single select** on and choose July 1, 2026 for the published checks.

## Add measures

Use **Modeling → New measure** for each. The source values are thousands of Canadian dollars.

```DAX
Retail Sales CAD =
SUM ( retail_sales_monthly[sales_cad_thousands] ) * 1000

Selected Month =
COALESCE (
    SELECTEDVALUE ( 'Report Month'[month_date] ),
    CALCULATE ( MAX ( retail_sales_monthly[month_date] ), REMOVEFILTERS ( retail_sales_monthly ) )
)

Edmonton Sales CAD =
VAR TargetMonth = [Selected Month]
RETURN
    CALCULATE (
        [Retail Sales CAD],
        REMOVEFILTERS ( retail_sales_monthly ),
        retail_sales_monthly[month_date] = TargetMonth,
        retail_sales_monthly[geography] = "Edmonton, Alberta"
    )

Calgary Sales CAD =
VAR TargetMonth = [Selected Month]
RETURN
    CALCULATE (
        [Retail Sales CAD],
        REMOVEFILTERS ( retail_sales_monthly ),
        retail_sales_monthly[month_date] = TargetMonth,
        retail_sales_monthly[geography] = "Calgary, Alberta"
    )

Alberta Sales CAD =
VAR TargetMonth = [Selected Month]
RETURN
    CALCULATE (
        [Retail Sales CAD],
        REMOVEFILTERS ( retail_sales_monthly ),
        retail_sales_monthly[month_date] = TargetMonth,
        retail_sales_monthly[geography] = "Alberta"
    )

Edmonton Sales Last Year CAD =
VAR PreviousMonth = EDATE ( [Selected Month], -12 )
RETURN
    CALCULATE (
        [Retail Sales CAD],
        REMOVEFILTERS ( retail_sales_monthly ),
        retail_sales_monthly[month_date] = PreviousMonth,
        retail_sales_monthly[geography] = "Edmonton, Alberta"
    )

Edmonton YoY % =
DIVIDE (
    [Edmonton Sales CAD] - [Edmonton Sales Last Year CAD],
    [Edmonton Sales Last Year CAD]
)

Edmonton Share of Alberta % =
DIVIDE ( [Edmonton Sales CAD], [Alberta Sales CAD] )

Trend YoY % =
VAR CurrentMonth = SELECTEDVALUE ( retail_sales_monthly[month_date] )
VAR CurrentSales = [Retail Sales CAD]
VAR PreviousSales =
    CALCULATE (
        [Retail Sales CAD],
        REMOVEFILTERS ( retail_sales_monthly[month_date] ),
        retail_sales_monthly[month_date] = EDATE ( CurrentMonth, -12 )
    )
RETURN
    IF (
        NOT ISBLANK ( CurrentMonth ),
        DIVIDE ( CurrentSales - PreviousSales, PreviousSales )
    )
```

The trend measure removes only the month filter for the prior-year lookup, preserving the geography filter from the chart legend. Growth is blank in 2023 because the dataset has no 2022 comparison.

## Assemble and check the page

Import [the theme](retail-theme.json) through **View → Themes → Browse for themes**, and use the [browser preview](../dashboard/index.html) as the layout reference.

1. Add four cards: `Edmonton Sales CAD`, `Edmonton YoY %`, `Edmonton Share of Alberta %`, and `Calgary Sales CAD`. Set sales to CAD with billions display units; set percentages to two decimals.
2. Add a line chart with `retail_sales_monthly[month_date]` on the x-axis, `Trend YoY %` on the y-axis and `retail_sales_monthly[geography]` as the legend. Filter this chart to Edmonton and Calgary. Avoid the automatic date hierarchy: use the date field itself.
3. Add three selected-month comparison cards using `Edmonton Sales CAD`, `Calgary Sales CAD` and `Alberta Sales CAD`, or a table containing all three. Keep their geography labels clear. A chart based directly on `Retail Sales CAD` needs an explicit month filter; otherwise it adds multiple months.
4. Add a source quality table with `month`, `geography`, and `quality_status`. This table shows source data quality for the full history; the month picker controls the headline measures.

Select July 2026 and compare with `python scripts/run_analysis.py`: Edmonton **CAD 3.583 billion**, Calgary **CAD 3.132 billion**, Edmonton **12.00% YoY**, Calgary **8.99% YoY** on the trend chart, and Edmonton share of Alberta **35.02%**. Check the five results and the chart visually before saving `powerbi/Edmonton-Retail-Pulse.pbix`. A `.pbip` project can also be saved for version control. Add a screenshot in `docs/` after verifying the native report.

These figures are unadjusted monthly sales and can be revised. The growth calculation compares each month with the same month a year earlier. The Edmonton share is a geographic share, not a company's market share.
