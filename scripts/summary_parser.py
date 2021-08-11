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

def read_summary(f,method):
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

    df['method']=method
    #logger.info(df)
    return df

if __name__ == "__main__":
    df1 = read_summary(f='bolt_jobs.txt',method='bolt-lmm')
    df2 = read_summary(f='plink_jobs.txt',method='plink')
    df = pd.concat([df1,df2])
    logger.info(f"Total number of GWAS by type:\n{df['method'].value_counts()}")

    count_df = df.groupby(['user','method']).size().unstack(fill_value=0)
    logger.info(f'Total number of GWAS by type and user\n{count_df}')