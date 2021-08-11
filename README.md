# UKBiobankGWAS
Notes and code for running UK Biobank GWAS at the MRC IEU

### Setup

- Clone repo to root of user directory `git clone git@github.com:MRCIEU/UKBiobankGWAS.git`
- Copy `.env` file into this 

### Run

Create `jobs.csv` in `input` directory, containing information on GWAS jobs, e.g.

```
name,application_id,pheno_file,pheno_col,covar_file,covar_col,qcovar_col,method
test,123,test.txt,test_name,bolt_covariates.txt,sex;chip,age,bolt
test2,123,test.txt,test_name,bolt_covariates.txt,sex;chip,age,bolt
```

- Each gwas job is first checked to make sure both phenotype and covariate files exist in correct format and contain specified columns.
- If all good, submission script is created and run as a new slurm job

#### Single job

`sbatch UKBiobankGWAS/ukb_gwas.sh`

#### Multiple jobs

```
for i in {0..1}; do echo $i; sbatch UKBiobankGWAS/ukb_gwas.sh $i; done
```

### To do

- add args to allow only qc step