#!/bin/bash

RDM=openssl rand -hex 16

GWAS_NAME=$1
PHENO_FILE=$2
PHENO_COL=$3
COVAR_FILE=$4

#SBATCH -p mrcieu
#SBATCH --job-name gwas-$RDM
#SBATCH -o $PIPELINE_DATA/data/phenotypes/$USER/output/$PHENO_NAME/$RDM/chr_all_run.log
#SBATCH -e $PIPELINE_DATA/data/phenotypes/$USER/output/$PHENO_NAME/$RDM/chr_all_run.err
#SBATCH --nodes=1 --tasks-per-node=14
#SBATCH --mem-per-cpu=4000
#SBATCH --time=5-00:00:00

cd $SLURM_SUBMIT_DIR
$PIPELINE_DATA/scripts/software/BOLT-LMM_v2.3.2/bolt\
 --bfile=$PIPELINE_DATA/bolt_bfile/grm6_european_filtered_ieu\
 --bgenFile=$UKBIOBANK_DATA/data.chr0{1..9}.bgen\
 --bgenFile=$UKBIOBANK_DATA/data.chr{10..22}.bgen\
 --bgenFile=$UKBIOBANK_DATA/data.chrX.bgen\
 --sampleFile=$UKBIOBANK_DATA/data.chr1-22.sample\
 --geneticMapFile=$PIPELINE_DATA/scripts/software/BOLT-LMM_v2.3.2/tables/genetic_map_hg19_withX.txt.gz\
 --bgenMinMAF=0.001\
 --phenoFile=$PIPELINE_DATA/data/phenotypes/$USER/input/$PHENO_FILE\
 --phenoCol=$PHENO_COL\
 --covarFile=$PIPELINE_DATA/data/phenotypes/$USER/input/$COVAR_FILE\
 --covarCol=sex --covarCol=chip --qCovarCol=age\
 --lmm\
 --LDscoresFile=$PIPELINE_DATA/scripts/software/BOLT-LMM_v2.3.2/tables/LDSCORE.1000G_EUR.tab.gz\
 --LDscoresMatchBp\
 --numThreads=14\
 --verboseStats\
 --modelSnps $PIPELINE_DATA/data/model_snps_for_grm/grm6_snps.prune.in\
 --statsFileBgenSnps=$PIPELINE_DATA/data/phenotypes/$USER/output/$PHENO_NAME/$RDM/${PHENO_NAME}_imputed.txt.gz\
 --covarMaxLevels=30\
 --statsFile=$PIPELINE_DATA/data/phenotypes/$USER/output/$PHENO_NAME/$RDM/${PHENO_NAME}_out.txt.gz