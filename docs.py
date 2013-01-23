import urllib
import urllib2
import simplejson
from pymongo import Connection
import hashlib 
import re
import os
import random

conn=Connection()
db=conn.pdfgrabber


def formatTitle(grabTitle):
	newTitle=re.sub('<,/,\,>',' ',grabTitle)
	return newTitle

query=urllib.urlencode({'q':'filetype:doc'})
url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)

num_queries=80*4 
count=0
for start in range(200,num_queries,6):
	request_url='{0}&start={1}'.format(url,start)
	print request_url
	search_results=urllib.urlopen(request_url)
	json=simplejson.loads(search_results.read())
	try:
		results=json['responseData']['results']
		for i in results:
			print i
			HASH=hashlib.sha1(i['url']).hexdigest()
			if db.grabs.find_one({'_id':HASH}):
				print 'Already dld!'
			elif i['fileFormat']=="Microsoft Word":
				db.grabs.insert({'_id':HASH})
				print str(i['url'])
                os.system("wget --no-check-certificate "+str(i['url']))
	except TypeError, KeyError:
		pass
	os.system("mv *.doc  doxc/")	
#			OFILE=open(str(count)+'.pdf','wb')
#			OFILE.write(search_results.read())
#			OFILE.close()
#		newTitle=formatTitle(i['title'])
#		print newTitle+' - '+i['url']



