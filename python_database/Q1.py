#!/usr/bin/env python

# Write a program that queries a public MySQL server to retrieve genomic coordinates of all exons in all transcripts of a certain gene, then outputs to STDOUT the genomic coordinates of the union of all subsequences in BED 4-column format (https://genome.ucsc.edu/FAQ/FAQformat.html#format1 ), no header. This means overlapping/adjacent exons should be merged into a single coordinate range such that each chromosome base appears in at most one output range.

#
#
                                                    
import mysql.connector    # import the mysql connector and the sys library for use in this script

# this command establishes the connection to the genome database @ UCSC
cnx = mysql.connector.connect(user='genomep', password='password', host='genome-mysql.cse.ucsc.edu', database='hg19')

cursor = cnx.cursor()         # define the pointer for the rows in the database

# set up the query for ENSG00000139618'
query = ("SELECT chrom,exonStarts,exonEnds FROM ensGene WHERE name2 = 'ENSG00000139618'")

cursor.execute(query)    # run the query

a=0    # establish a counter to use during the print portion of the script

for (chrom,exonStarts,exonEnds) in cursor:
       n=0
       for c in exonStarts:
            a+=1 
            print chrom, "    ", exonStarts[n:n+8], exonEnds[n:n+8],  chrom,".",a     # step through both exonStarts and exonEnds and format the output
            n += 9                                                                    # make sure we are pointing to the next exon
            if  (n == len(exonStarts)):                                               # break the for loop after the last row has been formatted
                 break   
       
cursor.close()   #shut down cursor
cnx.close()        # close database
   