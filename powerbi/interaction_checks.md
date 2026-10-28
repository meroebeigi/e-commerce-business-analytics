# Power BI interaction verification

Verified in Power BI Service on 28 October 2026 in My workspace.

- [Report](https://app.powerbi.com/groups/me/reports/2dce69d3-cc17-4a2b-8805-ce7d13ceb396/4b6414dad6b2f051cfff?experience=power-bi): Olist E-Commerce Performance, Page 1.
- [Dashboard](https://app.powerbi.com/groups/me/dashboards/9b87c2c7-445f-4fb3-a60b-412b38d58a43?experience=power-bi): Olist E-Commerce Dashboard, live report-page tile.

## Observed checks

| Selection | Source CSV: GMV / orders / units | Visible service cards |
| --- | --- | --- |
| All states | BRL 13,221,498.11 / 96,478 / 110,197 | 13.22M / 96K / 110K |
| Acre (AC) | BRL 15,930.97 / 80 / 91 | 15.93K / 80 / 91 |

In both the report and dashboard tile, selecting AC changes all three cards, reduces the state ranking to AC and updates the monthly trend. The first displayed AC monthly observation is January 2017, BRL 589.60. Clearing the selection restores all states and full totals. Both views were left unfiltered after testing. No report/model definitions or data were changed.

The business decision panel is static explanatory text. It does not recalculate with state selections. This is an interactive historical summary, not a streaming dashboard; no scheduled refresh is configured. The separate four-page design previews are static proposals.

## Clean picture provenance

[report_canvas.png](dashboard_preview/report_canvas.png) was rendered at 1920 pixels from Power BI’s native PDF export using Default Values. It is the implemented report canvas, also used by the live dashboard tile, without browser navigation or editor panes. It is a static preview; interactivity requires opening the service report/dashboard with existing access. A browser reload and this export do not establish a new source-data refresh.
