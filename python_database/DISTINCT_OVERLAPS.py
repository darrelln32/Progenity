#!/usr/bin/python
from collections import defaultdict
from OVERLAP2 import check_4_edges
from Bio import SeqIO


# read in the fastQ file and add the sequences to the read set to make them distinctive
reads = set()
for record in SeqIO.parse('ERR266411_1.for_asm.fastq','fastq'):
     reads.add(str(record.seq))

# print statement to verify the number of reads
print(len(reads))
		
k = 30

# this loop breaks the reads into kmers, and then places the kmers as keys into a dictionary
# and the reads as values with its associated kmer
kmers = defaultdict(set)
for read in reads:
	for base in range(0,len(read)-k+1,1):
		kmer = read[base:base+k]
		kmers[kmer].add(read)

# check for debug purposes
#print(len(kmers))

# function to grab the distinct edges
check_4_edges(reads, kmers, k)


# print statements for debug purposes
#print(kmers)
#print(kmers['TCGAAGTGGACTGCTGGCGGAAAATGAGAA'])

		
	
	
	
		
	

