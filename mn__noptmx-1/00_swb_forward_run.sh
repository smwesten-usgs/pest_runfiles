#!/bin/bash

source $( dirname ${BASH_SOURCE[0]} )/01_set_run_variables.sh

# --------------------------------------
# Run curve number aligner...
# --------------------------------------
printf "Running curve number aligner.\n\n"
python 02_swb_parameter_processor.py

# --------------------------
# Part 1 - run SWB
# Produces netcdf files for next step
# Uses environment variables from "set_run_variables.sh"
# -------------------------
printf Running SWB
./03_run_swb.sh
wait
printf "Finished SWB Run.\n\n"

# -------------------------
# Part 2 - Run swbstats to get zone stats 
# Processes netcdf files to produce .csv files
# Uses environment variables from "set_run_variables.sh"
# -------------------------
printf "Running swbstats2"
./04_run_swbstats2.sh
printf "Finished swbstats2 run.\n\n"

# ------------------------
# Part 3 - run post-processor observation 
# python script for PEST input
# ------------------------
printf "Running postprocessing script.\n\n"
python 05_swbstats2_post_processor.py

echo All Done!
# For debugging:
# pause
