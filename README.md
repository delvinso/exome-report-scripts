
# About

Series of scripts for handling dccforge WES reports from CCM's CRE ppeline. These scripts could be further integrated but were written separately.

1. `get_report_paths.py` - Obtains all relevant report_paths and dumps as dated csv
2. `get_family_participants.py` - Gets all family-participant identifiers by reading in each report from the previous step and dumping to a json.
3. `cp-reports.sh` - Copies, tarball and gunzips all reports from get_report_paths.py


`get_reports_mapping_cp.sh` - A wrapper for the above three scripts, all output will be moved to a folder given by the current date in yyyy-mm-dd format. eg. `2022-01-04`

