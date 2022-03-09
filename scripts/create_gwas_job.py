import pandas as pd
import os
import argparse
import sys
import logging
import textwrap
import uuid
from pathlib import Path
from functions import read_jobs

# Create the parser
parser = argparse.ArgumentParser(description="QC the data")

# Add the arguments
parser.add_argument("-j", "--job", type=int, help="the row number to run")
parser.add_argument(
    "-p", "--path", type=str, help="the path to the pipeline data directory"
)
parser.add_argument("-u", "--user", type=str, help="the user name")
parser.add_argument(
    "-d", "--data", type=str, help="path to the uk biobank genetic data"
)

args = parser.parse_args()

input_path = args.path
user = args.user
pipeline_data = args.data

# create uid
uid = uuid.uuid4()

job_cols = [
    "name",
    "application_id",
    "pheno_file",
    "pheno_col",
    "covar_file",
    "covar_col",
    "qcovar_col",
    "method",
]

# logging
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


def check_args():
    if args.path is None:
        print("Path to working directory (-p) required")
        sys.exit()
    if not os.path.isdir(args.path):
        logger.error(f"The path specified does not exist: {args.path}")
        sys.exit()
    if args.data is None:
        print("Data path (-d) required")
        sys.exit()
    if args.user is None:
        logger.error("User (-u) required")
        sys.exit()


def create_dirs(row):
    logger.debug(row)
    out_dir = f"{input_path}/data/phenotypes/{user}/output/{row['name']}/{uid}"
    logger.debug(out_dir)
    try:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
    except:
        logger.error(f"Can't make output directory: {out_dir}")
        sys.exit()


def create_gwas_sbatch(row):
    logger.debug(row)
    logger.debug(row["qcovar_col"])
    logger.debug(row["covar_col"])
    covarData=""
    # check if covar values exist, if not create empty
    if not pd.isna(row["qcovar_col"]):
        covarData += " ".join(
                [" --qCovarCol=" + s for s in row["qcovar_col"].split(";")]
            )
    if not pd.isna(row["covar_col"]):
        covarData += " ".join(
                [" --covarCol=" + s for s in row["covar_col"].split(";")]
            )
    if row["method"] == "bolt":
        create_bolt(
            pheno_name = row["name"],
            pheno_file = row["pheno_file"],
            pheno_col = row["pheno_col"],
            covar_file = row["covar_file"],
            covar_data = covarData,
        )


def create_bolt(pheno_name, pheno_file, pheno_col, covar_file, covar_data):
    # removing mrcieu partitions until permissions are sorted
    # SBATCH -p mrcieu,mrcieu2
    bolt_code = textwrap.dedent(
        f"""\
    #!/bin/bash

    #SBATCH -p cpu,mrcieu
    #SBATCH --job-name ukb_{pheno_name}
    #SBATCH -o {input_path}/data/phenotypes/{user}/output/{pheno_name}/{uid}/chr_all_run.log
    #SBATCH -e {input_path}/data/phenotypes/{user}/output/{pheno_name}/{uid}/chr_all_run.err
    #SBATCH --nodes=1 --tasks-per-node=14
    #SBATCH --mem-per-cpu=4000
    #SBATCH --time=5-00:00:00

    cd $SLURM_SUBMIT_DIR
    {input_path}/scripts/software/BOLT-LMM_v2.3.2/bolt\\
     --bfile={input_path}/data/bolt_bfile/grm6_european_filtered_ieu\\
     --bgenFile={pipeline_data}/data.chr0{{1..9}}.bgen\\
     --bgenFile={pipeline_data}/data.chr{{10..22}}.bgen\\
     --bgenFile={pipeline_data}/data.chrX.bgen\\
     --sampleFile={pipeline_data}/data.chr1-22.sample\\
     --geneticMapFile={input_path}/scripts/software/BOLT-LMM_v2.3.2/tables/genetic_map_hg19_withX.txt.gz\\
     --bgenMinMAF=0.001\\
     --phenoFile={input_path}/data/phenotypes/{user}/input/{pheno_file}\\
     --phenoCol={pheno_col}\\
     --covarFile={input_path}/data/phenotypes/{user}/input/{covar_file}\\
     {covar_data}\\
     --lmm\\
     --LDscoresFile={input_path}/scripts/software/BOLT-LMM_v2.3.2/tables/LDSCORE.1000G_EUR.tab.gz\\
     --LDscoresMatchBp\\
     --numThreads=14\\
     --verboseStats\\
     --modelSnps {input_path}/data/model_snps_for_grm/grm6_snps.prune.in\\
     --statsFileBgenSnps={input_path}/data/phenotypes/{user}/output/{pheno_name}/{uid}/{pheno_name}_imputed.txt.gz\\
     --covarMaxLevels=30\\
     --statsFile={input_path}/data/phenotypes/{user}/output/{pheno_name}/{uid}/{pheno_name}_out.txt.gz
    """
    )
    logger.info(bolt_code)
    # write to file
    sbatch_file = (
        f"{input_path}/data/phenotypes/{user}/output/{pheno_name}/{uid}/bolt.sh"
    )
    o = open(sbatch_file, "w")
    o.write(bolt_code)
    o.close()

    # run it
    try:
        os.system(f"sbatch {sbatch_file}")
    except:
        logger.error("sbatch failed: {sbatch_file}")


if __name__ == "__main__":
    check_args()
    job_df = read_jobs(input_path, user)
    row = job_df.iloc[args.job]
    create_dirs(row)
    create_gwas_sbatch(row)

