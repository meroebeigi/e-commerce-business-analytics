"""Export the implemented report snapshot; run the quality stage first."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from src.dashboard import export_dashboard

if __name__ == '__main__':
    summary = export_dashboard(root)
    print(f'{len(summary)} rows; {summary.Orders.sum():,} orders; '
          f'BRL {summary.GMV_BRL.sum():,.2f}')

