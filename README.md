# About

Series of scripts for aggregating exome and genome reports from CCM's CRE pipeline. 

The below scripts should be run in the directory you'd like the output saved in, eg. `python3 get_all_report_paths.py` and `python3 copy_reports.py --report_paths=./all_reports-2022-04-21/all-report-paths-2022-04-21.csv`

1. `get_all_report_paths.py `- traverses multiple known directories with exome and exome-like reports and dumps the information into two flat files
- known directories:
    - `current_exome`: `/hpf/largeprojects/ccm_dccforge/dccforge/results`
    - `old_exome` : `/hpf/largeprojects/ccmbio/naumenko/project_cheo/DCC_Samples_part1`
    - `current_genome`: `/hpf/largeprojects/ccmbio/ccmmarvin_shared/genomes`
    - `old_genome`: `/hpf/largeprojects/ccm_dccforge/dccdipg/c4r_wgs/results`
    - `in_progress_exome`: `/hpf/largeprojects/ccmbio/ccmmarvin_shared/exomes/in_progress`
- outputs:
    - `./all_reports-yyyy-mm-dd/all-fam-ptp-reports-yyyy-mm-dd.csv` - parsed family and participant codenames and the report they belong to 
    - `./all_reports-yyyy-mm-dd/all-report-paths-yyyy-mm-dd.csv` - report paths 
    	- sanity check report counts by type: `df[['report', 'report_type']].dropna().value_counts('report_type')`
2. `copy_reports.py `- takes output of above script, and cps all reports into a single, nested directory


