"""Run quality, dashboard, business, models, report, or all from the project script."""
from pathlib import Path
import argparse
from src.pipeline import quality,business,data_science,executive_report,run
from src.dashboard import export_dashboard

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=['quality','dashboard','business','models','report','all'],default='all')
    args=parser.parse_args()
    {'quality':quality,'dashboard':export_dashboard,'business':business,'models':data_science,'report':executive_report,'all':run}[args.stage](Path(__file__).resolve().parent)
