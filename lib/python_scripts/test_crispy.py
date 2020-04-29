#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@Program: test_crispy.py
@Purpose: Run unit tests for crispy.py.

@Usage  : run from top level of directory.
    python lib/python_scripts/test_crispy.py -v
    
    to run a single test:
        
    python lib/python_scripts/test_crispy.py -v Test_crispy.test_zymomonas_offsite_targets_only

@tests  :
    
  1 general case
  2 general case S288C Mito
  3 general case Y223 plus strand
  4 general case Y223 minus strand
  5 guide RNA
  6 guide RNA change reference
  7 test sequence search
  8 general case change target
  9 general case PAM TTTV
 10 guide RNA change reference paradoxus
 11 general case PAM NNGRRT
 12 PAM TTTV Many ost
 13 sequence search noRef
 14 general case Y223 strain specific gene
 15 general case Y223 strain specific gene minus strand
 16 offsite target checking for zymomonas
 17 general case search for guide RNA using zymomonas
 18 general case zymomonas      
 19 test general case 1011GENOMES
 20 test general case 1011GENOMES Mito
 21 test_blast 
    
@author: Mike Place

@Date:Tue Aug 15 16:20:25 2017
"""
import glob
import hashlib
import os
import unittest
from subprocess import Popen, PIPE

##### Read in config from file
path_config = {}

current_dir = os.getcwd() + '/'

with open(current_dir + 'lib/python_scripts/config.conf','r') as configFile:
    for line in configFile:
        path_vals = line.rstrip().split('\t')
        path_config[path_vals[0]] = path_vals[1].rstrip()
        
outputDir = current_dir + path_config['outputDir'] + '/'
testPath  = current_dir + path_config['testPath']  + '/'
tmpPath   = current_dir + path_config['tmpPath']   + '/'
program   = current_dir + 'lib/python_scripts/crispy.py'
blast     = current_dir + 'lib/python_scripts/blastHuman.py'                   # blastn script
blastDB   = '/mnt/crispy/blastdb/GRCh38.fa'                                    # path to Human Genome blast database
vcfPath   = current_dir + path_config['vcfPath']                               # path to vcf files
#vcfPath    = '/mnt/crispy/glbrc/'                                             # for Mike Place, testing

def hashFILE(ftoh):
    """
    Return the hashlib.md5 value for a file.
    Used to check for file similarity.
    """
    filehash = hashlib.new("md5")
    with open(ftoh,'rb') as f:
        filehash.update(f.read())
    return filehash.hexdigest()

class Test_crispy(unittest.TestCase):        
       
    def test_general_case(self):
        """
        Test the general use case, where the user enters a gene, strain name and
        asks for a comparison across all available strains.
        
        crispy.py -g hog1 -n W303 
        """
        # run crispy to generate a new results file
        cmd = ['python', program, '-g', 'hog1', '-n', 'W303' ,'-r', '1', '-pr', 'GLBRC']
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-1*')                   # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        #md5 = hashlib.md5(open(result,'rb').read()).hexdigest()               # generate the md5sum
        md5 = hashFILE(result)

        # get original results file for comparison
        testlst = glob.glob(testPath + 'hog1_standard/crispy-results-1.txt')        # These results have been validated previously
        #check_md5 = hashlib.md5(open(testlst[0],'rb').read()).hexdigest()
        check_md5 = hashFILE(testlst[0])

        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))
        
    def test_general_case_S288C_Mito(self):
        """
        Test the general use case, user enters a Mitochondrial gene, strain 
        name and asks for a comparison across all available strains. 
        
        The gene here is located on the plus strand.
        
        crispy.py  -g Q0065 -p NGG -l 20 -n BC187 -t gene -r 2
        
        This gene has 3 introns which are reported in the intron file.        
        """
        # run crispy to generate a new results file
        cmd = ['python', program, '-g', 'Q0065', '-n', 'BC187', '-t', 
               'gene', '-r', '2', '-p', 'NGG', '-l', '20' , '-pr', 'GLBRC']
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-2.txt*')                   # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'mito_Q0065_standard_S288C/crispy-results-2*')        # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))
        
        intronlst = glob.glob( tmpPath + 'intron-*')
        result    = max(intronlst, key=os.path.getctime)
        md5 = hashFILE(result)
        
        # get original intron file for comparison
        testlst = glob.glob(testPath + 'mito_Q0065_standard_S288C/intron-2*')   # These results have been validated previously
        check_md5 = hashFILE(testlst[0])        

        self.assertEqual(check_md5, md5, "md5 sum check fails, intron files differ : %s :  %s" %(testlst[0],result))
        
    def test_general_case_Y223_plus_strand(self):
        """
        Test the general use case, where the user enters a gene, strain name and
        asks for a comparison across all available strains and specifying GLBRCY22-3
        as strain of interest.  GLBRCY22-3 has it's own variants and separate GFF
        
        crispy.py  -g gre3 -p NGG -l 20 -n GLBRCY22-3 -t gene -r 3
        """
        # run crispy to generate a new results file
        cmd = ['python', program, '-g', 'gre3', '-n', 'GLBRCY22-3', '-t', 
               'gene', '-r', '3', '-p', 'NGG', '-l', '20' ]
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-3*')                   # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'gre3_standard_y223/crispy-results*')   # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))

    def test_general_case_Y223_minus_strand(self):
        """
        Test the general use case, where the user enters a gene, strain name and
        asks for a comparison across all available strains and specifying GLBRCY22-3
        as strain of interest.  GLBRCY22-3 has it's own variants and separate GFF
        
        The gene here is located on the minus strand.
        
        crispy.py  -g sec20 -p NGG -l 20 -n GLBRCY22-3 -t gene -r 4
        
        """
        # run crispy to generate a new results file
        cmd = ['python', program, '-g', 'sec20', '-n', 'GLBRCY22-3', '-t', 
               'gene', '-r', '4', '-p', 'NGG', '-l', '20', '-pr', 'GLBRC']
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-4*')                   # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'sec20_standard_y223/crispy-results*')  # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))
        
    def test_guide_RNA(self):
        """
        Test when user selects option of submitting a guide RNA sequence
        to find offsite targets in S288C.
        
        crispy.py  -sg AAAAAGCAATGGAGGAACGGNNN -r 5
        
        """
        cmd = ['python', program, '-sg', 'AAAAAGCAATGGAGGAACGGNNN', '-r', '5'  ]
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-5*')                   # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'S.cerevisiae_sg_test/crispy-results*') # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))
    
    def test_guide_RNA_change_reference(self):
        """
        Test when user selects option of submitting a guide RNA sequence
        to find offsite targets in kluuveromyces lactis
        
        crispy.py  -sg ACACCCCGCTCCTCCCTTTCNNN -ref kluuveromyces_lactis -r 6
        """
        cmd = ['python', program, '-sg', 'ACACCCCGCTCCTCCCTTTCNNN', '-ref', 'kluuveromyces_lactis', '-r', '6']
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-6*')                   # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'k.lactis_sg_test/crispy-results*')     # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))
    
    def test_sequence_search(self):
        """
        Test the -seq parameter, this runs a search of an input sequence for 
        guide RNA's and looks for offsite targets of in S288C.
        
        crispy.py -seq ATGTCGTCATCTACTCCCTTTGACCCTTATGCTCTATCCGAGCACGATGAAGAACG
        ACCCCAGAATGTACAGTCTAAGTCAAGGACTGCGGAACTACAAGCTGTAAGTACAGAAAGCCACAGAGTAC
        CATCTAGGAAATTAACATTATACTAACTTTCTACATCGTTGATACTTATGCGTATACATTCATATACGTTC
        TTCGTGTTTATTTTTAGGAAATTGATGATACCGTGGGAATAATGAGAGATAACATAAATAAAGTAGCAGAA
        AGAGGTGAAAGATTAACGTCCATTGAAGATAAAGCCGATAACCTAGCGGTCTCAGCCCAAGGCTTTAAGAG
        GGGTGCCAATAGGGTCAGAAAAGCCATGTGGTACAAGGATCTAAAAATGAAGATGTGTCTGGCTTTAGTAA
        TCATCATATTGCTTGTTGTAATCATCGTCCCCATTGCTGTTCACTTTAGTCGATAG -p NGG
        
        """
        snc1 = ('ATGTCGTCATCTACTCCCTTTGACCCTTATGCTCTATCCGAGCACGATGAAGAACG' 
        'ACCCCAGAATGTACAGTCTAAGTCAAGGACTGCGGAACTACAAGCTGTAAGTACAGAAAGCCACAGAGTAC' 
        'CATCTAGGAAATTAACATTATACTAACTTTCTACATCGTTGATACTTATGCGTATACATTCATATACGTTC' 
        'TTCGTGTTTATTTTTAGGAAATTGATGATACCGTGGGAATAATGAGAGATAACATAAATAAAGTAGCAGAA' 
        'AGAGGTGAAAGATTAACGTCCATTGAAGATAAAGCCGATAACCTAGCGGTCTCAGCCCAAGGCTTTAAGAG' 
        'GGGTGCCAATAGGGTCAGAAAAGCCATGTGGTACAAGGATCTAAAAATGAAGATGTGTCTGGCTTTAGTAA' 
        'TCATCATATTGCTTGTTGTAATCATCGTCCCCATTGCTGTTCACTTTAGTCGATAG')
        
        cmd = ['python', program, '-seq', snc1 , '-p', 'NGG', '-r', '7' , '-ref', 'S288C' ]
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-7*')                   # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'snc1_sequence_test/crispy-results-7*')   # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))
      
    def test_general_case_change_target(self):
        """
        Test the general use case, where the user enters a gene name, strain name and
        asks for a comparison across all available strains while changing the 
        feature target.
       
        crispy.py -g RPL32 -n W303 -t five_prime_UTR_intron
        
        """
        cmd = ['python', program, '-g', 'RPL32' , '-n', 'W303', '-t', 
               'five_prime_UTR_intron', '-r', '8','-pr', 'GLBRC']
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-8*')                   # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'target_change/crispy-results*')        # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))
        
    def test_general_case_PAM_TTTV(self):
        """
        Test the general use case, where the user enters a gene name, strain 
        name w/ a comparison across all available strains for an alternate 
        PAM sequence.
        
        crispy.py -g hog1 -n S288C -p TTTV 
        """
        cmd = ['python', program, '-g', 'hog1', '-n', 'S288C', '-p', 'TTTV', '-r', '9',
               '-pr', 'GLBRC']
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-9*')                   # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'hog1_standard_TTTV/crispy-results*')   # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))
    
    def test_guide_RNA_change_reference_paradoxus(self):
        """
        Test when user selects option of submitting a guide RNA sequence
        to find offsite targets in Saccharomyces_paradoxus
        
        crispy.py  -sg TCTCGCTGTCACTCCTTACCNNN -ref Saccharomyces_paradoxus
        """
        cmd = ['python', program, '-sg', 'TCTCGCTGTCACTCCTTACCNNN', '-ref', 'Saccharomyces_paradoxus', '-r', '10']
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-10*')                  # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'S.paradoxus_sg_test/crispy-results*')  # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))    

    def test_general_case_PAM_NNGRRT(self):
        """
        Test the general use case, where the user enters a gene, strain name, 
        an alternate PAM sequence (NNGRRT) and asks for a comparison across 
        all available strains. Default reference of S288C.

        crispy.py -g YAL030W -p NNGRRT -n UWOPS03_461_4 -t gene

        """
       # run crispy to generate a new results file
        cmd = ['python', program, '-g', 'YAL030W', '-n', 'UWOPS03_461_4' ,'-r', '11', 
               '-t', 'gene', '-p', 'NNGRRT','-pr', 'GLBRC']
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-11*')                  # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'YAL030W_PAM_NNGRRT/crispy-results*')   # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))                
    
    def test_PAM_TTTV_Many_ost(self):
        """
        Test the general use case, where the user enters a gene, strain name, 
        an alternate PAM sequence (TTTV) and asks for a comparison across 
        all available strains. Default reference of S288C.  Here cas-offinder
        finds many offsite targets on the same and different chromosomes.
        This is a test of the filtering, return guide RNA that fall w/in the 
        gene boundaries, and count all offsite hits.

        crispy.py -g flo1 -n YB908 -t gene -p TTTV -l 20 -ref S288C

        """
       # run crispy to generate a new results file
        cmd = ['python', program, '-g', 'flo1', '-n', 'YB908', '-p' , 'TTTV', '-l',
               '20', '-ref', 'S288C', '-t', 'gene', '-r', '12','-pr', 'GLBRC' ]
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-12*')                  # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'flo1_standard/crispy-results*')   # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))           
    
    def test_sequence_search_noRef(self):
        """
        Test the -seq parameter, this runs a search of an input sequence for 
        guide RNA's WITHOUT searching for offsite targets.
        
        crispy.py -seq ATGTCGTCATCTACTCCCTTTGACCCTTATGCTCTATCCGAGCACGATGAAGAACG
        ACCCCAGAATGTACAGTCTAAGTCAAGGACTGCGGAACTACAAGCTGTAAGTACAGAAAGCCACAGAGTAC
        CATCTAGGAAATTAACATTATACTAACTTTCTACATCGTTGATACTTATGCGTATACATTCATATACGTTC
        TTCGTGTTTATTTTTAGGAAATTGATGATACCGTGGGAATAATGAGAGATAACATAAATAAAGTAGCAGAA
        AGAGGTGAAAGATTAACGTCCATTGAAGATAAAGCCGATAACCTAGCGGTCTCAGCCCAAGGCTTTAAGAG
        GGGTGCCAATAGGGTCAGAAAAGCCATGTGGTACAAGGATCTAAAAATGAAGATGTGTCTGGCTTTAGTAA
        TCATCATATTGCTTGTTGTAATCATCGTCCCCATTGCTGTTCACTTTAGTCGATAG -p NGG -ref none
        
        """
        snc1 = ('ATGTCGTCATCTACTCCCTTTGACCCTTATGCTCTATCCGAGCACGATGAAGAACG' 
        'ACCCCAGAATGTACAGTCTAAGTCAAGGACTGCGGAACTACAAGCTGTAAGTACAGAAAGCCACAGAGTAC' 
        'CATCTAGGAAATTAACATTATACTAACTTTCTACATCGTTGATACTTATGCGTATACATTCATATACGTTC' 
        'TTCGTGTTTATTTTTAGGAAATTGATGATACCGTGGGAATAATGAGAGATAACATAAATAAAGTAGCAGAA' 
        'AGAGGTGAAAGATTAACGTCCATTGAAGATAAAGCCGATAACCTAGCGGTCTCAGCCCAAGGCTTTAAGAG' 
        'GGGTGCCAATAGGGTCAGAAAAGCCATGTGGTACAAGGATCTAAAAATGAAGATGTGTCTGGCTTTAGTAA' 
        'TCATCATATTGCTTGTTGTAATCATCGTCCCCATTGCTGTTCACTTTAGTCGATAG')
        
        cmd = ['python', program, '-seq', snc1 , '-p', 'NGG', '-r', '13' , '-ref', 'none' ]
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-13*')                  # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'snc1_sequence_noRef/crispy-results*')   # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))

    def test_general_case_Y223_strain_specific_gene(self):
        """
        Test the general use case, where the user enters a GLBRCY22-3 specific gene
        on the positive strand and asks for a comparison across all available 
        strains and specifying GLBRCY22-3 as strain of interest.  
        GLBRCY22-3 has it's own variants and separate GFF
        
        This will only be found in the GLBRCY22-3 strain, as a GLBRCY22-3 specific
        gene is "undefined" for the other strains. 
        
        crispy.py  -g FLO95 -p NGG -l 20 -n GLBRCY22-3 -t gene -r 14 -pr GLBRC
        """
        # run crispy to generate a new results file
        cmd = ['python', program, '-g', 'FLO95', '-n', 'GLBRCY22-3', '-t', 
               'gene', '-p', 'NGG', '-l', '20', '-r', '14' ]
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-14*')                  # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'flo95_standard_y223/crispy-results*')  # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))

    def test_general_case_Y223_strain_specific_gene_minus_strand(self):
        """
        Test the general use case, where the user enters a GLBRCY22-3 specific gene
        on the minus strand and asks for a comparison across all available 
        strains and specifying GLBRCY22-3 as strain of interest.  
        GLBRCY22-3 has it's own variants and separate GFF
        
        This will only be found in the GLBRCY22-3 strain, as a GLBRCY22-3 specific
        gene is "undefined" for the other strains. 
        
        crispy.py  -g FLO59 -p NGG -l 20 -n GLBRCY22-3 -t gene -r 15 -pr GLBRC
        """
        # run crispy to generate a new results file
        cmd = ['python', program, '-g', 'FLO59', '-n', 'GLBRCY22-3', '-t', 
               'gene', '-p', 'NGG', '-l', '20', '-r', '15' ,'-pr', 'GLBRC']
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-15*')                  # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'flo59_standard_y223_minus/crispy-results*')  # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))
        
    def test_zymomonas_offsite_targets_only(self):
        """
        Test the for offsite target searching only for Zymomonas mobilis.  Use a 
        user supplied sequence.
        
        python lib/python_scripts/crispy.py -sg ATCTTCCTGCC -ref ZYMOMONAS
        """
        # run crispy to find offsite targets only
        cmd = ['python', program, '-sg', 'ATCTTCCTGCC', '-ref', 'ZYMOMONAS', '-r', '16' ]
        job = Popen(cmd, stdout=PIPE)
        job.communicate()[0]
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-16*')                  # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'zymomonas_offsite/crispy-results*')    # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))       
        
    def test_sequence_search_zymomonas(self):
        """
        Test the -seq parameter, this runs a search of an input sequence for 
        guide RNA's using zymomonas for offsite targets.
        
        ZM4	Genbank	gene	149280	150656	.	+	.	ID=gene-ZMO1_ZMO0165;Name=tolB
        
        crispy.py -seq ATGAGCAGCGTAATCAGAAAATGGGCCTTAACGGCTTTGATGGCGGTAAGCAGCACGGCT
        TTGTTCGCGCAAAATCCTGCGGCTAGCGGTCAAGCAGCCAATCAGGGCGATAATCGCCGC
        ATCTTGCGAGTCGATATTACGGGCGGTATTTCCCAGCCTATGCCGATTGCGGTGCCGGTG
        ATGCCGACTCCGAGTTCGGTTGAAACCTTGGCGGGAACGACGGCGGTATTAGGTCGGCAG
        GTCGCTTCGGTTATTTCCAATGACCTGAAATCCAGTGGCCTTTTTACGCCATCGCAGCAA
        GCCTCCTTGCATAATGTATCTTTTCCTGAAGTAACCGCTCCGCAATATAGCTATTGGTTA
        TCGAGTGGCGCGCAGGCCTTGGTTCAGGGTTTCGTTCAGGCCAATGGCGATGGCACTCTG
        ACGGTAGGCTGTTATTTATATGACGTTTTCGCTTCGCAGGAAATGTTGCATAAAGGCTTT
        GTCGTGAAACCAGCCGACTGGCGGCGAGCCGCACATAAATGTGCTGATGCAGTTTATACC
        CGTTTGACAGGTGAAGGCCCCTATTTTGACAGCCGCATCGTTTATATTTCTGAAACGGGC
        CCAAAAAATCATCGCCTGAAGCGTCTGGCGATCATGGATCAGGATGGTGCCAATCACCGT
        TTCTTGACGAATGGCCAGTCGATGGTTCTGACCCCGCGTTTTGCGCCGAACCAGCAGACC
        GTTACCTATCTTTCTTATGTCGGTAATTCTCCGCGCATTTATGTCTATACTTTAGGTTCT
        GGCCATGTGCGTTTGGTGGTGAATAAGCCGAATACGACCTTTGCTCCGCGTTTTTCGCCA
        GATGGGAAAACGATTGTTTTCTCTATGTCTGTTGCGGGCAATACCGATATTTACAAGGTT
        CCGGTTTCCGGTGGGCAGGCAACCCGTCTGACTACTTCGCCCGGTATCGACACGGCACCG
        AGTTTCTCACCCGATGGCTCTAAAATCGTCTTTGAAAGTGATCGGTCAGGTAGTCAGCAG
        ATTTATATTATGAATGCTGATGGATCCAATCAGAACCGCATTAGTTTTGGTAGTGGACGT
        TACGCAACCCCAGTTTGGAGTCCGCGCGGTGATCTGATCGCCTTTACAAAATTGGGCGGC
        GGATTTCATGTCGGTGTGATGAAAACGGATGGTTCGGGTGAACAAATTCTGACCAATGGT
        TGGCAGGATGAAGGGCCTAGCTGGTCGCCGAATGGACGAGTCATTGCCTTCTTTAGAACA
        GCCCGTAATTCTGGTCATACGGAGTTATGGTCGGTTGATCTGACGGGGGTTAATGAACGG
        CATATTCCAACGCCTTTAGATGGTTCTGATCCATCTTGGGGGCCGTTATTGCCGTAA
        -p NGG -ref ZYMOMONAS
        
        """
        tolB = ('ATGAGCAGCGTAATCAGAAAATGGGCCTTAACGGCTTTGATGGCGGTAAGCAGCACGGCT'
                'TTGTTCGCGCAAAATCCTGCGGCTAGCGGTCAAGCAGCCAATCAGGGCGATAATCGCCGC'
                'ATCTTGCGAGTCGATATTACGGGCGGTATTTCCCAGCCTATGCCGATTGCGGTGCCGGTG'
                'ATGCCGACTCCGAGTTCGGTTGAAACCTTGGCGGGAACGACGGCGGTATTAGGTCGGCAG'
                'GTCGCTTCGGTTATTTCCAATGACCTGAAATCCAGTGGCCTTTTTACGCCATCGCAGCAA'
                'GCCTCCTTGCATAATGTATCTTTTCCTGAAGTAACCGCTCCGCAATATAGCTATTGGTTA'
                'TCGAGTGGCGCGCAGGCCTTGGTTCAGGGTTTCGTTCAGGCCAATGGCGATGGCACTCTG'
                'ACGGTAGGCTGTTATTTATATGACGTTTTCGCTTCGCAGGAAATGTTGCATAAAGGCTTT'
                'GTCGTGAAACCAGCCGACTGGCGGCGAGCCGCACATAAATGTGCTGATGCAGTTTATACC'
                'CGTTTGACAGGTGAAGGCCCCTATTTTGACAGCCGCATCGTTTATATTTCTGAAACGGGC'
                'CCAAAAAATCATCGCCTGAAGCGTCTGGCGATCATGGATCAGGATGGTGCCAATCACCGT'
                'TTCTTGACGAATGGCCAGTCGATGGTTCTGACCCCGCGTTTTGCGCCGAACCAGCAGACC'
                'GTTACCTATCTTTCTTATGTCGGTAATTCTCCGCGCATTTATGTCTATACTTTAGGTTCT'
                'GGCCATGTGCGTTTGGTGGTGAATAAGCCGAATACGACCTTTGCTCCGCGTTTTTCGCCA'
                'GATGGGAAAACGATTGTTTTCTCTATGTCTGTTGCGGGCAATACCGATATTTACAAGGTT'
                'CCGGTTTCCGGTGGGCAGGCAACCCGTCTGACTACTTCGCCCGGTATCGACACGGCACCG'
                'AGTTTCTCACCCGATGGCTCTAAAATCGTCTTTGAAAGTGATCGGTCAGGTAGTCAGCAG'
                'ATTTATATTATGAATGCTGATGGATCCAATCAGAACCGCATTAGTTTTGGTAGTGGACGT'
                'TACGCAACCCCAGTTTGGAGTCCGCGCGGTGATCTGATCGCCTTTACAAAATTGGGCGGC'
                'GGATTTCATGTCGGTGTGATGAAAACGGATGGTTCGGGTGAACAAATTCTGACCAATGGT'
                'TGGCAGGATGAAGGGCCTAGCTGGTCGCCGAATGGACGAGTCATTGCCTTCTTTAGAACA'
                'GCCCGTAATTCTGGTCATACGGAGTTATGGTCGGTTGATCTGACGGGGGTTAATGAACGG'
                'CATATTCCAACGCCTTTAGATGGTTCTGATCCATCTTGGGGGCCGTTATTGCCGTAA')
        
        cmd = ['python', program, '-seq', tolB , '-p', 'NGG', '-r', '17' , '-ref', 'ZYMOMONAS' ]
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results*')                     # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'zymomonas_sequence_offsite/crispy-results-17*')   # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))        
        
    def test_general_case_zymomonas(self):
        """
        Test the general use case, where the user enters a gene, strain name and
        asks for a comparison across all available strains.
        
        crispy.py -g hisC1_ZMO1_ZMO0002 -n zymomonas
        """
        # run crispy to generate a new results file
        cmd = ['python', program, '-g', 'hisC1_ZMO1_ZMO0002', '-n', 'zymomonas' ,'-r', '18']
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-18*')                  # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'zymomonas_hisC1/crispy-results-18*')        # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))        

    def test_general_case_1011GENOMES(self):
        """
        Test the general use case, where the user enters a gene, strain name and
        asks for a comparison across all available strains.
        
        crispy.py -g hog1 -n 03.vcf.gz -pr 1011GENOMES
        """
        # run crispy to generate a new results file
        cmd = ['python', program, '-g', 'hog1', '-n', '03' ,'-r', '19', '-pr', '1011GENOMES']
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-19*')                  # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'hog1_standard_1011/crispy-results-19*')        # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))

    def test_general_case_1011GENOMES_Mito(self):
        """
        Test the general use case for 1011GENOMES user enters a Mitochondrial gene, strain 
        name and asks for a comparison across all available strains. 
        
        The gene here is located on the plus strand.
        
        crispy.py  -g Q0065 -p NGG -l 20 -n CLIB1070 -t gene -r 20
        
        This gene has 3 introns which are reported in the intron file.        
        """
        # run crispy to generate a new results file
        cmd = ['python', program, '-g', 'Q0065', '-n', 'CLIB1070', '-t', 'gene', 
               '-r', '20', '-pr', '1011GENOMES' ]
        job = Popen(cmd, stdout=PIPE)   
        job.communicate()[0]    
        
        # get md5sum from the most recent results file
        filelst = glob.glob(outputDir + 'crispy-results-20*')                  # list of all crispy results files
        result  = max(filelst, key=os.path.getctime)                           # find the most recent, this is what we want to compare
        md5 = hashFILE(result)                                                 # generate the md5sum
        
        # get original results file for comparison
        testlst = glob.glob(testPath + 'mito_Q0065_standard_1011GENOMES/crispy-results-20*')        # These results have been validated previously
        check_md5 = hashFILE(testlst[0])
        
        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))
        
        intronlst = glob.glob( tmpPath + 'intron-*')
        result    = max(intronlst, key=os.path.getctime)
        md5 = hashFILE(result)
        
        # get original intron file for comparison
        testlst = glob.glob(testPath + 'mito_Q0065_standard_1011GENOMES/intron-20*')   # These results have been validated previously
        check_md5 = hashFILE(testlst[0])        

        self.assertEqual(check_md5, md5, "md5 sum check fails, files differ: %s :  %s" %(testlst[0],result))
        
    def test_blast(self):
        """
        Test blastHuman.py, input is the output from the 1st test case: test_general_case().  
        This has 2 hits w/ 100% identity (full length) on the Human Genome: 
        W303:YLR113W_30 GCAGGCACAGGCTCAGGCTCAGG  , W303:YLR113W_55 TGATCTTTCCCAGGGAACAAAGG
        
        Run individual test: python lib/python_scripts/test_crispy.py -v Test_crispy.test_blast
        """
        blastInput = testPath + 'hog1_standard/crispy-results-1.txt'
        result     = outputDir + 'test_blast_results.txt'
        
        # run blastHuman.py 
        cmd = ['python', blast, '-b', blastDB, '-f', blastInput, '-o', result ]
        
        job = Popen(cmd, stdout=PIPE)
        job.communicate()
        
        # get md5sum from the most recent results file
        md5 = hashFILE(result)
                
        # get original results file for comparison
        check_md5 = hashFILE(testPath + 'hog1_standard/crispy-results-1_blast.txt')
        self.assertEqual(check_md5, md5, "test_blast():\n md5 sum check fails, files differ: %s :  %s" %(blastInput,result))

if __name__ == '__main__':
    unittest.main()