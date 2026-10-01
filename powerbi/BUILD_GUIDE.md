# Build the retail report in Power BI Desktop

The repository includes source data, checked calculations, a theme, a browser preview and a prepared native Power BI project. For the faster route, follow [Open the prepared Power BI report](OPEN_PROJECT.md); its cards and charts are already defined. The instructions below explain how to build the same report manually and study its calculations. A native Desktop check and final `.pbix` export are still required.

## Import and select a month

Open the cloned repository in GitHub Desktop. In Power BI Desktop choose **Get data → Text/CSV** and select `data/retail_sales_monthly.csv`. Choose **Transform Data**. Verify `month` is Date, `geography` and `quality_status` are Text, and `sales_cad_thousands` is Whole number. Power BI Desktop already recognized the date in this import, so no additional date column is needed. Choose **Close & Apply**. Confirm 172 rows: 43 months × four geographies.

Under **Modeling → New table** add a disconnected month picker. Do not relate it to the source table: the selected month should control the cards while the trend chart displays the whole series.

```DAX
Report Month = DISTINCT ( retail_sales_monthly[month] )
```

Place `Report Month[month]` (the date field, not its automatic date hierarchy) in a slicer. Change its style from Between to Dropdown, set **Single select** on and choose July 1, 2026 for the published checks.

## Add measures

For a faster setup, open [`retail-measures.tmdl`](retail-measures.tmdl), copy the entire file, open **TMDL view** in Power BI Desktop, paste into an empty script tab, choose **Preview** to review the changes and then **Apply**. This adds all measures to the existing `retail_sales_monthly` table in one operation; it assumes the source table and the disconnected `Report Month` table above already exist. Save the report. The script uses self-contained measure expressions so newly introduced measure names do not trigger unresolved-reference diagnostics. Power BI Desktop must validate the script before you use the results. The formulas are also shown below for study or manual entry via **Modeling → New measure**. The source values are thousands of Canadian dollars.

```DAX
Retail Sales CAD =
SUM ( retail_sales_monthly[sales_cad_thousands] ) * 1000

Selected Month =
COALESCE (
    SELECTEDVALUE ( 'Report Month'[month] ),
    CALCULATE ( MAX ( retail_sales_monthly[month] ), REMOVEFILTERS ( retail_sales_monthly ) )
)

Edmonton Sales CAD =
VAR TargetMonth = [Selected Month]
RETURN
    CALCULATE (
        [Retail Sales CAD],
        REMOVEFILTERS ( retail_sales_monthly ),
        retail_sales_monthly[month] = TargetMonth,
        retail_sales_monthly[geography] = "Edmonton, Alberta"
    )

Calgary Sales CAD =
VAR TargetMonth = [Selected Month]
RETURN
    CALCULATE (
        [Retail Sales CAD],
        REMOVEFILTERS ( retail_sales_monthly ),
        retail_sales_monthly[month] = TargetMonth,
        retail_sales_monthly[geography] = "Calgary, Alberta"
    )

Alberta Sales CAD =
VAR TargetMonth = [Selected Month]
RETURN
    CALCULATE (
        [Retail Sales CAD],
        REMOVEFILTERS ( retail_sales_monthly ),
        retail_sales_monthly[month] = TargetMonth,
        retail_sales_monthly[geography] = "Alberta"
    )

Edmonton Sales Last Year CAD =
VAR PriorYearMonth = EDATE ( [Selected Month], -12 )
RETURN
    CALCULATE (
        [Retail Sales CAD],
        REMOVEFILTERS ( retail_sales_monthly ),
        retail_sales_monthly[month] = PriorYearMonth,
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
VAR CurrentMonth = SELECTEDVALUE ( retail_sales_monthly[month] )
VAR CurrentSales = [Retail Sales CAD]
VAR PreviousSales =
    CALCULATE (
        [Retail Sales CAD],
        REMOVEFILTERS ( retail_sales_monthly[month] ),
        retail_sales_monthly[month] = EDATE ( CurrentMonth, -12 )
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
2. Add a line chart with `retail_sales_monthly[month]` on the x-axis, `Trend YoY %` on the y-axis and `retail_sales_monthly[geography]` as the legend. Filter this chart to Edmonton and Calgary. Avoid the automatic date hierarchy: use the date field itself.
3. Add three selected-month comparison cards using `Edmonton Sales CAD`, `Calgary Sales CAD` and `Alberta Sales CAD`, or a table containing all three. Keep their geography labels clear. A chart based directly on `Retail Sales CAD` needs an explicit month filter; otherwise it adds multiple months.
4. Add a source quality table with `month`, `geography`, and `quality_status`. This table shows source data quality for the full history; the month picker controls the headline measures.

Select July 2026 and compare with `python scripts/run_analysis.py`: Edmonton **CAD 3.583 billion**, Calgary **CAD 3.132 billion**, Edmonton **12.00% YoY**, Calgary **8.99% YoY** on the trend chart, and Edmonton share of Alberta **35.02%**. Check the five results and the chart visually before saving `powerbi/Edmonton-Retail-Pulse.pbix`. A `.pbip` project can also be saved for version control. Add a screenshot in `docs/` after verifying the native report.

These figures are unadjusted monthly sales and can be revised. The growth calculation compares each month with the same month a year earlier. The Edmonton share is a geographic share, not a company's market share.
