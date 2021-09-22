# UKBiobankGWAS
Notes and code for running UK Biobank GWAS at the MRC IEU


## Steps

1. Request GWAS account from IEU data manager if not already done 
2. Create input files in your RDSF input directory
3. Wait for files to copy over to BC4
4. On BC4, clone this repo and get .env
5. Run the GWAS submission script
6. A job is submitted to the queue that QCs the files, and then creates a new submission job for the GWAS
6. Wait for GWAS to complete and output files to sync back to RDSF

## Details

### Create input files on RDSF

Create `jobs.csv` in `input` directory, containing information on GWAS jobs
- all column names must be present
- if no value, provide empty entry e.g. `,,`
- for multiple covariates, separate using `;` 

```
name,application_id,pheno_file,pheno_col,covar_file,covar_col,qcovar_col,method
test,123,test.txt,test_name,bolt_covariates.txt,sex;chip,age,bolt
test2,123,test.txt,test_name,bolt_covariates.txt,sex;chip,age,bolt
```

- Each gwas job is first checked to make sure both phenotype and covariate files exist in correct format and contain specified columns.
- If all good, submission script is created and run as a new slurm job

Create phenotype and covariate files, and place them in RDSF input directory as before.
- see https://github.com/MRCIEU/BiobankPhenotypes/wiki#phenotype-files for details

### Setup and run job submission code on BC4

- Set up [GitHub SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
- Clone repo to any directory on BC4 `git clone git@github.com:MRCIEU/UKBiobankGWAS.git` 
- Move into the directory `cd UKBiobankGWAS`
- Copy the `cp /mnt/storage/private/mrcieu/research/UKBIOBANK_GWAS_Pipeline/scripts/.env ./` file in this repository

#### Single job

Run from within the repository

`sbatch scripts/ukb_gwas.sh`

- by default this will run the first row in `jobs.csv`
- can specify rows using 0 based indexing, so row 3 is 2, e.g. `sbatch scripts/ukb_gwas.sh 2` 

#### Multiple jobs

Run from within this repository

```
for i in {0..1}; do echo $i; sbatch scripts/ukb_gwas.sh $i; done
```

### Summary

Can generate summary files and parse to create counts:

```
sbatch UKBiobankGWAS/scripts/summary.sh
python UKBiobankGWAS/scripts/summary_parser.py
```

### To do

- add args to allow only qc step
- add plink

