# Hail Mary attempt to keep netCDF from erroring out based on this SO entry:
# https://stackoverflow.com/questions/49317927/errno-101-netcdf-hdf-error-when-opening-netcdf-file
#
export HDF5_USE_FILE_LOCKING=FALSE

export RES=1000
export DATA_DIR=input_grids_1000m
export WEATHER_DIR=/caldera/projects/usgs/water/umwsc/swb/data/PRISM/minnesota_project_area
export SWB_CONTROL_FILE=mn__swb_control_file.ctl
export OUTPUT_FILE_PREFIX=mn_fullrun__${RES}m_

export SWBSTATS_ZONE_PERIOD_FILE=swbstats2_zone_period_file_ALLDATES_2000to2022.csv

export SWB2=swb2
export SWBSTATS2=swbstats2
export PYTHONPATH=/caldera/projects/usgs/water/umwsc/swb/miniconda3/
