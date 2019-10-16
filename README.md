# Genomic-data-crawler

This program retrieves cancer genomic data from a remote web service, and summarizes the results.

## For example, the following request:
```
curl -X POST
"http://www.cbioportal.org/api/molecular-profiles/gbm_tcga_mutations/mutations/fetch?projection=S
UMMARY&pageSize=10000000&pageNumber=0&direction=ASC" -H "accept: application/json" -H
"Content-Type: application/json" -d "{ \"entrezGeneIds\": [ 7157 ], \"sampleListId\":
\"gbm_tcga_cnaseq\"}"
```
