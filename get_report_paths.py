import pandas as pd
from glob import glob
from os.path import join
from datetime import datetime


if __name__ == "__main__":

    RESULTS_PATH = "/hpf/largeprojects/ccm_dccforge/dccforge/results"

    IGNORE_FOLDERS = set(join(RESULTS_PATH, folder) for folder in ["calx/", "misc/", "run_statistics/", "database/"])

    report_paths = []
    
    globbed_dir =  glob(join(RESULTS_PATH, "*x/"))
    

    for family_prefix_dir in globbed_dir:
        if family_prefix_dir in IGNORE_FOLDERS:
            print("\tIgnoring folder it's in an ignored folder..")
            continue

        # sorted - ascending order
        for family in glob(join(family_prefix_dir, "*/")):

            # non-clinical and synonymous reports
            reports = sorted([report for report in glob(join(family, "**/*wes*"), recursive = True) if "clinical" not in report and "synonymous" not in report])

            if len(reports) >= 1:
                report_paths.append(reports[-1]) #latest report since prefix is: yyyy-mm-dd
            else:
                print("No report files found for %s" % family)

    
    stripped_report_paths = [path.replace('/hpf/largeprojects/ccm_dccforge/dccforge/results', '.') for path in report_paths]
    
    stripped_report_path_df =  pd.DataFrame(stripped_report_paths)
    
    stripped_report_path_df.to_csv('report_paths_{}.csv'.format(format(datetime.today().strftime('%Y-%m-%d'))), index = False, header = False)