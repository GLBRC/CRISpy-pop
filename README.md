# Crispy Public

CRISpy-pop is a web application that generates and filters guide RNA sequences for CRISPR/Cas9 genome editing. This tool focuses on generating guide RNA sequences for Yeast and Bacterial species used in bioenergy research. This tool supports a 1011 genome Saccharomyces cerevisiae strain set as well as a 167 strain set of S. cerevisiae isolates

This application is currently hosted by the Great Lakes Bioenergy Research Center here:
https://crispy-pop.glbrc.org/

The search by gene feature requires ~7 GB of reference data.  If you would like access to this data, please contact us at https://github.com/orgs/GLBRC/teams/glbrc_github_developers


## app-specific prereqs  

ruby / rails  
sqlite3  
yarn  
python3  
pip  

### python/pip prereqs  
biopython  
gffutils  
numpy  
scipy  
scikit-learn  

### open source tools  
samtools (1.5)  
bcftools (1.5)  
intel opencl runtime (16.1.1)  
cas-offinder (2.4)  
ncbi-blast (2.7.1+) -- for: blastn  

### environment variables:  
export RAILS_ENV=production  
export crispy_DATABASE=crispy  
export crispy_USERNAME=crispy  
export crispy_PASSWORD=[in-keepass]  


### Setup Instructions  
1. install all dependencies  
2. clone repository (cd to app directory)  
3. create settings.yml and database.yml files in config/ based on the sample files threre  
4. bundle install  
5. yarn install  
6. rails db:migrate  
7. rails db:seed  
8. rails server  


### CRISpy-pop utilizes the following open-source software tools:  

## Cas-OFFinder  

Bae S., Park J. & Kim J.-S. Cas-OFFinder: A fast and versatile algorithm that searches for potential off-target sites of Cas9 RNA-guided endonucleases. Bioinformatics 30, 1473-1475 (2014).

## sgRNA Scorer
Chari R, Yeo N, Chavez A, Church GM (2017). sgRNA Scorer 2.0 – a species independent model to predict CRISPR/Cas9 activity. ACS Synthetic Biology. Accepted.

## CasFinder

Aach J, Mali P, Church GM (2014). CasFinder: Flexible algorithm for identifying specific Cas9 targets in genomes. BioRxiv.

## Contact Info

Please contact us at https://github.com/orgs/GLBRC/teams/glbrc_github_developers
with bugs or feature requests
