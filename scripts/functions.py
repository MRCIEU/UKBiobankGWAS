import pandas as pd
import logging
import sys

# logging
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

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


def read_jobs(input_path, user):
    job_file = f"{input_path}/data/phenotypes/{user}/input/jobs.csv"
    logger.info(f"Reading {job_file}")

    try:
        job_df = pd.read_csv(job_file)
        logger.info(f"\n{job_df.head()}")
        # check columns
        if not list(job_df.columns) == job_cols:
            logger.error(f"File structure is not right: {list(job_df.columns)}")
            sys.exit()
        else:
            return job_df
    except:
        logger.error(f"Can't read {job_file}")
        sys.exit()
