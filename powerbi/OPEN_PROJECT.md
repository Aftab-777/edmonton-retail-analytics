# Open Edmonton Retail Pulse in Power BI Desktop

The native project contains the report layout, five headline cards, a month dropdown, an Edmonton–Calgary annual-growth chart, a selected-month sales comparison, and a source data/notes page. Its twelve measures use the same Statistics Canada snapshot as the SQL analysis and web demo.

Use Power BI Desktop on Windows. Microsoft provides [Desktop download guidance](https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-get-the-desktop) and documents [Power BI projects](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview). Opening and editing this local report does not require a Power BI Pro subscription or a paid custom visual.

## Option 1: use the repository already on your computer

1. Save any report you currently have open in Power BI Desktop.
2. In **GitHub Desktop**, select `edmonton-retail-analytics`. Click **Pull origin** if it is shown, or **Fetch origin** and then **Pull origin** if new changes are found.
3. Choose **Repository → Show in Explorer**.
4. Open **powerbi → project → Edmonton-Retail-Pulse.pbip**. Keep `Retail.Report` and `Retail.SemanticModel` beside the `.pbip` file.
5. In Power BI Desktop, choose **Home → Refresh** to load the embedded data snapshot. A local data cache is intentionally not included in Git.

## Option 2: use the complete ZIP

1. Download [`Edmonton-Retail-Pulse-Project.zip`](Edmonton-Retail-Pulse-Project.zip).
2. **Extract all** to a normal folder; do not open the project while it is still inside the ZIP.
3. In the extracted `Edmonton-Retail-Pulse-Project` folder, open **Edmonton-Retail-Pulse.pbip**.
4. Choose **Home → Refresh** in Power BI Desktop.

Downloading only the small `.pbip` file is insufficient: its adjacent report and semantic model folders are required. The ZIP includes all three together.

## Verify the figures and interaction

On **Retail overview**, select July 2026 in **Report month**. The slicer may display `01-07-2026`: that is the first day used to represent the July monthly record, not a single day's sales.

| July 2026 item | Expected value |
| --- | ---: |
| Edmonton sales | CAD 3,583,120,000; approximately 3.583 billion on the card |
| Edmonton annual growth | 12.00% |
| Edmonton share of Alberta | 35.02% |
| Calgary sales | CAD 3,131,691,000; approximately 3.132 billion on the card |
| Calgary annual growth | 8.99% |
| Alberta sales in the comparison | CAD 10,231,135,000; approximately 10.231 billion |

The growth chart contains only Edmonton and Calgary. July's points should be 12.00% and 8.99%; 2023 growth is blank because there is no 2022 data. Select June next: headline values and the sales comparison should change, while the trend keeps its history. Edmonton's June annual growth is **9.91%**. Return to July for the main demonstration.

Open **Source data & notes** before a presentation. It displays the full 172-record snapshot rather than only the selected month. It has no grand total because the city, province, and country figures overlap. Check label readability and the source notes.

The project opened and refreshed in Desktop on October 1, 2026. The five July cards and both charts are visible in the [published native screenshot](../docs/screenshots/retail-overview-july-2026.png). The project owner confirmed month switching. A native screenshot of the source page remains an optional additional check; see the [validation record](../docs/VALIDATION.md).

## Optional single-file export

The `.pbip` project is the published native deliverable. For a single-file copy, use **File → Save as → Power BI file (.pbix)** in Desktop, for example `Edmonton-Retail-Pulse-Final.pbix`. Verify it before adding it to GitHub. A locally saved file does not appear on GitHub until it is committed and pushed.

## Refresh and rebuild

The project embeds the exact committed CSV. It does not need a CSV path on your computer or a web data connection. **Refresh** loads the fixed January 2023–July 2026 snapshot; it does not download a newer Statistics Canada release.

To regenerate project definitions, close the project in Desktop and run this from the repository root:

```bash
python scripts/build_powerbi_project.py
```

The builder uses Python's standard library. The disconnected month picker lets the cards change without reducing the historical trend to one point. `Selected Month Sales CAD` keeps the geography axis while applying the selected month. Source amounts are multiplied by 1,000 to convert thousands of CAD to CAD. Alberta includes both cities; do not add the bars together.
