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
biovu_cursor.execute("SELECT A.ACCESSION_NUMBER, S.SAMPLE_TUBE_ID, S.CONTAINER_ID, S.CONTAINER_ROW, S.CONTAINER_COLUMN, S.DATE_CREATED FROM SAMPLE_TABLE S INNER JOIN ACCESSION A ON S.ACCESSION_ID = A.ACCESSION_ID WHERE ((S.CLIENT_SAMPLE_TUBE_ID <> 'HapMap') or (S.CLIENT_SAMPLE_TUBE_ID IS NULL)) and (S.SAMPLE_STATUS IS NULL) and (S.DATE_CREATED > TO_DATE('2015-01-01','YYYY-MM-DD')) AND (S.SOURCE_TYPE = 'DNA') and ((CURRENT_DATE - S.DATE_CREATED) > 30)")
biovu_data = biovu_cursor.fetchall()
rts_cursor.execute("SELECT TUBE_ID FROM SIS_STORE_TUBE")
rts_data = rts_cursor.fetchall()

file_report = []
rts_data = [rec[0] for rec in rts_data]


# ###########################################################

for biovu_record in biovu_data:
    if biovu_record[1] not in rts_data:
        file_report.append(biovu_record)

# file_report =[biovu_record for biovu_record in biovu_data if biovu_record[1] not in rts_data]


# manipulating strings for output file
date = str(datetime.datetime.now().date())
time = str(datetime.datetime.now().time()).replace(':','_')
time = time.replace('.','_')
#filename_str = 'dna_small_volume_r4_' + date + '__' + time + '.csv'
filename_str = 'DNAnotInRTSpast30days' + date + '.csv'

with open(filename_str,'w') as output_csv:
    writer = csv.DictWriter(output_csv,fieldnames = ['REPORT','DATE','TIME'])
    writer.writeheader()
    writer.writerow({'REPORT':'DNA Samples not in RTS past 30 days','DATE':date,'TIME':time})
    output_csv.write('\n')
    writer = csv.DictWriter(output_csv,fieldnames = ['DBSC','SAMPLE_TUBE_ID','CONTAINER_ID','CONTAINER_ROW','CONTAINER_COLUMN','DATE_CREATED'])
    writer.writeheader()
    for record in file_report:
        writer.writerow({'DBSC':record[0],'SAMPLE_TUBE_ID':record[1],'CONTAINER_ID':record[2],'CONTAINER_ROW':record[3],'CONTAINER_COLUMN':record[4],'DATE_CREATED':record[5]})
        
print(len(file_report))


