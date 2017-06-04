# new monthly report

import cx_Oracle
import datetime
import csv

# Connect using Oracle's Easy Connect connection string.
# dbconn = cx_Oracle.connect(u'user/password@db-server:1521/service.name')
biovu_db = cx_Oracle.connect(u'dnalims/dnalims@eaprdscn07.ea.vanderbilt.edu:10922/LMSPRD_EA.mis.vanderbilt')
biovu_cursor = biovu_db.cursor()
rts_db = cx_Oracle.connect(u'sis_owner/sahara@eaprdscn07.ea.vanderbilt.edu:10922/LMSPRD_EA.mis.vanderbilt')
rts_cursor = rts_db.cursor()
# cursor.execute("SELECT SAMPLE_ID FROM SAMPLE_TABLE")
biovu_cursor.execute("SELECT A.ACCESSION_NUMBER, S.SAMPLE_TUBE_ID, S.DATE_CREATED FROM SAMPLE_TABLE S INNER JOIN ACCESSION A ON S.ACCESSION_ID = A.ACCESSION_ID WHERE ((S.CLIENT_SAMPLE_TUBE_ID <> 'HapMap') or (S.CLIENT_SAMPLE_TUBE_ID IS NULL)) and (S.SAMPLE_STATUS IS NULL) and (S.CONCENTRATION IS NULL) AND (S.SOURCE_TYPE = 'DNA')")
biovu_data = biovu_cursor.fetchall()
rts_cursor.execute("SELECT TUBE_ID FROM SIS_STORE_TUBE")
rts_data = rts_cursor.fetchall()

file_report = []
rts_data = [rec[0] for rec in rts_data]


# ###########################################################

for biovu_record in biovu_data:
    if biovu_record[1] in rts_data:
        file_report.append(biovu_record)

# file_report =[biovu_record for biovu_record in biovu_data if biovu_record[1] not in rts_data]


# manipulating strings for output file
date = str(datetime.datetime.now().date())
time = str(datetime.datetime.now().time()).replace(':','_')
time = time.replace('.','_')
#filename_str = 'dna_small_volume_r4_' + date + '__' + time + '.csv'
filename_str = 'DNAinRTSwithNullConcentration' + date + '.csv'

with open(filename_str,'w') as output_csv:
    writer = csv.DictWriter(output_csv,fieldnames = ['REPORT','DATE','TIME'])
    writer.writeheader()
    writer.writerow({'REPORT':'DNA Samples in RTS with Null Concentration','DATE':date,'TIME':time})
    output_csv.write('\n')
    writer = csv.DictWriter(output_csv,fieldnames = ['DBSC','SAMPLE_TUBE_ID','DATE_CREATED'])
    writer.writeheader()
    for record in file_report:
        writer.writerow({'DBSC':record[0],'SAMPLE_TUBE_ID':record[1],'DATE_CREATED':record[2]})
        
print(len(file_report))
        
