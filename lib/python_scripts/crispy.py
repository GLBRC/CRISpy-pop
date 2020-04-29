"""
@Program: crispy.py

@Purpose: Design CRISPR/cas9 guide RNA for use with S.cerevisiae,
          Saccharomyces paradoxus, Kluuveromyces lactis and Zymomomas Mobilis (ZM4).

          Available S.cerevisiae strains :

          S288C Standard Genome Reference from SGD
          GLBRCY22-3 McILLwain et al. G3  2016 Jun 1;6(6)
          GLBRC (165 yeast strains) see Sardi et al.  PLoS Genet. 2018 Feb; 14(2)
          1011 Genomes, see Schacherer et al.  Nature 2018 April 19;Vol 556

@Input  : Three modes are available.

    1)Search for all guide RNA's for a specific strain, gene and matches to groups
      of other available strains.  Only S. cerevisiae, its direct derivatives are
      supported for this option.  Only guide RNA that match the chromosome and
      are w/in the gene boundaries will be reported.

      crispy.py -g YDR099W -n W303

    Basic Steps:

    1) Extract gene sequence for each strain
    2) Run sgRNA Scorer 2.0
    3) Run Cas-OFFinder to find non-target interactions
       Cas-OFFinder looks for off site targets using S288C genome.
    4) Write results
       crispy-results.txt -- contains final table w/ guide RNA's and score
       crispy.log         -- job log file
       intron.txt         -- shows the presence of introns

    2)Search for offsite targets given a guide RNA sequence. Do not include PAM
      Sequence, use -p or accept the default of NGG.

       Examples:

       A) crispy.py -sg AAAAAGCAATGGAGGAACGG

        output file example:
        chrom   pos     %GC     sgRNA   strand  numMisMatches
        III     314616  47.83   AAAAAGCAATGGAGGAACGGAGG +       0
        VI      14673   47.83   AAAAAGCAATGGAGGAACGGAGG -       0
        XV      1988    47.83   AAAAAGCAATGGAGGAACGGAGG -       0

        B) using an alternate reference

        crispy.py -sg AAAAAGCAATGGAGGAACGG -ref Saccharomyces_paradoxus

        C) using an alternate PAM sequence

        crispy.py -sg ATGCCCCCATCCCAACGGGG -p TTTV

    3)Search for guide RNA's and offsite targets give a sequence and a reference genome.
      If the -ref is omitted S288C will be used as default reference.

        example:crispy.py -seq CAAAAAGACGAG...... -ref Saccharomyces_paradoxus

        output file example:
        GeneID  sgRNA   %Activity       %GC     chrom   pos     strand  NumReferenceMatches
        custom_Minus_1408       TGAAGGTGTCAACCCAGGTGGGG 4.25110900979   60.87   III     127097  -       1
        custom_Minus_1410       ACTGAAGGTGTCAACCCAGGTGG 3.27145506273   56.52   III     127099  -       1
        custom_Minus_581        AACAGTAATGACGCAAGAGGTGG 3.18267612546   47.83   III     126269  -       1
        custom_Minus_880        ATTGCAAGTACAAAAATGCGGGG 2.47706905021   43.48   III     126568  -       1
        ......

parameters:

  -h, --help          Show this help message and exit
  -b, --blast         blastn search  (only for gene specific searches)
  -g, --gene          Specific gene name
  -l, --length        Space length
  -n, --name          Strain Name i.e. W303
  -p, --pam           PAM sequence, default NGG
  -pr , --project     Project designation: GLBRC, 1011GENOMES,ZYMOMONAS, NONE  # FUTURE SUPPORT
  -r, --run           Run id number, default is randomly generated number
  -ref, --reference   Alternate Reference fasta file, supported for guide RNA
                      offsite Target matching and custom sequences
  -seq, --sequence    Sequence, search w/in to find guide RNAs
  -sg, --sgRNA        sgRNA sequence, find offsite targets for sequence.
  -t, --target        Target, default is gene, valid only for S.cerevisiae strains
  -i, --info          Detailed description of program.

@Output: Basic search using Gene and strain returns text table w/ columns:

    GeneID sgRNA %Activity chrom pos MisMatchseq strand numMisMatches numOffSiteMatch NumStrainsHit

@Dependencies:
        BioPython,
        gffutils ( https://pythonhosted.org/gffutils/contents.html )
        samtools (for indexing reference file)
        tabix    (for indexing the vcf file)
        bcftools (https://samtools.github.io/bcftools/)
        sgRNA Scorer (https://crispr.med.harvard.edu/sgRNAScorerV2/)
        Cas-OFFinder (http://www.rgenome.net/cas-offinder/portable)

        Directories with information required by program.

        genes     - contains subdirectories w/ Gene name which have all the strain specific fasta files
        reference - contains GFF and reference strain files
        vcfs      - contain all vcf files for variant strains
        Cas9.High.tab & Cas9.Low.tab - files required by sgRNA Scorer 2.0

Pam Sequences supported:
    S. pyogenes      , NGG    ,3'
    S. aureus        , NNGRRT ,3'
    AsCpf1           , TTTV   ,3'
    N. meningitidis  , NNNNGATT
    S. thermophilus 1, NNAGAAW
    not yet supported
    S. thermophilus 3, NGGNG


@Author: Mike Place
@Date:   6/26/2017
@Last Modified: 3/05/2019

"""
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from Bio.SeqUtils import GC

import argparse
import gffutils
import glob
import logging
import os
import random
import subprocess
import sys

from collections import defaultdict

# project modules
import blastHuman                  # run blastn using guide RNA's vs. Human Genome
import supported_strain_list       # contains dicts that support data for Maria et. al and the 1011 Genome project clade and ecological strain groupings
import target_list                 # set of feature type names from 3rd column of S288C gff file.
import variantGene                 # required to extract strain specific gene sequence
import yeast_Gene_name_to_ORF      # contains gene name mapping to ORF name
import yeastIntrons                # list of all yeast introns
import ZYMOMONAS_genes             # python set of all Zymomonas mobilis genes

##### Read in config from file
path_config = {}

current_dir = os.getcwd() + '/'

with open(current_dir + 'lib/python_scripts/config.conf','r') as configFile:
    for line in configFile:
        path_vals = line.split('\t')
        path_config[path_vals[0]] = path_vals[1].rstrip()

##### Read in supported reference names
refList = set()                                                                # Get List of supported Reference strains
with open('lib/reference/reference_info.conf','r') as f:
    for line in f:
        altRefInfo = line.split()
        refList.add(altRefInfo[0])

tmp_directory = current_dir + 'lib/python_scripts/tmp'
output_directory = current_dir + 'lib/python_scripts/output'
genes_directory = current_dir + 'lib/genes'
if not os.path.exists(tmp_directory):
    os.makedirs(tmp_directory)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
