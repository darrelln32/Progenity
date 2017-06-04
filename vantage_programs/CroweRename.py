import os
import glob
import re

## a rewrite of the name change script 4 crowe's samples

# putting this here in case i ever need it
# os.chdir() 
  
fastq = glob.glob('*fastq*')
sampleNumber = 21280

for fastqName in fastq:
	i = re.search('S(.+?)_',fastqName)
	newSampleNumber = sampleNumber + int(i.group(1)) - 1
	if '_R1_' in fastqName:
		read = '1'
	else:
		read = '2'
	newFastqName = 'sample_' + str(newSampleNumber) + '_' + read + '.fastq.gz'
	print(fastqName,' --> ',newFastqName)
    # os.rename(fastqName,newFastqName)
