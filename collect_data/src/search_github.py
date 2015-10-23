
# pip install requests
import requests
import json
import datetime
import csv
from os import mkdir

bigdata_directory = datetime.datetime.now().strftime("%y_%m_%d_%H_%M")
bigdata_prefix = bigdata_directory + "/"
bigdata_prefix += 'bigdata_'
bigdata_suffix = '.csv'

bigdata_info = bigdata_prefix + 'info_' + bigdata_suffix
bigdata_desc_directory = bigdata_directory + "/documents/"

bigdata_keyfile = bigdata_prefix + 'keys.txt'
bigdata_documentcatfile = bigdata_prefix + 'documents_cat.txt'

# todo say we failed if the mkdir creation fails
mkdir(bigdata_directory)
mkdir(bigdata_desc_directory)

payload = {'q' : 'language:C'}
r = requests.get('https://api.github.com/search/repositories', params=payload)
if(r.ok):
	repoItems = json.loads(r.text or r.content)
	with open(bigdata_info, 'wb') as csv_info_file:
		csv_info_writer = csv.writer(csv_info_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		with open(bigdata_keyfile, 'wb') as raw_keyfile:
			with open(bigdata_documentcatfile, 'wb') as raw_document_catfile:
				for repo in repoItems['items']:
					print("Getting repo (id,name,full_name,owner,created_at,updated_at,pushed_at,description,url) : " , repo['id'] , ", " + repo['name'] + ", " + repo['full_name'] + ", " , repo['owner']['id'] , ", " + repo['created_at'] + ", " + repo['updated_at'] + ", " + repo['pushed_at'] + ", " + repo['description'] + ", " + repo['url'])
					try:
						csv_info_writer.writerow([repo['id'],repo['name'],repo['url']])
						raw_document_catfile.write(repo['description'] + '\n')
						raw_keyfile.write(str(repo['id']) + '\n')
						documentname = bigdata_desc_directory + str(repo['id'])
						with open(documentname, 'wb') as documentfile:
							documentfile.write(repo['description'] + '\n')
					except UnicodeEncodeError:
							print("we cannot handle unicode")
