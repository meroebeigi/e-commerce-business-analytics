"""Dashboard aggregation must preserve order grain and eligible denominators."""
import unittest
import pandas as pd
from src.dashboard import build_dashboard_data


class DashboardTests(unittest.TestCase):
    def orders(self):
        return pd.DataFrame([
            dict(order_id='a', purchase_month='2018-01', customer_state='SP',
                 commercial_eligible=True, merchandise_value=100., number_of_items=2,
                 delivery_eligible=True, is_late=True, review_eligible=True,
                 low_review=True, is_returning=False),
            dict(order_id='b', purchase_month='2018-01', customer_state='SP',
                 commercial_eligible=True, merchandise_value=50., number_of_items=1,
                 delivery_eligible=False, is_late=None, review_eligible=False,
                 low_review=None, is_returning=True),
            dict(order_id='c', purchase_month='2018-01', customer_state='RJ',
                 commercial_eligible=False, merchandise_value=500., number_of_items=5,
                 delivery_eligible=True, is_late=True, review_eligible=True,
                 low_review=True, is_returning=False),
            dict(order_id='d', purchase_month='2018-02', customer_state='RJ',
                 commercial_eligible=True, merchandise_value=75., number_of_items=1,
                 delivery_eligible=True, is_late=False, review_eligible=True,
                 low_review=False, is_returning=False)])

    def test_commercial_totals_and_denominators(self):
        result = build_dashboard_data(self.orders())
        self.assertEqual(len(result), 2)
        self.assertEqual(result.GMV_BRL.sum(), 225.)
        self.assertEqual(result.Orders.sum(), 3)
        self.assertEqual(result.Units.sum(), 4)
        self.assertEqual(result.Eligible_deliveries.sum(), 2)
        self.assertEqual(result.Late_deliveries.sum(), 1)
        self.assertEqual(result.Reviewed_orders.sum(), 2)
        self.assertEqual(result.Low_reviews.sum(), 1)
        self.assertEqual(result.Returning_orders.sum(), 1)

    def test_invalid_outcomes_do_not_enter_issue_counts(self):
        orders = self.orders()
        orders.loc[1, ['is_late', 'low_review']] = True
        result = build_dashboard_data(orders)
        self.assertEqual(result.Late_deliveries.sum(), 1)
        self.assertEqual(result.Low_reviews.sum(), 1)

    def test_duplicate_order_grain_fails(self):
        orders = self.orders()
        with self.assertRaises(ValueError):
            build_dashboard_data(pd.concat([orders, orders.iloc[:1]]))

    def test_missing_destination_does_not_silently_drop_commerce(self):
        orders = self.orders()
        orders.loc[0, 'customer_state'] = None
        with self.assertRaises(ValueError):
            build_dashboard_data(orders)


if __name__ == '__main__':
    unittest.main()
