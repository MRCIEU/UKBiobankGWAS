#!/bin/bash

#SBATCH -p mrcieu

module load languages/anaconda3/3.7

if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

python qc.py $PIPELINE_DATA `whoami`