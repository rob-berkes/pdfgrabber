import urllib
import urllib2
import simplejson
from pymongo import Connection
import hashlib 
import re


conn=Connection()
db=conn.pdfgrabber


def formatTitle(grabTitle):
	newTitle=re.sub('<,/,\,>',' ',grabTitle)
	return newTitle

query=urllib.urlencode({'q':'sex filetype.pdf'})
url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
search_results=urllib.urlopen(url)
json=simplejson.loads(search_results.read())
results=json['responseData']['results']

count=0
for i in results:
	count+=1
	HASH=hashlib.sha1(i['url']).hexdigest()
	if db.grabs.find_one({'_id':HASH}):
		print 'Already dld!'
	else:
		db.grabs.insert({'_id':HASH})	
		PDFILE=urllib.urlopen(i['url'])
		OFILE=open(str(count)+'.pdf','wb')
		OFILE.write(PDFILE.read())
		OFILE.close()
#		newTitle=formatTitle(i['title'])
#		print newTitle+' - '+i['url']



