#!/home/mplace/anaconda/bin/python
"""
@Program: fixGFF_geneNames.py

@Purpose: Used to update the supported gene name list
          
@Input:  gff file

@Output: print python dictionary

@Dependencies: Python 3

@author: Mike Place

"""
import sys

def main():
    """
    main() 
    """
  
    # if no args print help
    if len(sys.argv) == 1:
        print "\n\tInput file required."
        print "\n"
        print "\tgff2Bed.py <text file>"
        print "\tConverts GFF file to Bed file"
        sys.exit(1)
    else:
        gff = sys.argv[1]
        
    with open(gff) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('#'):
                continue
            else:
                r = line.split('\t')
                if r[2] == 'gene':       
                    info = r[8].split(';')
                    tuple_data = [tuple(item.split('=')) for item in info]
                    data = dict(tuple_data)
                    if 'gene' in data:
                        print '%s %s %s %s %s' %(r[0], r[3], r[4], data['gene'], r[6])
                    else:
                        print '%s %s %s %s %s' %(r[0], r[3], r[4], data['Name'], r[6])


if __name__ == "__main__":
    main()

