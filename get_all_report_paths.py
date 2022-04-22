from typing import List
from glob import glob
from os.path import basename, join, dirname, exists
from os import makedirs
from datetime import datetime
import sys
import pandas as pd

def get_family_participants(report_paths:list) -> list:
    """
    iterates through list of reports, reading in the report and extracting family and participant codenames
    """
    mapping_list = []
    for item in report_paths:
        report = item.get('report')
        
        if report is None:
            mapping_list.append({'family': None, 'samples': None, 'report_name': report})
            continue
        
        if report.endswith(".csv"):
            sep = ","
        elif report.endswith(".tsv"):
            sep = "\t"
        else:
            print(f"Unknown fileformat and delimiter for {report}")
            sys.exit(1)

        try:
            df = pd.read_csv(report, sep=sep,  index_col=0, nrows=0)
        except UnicodeDecodeError:
            print("UnicodeDecodeError on %s. Trying latin-1 decoding." % report)
            df = pd.read_csv(report, encoding="latin-1", sep=sep, index_col=0, nrows=0)
            
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

        mapping_list.append({'family': family, 'samples': samples, 'report_name': report, 'report_type': item['report_type']})
        
    return mapping_list
    

def filter_reports(reports:List[str], report_type:str) -> List[str]:
        """
        filters out *sv files that are not wes reports
        """
        if report_type == 'old_exome':
            filtered_reports = sorted([x for x in reports 
                                           # for old exomes, filters out config files and files ending in {create|merge}_report.csv 
                                           if "config" not in x and "report" not in x and "data_versions" not in x])
        elif report_type == 'current_exome':
            filtered_reports = sorted([x for x in reports if "clinical" not in x and 'synonymous' not in x])
        elif 'genome' in report_type:
            filtered_reports = sorted([x for x in reports if "clinical" not in x])
        else:
            raise ValueError("report_type must contain either genome or exome")
        return filtered_reports
    
def traverse_get_report_paths(input_dict) -> List[str]:
    """
    exomes
    - analyses stored under an umbrella family identifier, eg. 1x, 2x, 3x
    - current exomes can have two different directory structures depending on whether they were run using bcbio or crg2
        - `/12x/1221R/1221R.wes.2019-07-25.csv`
        - `/25x/2535/report/coding/2535/2535.wes.regular.2022-02-05.csv`
    - old exomes are named as the family identifier, eg. <family>.csv, whereas new exomes are  `<family>.wes.<date>.csv` and `<family>.wes.regular.<date>.csv.`
    - latest report by date is taken
    - exclude clinical or synonymous reports
    genomes
    - no umbrella naming scheme 1x,2x, etc. naming scheme.
    - analyses are stored directly in the root path, with the reports being found in subfolders whose directory name contains 'report'
        - `<family>/report/coding/<family>/*csv` or `<family>/reports/*csv`
        - current: `/hpf/largeprojects/ccmbio/ccmmarvin_shared/genomes/1933/report/coding/1933/1933.wes.regular.2021-04-10.csv`, 
        `hpf/largeprojects/ccmbio/ccmmarvin_shared/genomes/1899/reports/1899.wes.regular.2021-01-30.csv`
        - old: `/hpf/largeprojects/ccm_dccforge/dccdipg/c4r_wgs/results/1544/reports/1544.wes.regular.2020-11-04.csv`,
                `/hpf/largeprojects/ccm_dccforge/dccdipg/c4r_wgs/results/2203/report/coding/2203/2203.wes.regular.2021-07-18.csv`
    - exclude clinical or synonymous reports
    """
    
    report_paths = []
    for report_type, root_path in input_dict.items():
        print(report_type, root_path)
        if 'exome' in report_type:
            root_path_pattern = "*x/"
        elif 'genome' in report_type:
            root_path_pattern = "*/"
        else:
            raise ValueError("report_type must contain either genome or exome")

        globbed_root_path = glob(join(root_path, root_path_pattern))

        # traversing the root path
        # this will be 2x, 3x, etc for exomes, or the family_id for genomes
        # additional logic to parse out family subdirs in exomes
        for subfolder in globbed_root_path:

            if 'exome' in report_type:

                for family in glob(join(subfolder, "*/")):
                    if 'bams' in family:
                        continue

                    if 'old_exome' in report_type:
                        pattern = "**/*sv"
                    elif 'current_exome' in report_type:
                        pattern = "**/*wes*sv"

                    reports = glob(join(family, pattern), recursive = True)
                    reports = filter_reports(reports, report_type)


                    if len(reports) > 1:
#                         print("\tMore than one report found for %s" % family)
                        report_paths.append({"folder": family,"report": reports[-1], "report_type": report_type, "all_reports": reports})
                    elif len(reports) == 1:
                        report_paths.append({"folder": family, "report": reports[-1], "report_type": report_type, "all_reports": None})
                    else:
                        report_paths.append({"folder": family, "report": None, "report_type": report_type, "all_reports": None})
                        print("\tNo report files found for %s" % family)

            elif 'genome' in report_type:
                # unlike exomes, the family_ids sit directly in the root path so we need to filter out some noise
                if basename(dirname(subfolder))[0].isdigit():

                    for folder in glob(join(subfolder, "*/")): # recursively searching for 'report' is very slow
                        if 'report' in folder:
                            reports = glob(join(folder, "**/*wes*sv"), recursive = True) # using w*s didn't capture anything else
                            reports = filter_reports(reports, report_type)

                            if len(reports) > 1:
#                                 print("\tMore than one report found for %s" % subfolder)
                                report_paths.append({"folder": subfolder, "report": reports[-1], "report_type": report_type, "all_reports": reports})
                            elif len(reports) == 1:
                                report_paths.append({"folder": subfolder, "report": reports[-1], "report_type": report_type, "all_reports": None})
                            else:
                                report_paths.append({"folder": subfolder, "report": None, "report_type": report_type, "all_reports": None})
                                print("\tNo report files found for %s" % folder)
                                
    return report_paths
                                

if __name__ == "__main__":

    out_dir = f"/home/delvinso/variant_report/all_reports-{datetime.today().strftime('%Y-%m-%d')}"
    if not exists(out_dir):
        makedirs(out_dir)

    input_dict = {
        'current_exome': '/hpf/largeprojects/ccm_dccforge/dccforge/results',
        'old_exome' : '/hpf/largeprojects/ccmbio/naumenko/project_cheo/DCC_Samples_part1',
        'current_genome': '/hpf/largeprojects/ccmbio/ccmmarvin_shared/genomes',
        'old_genome': '/hpf/largeprojects/ccm_dccforge/dccdipg/c4r_wgs/results'
    }
    
    report_paths = traverse_get_report_paths(input_dict)
    
    df = pd.json_normalize(report_paths)
    
    report_fn = join(out_dir, f"all-report-paths-{datetime.today().strftime('%Y-%m-%d')}.csv")
    df.to_csv(report_fn, index = False)
    
    all_fam_ptps = get_family_participants(report_paths)

    all_fam_ptps_df = pd.json_normalize(all_fam_ptps)
    all_fam_ptps_fn = join(out_dir, f"all-fam-ptp-reports-{datetime.today().strftime('%Y-%m-%d')}.csv")
    
    # for additional wrangling will need to call explode on the samples column
    all_fam_ptps_df.to_csv(all_fam_ptps_fn, index = False)
    

