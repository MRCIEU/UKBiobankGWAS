# UKBiobankGWAS
Notes and code for running UK Biobank GWAS at the MRC IEU



### Create input files on RDSF

Create `jobs.csv` in `input` directory, containing information on GWAS jobs, e.g.

```
name,application_id,pheno_file,pheno_col,covar_file,covar_col,qcovar_col,method
test,123,test.txt,test_name,bolt_covariates.txt,sex;chip,age,bolt
test2,123,test.txt,test_name,bolt_covariates.txt,sex;chip,age,bolt
```

- Each gwas job is first checked to make sure both phenotype and covariate files exist in correct format and contain specified columns.
- If all good, submission script is created and run as a new slurm job

Create phenotype and covariate files, and place them in RDSF input directory.
- see https://github.com/MRCIEU/BiobankPhenotypes/wiki#phenotype-files for details

### Setup code on BC4

- Clone repo to any directory on BC4
- `git clone git@github.com:MRCIEU/UKBiobankGWAS.git`
- Create `.env` file in this repository

#### Single job

`sbatch UKBiobankGWAS/scripts/ukb_gwas.sh`

#### Multiple jobs

```
for i in {0..1}; do echo $i; sbatch UKBiobankGWAS/scripts/ukb_gwas.sh $i; done
```

### Summary

Can generate summary files and parse to create counts:

```
sbatch UKBiobankGWAS/scripts/summary.sh
python UKBiobankGWAS/scripts/summary_parser.py
```

### To do

- add args to allow only qc step
