# Project checkpoint

## Completed

- Public Statistics Canada data: 172 monthly observations for Edmonton, Calgary, Alberta, and Canada, January 2023–July 2026.
- Reproducible data extraction and working SQLite analysis.
- Annual growth chart and a self-contained interactive dashboard preview with month selection.
- Power BI Desktop build instructions, a one-apply TMDL measure script, visual layout, and theme JSON.
- Prepared native Power BI project: five headline cards, month selector, city growth chart, selected-month sales comparison, and source data page. Includes the exact 172-row snapshot and the eleven measures previously checked in Desktop, plus one comparison measure.
- July 2026 checks: Edmonton CAD 3.583 billion, Calgary CAD 3.132 billion, Edmonton annual growth 12.00%, Calgary 8.99%, Edmonton share of Alberta 35.02%.

## Current Desktop handoff

The source CSV was imported on a Windows computer, with `month` typed as Date. The disconnected `Report Month` table and a dropdown month slicer were created, and a local `.pbix` was saved in the repository's `powerbi` folder. On October 1, 2026, the corrected TMDL script applied successfully: 11 measures, zero reported problems. The validation table matched all five July checks: Edmonton CAD 3,583,120,000; Calgary CAD 3,131,691,000; Edmonton annual growth 12.00%; Calgary 8.99%; and Edmonton share of Alberta 35.02%.

The separate project at [`powerbi/project/Edmonton-Retail-Pulse.pbip`](../powerbi/project/Edmonton-Retail-Pulse.pbip) supplies the report layout without requiring each visual to be assembled manually. Its 34 schema-bound JSON files pass Microsoft's PBIP/PBIR schemas; its theme passes the theme schema. Snapshot integrity, original measure preservation, visual field references and roles, page bounds and Windows path lengths have been checked. On October 1, 2026, the prepared project opened in Power BI Desktop and refreshed successfully. The native overview rendered all five July cards correctly: Edmonton CAD 3.583 billion, Edmonton annual growth 12.00%, Edmonton share of Alberta 35.02%, Calgary CAD 3.132 billion and Calgary annual growth 8.99%. Both charts populated; the comparison displayed Alberta CAD 10.231 billion, and the city growth chart displayed Edmonton and Calgary from January 2024 onward. Month selection behaviour, the source data page and final layout review remain to be checked. The earlier local `.pbix` is not overwritten.

## Next when working in Power BI Desktop

1. In GitHub Desktop, **Fetch origin**, then **Pull origin** if prompted. Choose **Repository → Show in Explorer**.
2. Open **powerbi → project → Edmonton-Retail-Pulse.pbip**. In Power BI Desktop choose **Home → Refresh** to load the embedded snapshot.
3. Follow [`powerbi/OPEN_PROJECT.md`](../powerbi/OPEN_PROJECT.md). Verify all five July figures, both July growth chart points, and month selection behaviour. Check the source page and label readability.
4. After the Desktop checks pass, save a final `.pbix`, add a verified report screenshot to `docs/`, and review GitHub Desktop's changed files before committing and pushing them.
5. Walk through the source, each measure, and the limits of unadjusted/revisable data before using the project in an interview.

The repository contains both a web dashboard preview and a native Power BI project. A verified `.pbix` export and native report screenshot remain pending. The month picker selects a reporting month; the embedded data is a fixed snapshot and does not fetch a newer release when refreshed.
