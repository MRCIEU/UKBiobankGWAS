import pandas as pd
import os
import argparse
import sys 

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

def check_args():
    if args.path is None:
        print("Error: path (-p) required")
        sys.exit()
    if not os.path.isdir(args.path):
        print(f'Error: the path specified does not exist: {args.path}')
        sys.exit()
    if args.user is None:
        print("Error: user (-u) required")
        sys.exit()


def read_jobs():
    job_file=f'{input_path}/data/phenotypes/{user}/input/jobs.csv'
    print(f'Reading {job_file}')

    try:
        job_df = pd.read_csv(job_file)
        print(job_df.head())
        # check columns
        if not list(job_df.columns) == ['name','application_id','pheno_file','pheno_col','covar_file','covar_col','qcovar_col']:
            print(f'Error: jobs.csv file structure is not right: {list(job_df.columns)}')
            sys.exit()
        else:
            return job_df
    except:
        print(f"Can't read {job_file}")
        sys.exit()

def read_pheno(job_df):
    for i,row in job_df.iterrows():
        pheno_file = f"{input_path}/data/phenotypes/{user}/input/{row['pheno_file']}"
        print(f'Reading {pheno_file}')
        try:
            pheno_df = pd.read_csv(pheno_file,sep=' ')
            print(pheno_df.head())
            # check if first two columns are FID and IID
            if not list(pheno_df.columns)[:2] == ['FID','IID']:
                print(f"Error: first two columns of pheno file must be FID and IID: {list(pheno_df.columns)[:2]}")
                sys.exit()
            # check that the pheno column exists
            pheno_col = row['pheno_col']
            if not pheno_col in pheno_df.columns:
                print(f"Error: pheno_col {pheno_col} does not exist in {pheno_file}")
                sys.exist()
            else:
                print(f"Value counts for {pheno_col}:")
                vc = pheno_df[pheno_col].value_counts()
                print(vc)
        except:
            print(f"Error: failed to qc pheno file {pheno_file}")

if __name__ == "__main__":
    check_args()
    job_df = read_jobs()
    read_pheno(job_df)