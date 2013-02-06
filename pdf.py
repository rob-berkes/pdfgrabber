import urllib
import urllib2
import simplejson
from pymongo import Connection
import hashlib 
import re
import os
import random
import time
NUMRANGE=800000
DICTWORDS=479820
conn=Connection()
db=conn.pdfgrabber


def formatTitle(grabTitle):
	newTitle=re.sub('<,/,\,>',' ',grabTitle)
	return newTitle


num_queries=5*4 
count=0
STARTNUM=random.randint(1,NUMRANGE)
lines=[line.strip() for line in open('/usr/share/dict/words')]
DWORD=random.randint(0,DICTWORDS)
SEARCHWORD=lines[DWORD]
#SEARCHWORD="immortal%20lobster"
print SEARCHWORD
PDFFOLDER="/pdfs/"+str(SEARCHWORD)+"/"
os.system("mkdir -p "+str(PDFFOLDER))
TIMESTR=time.strftime("%H%m%d%Y")


db.grabwords.insert({'word':str(SEARCHWORD),'time':TIMESTR})
time.sleep(5)
query=urllib.urlencode({'q':'filetype:pdf'})
url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
url+='%20'+str(SEARCHWORD)


for start in range(0,num_queries,4):
	TIMESTR=time.strftime("%H%m%d%Y")
	request_url='{0}&start={1}'.format(url,start)
	search_results=urllib.urlopen(request_url)
	json=simplejson.loads(search_results.read())
	try:
		results=json['responseData']['results']
		for i in results:
			HASH=hashlib.sha1(i['url']).hexdigest()
			try:
				if db.grabs.find_one({'_id':HASH}):
					print 'Already dld!'
				elif i['fileFormat']=="PDF/Acrobat":
					pass
			except KeyError:
				print '------downloading possible non-pdf file ------'
				TIMESTR+=str('_nonPDFpossible')
			db.grabs.insert({'_id':HASH,'url':str(i['url'])})
                	os.system("wget --no-check-certificate "+str(i['url']))
	except TypeError, KeyError:
		pass

	os.system("mv *.pdf* "+str(PDFFOLDER))	



