#!/bin/bash 

# All output will be moved to a folder given by the current date in yyyy-mm-dd format.
# 1. get_report_paths.py - Obtains all relevant report_paths and dumps as dated csv
# 2. get_family_participants.py - Gets all family-participant identifiers by reading in each report from the previous step and dumping to a json.
# 3. Copies, tarball and gunzips all reports from get_report_paths.py
# These scripts could be further integrated but were written separately!


todays_date=$(date +%F)

mkdir -p ${todays_date}

# get report paths 
python3 get_report_paths.py 

# read in csv and get family-participant identifiers
python3 get_family_participants.py --report_paths=report_paths_${todays_date}.csv

# cp relevant reports, keeping directory structure and gunzip
./cp_reports.sh 

rm -rf reports-${todays_date}

mv report_paths_${todays_date}.csv family-participant-reports-${todays_date}.json reports-${todays_date}.tar.gz ${todays_date}/