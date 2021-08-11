#!/bin/bash

#SBATCH -p mrcieu,mrcieu2

# read .env file
if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

# create some output summary files
bolt_out=bolt_jobs.txt
plink_out=plink_jobs.txt
if [ -f $bolt_out ]
then
  rm $bolt_out
fi
if [ -f $plink_out ]
then
  rm $plink_out
fi

for user in $PIPELINE_DATA/data/phenotypes/*/; do
  for o in ${user}output/*/; do
    #echo output directory: $o
    for j in ${o}*/; do 
      #echo gwas job: $j
      if [ -d $j ]
      then
        find $j -name "*_imputed.txt.gz" ! -name "chr*_out_imputed.txt.gz" -size +10M >> $bolt_out
        find $j -name "*.plink.gz" -size +10M >> $plink_out
      fi
    done
  done  
done 
