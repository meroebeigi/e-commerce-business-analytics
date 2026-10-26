# Business decision memo

## The decision I wanted to support

How should a marketplace allocate limited attention between acquiring customers, earning a second purchase and improving fulfillment?

I treated this as a prioritization problem. GMV shows commercial scale; issue rates show reliability; eligible order counts show how broadly a problem is observed. Together they identify where to investigate. They do not establish profit, lost sales or the return from an intervention.

My proposed sequence is **protect existing value → test repeat demand → scale only with evidence**. This is a management interpretation of the historical sample. Before applying it operationally, I would reproduce the diagnosis on current data.

## 1. Prioritize operational exposure, rather than the biggest market alone

São Paulo contributes **38.3%** of delivered merchandise GMV, with a **4.50%** late-delivery rate. Rio de Janeiro contributes **13.3%**, with a **12.12%** late rate across **12,330 delivery-eligible commercial orders**. Rio therefore deserves investigation even though it is smaller: the combination of material volume and an elevated rate makes it a more specific service diagnostic than a sales ranking alone.

I would ask operations to examine seller/category mix, promise accuracy and carrier timelines in that market. I would keep São Paulo's service performance under review because its commercial exposure is large. Neither comparison proves that a state, seller or carrier caused a delay; case mix and order-level attribution matter.

For a scale illustration, reducing Rio's late rate by **one percentage point** at the same eligible order volume would correspond to approximately **123 fewer late orders**. This is a scenario, not a forecast or a financial saving. To assess value, I would need intervention cost, contribution margin and evidence that outcomes improve.

Evidence: [geographic and seller analysis](../notebooks/02_business_analytics.ipynb). These state rates use commercial orders with valid delivery outcomes; the marketplace-wide executive late rate uses its separately defined delivery population.

## 2. Test whether customers can be earned back

Only **3.00%** of customers repeat within the observed history, while **2.28%** of the **75,320** customers with a full 90-day observation window make a second purchase within 90 days. These are different denominators, not conflicting retention estimates.

I would test an opt-in post-purchase journey against a randomized holdout before committing to broad discounts. The main outcome would be incremental 90-day second-purchase conversion. I would also track incremental GMV per eligible customer, incentive/contact costs, contribution margin once available, low-review rates and opt-outs.

The trade-off is straightforward: a campaign can generate orders while subsidizing customers who would have bought anyway. Conversion lift alone is insufficient to justify scaling. Inactivity also cannot be labeled churn without an appropriate business definition and follow-up window.

Evidence: [customer and cohort analysis](../notebooks/03_customer_analytics.ipynb).

## 3. Treat model deployment as an economic decision

The selected late-delivery model has **6.22% precision** and **36.40% recall** on the temporal holdout at its validation-selected threshold. Its average precision exceeds the prevalence baseline, but **3,693 of 3,938 alerts are false positives**. Ranking signal alone does not justify customer-facing automation.

I would retain shadow evaluation and compare precision/recall at an agreed alert capacity with a simple operational baseline. Deployment would require calibrated probabilities, stable future-period performance, false-alert and missed-delay costs, and evidence that an intervention helps. The simpler choice can be better if it supports the same decision with less operational burden.

Evidence: [temporal model evaluation](../notebooks/04_data_science.ipynb). No automated intervention or realized benefit is claimed.

## How I would turn this into an operating review

| Decision | Proposed owner | Evidence required to proceed | Hold or stop when |
|---|---|---|---|
| Investigate service exposure | Operations with seller/category managers | Current matched-population rates, eligible counts, confidence intervals and case review | The signal disappears after case-mix checks or sample quality is inadequate |
| Pilot a second-purchase journey | CRM/growth with analytics | Randomized, equal-follow-up lift; uncertainty; full incentive/contact costs | Costs exceed incremental contribution, or experience/opt-out guardrails worsen |
| Use predictive alerts | Operations and data science | Future-period precision/recall at capacity, calibration and a beneficial intervention | Alert burden exceeds capacity or a simpler rule performs as well |

These are proposed owners and decision gates, not an executed program. I would agree the minimum useful improvement, budget, sample size and guardrail thresholds with stakeholders before a pilot. The dataset cannot supply those commercial constraints.

## Why the analytical design matters to the decision

- Separating item and payment grains prevents inflated commercial figures from becoming budget inputs.
- Cohorts and equal follow-up make retention comparisons fairer than a single lifetime-repeat percentage.
- Contribution plus normalized issue rates prevents both large markets and tiny extreme-rate samples from dominating priorities.
- Reporting a weak model result demonstrates the judgment to withhold deployment when practical value is unproven.

The [metric contract](metric_dictionary.md) defines each denominator. The [executive report](executive_summary.md) summarizes the evidence. The [working Power BI report](../powerbi/README.md) supplies commercial exploration and a static decision lens; its state filter does not recalculate the detailed conclusions in this memo.
