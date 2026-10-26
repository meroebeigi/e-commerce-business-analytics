# SQLite analytical queries

The business stage writes the validated Python model to `output/olist.sqlite`, executes the six queries here, exports their result tables and checks eighteen shared metrics against Python. SQLite 3.25 or later is needed for window functions. Source populations and allocation rules are defined in the [metric contract](../docs/metric_dictionary.md).

| Query | Population and grain | Reconciled fields |
|---|---|---|
| 01_executive_kpis.sql | Commercial order sums/customer counts; late rate separately uses all delivery-eligible orders | GMV, orders, customers, AOV, repeat-customer rate, late rate |
| 02_monthly_growth.sql | Commercial orders per active purchase month | GMV, orders, customers, AOV on active SQL rows |
| 03_customer_analysis.sql | One observed commercial customer | Customer GMV |
| 04_product_performance.sql | Item GMV; one distinct order/category pair for experience | Category GMV, orders, late rate |
| 05_seller_performance.sql | Item GMV; one distinct order/seller pair for experience | Seller GMV, orders, late rate |
| 06_retention_analysis.sql | Acquisition cohort/month-age grid with censored latest month | Cohort retention rate |

Monthly SQL intentionally omits empty calendar months. Its `gmv_mom` compares consecutive active months and `trailing_3_active_month_gmv` averages active rows. Python `monthly.csv` fills calendar gaps before calculating growth. These growth/rolling fields are not among the eighteen parity checks. The Power BI summary similarly stores observed month/state combinations; it does not implement either rolling measure.

The seller SQL field `rate_sample_eligible` checks only at least 50 delivery observations. Python `rate_rank_eligible` requires both 50 delivery and 50 review observations for prioritization. These fields have different purposes and are not reconciled as equivalent. Commercial sums are additive; category/seller distinct orders and experience counts must not be summed across groups.

These SQLite results validate shared Python calculations, not the proposed DAX package. The working Power BI report uses the separate aggregate CSV. See [project status](../docs/project_status.md) and [validation](../docs/validation.md).
