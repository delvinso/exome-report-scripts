#!/bin/bash

# replace /hpf/largeprojects/ccm_dccforge/dccforge/results/ in the csv 
todays_date=$(date +%F)
dir_to_place=/home/delvinso/variant_report/reports-${todays_date}/
mkdir -p ${dir_to_place}
cd /hpf/largeprojects/ccm_dccforge/dccforge/results/
cat /home/delvinso/variant_report/report_paths_${todays_date}.csv | cut -d, -f2  | xargs cp --parents -t ${dir_to_place}
GZIP=-9 
cd ~/variant_report/
tar cvzf reports-${todays_date}.tar.gz ${dir_to_place}
