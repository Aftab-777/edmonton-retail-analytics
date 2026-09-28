# Project checkpoint

## Completed

- Public Statistics Canada data: 172 monthly observations for Edmonton, Calgary, Alberta, and Canada, January 2023–July 2026.
- Reproducible data extraction and working SQLite analysis.
- Annual growth chart and a self-contained interactive dashboard preview with month selection.
- Power BI Desktop build instructions, DAX measures, visual layout, and theme JSON.
- July 2026 checks: Edmonton CAD 3.583 billion, Calgary CAD 3.132 billion, Edmonton annual growth 12.00%, Calgary 8.99%, Edmonton share of Alberta 35.02%.

## Next when working in Power BI Desktop

1. Download this repository's ZIP from GitHub (**Code → Download ZIP**) and extract it on a Windows computer with Power BI Desktop.
2. Follow [`powerbi/BUILD_GUIDE.md`](../powerbi/BUILD_GUIDE.md), using the interactive preview as the layout reference.
3. Compare all five July 2026 values above with the Power BI report. Check the same-month-prior-year growth calculation.
4. Save the report as `powerbi/Edmonton-Retail-Pulse.pbix`, add a screenshot to `docs/`, and update the README link to the native report file.
5. Walk through the source, each measure, and the limits of unadjusted/revisable data before using the project in an interview.

The repository currently contains a dashboard **preview** and Power BI build materials. A native Power BI report file will be added after it has been created and verified in Power BI Desktop.
