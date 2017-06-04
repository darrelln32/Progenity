#!/usr/bin/env python

# Write a Python program (same setup as in Q1) that takes, as a single argument on the command line, a single ENSG ID (as in Q1) and outputs a human- readable gene name (or multiple gene names, one on each line) for all transcripts of that gene. Your solution must involve a join between table “ensGene” (see Q1) and table “ensemblToGeneName”; the latter cross-refs transcript IDs and human- readable names (the “value” column). The one-to-many mapping of ENSG to ENST will come from table “ensGene”, and the human-readable name for STDOUT will come from “ensemblToGeneName”.
#
#
#
                                                    
import mysql.connector, sys     # import the mysql connector and the sys library for use in this script

# this command establishes the connection to the genome database @ UCSC
cnx = mysql.connector.connect(user='genomep', password='password', host='genome-mysql.cse.ucsc.edu', database='hg19')

cursor = cnx.cursor()         # define the pointer for the rows in the database

user_gene = raw_input("Enter the name of the gene for which you wish to retrive the common name >> " )         # get the gene name from the user

# set the query
query = ("SELECT name2,  value FROM ensGene  G INNER JOIN ensemblToGeneName  T on G.name = T.name  WHERE name2 = '"+user_gene+"' ORDER BY  value")

cursor.execute(query)      # run the query

a = 0         # this is a counter so we can make unique gene names

row = cursor.fetchone()       # get a row from the query

# check for an empty row... if the row is empty, (this means not a valid gene from the user) we will exit the script
if row is None:
       print >> sys.stderr,  user_gene + "  is not a valid entry for a gene in this database"
       sys.exit(1)

# for the rows that aren't empty, go ahead and print the common gene name from the ensemblToGeneName table
for (value) in cursor:
       a+=1
       print str(value[1]) + "_TR00" + str(a)

cursor.close()        #  close cursor  connection
cnx.close()             # close the database



