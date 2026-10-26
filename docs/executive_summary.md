# Executive summary

## E-Commerce Decision Intelligence
Growth, Customer Value, Product Performance & Operational Risk

All findings below were generated from the public Olist source files after validation. Values are historical BRL, not current market forecasts or Olist accounting revenue. See the [metric contract](../docs/metric_dictionary.md) for populations and [output setup](../output/README.md) for evidence.

### Management recommendation

For this historical case, I would **diagnose high-value service exposure first, test a second-purchase journey next, and keep predictive alerts in shadow evaluation**. This ordering favors specific operational questions and measurable experiments. It is not an estimate of intervention ROI; the diagnosis must be refreshed on current data before spending decisions.

1. **Protect the commercial base.** Read GMV contribution alongside eligible order volume, late rates and uncertainty. A smaller market with substantial exposure and an elevated issue rate can deserve attention before the largest market. Investigate seller/category mix and fulfillment timelines before assigning responsibility.
2. **Earn repeat demand with a controlled test.** The observed repeat-customer rate is 3.00%; the equal-follow-up 90-day second-purchase baseline is 2.28%. I would use a randomized opt-in pilot and assess incremental conversion, GMV per eligible customer, incentive/contact costs and experience guardrails. Growth without incremental contribution would not justify scaling.
3. **Require operational value from the model.** Holdout precision is 6.22%. I would evaluate alert burden at the team's capacity and compare a simple rule before considering automation. Better ranking than baseline is insufficient without reliable future performance and a beneficial intervention.

The [business decision memo](../docs/business_case.md) explains the state comparison, the trade-offs, proposed owners and the evidence I would require to proceed. Margin, campaign cost and intervention outcomes are missing, so I make no claim of realized profit, savings or uplift.

### Six findings

1. Delivered merchandise value was **BRL 13,221,498.11**, across **96,478 orders** and **93,358 unique customers**; AOV was **BRL 137.04**.
2. **3.00%** of customers placed multiple observed eligible orders. Subsequent orders contributed **2.90%** of GMV. Among customers with 90 days of observation, **2.28%** bought again within 90 days. These are observation-window measures, not churn.
3. The highest-spending **45.00%** of customers contributed 80% of GMV. An automatic 80/20 claim is therefore inappropriate; use the measured concentration curves.
4. **6.78%** of delivery-eligible orders arrived after the promised calendar day. Low-review rates were **62.42%** for late orders and **9.26%** for on-time orders. This association does not identify a causal effect.
5. **health beauty** has **BRL 1,233,132** GMV, **7.52%** late deliveries and **8,629** delivery-eligible orders. Its classification is **Improvement priority** under the documented volume, confidence and contribution rules.
6. The selected **Random forest** achieved temporal holdout average precision **0.061** against a prevalence baseline of **0.035**, with recall **36.40%** and precision **6.22%** at threshold **0.48**. Low precision limits practical use: most alerts are false positives. Customer clustering selected **K=2**, with silhouette **0.676** and seed-stability ARI **1.000**. Inspect the profiles: strong separation can simply recover the rare repeat-buyer group, adding little beyond a frequency rule. Intervention value has not been tested.

### Six priorities to test

| Evidence | Proposed action | KPI and evaluation |
|---|---|---|
| Sparse repeat purchasing and unequal observation windows | Randomize an opt-in second-purchase journey among newly acquired customers; use equal 90-day follow-up | Incremental 90-day second-purchase rate and GMV per eligible customer; record incentive costs separately |
| High-volume seller and category delay exposure | Review the highest-priority seller/category pairs in the scorecards; investigate promise accuracy and dispatch processes | Late rate with interval, excess late-order count, low-review rate; compare against a suitable control |
| Large review gap by delivery status | Test proactive delay communication for eligible at-risk orders | Low-review rate, contact rate, satisfaction; verify that operational performance improves as well |
| Model ranking above the reported baseline, if confirmed in a deployment-like test | Shadow-score future orders before any automated intervention; select alert volume against team capacity | Precision/recall at capacity, calibration and drift; establish false-alert and missed-delay costs |
| Measured concentration across customers, categories and sellers | Monitor contribution and performance together; investigate overdependence where exposure is material | Top-N contribution and cumulative GMV share, paired with experience KPIs |
| Accounting and join risks in the original analysis | Use the reconciled order/item model as the shared reporting source | Reconciliation failures, missing payment coverage and SQL/Python agreement |

### Interpretation boundaries

The dataset is historical and observational. No channel spend, acquisition cost, profit margin, returns, market size or experimental interventions are observed. The last eligible month is conservatively censored in retention reporting. Delivered-only commercial results exclude unresolved and canceled orders. Seller/category experience uses order-level outcomes, including shared multi-seller orders; this cannot establish seller-level responsibility. Cluster separation, model metrics and correlations do not prove commercial benefit.

The implemented Power BI Service report has one summary page and a live-page dashboard, with GMV, orders, units, monthly GMV, state ranking and a state selector. It uses the month/state summary CSV. The separate four-page design, dimensional relationships, DAX and Power Query remain proposed Desktop implementation assets. See the [Power BI package](../powerbi/README.md) and [project status](../docs/project_status.md) for access, refresh and validation scope.
