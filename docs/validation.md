# Validation record

Validation is recorded by artifact and run. The original analytical run and the later working Power BI report are separate evidence; successful Python/SQLite checks do not validate proposed DAX.

## Original analytical run — 18 September 2026

Pinned source commit: `41710981b96a59a5399d88c62339ede3c8207e46` in the original public mirror. [validation.json](validation.json) preserves the original runtime and counts.

| Check | Recorded result |
|---|---|
| Public source files | Eight SHA-256 hashes matched the original manifest |
| Source/model financial and status totals | Seven checks passed |
| SQL/Python metrics | Eighteen shared-field comparisons passed; see [SQL scope](../sql/README.md) |
| Model regression tests | Six passed in the recorded analysis runtime |
| Notebook execution | Four notebooks, 30 executed code cells, no stored error outputs |
| Figures | Nine analytical charts and four static proposed dashboard designs reviewed |
| Proposed Desktop model / DAX | Not executed in a DAX engine |

The original tests cover item/payment multiplication, same-day promise handling, latest review selection, invalid chronology, duplicate keys, orphan references and unobserved cohort periods. Synthetic fixtures are used only for tests.

## Working Power BI report — 26 October 2026

The one-page **Olist E-Commerce Performance** report was created in Power BI Service and its page pinned live to **Olist E-Commerce Dashboard**. Both saved objects were reopened. The PBIX was exported from the service and inspected as a ZIP containing a DataModel, one report page and five visual definitions.

| Population | CSV / Power BI reconciliation |
|---|---|
| All commercial orders | BRL 13,221,498.11; 96,478 orders; 110,197 units |
| Acre (AC) state selection | BRL 15,930.97; 80 orders; 91 units |
| Report source | 556 observed month/state combinations in dashboard_data.csv |
| Interactions | State selector recalculated cards and charts; full view restored |
| Service refresh | Manual refresh available; no scheduled refresh configured |
| Desktop expansion | Separate proposed six-table model, DAX, theme and four-page specification; not implemented by this summary report |

The service cards abbreviate large totals. The CSV reconciles the exact amounts; the filtered Acre cards displayed 15.93K, 80 and 91. This establishes the tested summary behavior, not every proposed interaction or detailed-model measure.

During the dashboard build, quality and business-table/SQL calculations ran, but business chart rendering stopped because matplotlib was missing from that local runtime. The CSV export and six original tests completed independently. This partial run does not replace the original notebook/ML execution record.

## Repository consistency review — 26 October 2026

Descriptions, setup instructions, population definitions, notebook narratives and the executive-summary generator were aligned with [project status](project_status.md). The raw mirrors, original notebooks, historical numeric notebook outputs, PBIX and analytical model results were preserved. Source verification permits only Git checkout CRLF-to-LF normalization when exact hashes differ, and records that distinction. The live report screenshot was added to the package. Notebook narratives and the generated summary's status paragraph were updated without claiming new analytical executions.

The dashboard export now has an explicit pipeline stage, an import-safe standalone wrapper and population-aware aggregation tests. It regenerates the existing snapshot rather than enforcing fixed historical totals in code. Fixed-snapshot expectations belong to validation.

Reproduce the current checks:

```bash
python -m unittest discover -s tests -v
python scripts/validate_repository.py
```

The repository checker writes [repository_validation.json](repository_validation.json): ten passing regression tests (six original model tests and four dashboard tests), local-link checks, Python/JSON/notebook structure, source hashes, summary reconciliation, PBIX layout/schema and historical confusion-matrix arithmetic. If generated model/SQL tables are present, it also checks their reconciliation records and the rebuilt summary. Missing generated tables are reported as not checked rather than assumed to pass.

This consistency review does not rerun model fitting or all four notebooks, execute proposed DAX, change service permissions, or verify scheduled delivery. The model remains exploratory: precision and intervention evidence are insufficient for deployment.
