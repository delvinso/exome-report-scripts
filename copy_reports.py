
"""
usage: python3 copy_reports.py --report_paths=./all_reports-2022-04-21/all-report-paths-2022-04-21.csv

- copies reports into their respective report type folders (current/old exomes, current/old genomes) without the directory structure 
"""


import os 
import shutil
from datetime import datetime
import argparse
import pandas as pd

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report_paths",
        type=str,
        required=True,
        help="path to a csv of report paths",
    )

    return parser

if __name__ == "__main__":
    args = get_parser().parse_args()
    df = pd.read_csv(args.report_paths)

    to_move_dir = f"/home/delvinso/variant_report/all_reports-{datetime.today().strftime('%Y-%m-%d')}"

    ss_df = df[(~df['report'].isnull())]

    for report_type, subdf in ss_df.groupby('report_type'):
        
        report_type_folder = os.path.join(to_move_dir, report_type)

        if not os.path.exists(report_type_folder):
            os.makedirs(report_type_folder)
            
        for report in subdf['report'].tolist():
            # preserves the metadata
            shutil.copy2(report, os.path.join(report_type_folder, os.path.basename(report)))
        
