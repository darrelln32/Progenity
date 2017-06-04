import re
import sys
import glob	
import os
import linecache
import csv
import datetime

headers = ("SAMPLE_ID","BAIT_SET","TOTAL_READS","PCT_PF_READS_ALIGNED","PCT_SELECTED_BASES",
        "PCT_OFF_BAIT", "MEAN_TARGET_COVERAGE","PCT_TARGET_BASES_2X",
        "PCT_TARGET_BASES_10X","PCT_TARGET_BASES_20X","PCT_TARGET_BASES_30X",
        "PCT_TARGET_BASES_40X","PCT_TARGET_BASES_50X","PCT_TARGET_BASES_100X")

sep = ("	")

#s = open('coverage_summary.txt','a')
header = sep.join(headers)
#s.write(header + '\n')

tData = list()

for i in glob.iglob('*.coverage.stats.txt'):
    id = i.split('.')

    line = linecache.getline(i,8)
    line = line.rstrip('\n\r')
    line = line.split(None)
    
    #pstats = id[0] + '.pstats.txt'

    #linep = linecache.getline(pstats,10)
    #linep = linep.rstrip('\n\r')
    #linep = linep.split(None)
    
    values = [id[0],line[0],line[5],line[11],line[18],line[19],line[22],line[35],line[36],line[37],line[38],line[39],line[40],line[41]]
    #content = sep.join(str(n) for n in values)
    tData.append(values)
    
    #s.write(content + '\n')

#.close()
#  additions
date = str(datetime.datetime.now().date())
time = str(datetime.datetime.now().time()).replace(':','_')
time = time.replace('.','_')


with open('coverage_summary.csv','w') as output_csv:
    writer = csv.DictWriter(output_csv,fieldnames = ['REPORT','DATE','TIME'])
    writer.writeheader()
    writer.writerow({'REPORT':'Read Coverage Summary','DATE':date,'TIME':time})
    output_csv.write('\n')
    writer = csv.DictWriter(output_csv,fieldnames = ['SAMPLE_ID','BAIT_SET','TOTAL_READS','PCT_PF_READS_ALIGNED','PCT_SELECTED_BASES','PCT_OFF_BAIT','MEAN_TARGET_COVERAGE','PCT_TARGET_BASES_2X','PCT_TARGET_BASES_10X','PCT_TARGET_BASES_20X','PCT_TARGET_BASES_30X','PCT_TARGET_BASES_40X','PCT_TARGET_BASES_50X','PCT_TARGET_BASES_100X'])
    writer.writeheader()
    for n in tData:
        writer.writerow({'SAMPLE_ID':n[0],'BAIT_SET':n[1],'TOTAL_READS':n[2],'PCT_PF_READS_ALIGNED':n[3],'PCT_SELECTED_BASES':n[4],'PCT_OFF_BAIT':n[5],'MEAN_TARGET_COVERAGE':n[6],'PCT_TARGET_BASES_2X':n[7],'PCT_TARGET_BASES_10X':n[8],'PCT_TARGET_BASES_20X':n[9],'PCT_TARGET_BASES_30X':n[10],'PCT_TARGET_BASES_40X':n[11],'PCT_TARGET_BASES_50X':n[12],'PCT_TARGET_BASES_100X':n[13]})