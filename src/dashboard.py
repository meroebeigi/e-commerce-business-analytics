"""Month/state summary used by the implemented Power BI Service report."""
from pathlib import Path
import pandas as pd


def build_dashboard_data(orders):
    """Aggregate commercial orders; retain eligible denominators for optional rates."""
    if orders.order_id.isna().any() or not orders.order_id.is_unique:
        raise ValueError('Dashboard input must contain one non-null order_id per order')
    f = orders.loc[orders.commercial_eligible].copy()
    if f[['purchase_month', 'customer_state']].isna().any().any():
        raise ValueError('Commercial orders need a purchase month and destination state')
    f['eligible_deliveries'] = f.delivery_eligible.astype(int)
    f['late_deliveries'] = (f.delivery_eligible & f.is_late.fillna(False)).astype(int)
    f['reviewed_orders'] = f.review_eligible.astype(int)
    f['low_reviews'] = (f.review_eligible & f.low_review.fillna(False)).astype(int)
    f['returning_orders'] = f.is_returning.astype(int)
    summary = f.groupby(['purchase_month', 'customer_state']).agg(
        GMV_BRL=('merchandise_value', 'sum'), Orders=('order_id', 'size'),
        Units=('number_of_items', 'sum'), Eligible_deliveries=('eligible_deliveries', 'sum'),
        Late_deliveries=('late_deliveries', 'sum'), Reviewed_orders=('reviewed_orders', 'sum'),
        Low_reviews=('low_reviews', 'sum'), Returning_orders=('returning_orders', 'sum'))
    summary = summary.reset_index().rename(columns={
        'purchase_month': 'Purchase_month', 'customer_state': 'Customer_state'})
    summary.GMV_BRL = summary.GMV_BRL.round(2)
    return summary


def export_dashboard(root, orders=None):
    """Write the tracked report snapshot after the quality stage has built FactOrders."""
    root = Path(root)
    if orders is None:
        orders = pd.read_csv(root / 'output/FactOrders.csv', dtype={
            'commercial_eligible': 'boolean', 'delivery_eligible': 'boolean',
            'review_eligible': 'boolean', 'is_late': 'boolean',
            'low_review': 'boolean', 'is_returning': 'boolean'})
    summary = build_dashboard_data(orders)
    summary.to_csv(root / 'powerbi/dashboard_data.csv', index=False)
    return summary
