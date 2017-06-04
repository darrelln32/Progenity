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

# establish a counter to use during the print portion of the script
a=0

# will use thses empty lists to 
start = []                 
end = []

# process data retrieved from the database
for (chrom,exonStarts,exonEnds) in cursor:
       n=0
       for c in exonStarts:
            start.append(int(exonStarts[n:n+8]))                                      # pull start and end exons
            end.append(int(exonEnds[n:n+8]))
            n += 9                                                                                           # make sure we are pointing to the next exon
            if  (n == len(exonStarts)):                                                           # break the for loop after the last row has been formatted
                 break


# this nested for-loop goes through the start and end exons and  check for any overlapping exons
#  the exons that are overlapped are marked for deletion.  there are 7 types of overlaps that can occur
for i in range(len(start)):
    for n in range(len(start)):
           if start[i] > start[n] and end[i] < end[n] :
                 start[i] = 'delete'
                 end[i] = 'delete'
                 break
           if start[i] < start[n]  and end[i] == end[n]  :
                 start[n] = 'delete'
                 end[n] = 'delete'
                 break
           if start[i] > start[n] and end[i] == end[n] :
                 start[i] = 'delete'
                 end[i] = 'delete'
                 break
           if start[i] == start[n] and end[i] < end[n] :
                 start[i] = 'delete'
                 end[i] = 'delete'
                 break
           if start[i] == start[n] and end[i] > end[n] :
                 start[n] = 'delete'
                 end[n] = 'delete'
                 break
           if  start[i] < start[n] and end[i] > end[n] :
                 start[n] = 'delete'
                 end[n] = 'delete'
                 break
           if start[i] == start[n] and end[i] == end[n] :
                 if i > n:
                     start[i] = 'delete'
                     end[i] = 'delete'                   


# remove deleted exons from the table                 
start = filter(lambda a: a != 'delete', start)
end= filter(lambda a: a != 'delete', end)


# print the starting and ending exons            
for i in range(len(start)):
       a+=1 
       print chrom, "    ",start[i], end[i],  chrom,".",a
       
#shut down cursor and close database        
cursor.close()  
cnx.close()        
   