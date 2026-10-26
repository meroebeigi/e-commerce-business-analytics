# Project status and artifact scope

Status reviewed on 26 October 2026. Project name: **E-Commerce Decision Intelligence**. Source: public Brazilian e-commerce transactions from Olist. All monetary values are nominal historical BRL; merchandise GMV excludes freight and is not marketplace accounting revenue.

## Delivered artifacts

| Artifact | Implemented content | Validation scope |
|---|---|---|
| Four analytical notebooks | Data quality, business/customer analytics, exploratory models and recommendations | Stored outputs from the September analysis run; execution evidence in [validation](validation.md) |
| Python and SQLite | Order/item model, population-specific KPIs, scorecards, cohorts and temporal model evaluation | Seven source/model checks and eighteen SQL/Python comparisons; current checks listed in [validation](validation.md) |
| [Native Power BI report](../powerbi/Olist%20E-Commerce%20Performance.pbix) | One page: GMV, orders, units, monthly GMV, state ranking and state dropdown | Created in Power BI Service; full totals and Acre selection reconciled; exported PBIX inspected |
| Power BI dashboard | A live pin of that report page in My workspace | Saved dashboard reopened and content verified on 26 October 2026 |
| [Four-page specification](../powerbi/dashboard_specification.md) | Proposed executive, customer, commercial and operations pages | Four static real-data design previews; these are not four implemented report pages |
| [DAX](../powerbi/dax_measures.md), [Power Query](../powerbi/import_tables.pq), [schema](../powerbi/star_schema.svg), [theme](../powerbi/theme.json) | Supporting package for a future detailed order/item model in Power BI Desktop | Proposed Desktop implementation; separate from the working summary report |

The implemented report uses one imported `dashboard_data` table, not the six-table dimensional model. Its eight numeric fields are additive counts/amounts, aggregated by purchase month and order destination state. It has no unique-customer, category, seller, retention or model-risk visuals. Delivery/review counts are available in the CSV but are not visualized. The proposed DAX measures are not used in this report.

## Access and refresh

- [Open the dashboard](https://app.powerbi.com/groups/me/dashboards/9b87c2c7-445f-4fb3-a60b-412b38d58a43?experience=power-bi)
- [Open the report](https://app.powerbi.com/groups/me/reports/2dce69d3-cc17-4a2b-8805-ce7d13ceb396?experience=power-bi)
- [Report setup and data dictionary](../powerbi/README.md)

Service links require an authorized Power BI account and access to the owner's workspace. GitHub hosts the PBIX, summary CSV, code and documentation; it does not host the Power BI service. No public Publish to web link or scheduled refresh was configured. A live page pin reflects report changes when refreshed; it does not make the underlying historical source live.

Run the quality and dashboard stages to regenerate the summary. After committing a changed CSV, refresh the service model manually. Refreshing the service does not update the PBIX checked into GitHub: export a new PBIX and replace that file separately. Changing Python, CSV, theme or specification files alone does not modify the saved service report.

## Population and observation window

Commercial results use delivered orders with at least one item and a valid purchase timestamp. The included commercial purchase window is September 2016 through August 2018; early coverage is sparse and boundary periods are not proven complete. The summary CSV has 556 observed month/state combinations and omits combinations with no eligible orders. Python monthly analysis fills empty calendar months; SQL monthly analysis uses active months. See the [metric contract](metric_dictionary.md) and [SQL scope](../sql/README.md).

Full commercial totals are **BRL 13,221,498.11**, **96,478 orders**, **110,197 units** and **93,358 unique customers**. The customer total is available from the detailed model, not the aggregate report. Acre (AC) reconciles to **BRL 15,930.97**, **80 orders** and **91 units**.

Marketplace delivery and review populations can include delivered orders excluded from commerce. The summary CSV restricts experience counts to commerce first. Compare rates only with matching populations and eligible denominators. Statistical associations and model performance do not demonstrate causality or intervention value; the late-delivery model is exploratory and not deployment-ready.

## Provenance and reproducibility

The eight required source files and pinned original mirror are recorded in [the source manifest](../data/source_manifest.json). Existing `archive/` and `archive.zip` are legacy source mirrors; new working copies under `data/raw/` are ignored. Original notebooks at the root and under `docs/` are retained unchanged for provenance and contain superseded calculations.

[requirements.txt](../requirements.txt) specifies install ranges. [requirements-validated.txt](../requirements-validated.txt) records the original analysis environment, not a claim that this later review reran the models with those exact versions. The later Power BI/export checks and the historical notebook/ML run are recorded separately in [validation](validation.md).
