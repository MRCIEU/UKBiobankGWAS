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

def check_args():
    if args.path is None:
        print("path (-p) required")
        sys.exit()
    if not os.path.isdir(args.path):
        print(f'The path specified does not exist: {args.path}')
        sys.exit()
    if args.user is None:
        print("User (-u) required")
        sys.exit()

def read_jobs():
    input_path = args.path
    user = args.user

    job_file=f'{input_path}/data/phenotypes/{user}/input/jobs.csv'
    print(job_file)

    try:
        job_df = pd.read_csv(job_file)
        print(job_df.head())
        
        return job_df
    except:
        print(f'Can not read {job_file}')
        sys.exit()

#def read_pheno(job_df):
    #


if __name__ == "__main__":
    check_args()
    job_df = read_jobs()