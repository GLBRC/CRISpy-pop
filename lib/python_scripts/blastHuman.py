"""
@Program: blastHuman.py

@Purpose: Check for CRISpy guide RNA hits against the human genome.

@Input:  CRISpy output file.

 Example:
  Run as stand alone:
  python ./blastHuman.py -b GRCh38.fa -f crispy-results-2.txt -o BLAST_result.txt

  Or

  import blastHuman

  data = blastHuman.blastHuman(blastDB, rnaFile, outPut)
  data.createFasta()
  data.runBlast()
  data.writeBlast()

From Blast docs:

    pident    Percentage of identical matches
    length    Alignment length
    nident    Number of identical matches
    score     Raw blast score
    sseq      sequence

@Output: text file
@author: Mike Place
@Date:   10/19/2018
@Dependencies:  python 3
"""
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

import argparse
import re
import subprocess
import sys

num_threads = '4'

class blastHuman( object ):
    """
    blastHuman Object used to blast CRISpy guide RNA's against the human genome.

    """
    def __init__( self, blastDB, gRNA, outName):
        """
        Set up blastHuman object
        blastDB  = prebuilt blast database name
        gRNA     = CRISpy output file
        outName  = output file name
        fasta    = fasta file created from CRISpy guide RNA results
        length   = the guide RNA sequence length
        """
        self.blastDB = blastDB
        self.gRNA    = gRNA
        self.outName = outName
        self.fasta   = re.sub('.txt', '.fa', gRNA)
        self.length  = 0                              # will be used as a parameter for blast
        self.result  = []                             # list of guide RNA names that hit the human genome

    def createFasta(self):
        """
        Create a fasta file from the CRISpy guide RNA sequences for use w/ blastn.
        """
        records = []
        # open CRISpy guide RNA file
        with open(self.gRNA) as file:
            file.readline()                           # skip header
            for line in file:
                dat = line.split('\t')                # get the rowID and sequence
                records.append( SeqRecord(Seq(dat[1]), id=dat[0], description='') )

        SeqIO.write(records, self.fasta, 'fasta')     # write all sequences to a file at once

        self.length = len(records[0].seq)             # set guide RNA length

    def runBlast(self):
        """
        Call blastn on the newly created sgRNA fasta file

        We are only interested in 100 % sequence identity for the full guide RNA
        length.

        """
        #program = '/home/mplace/bin/ncbi-blast-2.8.1+/bin/blastn'      # full path to blastn
        program = 'blastn'
        self.length = str(self.length)                                # FOR TESTING ONLY

        # set up blastn command line parameters
        cmd = [ program, '-query', self.fasta, '-db', self.blastDB, '-outfmt',
               "6 qseqid pident length sseq", '-num_threads', num_threads,
               '-perc_identity', '100', '-word_size', self.length, '-num_alignments', '1' ]

        # run blastn command
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()   #
        # get output
        result1 = ''.join(output[0].decode('utf-8'))
        result2 = output[1].decode('utf-8')

        for hit in result1.rstrip().split('\n'):
            self.result.append(hit.split('\t')[0])                       # store gRNA name which hit the Human Genome

        with open('blast.log', 'a') as log:
            log.write(result2)
            log.write("")

    def writeBlast(self):
        """
        Write guide RNA identifiers for perfect blastn matches.
        """
        with open(self.outName, 'w') as out:
            for hit in self.result:
                out.write('%s\n' %(hit))
        out.close()

def main():
    """
    Main
    """
#******************************************************************************
# Command line args
#******************************************************************************
    cmdparser = argparse.ArgumentParser(description="Check for CRISpy gRNA hits agains Human genome.",
                                        usage='%(prog)s -b <blastn results file>' ,prog='blastnFilter.py'  )
    cmdparser.add_argument('-b', '--blastDB', action='store', dest='BLASTDB', help='Human blastdb name .', metavar='')
    cmdparser.add_argument('-f', '--file',    action='store', dest='FILE',    help='CRISpy output file', metavar='')
    cmdparser.add_argument('-o', '--outFile', action='store', dest='OUTFILE', help='Output file name.',metavar='')
    cmdResults = vars(cmdparser.parse_args())

    # if no args print help
    if len(sys.argv) == 1:
        print("")
        cmdparser.print_help()
        sys.exit(1)
    # get blast database name
    if cmdResults['BLASTDB']:
        blastDB = cmdResults['BLASTDB']
    # get CRISpy results file
    if cmdResults['FILE']:
        grnaFile = cmdResults['FILE']
    # Output file name
    if cmdResults['OUTFILE']:
        outFile = cmdResults['OUTFILE']

    data = blastHuman(blastDB, grnaFile, outFile)
    data.createFasta()
    data.runBlast()
    data.writeBlast()

if __name__ == "__main__":
    main()
