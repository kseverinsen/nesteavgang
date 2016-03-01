#!/usr/bin/python
import urllib2 as UL
from xml.etree import ElementTree as ET
import time
from datetime import date, timedelta, datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

##################################################################

url = 'http://reiskollektivt.no/tfk/tekstvisning.php?mapid=49769'

response = UL.urlopen(url)

stag = '<table>'
etag = '</table>'

s = response.read()
tstart = s.find(stag)
tend = s.find(etag)

s = s[tstart:tend+len(etag)]


table = ET.XML(s)

rows = iter(table)
headers = [col.text for col in next(rows)]

routes = dict()

for row in rows:
    values = [col.text for col in row]
    #routes[values[0]] = values[1:]

    d = datetime.now()
    lt = time.localtime()
    nd = date(lt.tm_year, lt.tm_mon, lt.tm_mday)+timedelta(1)

    times = []
    for tstring in values[1:]:
    	tstring = tstring + " " + d.strftime("%d %m %Y")
    	try:
    		t = datetime.strptime(tstring, "%H:%M %d %m %Y")

    	except ValueError:
    		tstring = tstring[:5] + " " + nd.strftime("%d %m %Y")
    		t = datetime.strptime(tstring, "%H:%M %d %m %Y")

    	times.append(t)

    routes[values[0]] = times
######################################################################    

threshold = 60
warningthresh = 15
nesteavg = [] 

for route in routes.keys():
	for t in routes[route]:
		delta = t - d 
		if delta < timedelta(minutes=threshold):
			#print route, delta
			nesteavg.append((delta.seconds, route))

nesteavg.sort()

for r in nesteavg:
	if ((r[0]/60) <= warningthresh): 
		rline = bcolors.OKBLUE + r[1] + ":"  + bcolors.ENDC 
		mline = "\t" + bcolors.FAIL + str(r[0]/60)  + " minute(s)" + bcolors.ENDC
	elif ((r[0]/60) <= threshold): 
		rline = bcolors.OKBLUE + r[1] + ":"  + bcolors.ENDC 
		mline = "\t" + bcolors.OKGREEN + str(r[0]/60)  + " minute(s)" + bcolors.ENDC

	print rline + mline.rjust(60-len(rline))

print bcolors.WARNING + "Updated: (" + d.strftime("%H:%M:%S") + ")\n" + bcolors.ENDC