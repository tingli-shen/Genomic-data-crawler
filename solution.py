import requests
import json
import sys

'''
This function will retrieve all mutations and all copy number alterations for genes and return in JSON format
'''
def get_data(gene_id):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    
    params_gistic = (
        ('discreteCopyNumberEventType', 'ALL'),
        ('projection', 'SUMMARY'),
    )
    params_mutations = (
        ('projection', 'SUMMARY'),
        ('pageSize', '10000000'),
        ('pageNumber', '0'),
        ('direction', 'ASC'),
    )
    data = '{ "entrezGeneIds": [ 7157 ], "sampleListId": "gbm_tcga_cnaseq"}'
    data='{ "entrezGeneIds": [ '+gene_id+' ], "sampleListId": "gbm_tcga_cnaseq"}'
    response_gistic = requests.post('http://www.cbioportal.org/api/molecular-profiles/gbm_tcga_gistic/discrete-copy-number/fetch', headers=headers, params=params_gistic, data=data)
    response_mutations = requests.post('http://www.cbioportal.org/api/molecular-profiles/gbm_tcga_mutations/mutations/fetch', headers=headers, params=params_mutations, data=data)
    gistic_content=response_gistic.content.decode('UTF-8')
    mutations_content=response_mutations.content.decode('UTF-8')
    gistic_json = json.loads(gistic_content)
    mutations_json = json.loads(mutations_content)
    return gistic_json,mutations_json

'''
this function will compute % of mutated and copy number altered cases, and 
cases of altered by either mutation or copy number alteration and return them
'''
def get_result(gistic_json,mutations_json, hash_set):
    altered=0 # store number of copy number altered cases
    patients_id=set() # store number of either mutation or copy number alteration cases
    n=len(gistic_json) # all cases
    
    # calculate number of mutated cases
    for case in mutations_json:
        if case['mutationType']:
            hash_set.add(case['sampleId'])
            patients_id.add(case['sampleId'])
    mutated=len(patients_id) # store number of mutated cases

    # calculate number of copy number altered cases
    for case in gistic_json:
        if case['alteration']==-2 or case['alteration']==2:
            altered+=1
            hash_set.add(case['sampleId'])
            patients_id.add(case['sampleId'])
            
    # calculate percentage for cases above 
    altered_rate=altered/n
    mutated_rate=mutated/n
    patients=len(patients_id)/n
    return "{0:.0%}".format(altered_rate),"{0:.0%}".format(mutated_rate),"{0:.0%}".format(patients),hash_set
'''
This function will read gene_results.1000.csv_1.tsv and return gene numerical id: 
Warning: genes that cannot be found will be skipped.
'''
def get_geneId(genes):
    mapping={} 
    # hash map that maps gene symbol to gene numerical id 
    # key: gene symbol 
    # value: gene numerical id
    # for example, TP53 -> 7157
    
    # Read each line in loop
    with open ('gene_results.1000.csv_1.tsv', "r") as fileHandler:

        for line in fileHandler:
            # As each line (except last one) will contain new line character, so strip that
            gene_id,gene=line.strip().split(',')
            mapping[gene]=gene_id
            
    genes_id=[] # genes numerical id
    
    # turn gene symbol into genes numerical id and store in genes_id
    for gene in genes:
        try:
            genes_id.append(mapping[gene])
        except:
            print(gene+' cannot be found')
    return genes_id

'''
This function prints the summary for only one gene
'''
def gene_result(genes):
    hash_set=set() # store all cases that are either mutation or copy number alteration
    genes_id=get_geneId(genes)
    gene_id=genes_id[0]
    # get JSON data
    gistic_json, mutations_json = get_data(gene_id)
    # get statistical summary
    altered_rate , mutated_rate, ans , _= get_result(gistic_json,mutations_json, hash_set)
    # formalize and print the summary
    print('%s is mutated in %s of all cases.' % (genes[0],mutated_rate))
    print('%s is copy number altered in %s of all cases.' % (genes[0],altered_rate))
    print()
    print('Total %% of cases where %s is altered by either mutation or copy number alteration: %s of all cases.' % (genes[0],ans))

'''
This function prints the summary for up to 3 genes
'''
def genes_result(genes):
    genes_id=get_geneId(genes)
    hash_set=set() # store all cases that are either mutation or copy number alteration
    for i,gene_id in enumerate(genes_id):
        # get JSON data
        gistic_json, mutations_json = get_data(gene_id) 
        # get statistical summary
        altered_rate , mutated_rate, ans ,hash_set= get_result(gistic_json,mutations_json, hash_set)
        # formalize and print the summary
        print('%s is altered in %s of cases.' % (genes[i],ans),end=' ')
    patients=len(hash_set)/len(gistic_json)
    patients="{0:.0%}".format(patients)
    print()
    print('The gene set is altered in %s of all cases.' % (patients))
    
'''
Main function
'''
if __name__ == '__main__':
    
    genes=sys.argv[1:] # input arguments
    
    if len(genes)==1: # only one gene is given
        gene_result(genes)
    else: # more than one genes are given
        genes_result(genes)
        
    
    
    