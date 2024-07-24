#!/bin/bash

# This SLURM file is from Jeff Falgout (2020-09-21). Modified by SMW for possible use
# with MAP files on Denali

#SBATCH --job-name=swb_mn_noptmax0
#SBATCH --output=%j-swb_mn_noptmax0.out
#SBATCH -n 1 
#SBATCH --hint=nomultithread
#SBATCH -p workq
#SBATCH --time=6:00:00
#SBATCH --account=umwsc
#SBATCH --mail-type=ALL
#SBATCH --mail-user=smwesten@usgs.gov

module load pestpp

echo "Currently loaded modules:"
module list

# Allow unlimited stack size for executable (e.g. SWB, MODFLOW)
ulimit -s unlimited

# Case name never makes sense to me; let's define the PEST control filename and use the 'basename'
# utility to strip off the '.pst' to populate 'CASE_NAME'
PEST_CONTROL_FILE_NAME="mn__noptmax0.pst"
CASE_NAME=$(basename ${PEST_CONTROL_FILE_NAME} .pst)

# Specify the full root pathname here; this is likely static and should not change much from run
# to run
ROOT_DIR="/caldera/projects/usgs/water/umwsc/swb/projects/Minnesota/pest_runs"

# Define the subdirectory within the 'ROOT_DIR' to use as the 'home base' for our project; note I 
# am still assuming that the subdirectory that we're working out of has the same base name as
# our pest control file
PROJECT_DIR="${ROOT_DIR}/${CASE_NAME}"

# Scratch dir can be literally anywhere on the shared file system. Since this SLURM file performs 
# no clean up at the end of the run, it makes sense to put 'scratch' somewhere easily
# accessible by the user for troubleshooting purposes or for easy manual deletion
SCRATCH_DIR="${PROJECT_DIR}/scratch"

# Jeff has this set up so that there may be a different set of files shared with the 'master' process
# and the 'worker' processes. in our case we can probably set them to be the same.
MASTER_TEMPLATE_DIR="${PROJECT_DIR}/master"
MASTER_DIR="${MASTER_TEMPLATE_DIR}_${SLURM_JOBID}"

# Setting the worker template to be the same as the master; they can be different if needs be 
# in order to avoid explicit copying of large amounts of data that is best shared via the
# filesystem
WORKER_TEMPLATE_DIR="${MASTER_TEMPLATE_DIR}"
export WORKER_DIR="${SCRATCH_DIR}/worker_"

# Set up the worker directories--create a directory for each worker with the worker id
# appended to the directory name
echo "Setting up worker directories"
srun setup_workers_pestpp.sh ${WORKER_TEMPLATE_DIR} ${WORKER_DIR}

# Create a copy of the 'master' directory to work from; directory name will have the
# SLURM_ID appended to it
echo "Setting up master directory"
cp -r ${MASTER_TEMPLATE_DIR} ${MASTER_DIR}
cd ${MASTER_DIR}

# Make up a random TCP/IP port number to avoid multiple instances of pestpp all glomming
# onto the same port number
MASTER_PORT=$((10000 + RANDOM % 1000))

# Write out a 'pestpp.conf' file; this file contains 1 line to handle firing off the pestpp
# master process and n-1 lines that handle firing off pestpp as dedicated worker processes.
echo "Writing out the multi-prog configuration file."
echo "0 bash -c 'cd ${MASTER_DIR} && pestpp-ies ${CASE_NAME}.pst /h :${MASTER_PORT}'" > pestpp.conf

# Write out the workers line adjusting for only 1 worker if necessary (-n2)
# *** NOTE: the "\$" in the lines below are there to 'escape' the '$' character; in other words, 
# we need to keep Linux from treating '$' as a special character and just literally print a '$' to 
# the configuration file
if [ ${SLURM_NTASKS} -eq 2 ]
then
  echo "1 bash -c 'cd \${WORKER_DIR}\${SLURM_PROCID} && pestpp-ies ${CASE_NAME}.pst /h ${SLURMD_NODENAME}:${MASTER_PORT}'" >> pestpp.conf
else
    echo "1-$((SLURM_NTASKS-1)) bash -c 'cd \${WORKER_DIR}\${SLURM_PROCID} && pestpp-ies ${CASE_NAME}.pst /h ${SLURMD_NODENAME}:${MASTER_PORT}'" >> pestpp.conf
fi

echo "Running pestpp; tasks determined by the contents of 'pestpp.conf'"
echo "srun --multi-prog pestpp.conf"

# Use --multi-prog slurm option to run the pest_hp master and agents; each line contained within
# the file 'pestpp.conf' represents an separate task that needs to be run by the scheduler.
srun --multi-prog pestpp.conf
