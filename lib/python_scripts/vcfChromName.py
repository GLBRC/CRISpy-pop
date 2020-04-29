"""
@Program: vcfChromName.py

@Purpose: Convert chromosome names in VCF file from chromosome# to Roman Numerals
          chromosome1 = I
         
@Input:  gzipped vcf file

@author: Mike Place

"""
import gzip
import re
import shutil
import subprocess
import sys                  

chrom = { "chromosome1" : "I", "chromosome2" : "II", "chromosome3" : "III", "chromosome4" : "IV",
        "chromosome5" : "V", "chromosome6" : "VI", "chromosome7" : "VII", "chromosome8" : "VIII", 
        "chromosome9" : "IX", "chromosome10" : "X", "chromosome11" : "XI", "chromosome12" : "XII", 
        "chromosome13" : "XIII", "chromosome14" : "XIV", "chromosome15" : "XV", "chromosome16" : "XVI"
        }           

def main():
    """
    main() 
    """
    # if no args print help
    if len(sys.argv) == 1:
        print("\n\tInput file required.")
        print("\n")
        print("\tvcfChromName.py <gzipped vcf file>")
        print("\tConverts chromosome1 to I, chromosome2 to II  etc...")
        sys.exit(1)
    else:
        vcf = sys.argv[1]
    
    print ('File %s ' %(vcf))
    
    pattern = re.compile('chromosome\d+')
        
    with gzip.open(vcf, 'rb') as f, open('outfile.vcf', 'w') as out:
        for line in f:
            if line.startswith('##contig'):                                    # Replace chromosome names in header
                capture = pattern.findall(line)
                line = re.sub(capture[0], chrom[capture[0]],line)
                out.write(line)
            elif line.startswith('chromosome'):                                # Replace chromosome on each row
                dat = line.split('\t')
                dat[0] = chrom[dat[0]]
                out.write( "\t".join(dat))
            else:
                out.write(line)
    
    cmd = ['bgzip', 'outfile.vcf']
    subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    shutil.move('outfile.vcf.gz', vcf)
    # tabix index
    cmd = ['tabix', '-p', 'vcf', vcf ]
    subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()                

if __name__ == "__main__":
    main()

