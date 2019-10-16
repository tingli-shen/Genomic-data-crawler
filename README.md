# Genomic-data-crawler

This program retrieves cancer genomic data from a remote web service, and summarizes the results.

### For example, the following request:
```
curl -X POST
"http://www.cbioportal.org/api/molecular-profiles/gbm_tcga_mutations/mutations/fetch?projection=S
UMMARY&pageSize=10000000&pageNumber=0&direction=ASC" -H "accept: application/json" -H
"Content-Type: application/json" -d "{ \"entrezGeneIds\": [ 7157 ], \"sampleListId\":
\"gbm_tcga_cnaseq\"}"
```

will retrieve all mutations for the gene TP53 in Glioblastoma patients assessed as part of The
Cancer Genome Atlas (TCGA) project. Each object contains information about the mutation call for a sample in the specified project.

### Likewise, the following URL:
```
curl -X POST
"http://www.cbioportal.org/api/molecular-profiles/gbm_tcga_gistic/discrete-copy-number/fetch?di
screteCopyNumberEventType=ALL&projection=SUMMARY" -H "accept: application/json" -H
"Content-Type: application/json" -d "{ \"entrezGeneIds\": [ 7157 ], \"sampleListId\":
\"gbm_tcga_cnaseq\"}"
```

will retrieve all copy number alterations for TP53 in the same set
of Glioblastoma patients:
