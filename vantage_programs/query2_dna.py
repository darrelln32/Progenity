import cx_Oracle
import datetime
import csv


# Connect using Oracle's Easy Connect connection string.
# dbconn = cx_Oracle.connect(u'user/password@db-server:1521/service.name')
db = cx_Oracle.connect(u'dnalims/dnalims@eaprdscn07.ea.vanderbilt.edu:10922/LMSPRD_EA.mis.vanderbilt')
cursor = db.cursor()
# cursor.execute("SELECT SAMPLE_ID FROM SAMPLE_TABLE")
cursor.execute("SELECT A.ACCESSION_NUMBER, S.SAMPLE_TUBE_ID, S.CONTAINER_ID, S.CONTAINER_ROW, S.CONTAINER_COLUMN, S.DATE_CREATED FROM SAMPLE_TABLE S INNER JOIN ACCESSION A ON S.ACCESSION_ID = A.ACCESSION_ID WHERE ((S.CLIENT_SAMPLE_TUBE_ID <> 'HapMap') or (S.CLIENT_SAMPLE_TUBE_ID IS NULL)) and (S.SAMPLE_STATUS IS NULL) and (S.DATE_CREATED > TO_DATE('2015-01-01','YYYY-MM-DD'))  and (S.CONCENTRATION IS NULL) AND (S.SOURCE_TYPE = 'DNA') and ((CURRENT_DATE - S.DATE_CREATED) > 25)")
data = cursor.fetchall()

# manipulating strings for output file
date = str(datetime.datetime.now().date())
time = str(datetime.datetime.now().time()).replace(':','_')
time = time.replace('.','_')
#filename_str = 'dna_no_conc_r2_' + date + '__' + time + '.csv'
filename_str = 'DNAnullConcentrationPast25days_' + date + '.csv'


with open(filename_str,'w') as output_csv:
	writer = csv.DictWriter(output_csv,fieldnames = ['REPORT','DATE','TIME'])
	writer.writeheader()
	writer.writerow({'REPORT':'DNA Samples with no Concentration and older than 25 days','DATE':date,'TIME':time})
	output_csv.write('\n')
	writer = csv.DictWriter(output_csv,fieldnames = ['DBSC','SAMPLE_TUBE_ID','CONTAINER_ID','CONTAINER_ROW','CONTAINER_COLUMN','DATE_CREATED'])
	writer.writeheader()
	for record in data:
		writer.writerow({'DBSC':record[0],'SAMPLE_TUBE_ID':record[1],'CONTAINER_ID':record[2],'CONTAINER_ROW':record[3],'CONTAINER_COLUMN':record[4],'DATE_CREATED':record[5]})
			
print(len(data))