#!/bin/bash
#
# {BASH_SOURCE[0]} is the name of the currently running bash script
# taking the 'dirname' of this yields the current working dir
#
source $( dirname ${BASH_SOURCE[0]} )/01_set_run_variables.sh
${SWB2} --output_prefix=${OUTPUT_FILE_PREFIX}  \
        --data_dir=${DATA_DIR}                 \
        --weather_data_dir=${WEATHER_DIR}      \
        ${SWB_CONTROL_FILE}
