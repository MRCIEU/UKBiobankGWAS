#!/bin/bash

#SBATCH -p mrcieu

module load languages/anaconda3/3.7

if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

# set default job row to 0
JOB="${1:-0}"

# QC the pheno and covariate files
python qc.py -j $JOB -p $PIPELINE_DATA -u `whoami`

# Create and run the gwas script
python create_gwas_job.py -j $JOB -p $PIPELINE_DATA -u `whoami` -d $UKBIOBANK_DATA 