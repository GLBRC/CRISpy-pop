Help on module crispy:

NAME
    crispy - @Program: crispy.py

FILE
    /home/mplace/scripts/crispy/lib/python_scripts/crispy.py

DESCRIPTION
    @Purpose: Design CRISPR/cas9 spacers for use with S.cerevisiae.            
    
    @Input  : Three modes are available.   
    
        1)Search for all guide RNA's for a specific strain, gene and matches to all
          other available strains.  Only S. cerevisiae and its direct derivatives are
          supported for this option.  Only guide RNA that match the chromosome and 
          are w/in the gene boundaries will be reported.
    
            example:crispy.py -g YDR099W -n W303 -c groups.txt
            
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
      -c, --compare       Text file listing the subgroups from groups [GLBRC|Clade|Ecological] to compare guide RNAs 
      -g, --gene          Specific gene name
      -l, --length        Space length
      -n, --name          Strain Name i.e. W303
      -p, --pam           PAM sequence, default NGG (currently the only one supported)
      -pr , --project       Project Name, GLBRC or 1002Genomes
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
            Python 2.7
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
       Not yet supported: 
        N. meningitidis  , NNNNGATT 
        S. thermophilus 1, NNAGAAW
        S. thermophilus 3, NGGNG
    
    @Author: Mike Place
    @Date:   6/26/2017 
            
    Future support for alternate species such as E.coli & Zymomonas mobilis

CLASSES
    __builtin__.object
        Crispy
    
    class Crispy(__builtin__.object)
     |  Class creates and runs the sgRNA pipeline.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, gene, standard_gene, pam, spacerLen, strains, compare, runID, target, project)
     |      Set up Crispy object
     |      gene        = Systematic gene name, best for searching GFF file
     |      std_gene    = standard gene name, most familiar to user
     |      orientation = pam orientation, 5 = 5', 3 = 3'
     |      pam         = pam sequence, i.e. NGG
     |      spLen       = spacer length in base pairs
     |      strains     = List of strains to process
     |      compare     = strain subgroups to use for comparions
     |      species     = alternate species, E. coli, Zymomonas mobilis
     |      runID       = run identication number, used to provide a unique file name
     |      target      = feature type used to retrieve coordinates from the GFF 
     |      project     = data is from GLBRC or 1002 Genome Project
     |  
     |  __str__(self)
     |      Format job information and return a string
     |  
     |  checkIntron(self)
     |      Check for the presence of gene name in the list of yeast introns.
     |      If present returns string of pairs of start & end positions.
     |  
     |  findOffSiteTargets(self)
     |      Use Cas-OFFinder to evaluate off site target interactions for the guide RNA
     |  
     |  getChrom(self)
     |      Set the Chromosome number for gene
     |  
     |  getGenePosition(self)
     |      Set the gene start and stop positions.  Will be used to filter the final
     |      results of cas-offinder, to limit results to what is present within a gene.
     |      
     |      returns a tuple of the gene start and end
     |  
     |  getStrand(self)
     |      Set the strand for gene, + or -
     |  
     |  getVariantGene(self)
     |      Use module variantgene to extract sequence from reference genome.
     |      This will create a directory with the gene name and contain all the 
     |      gene fasta files.
     |  
     |  matchResults(self, sgRNADict, offsiteTargetsFile)
     |      Match up sgRNA Scorer data to offsitesTargets data from cas-offinder.
     |      
     |      sgRNADict - dictionary with guide RNA as key
     |      offsiteTargetsFile - file containing results of cas-offinder
     |      
     |      This will create a total count of all offsite targets,  if a sgRNA hits
     |      3 times, the count will be 2, as one is the "correct" hit.  sgRNA not on
     |      the chromosome of interest are also counted.
     |  
     |  matchSeqResults(self, sgRNADict, offsiteTargetsFile)
     |      Match up sgRNAScorer data w/ guide RNA generated using input Sequence to offsitesTargets
     |      and write results to file.
     |      
     |      example sgRNADict entry:        
     |      sgRNADict[target[0]] 'custom_Plus_1053', 'AATTCCTTGACTCAAAAATATGG', '-2.18019098656 
     |      
     |      example offsiteTargetsFile 1st 3 lines:    
     |      GGATCTCAAAGAGAACATTAAGG III     314827  GGATCTCAAAGAGAACATTAAGG +       0
     |      GGATCTCAAAGAGAACATTAAGG XV      1777    GGATCTCAAAGAGAACATTAAGG -       0
     |      CTTGTGATTACCACAGTAGTTGG III     314235  CTTGTGATTACCACAGTAGTTGG -       0
     |      
     |      results table header:
     |      GeneID  sgRNA   %Activity  %GC   chrom pos  strand NumReferenceMatches
     |  
     |  parseScorer(self, altRef='')
     |      Parse the file returned by sgRNAScorer for input into cas-offinder
     |      
     |      cas-offinder input file format:
     |      
     |      First line - path of chromosomes FASTA files
     |      Second line - desired pattern including PAM sequence
     |      Third (or more) line - query sequences with maximum mistmatched numbers (currently set to 0),
     |      seperated by spaces. (The length of the desired pattern and the query sequences should be the same!)
     |      
     |      An example of input file:
     |      
     |          /var/chromosomes/yeast
     |          NNNNNNNNNNNNNNNNNNNNNGG
     |          GGCCGACCTGTCGCTGACGCNNN 0
     |          CGCCAGCGTCAGCGACAGGTNNN 0
     |          ACGGCGCCAGCGTCAGCGACNNN 0
     |          GTCGCTGACGCTGGCGCCGTNNN 0
     |          
     |      to run:
     |          cas-offinder casinput.txt C out.txt
     |  
     |  prepSingleOffSite(self, seq, altRef='')
     |      Prepare request to search for offsite targets given a single guide RNA sequence.  
     |      The input guide RNA sequence should not have the PAM sequence included, as it is
     |      added below.
     |  
     |  setAltRef(self, Ref)
     |      Set up user provided alternate reference for use.
     |      Steps:
     |          1) Check that reference is supported
     |          2) Return path
     |  
     |  sgRNAScorer(self, strain)
     |      Make external call to sgRNA Scorer 2.0 to get a list of guide RNA's.
     |      This identifies and scores all SpCas9 guide RNA sites.
     |      
     |      python identifyAndScore.py -i eGFP.fasta -o eGFP.SpCas9.tab -p 3 -s 20 -l NGG
     |  
     |  singleWriteResults(self, altRef='')
     |      Write the final results for a single guide RNA offsite search.
     |      Results are sorted by chromosome and position.
     |  
     |  strainCount(self, seq, strand)
     |      Find the number of perfect matches for seq in the list of strain specific gene fasta files.
     |      
     |      The sgRNA_list_matching_stains.txt is deleted prior to this function call
     |      every time the program is run.
     |  
     |  writeNoResults(self, outFile)
     |      Write No Results Found to output file
     |  
     |  writeResults(self, data)
     |      Write final sgRNA, % activity, offsitetarget information to file.
     |      
     |      results table header:
     |          
     |      GeneID  sgRNA  %Activity  %GC  chrom  pos  MisMatchseq  strand  numMisMatches  numOffSiteMatch  NumStrainsHit
     |  
     |  writeResultsNoOffSiteTarges(self, data)
     |      Write results for targeting a custom sequence to a file when no offsite
     |      target results are found.  This parses and writes the results of running
     |      sgRNAScorer to a file.
     |      
     |      results table header:
     |          
     |      GeneID  sgRNA  %Activity  %GC  position_w/in_seq  strand
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

