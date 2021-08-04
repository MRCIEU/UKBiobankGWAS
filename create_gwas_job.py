import pandas as pd
import os
import argparse
import sys
import logging
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
    out_dir = f"{input_path}/data/phenotypes/{user}/output/{row['name']}"
    logger.debug(out_dir)
    try:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
    except:
        logger.error(f"Can't make output directory: {out_dir}")
        sys.exit()
        
if __name__ == "__main__":
    check_args()
    job_df = read_jobs(input_path,user)
    row = job_df.iloc[args.job]
    create_dirs(row)

