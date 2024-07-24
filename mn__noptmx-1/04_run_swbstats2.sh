#!/bin/bash
# Run ANNUAL and SEASONAL zonal stats - together in one zone period file:
source $( dirname ${BASH_SOURCE[0]} )/01_set_run_variables.sh

${SWBSTATS2} --zone_period_file=${SWBSTATS_ZONE_PERIOD_FILE} --no_netcdf_output $(ls *1000m_net_infiltration*.nc)

${SWBSTATS2} --zone_period_file=${SWBSTATS_ZONE_PERIOD_FILE}  --no_netcdf_output $(ls *1000m_actual_et*.nc)

${SWBSTATS2} --zone_period_file=${SWBSTATS_ZONE_PERIOD_FILE}  --no_netcdf_output $(ls *1000m_gross_precipitation*.nc)

${SWBSTATS2} --zone_period_file=${SWBSTATS_ZONE_PERIOD_FILE}  --no_netcdf_output $(ls *1000m_rejected_net_infiltration*.nc)

${SWBSTATS2} --zone_period_file=${SWBSTATS_ZONE_PERIOD_FILE}  --no_netcdf_output $(ls *1000m_runoff__*.nc)

printf "Completed running swbstats2 on the swb2 netCDF output.\n\n"