FUNCTIONS
    definition()
        # set up global functions
    
    is_fasta(filename)
        Check if a file is a fasta file.
    
    main()
        Main

DATA
    Y223Fasta = '/home/mplace/scripts/crispy/lib/reference/GLBRCY22-3.fast...
    Y223GFF = '/home/mplace/scripts/crispy/lib/reference/GLBRCY22-3.gff'
    altRefInfo = ['SACCHAROMYCES_PARADOXUS', 'Saccharomyces_paradoxus.gff'...
    altRefPath = '/home/mplace/scripts/crispy/lib/reference/'
    binPath = '/home/mplace/scripts/crispy/bin/'
    chroms = {'kluuveromyces': ['A', 'B', 'C', 'D', 'E', 'F', 'MT'], 'yeas...
    configFile = <closed file '/home/mplace/scripts/crispy/lib/python_scri...
    current_dir = '/home/mplace/scripts/crispy/'
    f = <closed file 'lib/reference/reference_info.conf', mode 'r'>
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    genePath = '/home/mplace/scripts/crispy/lib/genes/'
    genes_directory = '/home/mplace/scripts/crispy/lib/genes'
    line = 'SACCHAROMYCES_PARADOXUS Saccharomyces_paradoxus....adoxus.fast...
    logger = <logging.Logger object>
    outputDir = '/home/mplace/scripts/crispy/lib/python_scripts/output'
    output_directory = '/home/mplace/scripts/crispy/lib/python_scripts/out...
    pamLen = {'NGG': 3, 'NNGRRT': 6, 'TTTV': 4}
    pamOptions = {'NGG': '3', 'NNGRRT': '3', 'TTTV': '3'}
    path = '/home/mplace/scripts/crispy/lib/python_scripts/'
    path_config = {'Y223Fasta': 'lib/reference/GLBRCY22-3.fasta', 'Y223GFF...
    path_vals = ['referencePath', 'lib/reference/\n']
    refDir = '/home/mplace/scripts/crispy/lib/reference/'
    refList = set(['KLUUVEROMYCES_LACTIS', 'S288C', 'SACCHAROMYCES_PARADOX...
    refPath = '/home/mplace/scripts/crispy/lib/reference/S288C'
    tmp_directory = '/home/mplace/scripts/crispy/lib/python_scripts/tmp'
    vcfPath = '/home/mplace/scripts/crispy/lib/vcfs/'
    yeastFasta = '/home/mplace/scripts/crispy/lib/reference/S288C_referenc...
    yeastGFF = '/home/mplace/scripts/crispy/lib/reference/S288C_R64-1-1.gf...


One liners for checking results in Genes directories:

Count matches of strings

count the number of sequence w/ 1 match ( change the value in the perl statement to check for other numbers of string matches)
for i in *.fasta; do sed ':a;N;$!ba;s/\n//g' $i | grep -o GAAACCGTGATTGTTATCAGAACT | wc -l ; done | perl -nae 'if($_ == 1){ print $_;}'