if not os.path.exists(genes_directory):
    os.makedirs(genes_directory)

#####  PATHS used in program
path       = current_dir + path_config['path']                                 # path to script directory
refPath    = current_dir + path_config['refPath']                              # path to yeast reference sequence for cas-offinder, see parseScorer()
altRefPath = current_dir + path_config['altRefPath']                           # path to alternate reference directories
genePath   = current_dir + path_config['genePath']                             # path to gene directory
vcfPath    = current_dir + path_config['vcfPath']                              # path to vcf files
#vcfPath    = '/mnt/crispy/glbrc/'                                             # for Mike Place, testing
#vcfPath1011 = '/mnt/crispy/1011genomes/'                                      # for Mike Place, testing
vcfPath1011 = current_dir + 'lib/vcfs/1011genomes/'
outputDir  = current_dir + path_config['outputDir']
refDir     = current_dir + path_config['referencePath']
binPath    = current_dir + path_config['binPath']
blastDB    = current_dir + 'lib/vcfs/GRCh38.fa'
blastDB    = '/mnt/crispy/blastdb/GRCh38.fa'                                    # Human Genome blastn database

##### sgRNAScore supported PAM sequences & the end they start at 3' or 5'
pamOptions = { 'NGG':'3', 'NNGRRT':'3', 'TTTV':'3', 'NNNNGATT':'3', 'NNAGAAW':'3'}
##### PAM sequence lengths, used to trim custom sgRNA sequences used to search for off site targets
pamLen     = { 'NGG': 3,  'NNGRRT': 6,  'TTTV': 4,  'NNNNGATT':'8', 'NNAGAAW':'7'}

##### default reference files, S288C and GLBRCY22-3
yeastGFF       = current_dir + path_config['yeastGFF']
yeastFasta     = current_dir + path_config['yeastFasta']
Y223GFF        = current_dir + path_config['Y223GFF']
Y223Fasta      = current_dir + path_config['Y223Fasta']
zymomonasGFF   = current_dir + path_config['zymomonasGFF']
zymomonasFasta = current_dir + path_config['zymomonasFasta']

formatter = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')           # Set up formatting for logging
logging.basicConfig(filename = path + 'crispy.log', level=logging.INFO, format=formatter,filemode='w')  # Set up logging
logger = logging.getLogger(path + 'crispy.py')                                 # create logger instance

##### dictionary of alternate reference chromosomes
chroms = { 'yeast': ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
          'XIII', 'XIV', 'XV', 'XVI', 'Mito' ], 'kluuveromyces': ['A','B','C','D','E','F','MT'],
         'zymomonas': ['ZM4', 'pZM32', 'pZM33', 'pZM36', 'pZM39'] }

# list of yeast mitochondrial genes
mitoGenes = {'Q0010','Q0017','Q0032','Q0050','Q0055','Q0060','Q0065','Q0070','Q0045',
             'Q0075','Q0080','Q0085','Q0092','Q0110','Q0115','Q0120','Q0105','Q0130',
             'Q0140','Q0142','Q0143','Q0144','Q0160','Q0182','Q0250','Q0255','Q0275','Q0297'}

# set up global functions
def definition():
    global is_fasta

def is_fasta(filename):
    """
    Check if a file is a fasta file.
    """
    with open(filename, "r") as handle:
        fasta = SeqIO.parse(handle, "fasta")
        return any(fasta)

