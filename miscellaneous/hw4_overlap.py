#!/usr/bin/python
import itertools

def pick_max_overlap(reads,k):
	read_a, read_b = None, None
	best_olen = 0
	for a,b in itertools.permutations(reads,2):
		olen = overlap(a,b,k)
		if olen > best_olen:
			read_a, read_b = a,b
			best_olen = olen
	return read_a,read_b,best_olen


def overlap(a, b, k):
	""" Return length of longest suffix of 'a' matching
		a prefix of 'b' that is at least 'min_length'
		characters long.  If no such overlap exists,
		return 0. """
	start = 0  # start all the way at the left
	while True:
		start = a.find(b[:k], start)  # look for b's suffx in a
		if start == -1:  # no more occurrences to right
			return 0
		# found occurrence; check for full suffix/prefix match
		if b.startswith(a[start:]):
			return len(a)-start
		start += 1  # move just past previous match

# function uses a greedy algorithm to assemble a DNA string or genome
def greedy_scs(reads,k):
	read_a, read_b, olen = pick_max_overlap(reads,k)
	while olen > 0:
		reads.remove(read_a)
		reads.remove(read_b)
		reads.append(read_a + read_b[olen:])
		read_a,read_b, olen = pick_max_overlap(reads,k)
	return ''.join(reads)


