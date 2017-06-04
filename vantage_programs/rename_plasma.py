import os
import glob
import re

## a rewrite of the name change script 4 crowe's samples

# putting this here in case i ever need it
# os.chdir() 
  
fileList = glob.glob('*2017*')
	

for fileName in fileList:
	if not fileName[0:4].isdigit():
		continue
	textPart = (re.search('_(.*)\.',fileName)).group(1)
	# print(text_part)
	if fileName[-3:] == 'csv':
		newFileName = 	textPart + '_' + fileName[:8] + '.csv'
	else:
		 if fileName[-3:] == 'txt':
		 	newFileName = 	textPart + '_' + fileName[:8] + '.txt'
	print(fileName,' --> ',newFileName)
	os.rename(fileName,newFileName)
