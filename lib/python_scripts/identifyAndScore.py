"""
# Author: Raj Chari
# Date: October 5th, 2016

# Main wrapper script for sgRNA Scorer 2.0 (RUN THIS ONLY, DO NOT RUN THE OTHER THREE SCRIPTS)

Modified by Mike Place June 2017

I added the path variable to make calling the subscripts easier.  Path set to script home directory.
When deploying script make sure path is set correctly.

Logging added

"""
from __future__ import division

import argparse
import logging
import os
import platform
import sys
import subprocess
from collections import defaultdict
from Bio import SeqIO

# set up logging
logger = logging.getLogger(__name__)

cwd  = os.getcwd()        # get current working directory to use w/ input files 
path = cwd + '/lib/python_scripts/'           # path to script directory

def validPAM(pamSequence):
    goodPAM = True
    validCharacters = ['A','C','T','G','K','M','R','Y','S','W','B','V','H','D','N']
    for character in pamSequence:
        if character not in validCharacters:
            goodPAM = False
            break
    return goodPAM

def runPipeline(inputFile,outputFile,spacerLength,pamSequence,pamOrientation):
    # call the identify function
    logger.info('Identifying sgRNAs in input file using sgRNA Scorer 2.0')     # write job info to log file
    outputFile1 = inputFile.name.replace('.fasta','.putative.fasta')
    command1 = 'python ' + path + 'identifyPutativegRNASites.V2.py -i ' + inputFile.name + ' -p ' + pamSequence + ' -q ' + pamOrientation + ' -s ' + spacerLength + ' -o ' + outputFile1
    p = subprocess.Popen(command1,shell=True)
    p.communicate()
    # next call the SVM function
    logger.info('Classifying identified sgRNA sequences')
    outputFile2 = inputFile.name.replace('.fasta','.SVMOutput.tab')
    command2 = 'python ' + path + 'generateSVMFile.V2.py -g ' + path + 'Cas9.High.tab -b ' + path + 'Cas9.Low.tab -i ' + outputFile1 + ' -s ' + spacerLength + ' -p ' + pamOrientation + ' -l ' + str(len(pamSequence)) + ' -o ' + outputFile2
    p = subprocess.Popen(command2,shell=True)
    p.communicate()
    # finally call the make table function to put it into a table
    logger.info('Making final output file')
    command3 = 'python ' + path + 'makeFinalTable.V2.py -g ' + outputFile1 + ' -s ' + outputFile2 + ' -o ' + outputFile.name + ' -p ' + pamOrientation
    p = subprocess.Popen(command3,shell=True)
    p.communicate()	                                                    
    # delete the temporary files
    if platform.system()=='Windows':
        delCommand = 'del '
    else:
        delCommand = 'rm '
        delOutput = delCommand + outputFile1 + ' ' + outputFile2
    p = subprocess.Popen(delOutput,shell=True)
    p.communicate()
    return

def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i','--input',type=argparse.FileType('r'),required=True)
    parser.add_argument('-o','--output',type=argparse.FileType('w'),required=True)
    parser.add_argument('-s','--spacerLength',required=True)
    parser.add_argument('-p','--pamOrientation',required=True)
    parser.add_argument('-l','--pamSequence',required=True)
    opts = parser.parse_args(argv)
    # initialize variables
    validPAMSequence = ''
    spacerLength = '20'
    pamOrientation = '3'
    fastaDictionary = defaultdict(str)
    
    # make sure the input is proper, first check PAM
    if validPAM(opts.pamSequence)==False:
        logger.info('PAM sequence has invalid characters. PAM sequence must only contain A,C,T,G,K,M,R,Y,S,W,B,V,H,D,N') 
        sys.exit('PAM sequence has invalid characters. PAM sequence must only contain A,C,T,G,K,M,R,Y,S,W,B,V,H,D,N')
    else:
        validPAMSequence = opts.pamSequence
    # next check that the spacer is only numbers
    if opts.spacerLength.isdigit()==False:
        logger.info('Spacer length must be an integer with a minimum size of 14')
        sys.exit('Spacer length must be an integer with a minimum size of 14')
    else:
        spacerLength = opts.spacerLength
    # check PAM orientation
    if opts.pamOrientation!='5' and opts.pamOrientation!='3':
        logger.info('Valid PAM orientations are 5 or 3')
        sys.exit('Valid PAM orientations are 5 or 3')
    else:
        pamOrientation = opts.pamOrientation
    # go through the input file
    for record in SeqIO.parse(opts.input,'fasta'):
        fastaDictionary[str(record.id)] = str(record.seq)
    if any(fastaDictionary):
        runPipeline(opts.input,opts.output,spacerLength,validPAMSequence,pamOrientation)
    else:
        logger.info('Invalid sequence file. Please make sure file is in FASTA format')
        sys.exit('Invalid sequence file. Please make sure file is in FASTA format')

if __name__ == '__main__':
    main(sys.argv[1:])
