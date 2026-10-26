# Generated analytical outputs

Run the stages in the [root README](../README.md#reproduce) from the repository root. Full reproduction requires the eight source files and all packages in `requirements.txt`.

| Stage | Outputs in this directory |
|---|---|
| quality | Six core tables, FactPayments/FactReviews audit tables, inventory, source checksums, date/coverage audits and seven financial/status reconciliations |
| business | KPIs, monthly/customer/cohort tables, category/seller/state scorecards, payment/experience summaries, SQLite database, six SQL result tables and eighteen SQL/Python comparisons |
| models | Customer clusters, diagnostics, temporal risk-model results, predictions and model_metrics.json |
| report | Reads business/model outputs and regenerates docs/executive_summary.md |

Business and model stages also render charts under `images/`; business renders four static proposed dashboard designs under `powerbi/dashboard_preview/`. The `dashboard` stage writes the intentionally tracked `powerbi/dashboard_data.csv`, not an additional output table here. It requires quality outputs and does not require the business or model stages.

Generated CSV/SQLite files are excluded from Git. The existing `model_metrics.json` is a tracked historical analysis result and is replaced by a successful model run. Stored results are also visible in the four [analytical notebooks](../notebooks/01_data_quality.ipynb), [executive summary](../docs/executive_summary.md) and [validation record](../docs/validation.md).

Experience tables and commercial tables have different eligible populations; use the [metric contract](../docs/metric_dictionary.md). The implemented summary Power BI report is separate from these detailed outputs and proposed designs; see [project status](../docs/project_status.md).

A failed stage can leave partial files. File existence alone is not proof that the stage completed. Review the command's exit status and reconciliation results before using regenerated outputs.
