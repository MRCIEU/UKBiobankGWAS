#!/bin/bash

#SBATCH -p mrcieu

module load languages/anaconda3/3.7

if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

JOB="${1:-0}"

python qc.py -j $JOB -p $PIPELINE_DATA -u `whoami`
python create_gwas_job.py -j $JOB -p $PIPELINE_DATA -u `whoami` -d $UKBIOBANK_DATA 