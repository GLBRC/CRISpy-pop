"""
@Program: variantGene.py

@Purpose: Given a gene name, reference, GFF, sample name and VCF file extract strain specific gene sequence.
          User may choose to add a window on both sides of gene if desired.
          
          Gene sequences on the minus strand will be reverse complemented.
          
@Input:  Reference fasta file  - standard fasta format
         GFF file - general feature file format
         Gene Name
         VCF file for a single sample
         sample name         

@Output:  Fasta file, called Gene-Sequences.fa

Steps:  Using gene name retrieve the gene information from the gff file (chr, start, stop, strand )
    Add the window bases to the start & end if required.  Then use samtools and vcftools to 
    create the strain specific gene sequence.  Write results to file.
    
    This is how the strain specific sequence is created.
    
    samtools faidx genome-reference.fa chr12:356155-357468 | bcftools consensus -s 46.2 46.2.vcf.gz > 46.2-HOG1.fa
    
        Where the -s is the strain name in the vcf file.
        
    
I assume the sample name in the VCF has been cleaned up. This means the file path has been 
removed from the sample name.

example:    #CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  Y128

I usually split the vcf file by sample:

 for sample in `bcftools view -h latest_snp_R64-1-1.vcf | grep "^#CHROM" | \
 cut -f10-`; do bcftools view -c1 -Oz -s $sample -o $sample.vcf latest_snp_R64-1-1.vcf ; done

         
@Dependencies: 
        Python 2.7, 
        bgzip    (compress the vcf file)
        BioPython, 
        gffutils ( https://pythonhosted.org/gffutils/contents.html )
        samtools (for indexing reference file)
        tabix    (for indexing the vcf file)
        bcftools
        
        to make gffutils database:
            open a python console and run
            
            import gffutils
            gffutils.create_db('GLBRCY22-3.gff', dbfn='y22-3.db')
      
            then copy the database to the reference directory
            currently databases:  y22-3.db, yeast.db (S288C)
        
@Output: DNA fasta file
@Author: Mike Place
@Date:   11/17/2016
@Last Date modified:  6/26/2017 -- convert to python 2.7 from 3 for crispr project

"""
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
import argparse	
import gffutils
import logging
import os
import re
import subprocess
import sys

import yeast_Gene_name_to_ORF      # must be present, contains gene name mapping to ORF name

# set up logging
logger = logging.getLogger(__name__)

refDir = '../../../lib/reference/'

