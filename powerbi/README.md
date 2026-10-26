# Power BI dashboard and implementation package

This project delivers a working one-page summary report and a separate proposed four-page analytical design. [Project status](../docs/project_status.md) defines the shared scope and validation boundaries.

## Open the working report

- [Download Olist E-Commerce Performance.pbix](Olist%20E-Commerce%20Performance.pbix) and open it in Power BI Desktop.
- [Open the saved report](https://app.powerbi.com/groups/me/reports/2dce69d3-cc17-4a2b-8805-ce7d13ceb396?experience=power-bi).
- [Open Olist E-Commerce Dashboard](https://app.powerbi.com/groups/me/dashboards/9b87c2c7-445f-4fb3-a60b-412b38d58a43?experience=power-bi), containing a live pin of the report page.

Service links require workspace access and Power BI sign-in. GitHub hosts the downloadable PBIX and public-data snapshot. No public Publish to web link or scheduled refresh was configured.

![Working Power BI report](dashboard_preview/live_report.png)

The implemented page contains three commercial cards (GMV, orders, units), monthly merchandise GMV, state GMV ranking, a state dropdown and a static business decision panel. It uses a single imported `dashboard_data` table with implicit sums. The original DAX, relationship diagram, theme and four-page specification are separate design assets; they are not the implementation inside this PBIX.

## Rebuild and refresh the summary

Set up the eight inputs as described in [data setup](../data/README.md), then run from the repository root:

```bash
python -m pip install -r requirements.txt
python run_pipeline.py --stage quality
python run_pipeline.py --stage dashboard
python -m unittest discover -s tests -v
python scripts/validate_repository.py
```

`python powerbi/build_dashboard_data.py` is an equivalent dashboard-only command after quality. The full pipeline also exports the snapshot. Its calculation lives in [src/dashboard.py](../src/dashboard.py); importing the wrapper does not rewrite the CSV. The export deliberately updates tracked `powerbi/dashboard_data.csv`, while detailed generated tables under `output/` remain ignored.

The service model connects anonymously to the repository's raw `master/powerbi/dashboard_data.csv`. After regenerating and committing the CSV, refresh the service model manually. A service refresh does not replace the GitHub PBIX: export a new report file separately when updating the packaged snapshot. Rebuilding the data does not recreate the service report, dashboard or permissions.

## Summary table contract

Grain: one observed `Purchase_month` / `Customer_state` combination, restricted to commercial-eligible orders. Month is serialized as `YYYY-MM` and imported as the first calendar day of that month. State is the destination on the order, not first-observed customer geography. No individual IDs are included. Absent month/state combinations are omitted rather than materialized as zero rows.

| Field | Meaning and aggregation |
|---|---|
| Purchase_month | Eligible order purchase month; group/filter, do not sum |
| Customer_state | Destination state; group/filter, do not sum |
| GMV_BRL | Sum of delivered merchandise value, excluding freight; rounded to cents per row |
| Orders | Number of commercial-eligible orders |
| Units | Number of item rows on those orders |
| Eligible_deliveries | Commercial orders also meeting the delivery eligibility contract |
| Late_deliveries | Late orders among Eligible_deliveries |
| Reviewed_orders | Commercial orders with a valid selected review |
| Low_reviews | Review scores 1–2 among Reviewed_orders |
| Returning_orders | Subsequent eligible orders, sequenced across the full observation window |

All eight numeric fields are additive. Optional AOV is `SUM(GMV_BRL) / SUM(Orders)`; late rate is `SUM(Late_deliveries) / SUM(Eligible_deliveries)`; low-review rate is `SUM(Low_reviews) / SUM(Reviewed_orders)`. A zero denominator yields blank. Never average row rates. Returning_orders is not unique repeat customers, and unique customers cannot be reconstructed from this aggregate. The experience fields are not currently visualized.

Snapshot: **556 rows**, September 2016–August 2018, **BRL 13,221,498.11**, **96,478 orders**, **110,197 units**. Acre (AC): **BRL 15,930.97**, **80 orders**, **91 units**. Cards were reconciled in the service; regression and packaging checks are described in [validation](../docs/validation.md). Sparse early coverage and boundary months do not establish comparable complete growth periods.

## Proposed detailed model and four-page expansion

The [specification](dashboard_specification.md) and `dashboard_preview/page_1.png` through `page_4.png` are static real-data designs. The [DAX measures](dax_measures.md) and loader below target a future detailed Power BI Desktop implementation and still require engine and interaction validation.

1. Run quality for the six core tables; run business for scorecards, customer snapshots and SQL comparisons. Run models only if cluster/model panels are needed. See [pipeline stages](../README.md#reproduce).
2. Open a new Power BI Desktop project. Create a text parameter `OutputFolder` pointing to `output/`, ending in a path separator.
3. Save [import_tables.pq](import_tables.pq) as a function query called `LoadOlist`. Create `= LoadOlist("FactOrders")` and one query for each other core table.
4. Disable automatic relationship detection and create only the relationships below. Mark `DimDate[date]` as the date table; sort month names by month number and year-month by date. Import [theme.json](theme.json) for this proposed design.
5. Add the proposed measures and pages. Compare unfiltered cards to `output/kpis.csv`, category values to `output/categories.csv` and seller values to `output/sellers.csv`.
6. Test category/seller propagation, date filtering, missing outcomes and distinct-order behavior. Keep relationships single-direction; do not replace explicit propagation with global bidirectional filtering.

### Detailed-model relationships

![Proposed dimensional relationship diagram](star_schema.svg)

| Table | Grain / primary key | Relationship | Direction |
|---|---|---|---|
| DimCustomer | One customer_unique_id | 1 → * FactOrders.customer_unique_id | Dimension to orders |
| DimDate | One date | 1 → * FactOrders.purchase_date | Dimension to orders |
| FactOrders | One order_id | 1 → * FactOrderItems.order_id | Orders to items |
| DimProduct | One product_id | 1 → * FactOrderItems.product_id | Dimension to items |
| DimSeller | One seller_id | 1 → * FactOrderItems.seller_id | Dimension to items |
| FactOrderItems | One (order_id, order_item_id) | Many-side of the three relationships above | No outgoing filters |

Schemas and row counts are exported to `output/model_inventory.csv`. This order-header/detail fact constellation is not the flat table used by the implemented report. Avoid redundant date/customer paths into items. FactPayments and FactReviews are separate audit exports, not required in this proposed core model.

### Detailed-model types and optional snapshots

Keep IDs and ZIP prefixes as text; use Date for purchase_date, first_purchase_date and DimDate.date; Date/Time for timestamps; Fixed Decimal Number for money; Whole Number for counts; True/False for flags. Preserve null `is_late` and `low_review`; missing outcomes must not become false. The loader supplies these conversions for the core tables.

For optional RFM/cluster slicers, merge `customers.csv` and `customer_clusters.csv` into DimCustomer by customer_unique_id without breaking its unique grain. These are full-window snapshots, not historical as-of segments. Keep cohorts and 90-day tables disconnected unless a separate cohort model is designed. The detailed order-level population contract is in [metric_dictionary.md](../docs/metric_dictionary.md).
