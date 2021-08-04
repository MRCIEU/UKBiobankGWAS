import pandas as pd
import os
import argparse
import sys 
import logging

# Create the parser
parser = argparse.ArgumentParser(description='QC the data')

# Add the arguments
parser.add_argument('-p',
                       '--path',
                       type=str,
                       help='the path to the pipeline data directory')
parser.add_argument('-u',
                       '--user',
                       type=str,
                       help='the user name')

args = parser.parse_args()

input_path = args.path
user = args.user

job_cols = [
    'name',
    'application_id',
    'pheno_file',
    'pheno_col',
    'covar_file',
    'covar_col',
    'qcovar_col',
    'method'
]

#logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

def check_args():
    if args.path is None:
        print("Path (-p) required")
        sys.exit()
    if not os.path.isdir(args.path):
        logger.error(f'The path specified does not exist: {args.path}')
        sys.exit()
    if args.user is None:
        logger.error("User (-u) required")
        sys.exit()


def read_jobs():
    job_file=f'{input_path}/data/phenotypes/{user}/input/jobs.csv'
    print(f'Reading {job_file}')

    try:
        job_df = pd.read_csv(job_file)
        print(f'\n{job_df.head()}')
        # check columns
        if not list(job_df.columns) == job_cols:
            logger.error(f'File structure is not right: {list(job_df.columns)}')
            sys.exit()
        else:
            return job_df
    except:
        logger.error(f"Can't read {job_file}")
        sys.exit()

def read_file(job_df,file_type):
    for i,row in job_df.iterrows():
        try:
            file_name = row[f'{file_type}_file']
            file_col = row[f'{file_type}_col']
            file_path = f"{input_path}/data/phenotypes/{user}/input/{file_name}"
            logger.info(f'\nReading {file_path}')
            df = pd.read_csv(file_path,sep=' ')
            logger.info(f'\ndf.head()')
            
            # check if first two columns are FID and IID
            if not list(df.columns)[:2] == ['FID','IID']:
                logger.error(f"First two columns of pheno file must be FID and IID: {list(pheno_df.columns)[:2]}")
                sys.exit()

            # check that the columns exist in the pheno/covar files
            file_cols = file_col.split(';')
            if file_type == 'covar':
                file_cols.extend(row[f'q{file_type}_col'].split(';'))
            logger.info(f'file_cols: {file_cols}')
            for col in file_cols:
                if not col in df.columns:
                    logger.error(f"Col {col} does not exist in {file_name}")
                    sys.exist()
                else:
                    logger.info(f"\nValue counts for {col}:")
                    vc = df[col].value_counts()
                    logger.info(vc)

            # check that method is bolt or plink
            if row['method'] not in ['bolt','plink']:
                logger.error('Method needs to be either bolt or plink')
                sys.exit()
        except:
            logger.error(f"Failed to qc file {file_name}")
            sys.exit()

if __name__ == "__main__":
    check_args()
    job_df = read_jobs()
    read_file(job_df,"pheno")
    read_file(job_df,"covar")
