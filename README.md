# UKBiobankGWAS
Notes and code for running UK Biobank GWAS at the MRC IEU

### Setup

- When creating a new directory structure for a new user, need to add `.env` file containing paths to ukbiobank directories

### Run

Create `jobs.csv` containing information on GWAS jobs

```
name,application_id,pheno_file,pheno_col,covar_file,covar_col,qcovar_col,method
test,123,test.txt,test_name,bolt_covariates.txt,sex;chip,age,bolt
test2,123,test.txt,test_name,bolt_covariates.txt,sex;chip,age,bolt
```

- Each gwas job is first checked to make sure both phenotype and covariate files exist in correct format and contain specified columns.
- If all good, submission script is created and run as a new slurm job

#### Single job

`sbatch ukb_gwas.sh`

#### Multiple jobs

```
for i in {0..1}; do echo $i; sbatch ukb_gwas.sh $i; done
```