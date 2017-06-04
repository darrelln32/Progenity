#!/usr/bin/python

# this program is used in conjunction with the DISTINCT_OVERLAPS
from collections import defaultdict
k = 30

# this function checks for overlaps
def overlap(a,b,k):
	start = 0
	while True:
		start = a.find(b[:k],start)
		if start == -1:
			return 0
		if b.startswith(a[start:]):
			return len(a)-start
		start += 1

# this function checks for distinct edges and
# records them in its own set
def check_4_edges(reads,kmers,k):
	print('START')
	overlaps = defaultdict(set)
	distinct_nodes = set()
	for read_a in reads:
		read_a_suffix = read_a[-k:]
		for read_b in kmers[read_a_suffix]:
			if (read_a != read_b):
				olen = overlap(read_a,read_b,k)
				if olen > 0:
					overlaps[(read_a,read_b)] = olen
					distinct_nodes.add(read_a)
	#print(overlaps)
print(len(overlaps))    #print the distinct edges
	print('distinct_nodes')
	#print(distinct_nodes)     #print the distinct nodes
	print(len(distinct_nodes))


