import itertools
from hw4_overlap import greedy_scs
from Bio import SeqIO
# it will take some time to run

# program assembles a genome from a fastq file
# then give the number of A's and T's in the genome

# grab the reads from the fastQ file and place them in a list called reads
reads = list()
for record in SeqIO.parse('ads1_week4_reads.fq','fastq'):
	 reads.append(str(record.seq))

k = 30

genome = greedy_scs(reads,k)  # run the greedy_scs algorithm and store it in genome
print(genome)
print(len(genome))
total_A = genome.count('A')   #number of A's in the genome
total_T = genome.count('T')   # number of T's in the genome
print('A -> ',total_A)
print('T -> ',total_T)



