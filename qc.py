import pandas as pd
import sys 

PIPELINE_DATA= sys.argv[1]
USER = sys.argv[2]

print(PIPELINE_DATA,USER)

job_file=f'{PIPELINE_DATA}/data/phenotypes/{USER}/input/jobs.csv'

job_df = pd.read_csv(job_file)
print(job_df.head())