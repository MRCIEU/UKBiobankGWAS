#!/bin/bash

#SBATCH -p cpu,mrcieu
#SBATCH --account=SSCM013902

# load anaconda for pandas
module load languages/python/3.12.3

# read .env file
if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
else
  echo "No .env file exists, exiting"
  exit
fi

# set default job row to 0
JOB="${1:-0}"

USER=$(whoami)

# QC the pheno and covariate files
python scripts/qc.py -j $JOB -p $PIPELINE_DATA -u $USER

# Create and run the gwas script
python scripts/create_gwas_job.py -j $JOB -p $PIPELINE_DATA -u $USER -d $UKBIOBANK_DATA 
