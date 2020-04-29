Directions for adding a new reference genome

Need these files:

 1) Reference genome fasta file
 2) Sam indexed Reference genome fasta file
 3) GFF file
 4) Need to create a gff database for gffutils
 
 in python :
 
 import gffutils
 
   gffutils.create_db('GLBRCY22-3.gff', dbfn='y22-3.db')
   
 5) gene name bed file
 6) intron bed file if appropriate
 7) make a all capital letter directory under lib/reference
 8) add information to reference_info.conf


In crispy.py  check the following:

1) Might need a new_Reference_gene.py file
2) Add default reference files see ~line 210
3) Check chroms dictionary
4) Check the following functions:
    getGenePosition()
    getStrand()
    getChrom()
    getVariantGene()
    singleWriteResults()
5) command line variable parsing
    cmdResults['NAME']

In variantGene.py check the following:
    geneExtract()
    processGene()


