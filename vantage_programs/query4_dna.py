import cx_Oracle
import datetime
import csv


# Connect using Oracle's Easy Connect connection string.
# dbconn = cx_Oracle.connect(u'user/password@db-server:1521/service.name')
db = cx_Oracle.connect(u'dnalims/dnalims@eaprdscn07.ea.vanderbilt.edu:10922/LMSPRD_EA.mis.vanderbilt')
cursor = db.cursor()
# cursor.execute("SELECT SAMPLE_ID FROM SAMPLE_TABLE")
cursor.execute("SELECT A.ACCESSION_NUMBER, S.SAMPLE_TUBE_ID, S.CONTAINER_ID, S.CONTAINER_ROW, S.CONTAINER_COLUMN, S.VOLUME, S.DATE_CREATED FROM SAMPLE_TABLE S INNER JOIN ACCESSION A ON S.ACCESSION_ID = A.ACCESSION_ID WHERE ((S.CLIENT_SAMPLE_TUBE_ID <> 'HapMap') or (S.CLIENT_SAMPLE_TUBE_ID IS NULL)) and (S.SAMPLE_STATUS IS NULL) and (S.DATE_CREATED > TO_DATE('2015-01-01','YYYY-MM-DD')) and (S.VOLUME < 150) AND (S.SOURCE_TYPE = 'DNA') and (MONTHS_BETWEEN(CURRENT_DATE,S.DATE_CREATED) < 3)")
data = cursor.fetchall()


# manipulating strings for output file
date = str(datetime.datetime.now().date())
time = str(datetime.datetime.now().time()).replace(':','_')
time = time.replace('.','_')
#filename_str = 'dna_small_volume_r4_' + date + '__' + time + '.csv'
filename_str = 'DNAsmallVolumeLess3months_' + date + '.csv'


with open(filename_str,'w') as output_csv:
	writer = csv.DictWriter(output_csv,fieldnames = ['REPORT','DATE','TIME'])
	writer.writeheader()
	writer.writerow({'REPORT':'DNA Samples with volumes of 150 uL or less and older than 3 months','DATE':date,'TIME':time})
	output_csv.write('\n')
	writer = csv.DictWriter(output_csv,fieldnames = ['DBSC','SAMPLE_TUBE_ID','CONTAINER_ID','CONTAINER_ROW','CONTAINER_COLUMN','VOLUME','DATE_CREATED'])
	writer.writeheader()
	for record in data:
		writer.writerow({'DBSC':record[0],'SAMPLE_TUBE_ID':record[1],'CONTAINER_ID':record[2],'CONTAINER_ROW':record[3],'CONTAINER_COLUMN':record[4],'VOLUME':record[5],'DATE_CREATED':record[6]})
	
print(len(data))