class Crispy( object ):
    """
    Class creates and runs the sgRNA pipeline.
    """

    def __init__( self, gene, standard_gene, pam, spacerLen, strain, compare, runID, target, project):
        """
        Set up Crispy object
        gene        = Systematic gene name, best for searching GFF file
        std_gene    = standard gene name, most familiar to user
        orientation = pam orientation, 5 = 5', 3 = 3'
        pam         = pam sequence, i.e. NGG
        spLen       = spacer length in base pairs
        strain      = primary strain of interest
        compare     = strain subgroups to use for comparions
        runID       = run identication number, used to provide a unique file name
        target      = feature type used to retrieve coordinates from the GFF
        project     = name of project [ GLBRC, 1011GENOMES, ZYMOMONAS, NONE ]
        """
        self.gene     = gene
        self.orient   = pamOptions[pam]
        self.std_gene = standard_gene
        self.pam      = pam
        self.splen    = spacerLen
        self.strain   = strain
        self.compare  = compare                                                # list of strain subgroups to use for comparions
        self.runID    = str(runID)
        if gene != 'sg' and gene != 'seq':
            self.chrom    = self.getChrom()
            self.start, self.end  = self.getGenePosition()
        else:
            self.chrom = 'N/A'
            self.start = 0
            self.end   = 0
        self.target   = target

        if gene != 'sg' and gene != 'seq':
            self.geneStrand = self.getStrand()
        else:
            self.geneStrand = 'NA'
        self.project  = project

    def getGenePosition(self):
        """
        Set the gene start and stop positions.  Will be used to filter the final
        results of cas-offinder, to limit results to what is present within a gene.

        returns a tuple of the gene start and end

        """
        if self.strain == 'GLBRCY22-3':
            refdb = refDir + 'y22-3.db'
            tdb   = gffutils.FeatureDB(refdb, keep_order=True)
            gene  = tdb[self.gene]
            return (gene.start,gene.end)
        elif self.strain == 'ZYMOMONAS':
            refdb = refDir + 'ZYMOMONAS.db'
            tdb   = gffutils.FeatureDB(refdb, keep_order=True)
            gene  = tdb[self.gene]
            return (gene.start,gene.end)
        else:
            refdb = refDir + 'yeast.db'
            tdb   = gffutils.FeatureDB(refdb, keep_order=True)
            gene  = tdb[self.gene]
            return (gene.start,gene.end)

    def getStrand(self):
        """
        Set the strand for gene, + or -
        """
        if self.strain == 'GLBRCY22-3':
            refdb = refDir + 'y22-3.db'
            try:
                tdb    = gffutils.FeatureDB(refdb, keep_order=True)
                gene   = tdb[self.gene]
                # add window to both ends
                return gene.strand
            except gffutils.exceptions.AttributeStringError:
                logger.info("Strand information not found for sample: %s" %(self.sample))
        if self.strain == 'ZYMOMONAS':
            refdb = refDir + 'ZYMOMONAS.db'
            try:
                tdb    = gffutils.FeatureDB(refdb, keep_order=True)
                gene   = tdb[self.gene]
                # add window to both ends
                return gene.strand
            except gffutils.exceptions.AttributeStringError:
                logger.info("Strand information not found for sample: %s" %(self.sample))
        else:
            refdb = refDir + 'yeast.db'
            try:
                tdb    = gffutils.FeatureDB(refdb, keep_order=True)
                gene   = tdb[self.gene]
                # add window to both ends
                return gene.strand
            except gffutils.exceptions.AttributeStringError:
                logger.info("Strand information not found for sample: %s" %(self.sample))


    def getChrom(self):
        """
        Set the Chromosome number for gene
        """
        if self.strain == 'GLBRCY22-3':
            refdb = refDir + 'y22-3.db'
            try:
                tdb    = gffutils.FeatureDB(refdb, keep_order=True)
                gene   = tdb[self.gene]
                # add window to both ends
                return gene.chrom
            except gffutils.exceptions.AttributeStringError:
                logger.info("Chromosome information not found for sample: %s" %(self.sample))
        elif self.strain == 'ZYMOMONAS':
            refdb = refDir + 'ZYMOMONAS.db'
            try:
                tdb    = gffutils.FeatureDB(refdb, keep_order=True)
                gene   = tdb[self.gene]
                # add window to both ends
                return gene.chrom
            except gffutils.exceptions.AttributeStringError:
                logger.info("Chromosome information not found for sample: %s" %(self.sample))
        else:
            refdb = refDir + 'yeast.db'
            try:
                tdb    = gffutils.FeatureDB(refdb, keep_order=True)
                gene   = tdb[self.gene]
                # add window to both ends
                return gene.chrom
            except gffutils.exceptions.AttributeStringError:
                logger.info("Chromosome information not found for sample: %s" %(self.sample))


    def getVariantGene(self):
        """
        Use module variantgene to extract sequence from reference genome.
        This will create a directory with the gene name and contain all the
        gene fasta files based on the project.
        """
        cwd = os.getcwd()
        os.chdir(genePath)                                                     # move to gene directory

        if not os.path.exists(self.gene):                                      # make specific gene directory if it doesn't exist
            os.mkdir(self.gene)

        os.chdir(self.gene)

        fastaList = glob.glob('*.fasta')                                       # get a list of gene fasta files

        # because the user can specify a feature type, we remove any previous sequences to start from scratch
        for fl in fastaList:
            os.remove(fl)

        # create all the required strain specific gene sequences
        if self.compare:
            dict_to_call = getattr(supported_strain_list, 'supportedStrains')  # dictionary in supported_strain_list to call

            for gp in self.compare:
                for s in dict_to_call[gp]:
                    if s == 'S288C':
                        vcfFile = 'S288C-none.gz'
                        varGene = variantGene.VariantGene(self.gene, yeastGFF, yeastFasta, 0, vcfFile, s)
                    elif s == 'GLBRCY22-3':
                        vcfFile = 'GLBRCY22-3-none.gz'
                        varGene = variantGene.VariantGene(self.gene, Y223GFF, Y223Fasta, 0, vcfFile, s)
                    else:
                        if gp == 'GLBRC':
                            vcfFile =  vcfPath + s + '.vcf.gz'
                            varGene = variantGene.VariantGene(self.gene, yeastGFF, yeastFasta, 0, vcfFile, s)
                        elif gp == '1011GENOMES':
                            vcfFile = vcfPath1011 + s + '.vcf.gz'
                            varGene = variantGene.VariantGene(self.gene, yeastGFF, yeastFasta, 0, vcfFile, s)

                    varGene.processGene(self.target)

        # If no comparison is requested process individually chosen strain
        if self.strain == 'S288C':
            vcfFile = 'S288C-none.gz'
            varGene = variantGene.VariantGene(self.gene, yeastGFF, yeastFasta, 0, vcfFile, self.strain)
        elif self.strain == 'GLBRCY22-3':
            vcfFile = 'GLBRCY22-3-none.gz'
            varGene = variantGene.VariantGene(self.gene, Y223GFF, Y223Fasta, 0, vcfFile, self.strain)
        elif self.strain == 'ZYMOMONAS':
            vcfFile = 'ZYMOMONAS-none.gz'
            varGene = variantGene.VariantGene(self.gene, zymomonasGFF, zymomonasFasta, 0, vcfFile, self.strain)
        else:
            if self.project == 'GLBRC':
                vcfFile =  vcfPath + self.strain + '.vcf.gz'
                varGene = variantGene.VariantGene(self.gene, yeastGFF, yeastFasta, 0, vcfFile, self.strain)
            elif self.project == '1011GENOMES':
                vcfFile = vcfPath1011 + self.strain + '.vcf.gz'
                varGene = variantGene.VariantGene(self.gene, yeastGFF, yeastFasta, 0, vcfFile, self.strain)

        varGene.processGene(self.target)

        os.chdir(cwd)

    def sgRNAScorer(self, strain ):
        """
        Make external call to sgRNA Scorer 2.0 to get a list of guide RNA's.
        This identifies and scores all SpCas9 guide RNA sites.

        python identifyAndScore.py -i eGFP.fasta -o eGFP.SpCas9.tab -p 3 -s 20 -l NGG
        """
        program = path + 'identifyAndScore.py'
        outFile = path + 'tmp/' + self.std_gene + '-' + self.runID + '-sgRNA.txt'

        if strain == 'custom':
            fasta = genePath +'seq/' + 'custom' + '-' + 'seq' + '.fasta'
        else:
            fasta = genePath + self.gene + '/' + strain + '-' + self.gene + '.fasta'

        # set up command line parameters
        cmd = ['python', program, '-i', fasta, '-o', outFile, '-p', self.orient,
               '-l', self.pam, '-s', str(self.splen) ]
        subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()      # call sgRNA Scorer 2.0
        logger.info('crispy.py sgRNAScorer command \n' + " ".join(cmd))

    def parseScorer(self, altRef=''):
        """
        Parse the file returned by sgRNAScorer for input into cas-offinder

        cas-offinder input file format:

        First line - path of chromosomes FASTA files
        Second line - desired pattern including PAM sequence
        Third (or more) line - query sequences with maximum mistmatched numbers (currently set to 0),
        seperated by spaces. (The length of the desired pattern and the query sequences should be the same!)

        An example of input file:

            /var/chromosomes/yeast
            NNNNNNNNNNNNNNNNNNNNNGG
            GGCCGACCTGTCGCTGACGCNNN 0
            CGCCAGCGTCAGCGACAGGTNNN 0
            ACGGCGCCAGCGTCAGCGACNNN 0
            GTCGCTGACGCTGGCGCCGTNNN 0

        to run:
            cas-offinder casinput.txt C out.txt

        """
        # dictionary for sgRNA Scorer results
        sgRNA = {}                                                             # key = sgRNA, value = list of results
        if os.path.exists(path + 'tmp/' + self.std_gene + '-' + self.runID + '-sgRNA.txt'):
            with open(path + 'tmp/' + self.std_gene + '-' + self.runID + '-sgRNA.txt', 'r') as f:
                for seq in f:
                    if seq.startswith('SeqID'):
                        continue
                    row = seq.split()
                    sgRNA[row[1]] = seq.split()                                # get the guide sequence
            f.close()
        else:
            logger.info('parseScorer()' + path + 'tmp/' + self.std_gene + '-' + self.runID + '-sgRNA.txt' + 'input file missing')
            sys.exit(1)

        # create pattern for cas-offinder , example: NNNNNNNNNNNNNNNNNGG
        pattern = "N" * self.splen + self.pam

        with open(path + 'tmp/cas-in-' + self.runID + '.txt','w') as casfile:
            if altRef:
                casfile.write("%s\n" %(altRef))                                # path to reference fasta
            else:
                casfile.write("%s\n" %(refPath))
            casfile.write("%s\n" %(pattern))                                   # match pattern
            for k in sgRNA.keys():
                casfile.write("%s %s\n" %(k,'0'))                              # write sgRNA guide rna's to file

        casfile.close()
        return sgRNA

    def findOffSiteTargets(self):
        """
        Use Cas-OFFinder to evaluate off site target interactions for the guide RNA
        """
        if os.path.exists(path + 'tmp/cas-in-' + self.runID + '.txt'):
            program = 'cas-offinder'
            outFile = path + 'tmp/' + self.std_gene + '-' + self.runID + '-offinder.txt'
            cmd = [program, path + 'tmp/cas-in-' + self.runID + '.txt','C', outFile ]           # set up command line parameters
            subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()  # call cas-offinder
            logger.info("findOffSiteTarget " + " ".join(cmd))
            return outFile
        else:
            logger.info("findOffSiteTarget() cas-in-" + self.runID +  ".txt cas-offinder input file missing")
            sys.exit(1)

    def prepSingleOffSite(self, seq, altRef='' ):
        """
        Prepare request to search for offsite targets given a single guide RNA sequence.
        The input guide RNA sequence should not have the PAM sequence included, as it is
        added below.
        """

        # create pattern for cas-offinder , example: NNNNNNNNNNNNNNNNNGG
        pattern = "N" * self.splen + self.pam

        with open(path + 'tmp/cas-in-' + self.runID + '.txt','w') as casfile:
            if altRef:
                casfile.write("%s\n" %(altRef))                                # path to reference fasta
            else:
                casfile.write("%s\n" %(refPath))                               # path to reference fasta
            casfile.write("%s\n" %(pattern))                                   # match pattern
            casfile.write("%s %s\n" %(seq,'0'))                                # write sgRNA guide rna's to file

        casfile.close()

    def singleWriteResults(self, altRef=''):
        """
        Write the final results for a single guide RNA offsite search.
        Results are sorted by chromosome and position.

        """
        osTarget = path + 'tmp/' + self.std_gene + '-' + self.runID + '-offinder.txt'   # offsite target file
        outFile  = outputDir + '/crispy-results-' + self.runID + '.txt'                 # final results file

        data = defaultdict(dict)

        baseName = os.path.basename(os.path.normpath(altRef))                  # get reference name to use chromosome numbers in output
        if baseName == 'KLUUVEROMYCES_LACTIS':
            refName = 'kluuveromyces'
        elif baseName == 'ZYMOMONAS':
            refName = 'zymomonas'
        else:
            refName = 'yeast'

        if os.path.exists(osTarget):                                           # open cas-offinder results & put in dictionary
            with open(osTarget, 'r') as osf:
                for line in osf:
                    line = line.rstrip()
                    row  = line.split('\t')
                    data[row[1]][row[2]] = row
            osf.close()

            with open(outFile, 'w') as out:
                out.write('chrom\tpos\t%GC\tsgRNA\tstrand\tnumMisMatches\n')   # header
                for c in chroms[refName]:                                      # get the appropriate chromosome list
                    if c in data:
                        sorted_keys = sorted( data[c].keys(), key=lambda y: (float(y))) # sort each chromosomes data by position
                        for k in sorted_keys:
                            gc =  str('{0:3.2f}'.format(GC(Seq(data[c][k][0] + self.pam, IUPAC.unambiguous_dna))))
                            #endPosition = int(data[c][k][2]) + len(data[c][k][4])
                            outRow = data[c][k][1] + '\t' + data[c][k][2] + '\t' + gc + '\t' + data[c][k][3] + '\t' + data[c][k][4] + '\t' + data[c][k][5] + '\n'
                            out.write(outRow)
            out.close()
        else:
            logger.info('singleWriteResults - offSiteTarget file %s not found' %(osTarget))
            with open(outFile, 'w') as out:                                    # In the event offsite match wasn't found
                out.write('No match found\n')
            out.close()

    def checkIntron(self):
        """
        Check for the presence of gene name in the list of yeast introns.
        If present returns string of pairs of start & end positions.
        """
        with open(path + 'tmp/intron-' + self.runID + '.txt', 'w') as out:
            if self.gene in yeastIntrons.introns:
                start = yeastIntrons.introns[self.gene]['start']
                stop  = yeastIntrons.introns[self.gene]['stop']
                chrom = yeastIntrons.introns[self.gene]['chrom']

                out.write('track name=introns description=%s\n' %(self.gene))

                for i in range(len(start)):
                    introns = '%s %s %s' %(chrom, start[i], stop[i])
                    out.write(introns + '\n')
            else:
                introns = 'Not Present'
        out.close()
        logger.info(" checkIntron() %s " %(introns))

    def matchResults(self, sgRNADict, offsiteTargetsFile ):
        """
        Match up sgRNA Scorer data to offsitesTargets data from cas-offinder.

        sgRNADict - dictionary with guide RNA as key
        offsiteTargetsFile - file containing results of cas-offinder

        This will create a total count of all offsite targets,  if a sgRNA hits
        3 times, the count will be 2, as one is the "correct" hit.  sgRNA not on
        the chromosome of interest are also counted.

        """
        count = {}                                                             # count occurances of guide RNA
        match = {}                                                             # dict for matched results
        dat   = defaultdict(dict)                                              # temporary used for sorting
        byPos = []                                                             # list of guide RNA's group by chrom, sorted by position

        if os.path.exists(offsiteTargetsFile):                                 # open cas-offinder results

            with open(offsiteTargetsFile, 'r') as f:                           # Group data by Chromosome
                for item in f:
                    itemlist = item.rstrip().split()
                    dat[itemlist[1]][itemlist[2]] = itemlist
            f.close()
            # Take the grouped data and sort by position
            for key in dat.keys():
                sorted_keys = sorted(dat[key].keys(), key=lambda y:(int(y)))   # sort by position, which is a sub key
                for i in sorted_keys:
                    byPos.append(dat[key][i])
            # Run through all the sorted data, assign sgRNA to a offsite target match
            for line in byPos:
                target = line
                target.append(0)

                if target[0] not in count:
                    count[target[0]] = 0

                if target[0] in sgRNADict:                                     # use sequence as key
                    # find offsitetarget sequence
                    if target[0] not in match and target[1] == self.chrom and (self.start <= int(target[2]) <= self.end ):   # guide RNA of interest, needs to be w/in gene boundary
                        match[target[0]] = sgRNADict[target[0]] + target
                    elif target[0] not in match and target[1] == self.chrom and not (self.start <= int(target[2]) <= self.end ):
                        count[target[0]] += 1
                    elif target[0] not in match and target[1] != self.chrom:   # count items not on the 'correct' chromosome
                        count[target[0]] += 1
                    elif target[0] in match and target[1] == self.chrom:       # count items that hit multiple times
                        count[target[0]] += 1
                    elif target[0] in match and target[1] != self.chrom:
                        count[target[0]] += 1
                else:
                    logger.info('matchResults()  -  Target %s not in sgRNADict' %(target[0]))

            # match counts w/ guide RNA for final table
            for k,v in count.items():
                if k in match:
                    match[k][9] = v
                #else:
                #    print ('matchresults() count & match problem %s %s' %(k,v))
            return match

        else:
            self.writeNoResults(outputDir + '/crispy-results-' + self.runID + '.txt')
            logger.info('offsiteTargets file missing, No offsite targets found:  crispy.matchResults()')
            sys.exit(1)

    def matchSeqResults( self, sgRNADict, offsiteTargetsFile):
        """
        Match up sgRNAScorer data w/ guide RNA generated using input Sequence to offsitesTargets
        and write results to file.

        example sgRNADict entry:
        sgRNADict[target[0]] 'custom_Plus_1053', 'AATTCCTTGACTCAAAAATATGG', '-2.18019098656

        example offsiteTargetsFile 1st 3 lines:
        GGATCTCAAAGAGAACATTAAGG III     314827  GGATCTCAAAGAGAACATTAAGG +       0
        GGATCTCAAAGAGAACATTAAGG XV      1777    GGATCTCAAAGAGAACATTAAGG -       0
        CTTGTGATTACCACAGTAGTTGG III     314235  CTTGTGATTACCACAGTAGTTGG -       0

        results table header:
        GeneID  sgRNA   %Activity  %GC   chrom pos  strand NumReferenceMatches

        """
        refChrom = ''
        stop = False
        count = {}                                                             # count occurances of guide RNA
        match = {}                                                             # dict for matched results
        # We need offsite results
        if os.path.exists(offsiteTargetsFile) and os.path.getsize(offsiteTargetsFile) != 0:
            with open(offsiteTargetsFile, 'r') as f:
                for row in f:
                    target = row.rstrip().split()
                    if stop == False:
                        refChrom = target[1]
                        stop = True

                    if target[0] in sgRNADict:                                 # count each guide RNA
                        if target[0] not in count:
                            count[target[0]] = 1
                        else:
                            count[target[0]] += 1

                        del target[3]
                        del target[4]
                        if target[1] not in match:
                            match[target[1]] = { target[2] : sgRNADict[target[0]] + target }
                        else:
                            match[target[1]][target[2]] = sgRNADict[target[0]] + target
            f.close()

            # find the chromosome list to use, this is to allow the use of alternate reference genomes
            strain = ''
            for key, value in chroms.items():
                if refChrom in value:
                    strain = key

            with open(outputDir + '/crispy-results-' + self.runID + '.txt', 'w') as out:
                out.write('GeneID\tsgRNA\t%Activity\t%GC\tchrom\tpos\tposition_w/in_gene\tstrand\tNumReferenceMatches\n')          # header
                for chrom in chroms[strain]:                                                                   # used to order the results
                    index = 1
                    if chrom in match:
                        sorted_keys = sorted( match[chrom].keys(), key=lambda y: (float(match[chrom][y][2])), reverse=True)
                        for i in sorted_keys:
                            gc =  str('{0:3.2f}'.format(GC(Seq(match[chrom][i][1], IUPAC.unambiguous_dna))))   # calculate GC content and insert
                            match[chrom][i].insert(3, gc)
                            del match[chrom][i][4]                                                             # remove duplicate sequence
                            strandedness = match[chrom][i][0].split('_')       # split sgRNAScorer name: custom_Minus_184
                            genePosition  = strandedness[-1]                   # get position of guide RNA within the gene



                            #if strandedness[1] == 'Plus':                      # make sure the strandedness agrees w/ sgRNAScorer
                            if 'Plus' in strandedness:
                                strand = '+'
                            else:
                                strand = '-'

                            match[chrom][i][6] = strand
                            match[chrom][i].insert(6, genePosition)            # insert the position of guide RNA
                            match[chrom][i][0] = self.strain + "_" + str(index)
                            index += 1

                            line = "\t".join(match[chrom][i]) + '\t' + str(count[match[chrom][i][1]])
                            out.write(line + '\n')
        else:
            self.writeResultsNoOffSiteTargets(sgRNADict)                        # No offsite target results, just write sgRNAScorer result to file
            logger.info('offsiteTargets file missing, No offsite targets found:  crispy.matchSeqResults()')
            sys.exit(1)

    def writeResultsNoOffSiteTargets(self, data ):
        """
        Write results for targeting a custom sequence to a file when no offsite
        target results are found.  This parses and writes the results of running
        sgRNAScorer to a file.

        results table header:

        GeneID  sgRNA  %Activity  %GC  position_w/in_seq  strand
        """
        # sort results by predicted activity
        sorted_keys = sorted( data.keys(), key=lambda y: (float(data[y][2])), reverse=True)

        with open(outputDir + '/crispy-results-' + self.runID + '.txt', 'w') as out:
            # write header
            out.write('GeneID\tsgRNA\t%Activity\t%GC\tchrom\tpos\tposition_w/in_gene\tstrand\tNumReferenceMatches\n')

            index = 1                                                          # use to give a unique number to each row

            for key in sorted_keys:
                strData = [str(i) for i in data[key]]
                info = strData[0].split('_')                                   # split up GeneID field to get name, strand, position
                strData[0] = info[0] + "_" + str(index)                        # add _#, for unique id, example: _3
                index += 1
                gc =  str('{0:3.2f}'.format(GC(Seq(strData[1], IUPAC.unambiguous_dna))))   # calculate %GC content
                strData.append(gc)
                strData.append(info[2])
                #if info[1] == 'Plus':
                if 'Plus' in info:
                    strData.append('+')
                else:
                    strData.append('-')
                # insert 'NA' for chrom and position, append zero for reference match hits, this keeps formatting consistent
                strData.insert(4, 'NA')
                strData.insert(5, 'NA')
                strData.append('0')

                out.write("\t".join(strData) + "\n")
        out.close()

    def strainCount(self, seq, strand ):
        """
        Find the number of perfect matches for seq in the list of strain specific gene fasta files.

        The sgRNA_list_matching_stains.txt is deleted prior to this function call
        every time the program is run.
        """
        if self.project == '1011GENOMES' and self.gene in mitoGenes:           # No Mito info for 1011GENOMES, always return 1 hit
            return 1
        else:
            original_seq = seq                                                 # write original sequence from sgRNAScorer to out list file
            # because gene sequences are always presented as 5' -> 3',
            # the guide sequences need to be rvse complemented in some cases
            if self.geneStrand == '+' and strand == '-':
                seq = Seq(seq).reverse_complement()
            elif self.geneStrand == '-' and strand == '+':
                seq = Seq(seq).reverse_complement()

            count = 0
            strainLst = []
            for gene in os.listdir(genePath + self.gene):                      # go through all files in fasta directory
                if gene.endswith('fasta'):
                    rec = SeqIO.read(genePath + self.gene + '/' + gene, "fasta")
                    if rec.seq.find(seq) > -1:                                 # is there a perfect match?
                        count += 1
                        strainName = gene.split('-')
                        if gene.startswith('GLBRCY22-3'):                      # the dash in Y22-3 causes a spliting problem
                            strainName[0] = 'GLBRCY22-3'
                        strainLst.append(strainName[0])

            if strainLst:
                with open(path + 'tmp/sgRNA_list_matching_strains-' +  self.runID +'.txt','a') as out:
                    out.write( original_seq + ":" + ",".join(strainLst) + "\n")
                out.close()

            return count

    def writeResults(self, data ):
        """
        Write final sgRNA, % activity, offsitetarget information to file.

        results table header:

        GeneID  sgRNA  %Activity  %GC  chrom  pos  MisMatchseq  strand  numMisMatches  numOffSiteMatch  NumStrainsHit

        """
        # sort results by predicted activity
        sorted_keys = sorted( data.keys(), key=lambda y: (float(data[y][2])), reverse=True)

        with open(outputDir + '/crispy-results-' + self.runID + '.txt', 'w') as out:
            # write header
            if self.compare:
                out.write('GeneID\tsgRNA\t%Activity\t%GC\tchrom\tpos\tposition_w/in_gene\tMisMatchseq\tstrand\tnumMisMatches\tnumOffSiteMatch\tNumStrainsHit\n')
            else:
                out.write('GeneID\tsgRNA\t%Activity\t%GC\tchrom\tpos\tposition_w/in_gene\tMisMatchseq\tstrand\tnumMisMatches\tnumOffSiteMatch\n')

            index = 1             # use to give a unique number to each row

            for key in sorted_keys:
                data[key].pop(3)
                strData = [str(i) for i in data[key]]
                strandedness = strData[0].split(':')[1].split('_')             # split sgRNAScorer name: UWOPS03_461_4:YAL030W_Minus_184
                strData[0] = self.strain + ":" + self.gene  + "_" + str(index) # change row name to strainName:GeneName e.g.  W303:YAL030W_1
                index += 1
                genPosition = str(strandedness[-1])                            # the last item should be the position w/in the gene

                if 'Plus' in strandedness:
                #if strandedness[1] == 'Plus':                                  # make sure the strandedness is the same as sgRNAScorer
                    strand = '+'
                else:
                    strand = '-'
                strData[6] = strand
                gc =  str('{0:3.2f}'.format(GC(Seq(strData[1], IUPAC.unambiguous_dna))))   # calculate %GC content
                strData.insert(3, gc)
                strData.insert(6, genPosition)

                if strData[4] == self.chrom:
                        out.write("\t".join(strData))
                        out.write("\n")

        out.close()

    def writeNoResults(self, outFile):
        """
        Write No Results Found to output file
        """
        with open(outFile,'w') as out:
            out.write('No Results Found')
        out.close()


    def setAltRef(self, Ref):
        """
        Set up user provided alternate reference for use.
        Steps:
            1) Check that reference is supported
            2) Return path
        """
        Ref = Ref.upper()
        if Ref in refList:
            newPath  = altRefPath + Ref
        else:
            print( "%s does not appear to be supported." %(Ref))
            logging.error("%s does not appear to be supported." %(Ref))
            sys.exit(1)

        return newPath + '/'

    def __str__(self):
        """
        Format job information and return a string
        """
        result  = "\n  crispy.py job information:\n"
        result += "\tGene (Systematic Name): %s\n" %(self.gene)
        result += "\tGene (Standard Name)  : %s\n" %(self.std_gene)
        result += "\tChromosome            : %s\n" %(self.chrom)
        result += "\tStart-Stop Positions  : %s-%s\n" %(self.start,self.end)
        result += "\tStrand                : %s\n" %(self.geneStrand)
        result += "\tPAM sequence          : %s\n" %(self.pam)
        result += "\tPAM Orientation       : %s\n" %(self.orient)
        result += "\tSpacer Length         : %s\n" %(self.splen)
        result += "\tStrains               : %s\n" %(self.strain)
        result += "\tTarget                : %s\n" %(self.target)
        result += "\tProject               : %s\n" %(self.project)
        return result

    def runBlast(self, blastDB, rnaFile, outPut):
        """
        Call blastHuman to find any guide RNA's that have a 100% identity for the
        full guide RNA length w/ the human genome.  Output is placed in outputDir
        w/ the name crispy-results-(runID)_blast.txt.  The file lists the identifiers
        of guide RNAs that have 100% identity w/ the Human Genome.
        """
        data = blastHuman.blastHuman(blastDB, rnaFile, outPut)
        data.createFasta()
        data.runBlast()
        data.writeBlast()

