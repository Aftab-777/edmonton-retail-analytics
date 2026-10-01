# Open the prepared Power BI report

The native project in [`project/`](project/) contains the report layout, five headline cards, a month dropdown, an Edmonton–Calgary growth chart, a selected-month sales comparison and a second page with the source records and calculation notes. It uses the same Statistics Canada snapshot and the eleven measures already checked in Power BI Desktop. One additional measure supplies the selected-month comparison chart.

Use the Power BI Desktop already installed on your computer. Opening and editing this local project does not require a Power BI Pro subscription, a new application or a paid custom visual. Microsoft documents [Power BI projects](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview) and [the report format](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report).

## Open it

1. Save the report you currently have open in Power BI Desktop. The prepared project is in its own folder and does not replace that file.
2. In **GitHub Desktop**, select `edmonton-retail-analytics`, click **Fetch origin**, then **Pull origin** if it appears.
3. Choose **Repository → Show in Explorer**. Open **powerbi → project**, then double-click **Edmonton-Retail-Pulse.pbip**. Keep both the `Retail.Report` and `Retail.SemanticModel` folders beside this file; opening only the small `.pbip` file downloaded from GitHub will not work.
4. In Power BI Desktop choose **Home → Refresh**. This loads the public data snapshot embedded in the project. It does not need a CSV path on your computer or a web data connection. If the report opens without values before this refresh, that is expected: a local data cache is not included in Git.
5. On **Retail overview**, select **Jul 2026** in the **Report month** dropdown and check the figures below. Open the **Source data & notes** page as well.

If Power BI shows an error, capture its full wording before changing anything. The exact file or field named in the error will help identify the correction.

## Check the report in Desktop

| July 2026 item | Expected value |
| --- | ---: |
| Edmonton sales | CAD 3,583,120,000; approximately 3.583 billion on the card |
| Edmonton annual growth | 12.00% |
| Edmonton share of Alberta | 35.02% |
| Calgary sales | CAD 3,131,691,000; approximately 3.132 billion on the card |
| Calgary annual growth | 8.99% |
| Alberta sales in the comparison chart | CAD 10,231,135,000; approximately 10.231 billion |

The growth chart must contain only Edmonton and Calgary. Its July 2026 points should be **12.00%** and **8.99%**. Growth for 2023 must be blank because the snapshot has no 2022 figures. Select **Jun 2026** next: the cards and sales comparison should change, while the growth chart should keep its complete history. Edmonton's June annual growth should be **9.91%**. Return to July for the final screenshot.

The source table displays all 172 records, rather than only the selected month. It intentionally has no grand total: the city, province and country observations overlap.

Check that all card values, headings, axis labels and notes are readable. The project has passed JSON schema, snapshot integrity, field reference and layout-bound checks. Its native model parsing, refresh, DAX execution and visual rendering still require this Desktop check; those checks cannot be completed by inspecting the project files alone.

## Save the final report

After the native checks pass, choose **File → Save as** and save a **Power BI file (.pbix)** in the repository's `powerbi` folder, for example `Edmonton-Retail-Pulse-Final.pbix`. Take a screenshot of **Retail overview** and add it to `docs/`. Review the changed files in GitHub Desktop, then commit and push the verified report and screenshot. Update the project checkpoint to record the completed Desktop check.

The `.pbip` project is already suitable for version control. The `.pbix` export makes the checked report easier to share as one file. GitHub stores both formats; Power BI Desktop opens and renders the native report.

## Data refresh and reproducibility

This is a fixed snapshot: January 2023–July 2026, accessed September 27, 2026. **Refresh** loads that snapshot into the local Power BI model; it does not download a newer Statistics Canada release.

From the repository root, rebuild the project definitions with:

```bash
python scripts/build_powerbi_project.py
```

The builder uses Python's standard library, embeds the exact committed CSV and reuses `powerbi/retail-measures.tmdl`. Build while the prepared project is closed in Desktop. The embedded snapshot avoids machine-specific paths. The disconnected month table makes the cards respond to month selection without reducing the historical chart to one point.

The comparison chart uses `Selected Month Sales CAD`, which filters the fact table to the chosen month while preserving the geography on its axis. Alberta includes both cities, so the bars must not be added. Source amounts are multiplied by 1,000 to convert thousands of CAD to CAD; growth compares the same month a year earlier. Unadjusted sales can be revised and do not isolate inflation or seasonal effects.
