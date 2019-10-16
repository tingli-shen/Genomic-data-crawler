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

### entrezGeneIds
The Entrez gene id can be obtained from the included file “gene_results.1000.tsv” which
contains the symbol, and numerical id of the top 1000 genes from the NCBI. It is recommended
that this file be loaded first and then the command line tool can map between the text symbol
and numerical identifier.

## Output:
The program summarizes genomic alterations for the same set of TCGA GBM patients
described above.

For example, in the simplest instance, a user would execute your program with a single gene,
and output a simple summary.

`
solution.py TP53
`

will return
```
TP53 is mutated in 29% of all cases.
TP53 is copy number altered in 2% of all cases.
Total % of cases where TP53 is altered by either mutation or copy number alteration: 30% of all
cases.
```

For more than one gene:
`
solution.py TP53 MDM2 MDM4
`

will return 
```
TP53 is altered in 30% of cases. MDM2 is altered in 10% of cases. MDM4 is altered in 10% of
cases.
The gene set is altered in 47% of all cases.
```
