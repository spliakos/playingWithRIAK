#!/usr/bin/python

import sys
import urllib
import time
import signal
import logging
import os.path
import httplib
import json
import os

################################################################################
#  generic boring stuff
################################################################################
# no stacktrace on SIGINT
def signal_handler(signal, frame):
        print('Terminated with SIGINT (Ctrl+C)')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# logging setup
FORMAT = '%(asctime)-15s - %(message)s'
logging.basicConfig(stream=sys.stdout, format=FORMAT)
logger = logging.getLogger(sys.argv[0])
logger.setLevel(logging.INFO)
################################################################################

dryrun = False
shallow = False
filename = sys.argv[1]

if ("-v" in sys.argv):
   logger.setLevel(logging.DEBUG)
if ("-s" in sys.argv):
   logger.setLevel(logging.ERROR)
if ("--dry" in sys.argv):
   dryrun = True
if ("--coward" in sys.argv):
   shallow = True

riakipandport = "int-api-sports-sb-riak:8098"
#riakipandport = "localhost:8198"
pathprefix = "/types/banners_type/buckets/banners/keys"
cont_type = "application/json"

c = 1
upcount = 0 # count updated urls
igcount = 0 # count ignored urls (not 200 repo code on get call)

keyfile = open(filename + "_key", 'r')
url = keyfile.read()

riakkey = urllib.quote(url, "")

fullurl = "http://"+riakipandport+pathprefix+"/"+riakkey
puturl = "/buckets/fillup/keys/"+riakkey
logger.debug(str(c)+": getting "+fullurl)

valuefile = open(filename+ "_res", 'r')
page = valuefile.read()

# Delete key/value if already exists
connection = httplib.HTTPConnection(riakipandport)
puturl = pathprefix+"/"+riakkey
connection.request('DELETE', puturl)
result = connection.getresponse()
connection.close()

# Load new key/value
connection =  httplib.HTTPConnection(riakipandport)
puturl = pathprefix+"/"+riakkey
connection.request('PUT', puturl , page, {'Content-Type': cont_type, 'Accept': '*/*', 'User-Agent': 'python/httplib'})
result = connection.getresponse()
connection.close()