class VariantGene( object ):
    """
    VariantGene Object, used to manipulate & extract specific gene sequences.
    """
    
    def __init__( self, gene, gff, fasta, win, vcf, sample):
        """
        Set up VariantGene object
        gene  = gene name
        gff   = reference GFF file
        fasta = reference fasta file
        win   = window of bases to add to both sides of gene.
        sample = sample name in vcf to use.
        """
        self.gene   = gene
        self.chrom  = ''
        self.strand = ''
        self.gff    = gff
        self.fasta  = fasta
        self.sample = sample
        self.vcf    = vcf
        self.window = win   
        self.fileHandle = ''
        
        # bgzip vcf file for use with vcftools
        if not self.vcf.endswith('.gz'):
            cmd = ['bgzip', self.vcf]
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
            self.vcf = self.vcf + '.gz'
            # tabix index
            cmd = ['tabix', '-p', 'vcf', self.vcf ]
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        # index the reference file for use with samtools, use full path on scarcity
        #cmd = ['samtools', 'faidx', self.fasta]
        #output = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()        

    def geneExtract( self, loc, chrom, strand ):
        """
        Use samtools faidx reference.fasta chr:start-end to extract gene sequence
        from reference and write it to a file.
        example:
        
            samtools faidx genome-reference.fa chr12:356155-357468 | bcftools consensus -s 46.2 46.2.vcf.gz
            
        """      
        # setup the commands to extract gene sequence
        # if genome is S288C or Y22-3, these are complete genomes 
        # which don't require a vcf file to get gene sequence
        if self.sample == 'S288C':
            sam    = subprocess.Popen([ 'samtools', 'faidx', self.fasta, chrom + ":" + loc], stdout=subprocess.PIPE)   # run samtools
            result = sam.communicate()[0]    
            output = result.decode('utf-8')     # convert byte output to string
        elif self.sample == 'GLBRCY22-3':
            sam    = subprocess.Popen([ 'samtools', 'faidx', self.fasta, chrom + ":" + loc], stdout=subprocess.PIPE)   # run samtools
            result = sam.communicate()[0]    
            output = result.decode('utf-8')     # convert byte output to string   
        elif self.sample == 'ZYMOMONAS':
            sam    = subprocess.Popen([ 'samtools', 'faidx', self.fasta, chrom + ":" + loc], stdout=subprocess.PIPE)   # run samtools
            result = sam.communicate()[0]    
            output = result.decode('utf-8')     # convert byte output to string                          
        else:
            # we pipe samtools to bcftools
            sam    = subprocess.Popen([ 'samtools', 'faidx', self.fasta, chrom + ":" + loc], stdout=subprocess.PIPE)   # run samtools
            bcf    = subprocess.Popen(['bcftools', 'consensus', '-s', self.sample, self.vcf  ],
                                      stdin=sam.stdout, stdout=subprocess.PIPE)  # capture samtools output with STDIN arg
            sam.stdout.close()
            result = bcf.communicate()[0] 
            output = result.decode('utf-8')     # convert byte output to string
            
        seqRegion = output.split('\n')
        seqName   = seqRegion.pop(0)           # get fasta header
        seqName   = re.sub(r'>', '', seqName)
        #construct sequence object
        seqResult = Seq(''.join(seqRegion), IUPAC.unambiguous_dna)
            
        # if sequence is on the minus strand reverse complement it
        if strand == '-':
            seqResult = seqResult.reverse_complement()
    
        # now create a SeqRecord object for writing to file
        seqOut = SeqRecord(seqResult, id = self.sample + ":" + self.gene, name = self.sample, description = seqName )
    
        # write sequence to file
        outFile = self.sample + '-' + self.gene + '.fasta'
        self.fileHandle = outFile
        handle = open(outFile, 'w')
        SeqIO.write(seqOut, handle, 'fasta')
        
    def processGene(self, feature='gene'):
        """
        Get the feature location from GFF file, then call geneExtract().    
        Relies upon gffutils python module to parse gff file and use a gffutils
        gff database.
        
        to make database:
            import gffutils
            gffutils.create_db('GLBRCY22-3.gff', dbfn='y22-3.db')
        
        S288C GFF is used for all yeast strains except GLBRC Y22-3
        which has its own GFF.
        
        default feature to use is gene, only features found in the above GFF
        are supported.        
        """        
        start      = None
        end        = None
        chromosome = None
        strand     = None
        item       = None
        
        if self.sample == 'GLBRCY22-3':
            refdb = refDir + 'y22-3.db'   
        elif self.sample == 'ZYMOMONAS':
            refdb = refDir + 'ZYMOMONAS.db'
        else:
            refdb = refDir + 'yeast.db'
        try:
            tdb    = gffutils.FeatureDB(refdb, keep_order=True)
            if feature != 'gene':
                for row in tdb.children(self.gene, featuretype=feature):       # I assume there is only 1 feature, this maybe wrong
                    item = row
                if item != None:                                               # Get feature information
                    start      = int(item.start) - self.window
                    end        = int(item.stop)  + self.window  
                    chromosome = item.chrom
                    strand     = item.strand
                    # set location for extraction                
                    loc    = str(start) + '-' + str(end)
                    # extract gene sequence
                    self.geneExtract( loc, chromosome, strand)
                    logger.info(VariantGene.printLog(self, chromosome, start, end, strand))
                    self.chrom  = chromosome
                    self.strand = strand
                else:
                    logger.info(VariantGene.printLog(self, 'No Feature found', '', '', 'N/A'))
            else:
                gene   = tdb[self.gene]
                # add window to both ends
                start       = int(gene.start) - self.window  # 
                end         = int(gene.end)   + self.window
                chromosome  = gene.chrom
                strand      = gene.strand
                # set location for extraction                
                loc    = str(start) + '-' + str(end)
                # extract gene sequence
                self.geneExtract( loc, chromosome, strand)
                logger.info(VariantGene.printLog(self, chromosome, start, end, strand))
                self.chrom  = chromosome
                self.strand = strand
                   
        except gffutils.exceptions.FeatureNotFoundError:
            logger.info("Feature Not Found for sample: %s" %(self.sample))
            print ("Feature Not Found for sample: %s" %(self.sample))
                  
    
    def printLog( self, chrom, start, end, strand ):
        """
        Print job information to screen.
        """
        result = "\n\tReference: %s\n" %(self.fasta)
        result += "\tGFF file : %s\n" %(self.gff)
        result += "\tVCF file : %s\n" %(self.vcf)
        result += "\tSample   : %s\n" %(self.sample)
        result += "\tGene name: %s\n" %(self.gene)
        if strand == 'N/A':
            result += "\tposition : N/A\n" 
        else:
            result += "\tposition : %s\n" %( chrom + ':' + str(start) + '-' + str(end) ) 
        result += "\tStrand   : %s\n" %(strand)
        result += "\tWindow   : %s\n" %(self.window)        
        return result                                                   
    
