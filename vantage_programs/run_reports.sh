#!/bin/bash

# run the weekly reports 

# make sure we are in the right directory
cd /Users/darrell32/Documents/WeeklyReports/
pwd

#run the python scripts
python3 query1_blood.py
python3 query2_dna.py
python3 query3_dna.py
python3 query4_dna.py
python3 query5_dna_monthly.py
python3 email_reports.py
