# About

Series of scripts for handling exome reports from CCM's CRE pipeline. 

1. `get_all_report_paths.py `- traverses multiple known directories with exome and exome-like reports and dumps the information into two flat files
- known directories:
    - `current_exome`: `/hpf/largeprojects/ccm_dccforge/dccforge/results`
    - `old_exome` : `/hpf/largeprojects/ccmbio/naumenko/project_cheo/DCC_Samples_part1`
    - `current_genome`: `/hpf/largeprojects/ccmbio/ccmmarvin_shared/genomes`
    - `old_genome`: `/hpf/largeprojects/ccm_dccforge/dccdipg/c4r_wgs/results`
    - `in_progress_exome`: `/hpf/largeprojects/ccmbio/ccmmarvin_shared/exomes/in_progress`
- outputs:
    - `all-fam-ptp-reports-yyyy-mm-dd.csv` - parsed family and participant codenames and the report they belong to 
    - `all-report-paths-yyyy-mm-dd.csv` - report paths 
2. `copy_reports.py `- takes output of above script, and cps all reports into a single, nested directory


