#!/bin/bash

#SBATCH -p mrcieu

module load languages/anaconda3/3.7

if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

python qc.py -p $PIPELINE_DATA -u `whoami`
python create_submission.py -p $PIPELINE_DATA -u `whoami` -d $UKBIOBANK_DATA 