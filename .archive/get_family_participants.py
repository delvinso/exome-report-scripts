import pandas as pd
import json
import sys
from os.path import basename
from datetime import datetime
import argparse



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

    for arg in vars(args):
        print(arg + ": " + str(getattr(args, arg)))

    mapping_list = []

    report_path_df = pd.read_csv(args.report_paths, names = ['path'])

    for report in report_path_df['path'].tolist():

        report = report.replace('.', '/hpf/largeprojects/ccm_dccforge/dccforge/results', 1) 
        
        if report.endswith(".csv"):
            sep = ","
        elif report.endswith(".tsv"):
            sep = "\t"
        else:
            print("Unknown fileformat and delimiter")
            sys.exit(1)

        try:
            df = pd.read_csv(report, sep=sep)
        except UnicodeDecodeError:
            print("UnicodeDecodeError on %s. Trying latin-1 decoding." % report)
            df = pd.read_csv(report, encoding="latin-1", sep=sep)
        except Exception as e:
            print(
                "Report '{}' could not be read in, please double check this is a valid csv!".format(
                    report
                )
            )
            sys.exit(1)

        # these columns are 'wide' wrt the variants
        d = {"Zygosity": [], "Burden": [], "Alt_depths": []}

        # get all columns with Zygosity, Burden, or Alt_depths - these are unique for each participant
        for key in d:
            d[key].extend([col for col in df.columns if col.startswith(key)])

        # get sample names - preserved order for genotype and trio coverage
        samples = [col.replace("Zygosity.", "").strip() for col in d["Zygosity"]]
        
        family = basename(report).split(".")[0]
        
        mapping_list.append({'family': family, 'samples': samples, 'report_name': report})


    with open(f"family-participant-reports-{datetime.today().strftime('%Y-%m-%d')}.json", 'w') as f:
        json.dump(mapping_list,f, indent = 4)