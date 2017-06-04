#!/usr/bin/python
import json
import urllib

#url = 'http://python-data.dr-chuck.net/comments_42.json'
url = 'http://python-data.dr-chuck.net/comments_167599.json'

url_data = urllib.urlopen(url).read()

print('Retrieved',len(url_data),'characters')
#print(url_data)

json_data = json.loads(url_data)
#print(json_data)
#print(json_data['comments'])

total = 0

for item in json_data['comments']:
	#print type(item['count'])
	total += item['count']

print total


