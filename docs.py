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
#url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=filetype:doc'

num_queries=25*4*8 
count=0
STARTAT=0
for start in range(STARTAT+0,STARTAT+100*3,4):
	print start
	request_url=url+'&start='+str(start)
	print request_url
	search_results=urllib.urlopen(request_url)
	try:
		json=simplejson.loads(search_results.read())
		results=json['responseData']['results']
	except TypeError:
		pass
		try:
			for i in results:
				#print i
				HASH=hashlib.sha1(i['url']).hexdigest()
				if db.grabs.find_one({'_id':HASH}):
					print 'Already dld!\n\n\n\n'
	#			elif i['fileFormat']=="Microsoft Word":
				else:
					db.grabs.insert({'_id':HASH})
					print str(i['url']+"\n\n\n\n")
	               			os.system("wget --no-check-certificate "+str(i['url'])+"\n\n\n\n")
		except KeyError:
			print "Exception error in results\n\n\n\n"
		except NameError:
			pass
	os.system("mv *.doc  /home/rob/Downloads/pdfgrabber/docs/")	
#			OFILE=open(str(count)+'.pdf','wb')
#			OFILE.write(search_results.read())
#			OFILE.close()
#		newTitle=formatTitle(i['title'])
#		print newTitle+' - '+i['url']