def main():
    """
    Main
    """
    cmdparser = argparse.ArgumentParser(description="Design CRISPR/cas9 spacers for use with S.cerevisiae.",
                                        usage='%(prog)s -g geneName -p PAM sequence -pr projectName -l spacer length -n strainName' ,
                                        prog='crispy.py'  )
    cmdparser.add_argument('-b', '--blast', action='store_true', dest='BLAST',
                           help='Blastn search guide RNAs against the human genome.')
    cmdparser.add_argument('-g', '--gene',   action='store', dest='GENE',
                           help='Specific gene name' , metavar='')
    cmdparser.add_argument('-l', '--length', action='store', dest='LEN',
                           help='Spacer length', metavar='')
    cmdparser.add_argument('-n', '--name',   action='store', dest='NAME',
                           help='Strain Name, e.g. W303',     metavar='')
    cmdparser.add_argument('-p', '--pam',    action='store', dest='PAM',
                           help='PAM sequence, default NGG', metavar='' )
    cmdparser.add_argument('-pr', '--project', action='store', dest='PROJECT',
                           help='Project: GLBRC or 1011GENOMES, NONE', metavar='')
    cmdparser.add_argument('-r', '--run',    action='store', dest='RUNID', metavar='',
                           help='Run id number')
    cmdparser.add_argument('-ref', '--reference', action='store', dest='REF',
                           metavar='', help='Alternate reference name')
    cmdparser.add_argument('-seq', '--sequence', action='store', dest='SEQUENCE',
                           help='Sequence, search w/in to find guide RNAs', metavar='')
    cmdparser.add_argument('-sg', '--sgRNA', action='store', dest='SGRNA',
                           help='sgRNA sequence, find offsite targets for sequence.', metavar='')
    cmdparser.add_argument('-t', '--target',   action='store', dest='TARGET',
                           help='Target, defaults to Gene, see GFF 3 column for values', metavar='')
    cmdparser.add_argument('-i', '--info',   action='store_true',dest='INFO',
                           help='Detailed description of program.')
    cmdResults = vars(cmdparser.parse_args())
    cmdparser.parse_args()

    # if no args print help
    if len(sys.argv) == 1:
        print ("")
        cmdparser.print_help()
        sys.exit(1)

    if cmdResults['INFO']:
        print( "\n  crispy.py ")
        print( "\n  Purpose: Design CRISPR/cas9 spacers(guide sequences) for use with S.cerevisiae.")
        print( "\n  Input  : ")
        print( "\n\t   -b     blastn search ")
        print( "\n\t   -g     gene name ")
        print( "\n\t   -l     Length of spacer (sgRNA primer)")
        print( "\n\t   -n     Strain name, e.g.: W303")
        print( "\n\t   -p     PAM sequence defaults to NGG for S. pyogenes Cas 9")
        print( "\n\t   -pr    Project name, must be GLBRC, 1011GENOMES or ZYMOMONAS.")
        print( "\n\t   -r     Run ID number.")
        print( "\n\t   -ref   Alternate reference name ")
        print( "\n\t   -seq   Sequence, search w/in this sequence to find guide RNAs.")
        print( "\n\t   -sg    sgRNA sequence, find offsite targets for sequence.")
        print( "\t          Include the PAM sequence, set pam w/ -p or use default NGG")
        print( "\n\t   -t     Target, defaults to Gene, see GFF 3 column for values")
        print( "\n  Output :  Text table w/ columns:")
        print( "\n\t  GeneID       - gene name")
        print( "\n\t  sgRNA        - guide sequence")
        print( "\n\t  Activity     - predicted guide RNA activity, from sgRNA Scorer 2.0")
        print( "\n\t  chrom        - chromosome")
        print( "\n\t  pos          - base pair position on chromosome")
        print( "\n\t  MisMatchseq  - lowercase letter denote mismatches")
        print( "\n\t  Strand       - plus or minus")
        print( "\n\t  numMisMatches- number of mismatches in guide sequence")
        print( "\n\t  numOffSiteMatch  - Number of targets other than primary target")
        print( "\n\t  NumStrainsHit    - Total number of supported strains w/ a perfect match to the guide sequence")
        print( "\n  Usage  : crispy.py -g geneName -p PAM sequence -l spacer length -n strainName -t target(cds)")
        print( "\n  *** NOTE: Off target search is based on the S288C genome. *** ")
        print( "      Number of mismatches for off target searches set to 0.")
        print( "\n\tTo see Python Docs for this program:")
        print( "\n\tOpen python console and enter")
        print( "\timport sys")
        print( "\tsys.path.append('/full/path/to/script')")
        print( "\timport crispy")
        print( "\thelp(crispy)")
        print( "\n\tSee Mike Place for any problems or suggestions.")
        sys.exit(1)

    logger.info('crispy.py running')

    # check for PAM sequence support
    if cmdResults['PAM']:
        pam = cmdResults['PAM'].rstrip().upper()
        if pam not in pamOptions:
            print ("\n\tPAM sequence %s not supported.\n" %(pam))
            logging.error("PAM sequence %s not supported." %(pam))
            cmdparser.print_help()
            sys.exit(1)
    else:
        logger.info('PAM sequence NGG (default).')
        pam = 'NGG'

    # check for Project selection
    if cmdResults['PROJECT']:
        project = cmdResults['PROJECT'].rstrip().upper()
        if project not in ['GLBRC', '1011GENOMES', 'ZYMOMONAS', 'NONE']:
            print( "\n\tProject name not supported: %s" %(project))
            print( "\tProject must be one of the following: GLBRC,1011GENOMES, ZYMOMONAS, NONE\n")
            logging.error("Project name %s not supported." %(project))
            cmdparser.print_help()
            sys.exit(1)
    else:                                                                      # default to GLBRC project
        project = 'GLBRC'

    # Get primary strain name to extract gene seqeuence from and generate guide RNA sequences
    strain = ''
    if cmdResults['NAME']:
        strain = cmdResults['NAME'].rstrip().upper()
        if strain == 'ZYMOMONAS':
            project = 'ZYMOMONAS'

    # set compare parameter using project as guide
    if project == 'GLBRC':
        compare = ['GLBRC']
    elif project == '1011GENOMES':
        compare = ['1011GENOMES']
    elif project == 'ZYMOMONAS' or cmdResults['NAME'].upper() == 'ZYMOMONAS':
        compare = []                                                           # if ZYMOMONAS , nothing to compare to, set empty list
    elif project == 'NONE':
        compare = []

    # check for run id number, if not present assign a random number
    if cmdResults['RUNID']:
        runID = cmdResults['RUNID']
    else:
        runID = random.randint(1,100000)

    #check Length of spacer sequence for extremes
    if cmdResults['LEN']:
        spacerLen = int(cmdResults['LEN'])
        if spacerLen < 14:
            print( "\n\tERROR: Spacer length less than 14, insufficient length")
            logger.error('Spacer length less than 14, insufficient length')
            sys.exit(1)
        if spacerLen > 100:
            print ("\n\tERROR: Spacer length greater than 100, try a shorter length")
            logger.error('Spacer length greater than 100, try a shorter length')
            sys.exit(1)
    else:
        spacerLen = 20

    # USER REQUESTS OFFSITE TARGET SEARCH ONLY
    # AAAAAGCAATGGAGGAACGGAGG = test, should hit 3x, 2 offsite hits in S288C
    if cmdResults['SGRNA']:
        spacerLen = len(cmdResults['SGRNA'])                                   # get length including PAM Seq
        trim = spacerLen - pamLen[pam]                                         # get length minus PAM Seq
        sgRNA = cmdResults['SGRNA'][0:trim]                                    # trim PAM seq from input sequence
        spacerLen = len(sgRNA)

        # create crispy object
        guide = Crispy( 'sg', 'sg', pam, spacerLen, 'None', compare, runID, 'gene', project )
        logger.info(guide.__str__())
        #IF USER PROVIDED AN ALTERNATE REFERENCE USE IT
        if cmdResults['REF']:
            altRef = guide.setAltRef(cmdResults['REF'])
            guide.prepSingleOffSite(sgRNA, altRef)
            guide.findOffSiteTargets()
            guide.singleWriteResults(altRef)
        else:
            guide.prepSingleOffSite(sgRNA)
            guide.findOffSiteTargets()
            guide.singleWriteResults()

    #user inputs sequence to search for CRISPR guide RNA's
    elif cmdResults['SEQUENCE']:
        sequence = cmdResults['SEQUENCE']

        guide = Crispy( 'seq', 'seq', pam, spacerLen, 'custom', False, runID, 'gene', project)  # create sequence crispy object
        logger.info(guide.__str__())
        customSeq = SeqRecord(Seq(sequence), id='custom', description=':user provided sequence')

        if not os.path.exists(genePath + 'seq/'):                              # make gene directory if it doesn't exist
            os.mkdir(genePath + 'seq')

        seqFile = genePath +'seq/' + 'custom' + '-' + 'seq' + '.fasta'         # write input seq to fasta file
        SeqIO.write(customSeq, seqFile, 'fasta')
        guide.sgRNAScorer( 'custom')                                           # search for guide RNA's

        # USER PROVIDED REFERENCE USE IT
        if cmdResults['REF'] and cmdResults['REF'].upper() != 'NONE':
            altRef = guide.setAltRef(cmdResults['REF'])
            sgRnaDict      = guide.parseScorer(altRef)                         # dictionary of sgRNA results, key= guide sequence
            offSiteTargets = guide.findOffSiteTargets()
        # assume no reference, no offsite checking
        else:
            sgRnaDict      = guide.parseScorer()                               # dictionary of sgRNA results, key= guide sequence
            offSiteTargets = path + 'tmp/' + 'seq' + '-' + str(runID) + '-offinder.txt'
            cmd = ['touch', offSiteTargets ]
            subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()

        results = guide.matchSeqResults(sgRnaDict, offSiteTargets)

    else:
        # check gene input
        if cmdResults['GENE']:
            orig_gene = cmdResults['GENE']
            orig_gene = orig_gene.rstrip().upper()

            if strain == 'GLBRCY22-3':                                         # handle GLBRCY22-3 gene names separately
                if orig_gene in yeast_Gene_name_to_ORF.y223_geneToOrf:
                    gene =  yeast_Gene_name_to_ORF.y223_geneToOrf[orig_gene]   # gene = systematic name, best for searching GFF
                elif orig_gene in yeast_Gene_name_to_ORF.y223_orfToGene:
                    gene = orig_gene
                    orig_gene = yeast_Gene_name_to_ORF.y223_orfToGene[gene]
                else:
                    print ("%s Gene not found in Y22-3 GFF, check the name" %(orig_gene))     # orig_gene = standard name, most familiar to users
                    logging.error("%s Gene not found in Y22-3 GFF, check the name" %(orig_gene))
                    sys.exit(1)
            elif strain == 'ZYMOMONAS':
                orig_gene = cmdResults['GENE']
                if orig_gene in ZYMOMONAS_genes.zymo_genes:
                    gene = orig_gene
                else:
                    print ("%s Gene not found in Zymomonas mobilis GFF, check the name" %(orig_gene))     # orig_gene = standard name, most familiar to users
                    logging.error("%s Gene not found in Zymomonas mobilis GFF, check the name" %(orig_gene))
                    sys.exit(1)
            else:
                # strain is S.cerevisiae but not GLBRCY22-3
                if orig_gene in yeast_Gene_name_to_ORF.sc_geneToOrf:
                    gene =  yeast_Gene_name_to_ORF.sc_geneToOrf[orig_gene]     # gene = systematic name, best for searching GFF
                elif orig_gene in yeast_Gene_name_to_ORF.sc_orfToGene:
                    gene = orig_gene
                    orig_gene = yeast_Gene_name_to_ORF.sc_orfToGene[gene]
                else:
                    print ("%s Gene not found, check the name" %(orig_gene))     # orig_gene = standard name, most familiar to users
                    logging.error("%s Gene not found, check the name" %(orig_gene))
                    sys.exit(1)

        else:
            print("\n\tGene name is required!.\n")
            cmdparser.print_help()
            sys.exit(1)

        # verify the target feature type exists, if it does not exist run using gene as target
        target = None
        if cmdResults['TARGET']:
            target = cmdResults['TARGET']
            if strain == 'ZYMOMONAS':
                target = 'gene'
            elif strain == 'GLBRCY22-3':
                if target not in target_list.y223_targets:
                    print ('target %s not a supported feature for GLBRCY22-3.' % target)
                    logger.error('target %s not a supported feature for GLBRCY22-3.' % target)
                    target = 'gene'
            else:
                if target not in target_list.s288c_targets:
                    print ('target %s not a supported feature.' % target)
                    logger.error('target %s not a supported feature.' % target)
                    target = 'gene'
        else:
            target = 'gene'

        # currently only supports one strain
        if strain:
            if target:
                guide = Crispy(gene, orig_gene, pam, spacerLen, strain, compare, runID, target, project) # create crispy object
            else:
                guide = Crispy(gene, orig_gene, pam, spacerLen, strain, compare, runID, target, project) # create crispy object
            logger.info(guide.__str__())                                       # write job information to log file
            guide.getVariantGene()                                             # extract strain specific gene sequence
            guide.sgRNAScorer(strain)                                            # call sgRNA Scorer 2.0
            if strain == 'GLBRCY22-3':
                altRef = guide.setAltRef('Y22-3')
                sgRnaDict      = guide.parseScorer(altRef)                     # dictionary of sgRNA results, key= guide sequence
            elif strain == 'ZYMOMONAS':
                altRef = guide.setAltRef('ZYMOMONAS')
                sgRnaDict      = guide.parseScorer(altRef)                     # dictionary of sgRNA results, key= guide sequence
            else:
                sgRnaDict      = guide.parseScorer()                           # dictionary of sgRNA results, key= guide sequence

            offSiteTargets = guide.findOffSiteTargets()

            results = guide.matchResults(sgRnaDict, offSiteTargets)

        # count strains that have a match to the GLBRC
        if guide.compare:
            for k,v in results.items():
                cnt = guide.strainCount(k, v[7])
                results[k].append(cnt)

        # match up sgRNA Scorer to off site target info and write file
        guide.writeResults(results)                                            # write table to file
        guide.checkIntron()                                                    # check for presence of intron

        # run blastn search if requested
        if cmdResults['BLAST']:
            rnaFile = outputDir + '/crispy-results-' + guide.runID + '.txt'
            outPut  = outputDir + '/crispy-results-' + guide.runID + '_blast.txt'
            guide.runBlast(blastDB, rnaFile, outPut )

    logger.info('Program Complete!')

if __name__ == "__main__":
    definition()
    main()

