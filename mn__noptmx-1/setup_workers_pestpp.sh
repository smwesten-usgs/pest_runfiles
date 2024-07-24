#!/bin/bash

WORKER_TEMPLATE_DIR=${1}
WORKER_DIR=${2}${SLURM_PROCID}

mkdir --parents ${WORKER_DIR}
cp -Rp ${WORKER_TEMPLATE_DIR} ${WORKER_DIR}
cd ${WORKER_DIR}

#pestpp-ies ${CASE_NAME}.pst /h

if [ $? -ne 0 ]
then
	  echo "Setting up worker directories failed!!"
	    exit 255
    fi

    exit 0
