#!/bin/bash

#SBATCH -p mrcieu

# read .env file
if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

for user in $PIPELINE_DATA/data/phenotypes/*/; do
  echo user: $user
  for o in ${user}output/*/; do
    echo output directory: $o
    for j in ${o}*/; do 
      echo gwas job: $j
      find $j -name "*_imputed.txt.gz"
      find $j -name "*.plink.gz"
    done
  done  
done 
