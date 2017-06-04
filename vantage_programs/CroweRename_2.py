import os
import glob
import re

## a rewrite of the name change script 4 crowe's samples

# putting this here in case i ever need it
# os.chdir() 
  
fastq = glob.glob('*fastq*')
sampleNumber = 22428

#print(fastq)

for fastqName in fastq:
	#print(fastqName)
	i = re.search('S(.+?)_',fastqName)
	n = int(i.group(1))
	if n > 3:
		start_str = 'control_'
		newSampleNumber = n - 3
	else:
		start_str = 'sample_'
		newSampleNumber = sampleNumber + n - 1
	if '_R1_' in fastqName:
		read = '1'
	else:
		read = '2'
	newFastqName = start_str + str(newSampleNumber) + '_' + read + '.fastq.gz'
	print(fastqName,' --> ',newFastqName)
    	# os.rename(fastqName,newFastqName)
