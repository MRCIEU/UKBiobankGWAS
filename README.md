# UKBiobankGWAS
Notes and code for running UK Biobank GWAS at the MRC IEU

### Setup

- When creating a new directory structure, need to .env file containing paths to various things

### Run

Create `jobs.csv` containing information on GWAS jobs

```
name,application_id,pheno_file,pheno_col,covar_file,covar_col,qcovar_col,method
test,123,test.txt,test_name,bolt_covariates.txt,sex;chip,age,bolt
test2,123,test.txt,test_name,bolt_covariates.txt,sex;chip,age,bolt
```

#### Single job

`sbatch ukb_gwas.sh`

#### Multiple jobs

```
for i in {0..1}; do echo $i; sbatch ukb_gwas.sh $i; done
```