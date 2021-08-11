import pandas as pd
import os
import sys
import logging

# logging
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

def read_summary(f):
    #cols = 
    df = pd.read_csv(f,sep="/",header=None)
    logger.info(df.shape)
    
    # drop columns with same values
    df = df[df.columns[df.nunique() > 1]]
    df.columns = ['user','name','job_id','file_name']
    logger.info(df.shape)

    # drop duplicates
    df.drop_duplicates(inplace=True)
    logger.info(df.shape)

    # counts per user
    vc = df['user'].value_counts()
    logger.info(f'\n{vc}')

if __name__ == "__main__":
    read_summary('bolt_jobs.txt')
    read_summary('plink_jobs.txt')