def main():
    """
    Main 
    """     
    cmdparser = argparse.ArgumentParser(description="Retrieve a gene sequence, substitute variant calls to create a strain specific gene sequence.",
                                        usage='%(prog)s -g geneName -gff ref.gff -f S288C.fa  -w 1000 -v sample.vcf' ,prog='variantGene.py'  )  
    cmdparser.add_argument('-f',  '--fasta',  action='store',     dest='FASTA' , help='Reference fasta file', metavar='')
    cmdparser.add_argument('-g',  '--gene',   action='store',     dest='GENE',   help='Specific gene name' , metavar='')
    cmdparser.add_argument('-gff','--gff',    action='store',     dest='GFF',    help='GFF file',            metavar='' )
    cmdparser.add_argument('-s',  '--sample', action='store',     dest='SAMPLE', help='Sample name',         metavar='')
    cmdparser.add_argument('-v',  '--vcf',    action='store',     dest='VCF',    help='Sample VCF file',     metavar='')
    cmdparser.add_argument('-w',  '--window', action='store',     dest='WIN' ,   help='Sequence Window include, default: 0', metavar='')
    cmdparser.add_argument('-i',  '--info',   action='store_true',dest='INFO',   help='Detailed description of program.')
    cmdResults = vars(cmdparser.parse_args())
    cmdparser.parse_args()
    
    # if no args print help
    if len(sys.argv) == 1:
        print ("")
        cmdparser.print_help()
        sys.exit(1)
             
    if cmdResults['INFO']:
        print ("\n  variantGene.py ")
        print ("\n  Purpose: Retrieve a gene sequence, substitute variant calls to create a strain specific gene sequence.")
        print ("\n  Input  : ")
        print ("\t   -g      gene name ")
        print ("\n\t   -gff    GFF file, standard General Feature Format ")
        print ("\n\t   -f      Reference Fasta file")
        print ("\n\t   -s      sample name")
        print ("\n\t   -v      Sample VCF file")
        print ("\n\t   -w      Number of to include on both sides of gene (default: 0 )")
        print ("\n  Output : A single fasta file, strain-geneName.fa, example: GLBRCY22-3-YJL101C.fa ")
        print ("\n  Usage  : variantGene.py -f Y22-3.fa -g GSH1 -gff Y22-3.gff3 -s YPS128 -v vcf/YPS128.vcf.gz")
        print ("\n           This will return a gene sequence plus 200 bases on either end.")
        print ("\n  NOTE:  Genes on the minus strand will be reverse complemented.")
        print ("\n")       
        print ("\tTo see Python Docs for this program:")
        print ("\n\tOpen python console and enter")
        print ("\timport sys")
        print ("\tsys.path.append('/full/path/to/script')")
        print ("\timport variantGene")
        print ("\thelp(variantGene)")
        print ("\n\tSee Mike Place for any problems or suggestions.")
        sys.exit(1)
    
    # check reference fasta file
    if cmdResults['FASTA']:
        fastaFile = cmdResults['FASTA']
        if not os.path.exists(fastaFile):
            print ("\n\tfasta input file does not exist.\n")
            cmdparser.print_help()
            sys.exit(1)
    else:
         print ("\n\tReference Fasta file is required.\n")
         cmdparser.print_help()
         sys.exit(1)
    
    #check GFF file
    if cmdResults['GFF']:
        gffFile = cmdResults['GFF']
        if not os.path.exists(gffFile):
            print ("\n\tGFF file does not exist.\n")
            cmdparser.print_help()
            sys.exit(1)
    else:
        print ("\n\tGFF file is required.\n")
        cmdparser.print_help()
        sys.exit(1)
            
    # check gene 
    if cmdResults['GENE']:
        gene = cmdResults['GENE']
        gene = gene.rstrip()
        gene = gene.upper()
        if not gene.startswith('Y'):
            gene =  yeast_Gene_name_to_ORF.geneToOrf[gene]
    else:
        print ("\n\tGene name is required!.\n")
        cmdparser.print_help()
        sys.exit(1)
        
    #check VCF file
    if cmdResults['VCF']:
        vcfFile = cmdResults['VCF']
        if not os.path.exists(vcfFile):
            print ("\n\tVCF file does not exist.\n")
            cmdparser.print_help()
            sys.exit(1)
    else:
        print ("\n\tVCF file is required.\n")
        cmdparser.print_help()
        sys.exit(1)
      
    #check for sample name
    if cmdResults['SAMPLE']:
        sample = cmdResults['SAMPLE']
    else:
        print ("\n\tSample name is required.\n")
        cmdparser.print_help()
        sys.exit(1)
        
    # check for window size
    if cmdResults['WIN']:
        window = int(cmdResults['WIN'])
    else:
        window = 0

    # get gene sequences and write to file.
    varGene = VariantGene(gene, gffFile, fastaFile, window, vcfFile, sample) 
    varGene.processGene()


if __name__ == "__main__":
    main()
    




