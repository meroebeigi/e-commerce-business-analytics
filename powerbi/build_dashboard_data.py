"""Build an additive month/state snapshot for Power BI Service quick creation."""
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parents[1]
f = pd.read_csv(root / 'output/FactOrders.csv')
f = f.loc[f.commercial_eligible].copy()
f['eligible_deliveries'] = f.delivery_eligible.astype(int)
f['late_deliveries'] = f.is_late.fillna(False).astype(bool).astype(int)
f['reviewed_orders'] = f.review_eligible.astype(int)
f['low_reviews'] = f.low_review.fillna(False).astype(bool).astype(int)
f['returning_orders'] = f.is_returning.astype(int)
g = f.groupby(['purchase_month', 'customer_state']).agg(
    GMV_BRL=('merchandise_value', 'sum'), Orders=('order_id', 'size'),
    Units=('number_of_items', 'sum'), Eligible_deliveries=('eligible_deliveries', 'sum'),
    Late_deliveries=('late_deliveries', 'sum'), Reviewed_orders=('reviewed_orders', 'sum'),
    Low_reviews=('low_reviews', 'sum'), Returning_orders=('returning_orders', 'sum')).reset_index()
g = g.rename(columns={'purchase_month':'Purchase_month', 'customer_state':'Customer_state'})
g.GMV_BRL = g.GMV_BRL.round(2)
assert g.Orders.sum() == 96478
assert abs(g.GMV_BRL.sum() - 13221498.11) < .01
g.to_csv(root / 'powerbi/dashboard_data.csv', index=False)
print(f'{len(g)} rows; {g.Orders.sum():,} orders; BRL {g.GMV_BRL.sum():,.2f}')

