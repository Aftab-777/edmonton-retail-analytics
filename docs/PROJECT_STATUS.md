# Project checkpoint

## Completed

- Public Statistics Canada data: 172 monthly observations for Edmonton, Calgary, Alberta, and Canada, January 2023–July 2026.
- Reproducible data extraction and working SQLite analysis.
- Annual growth chart and a self-contained interactive dashboard preview with month selection.
- Power BI Desktop build instructions, a one-apply TMDL measure script, visual layout, and theme JSON.
- July 2026 checks: Edmonton CAD 3.583 billion, Calgary CAD 3.132 billion, Edmonton annual growth 12.00%, Calgary 8.99%, Edmonton share of Alberta 35.02%.

## Current Desktop handoff

The source CSV was imported on a Windows computer, with `month` typed as Date. The disconnected `Report Month` table and a dropdown month slicer were created. A local report file was saved in the cloned repository's `powerbi` folder; that local file has not yet been checked or published here. The latest selected month was July 2026. If a `Retail Sales CAD` measure was created manually, the TMDL script replaces its definition with the checked version.

## Next when working in Power BI Desktop

1. In GitHub Desktop, **Fetch origin**, then **Pull origin** if prompted, to receive the new `powerbi/retail-measures.tmdl` file. Do not overwrite the local report file.
2. Open the locally saved report in Power BI Desktop. In **TMDL view**, paste the entire script from [`powerbi/retail-measures.tmdl`](../powerbi/retail-measures.tmdl), preview and apply; Power BI Desktop will validate it. Save the local report.
3. Use [`powerbi/BUILD_GUIDE.md`](../powerbi/BUILD_GUIDE.md) and the interactive preview to create the visuals, then compare all five July 2026 values above. Check the same-month-prior-year growth calculation.
4. Add a verified report screenshot to `docs/`; review GitHub Desktop's changed files before pushing the completed report.
5. Walk through the source, each measure, and the limits of unadjusted/revisable data before using the project in an interview.

The repository currently contains a dashboard **preview** and Power BI build materials. A native Power BI report file will be added after it has been created and verified in Power BI Desktop.
