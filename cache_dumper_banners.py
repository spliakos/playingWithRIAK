#!/usr/bin/python

import sys
import urllib
import urllib2
import time
import signal
import logging
import os
import httplib
import json
import shutil

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
riakipandport = sys.argv[1] 

if ("-v" in sys.argv):
   logger.setLevel(logging.DEBUG)
if ("-s" in sys.argv):
   logger.setLevel(logging.ERROR)
if ("--dry" in sys.argv):
   dryrun = True
if ("--coward" in sys.argv):
   shallow = True

pathprefix = "/types/banners_type/buckets/banners/keys"
keydir = "banners-keys"
valdir = "banners-values"

keylisturl = "http://"+riakipandport+pathprefix+"?keys=true"
if dryrun:
   logger.info("running in dry mode - won't update anything")
   
logger.info("reading urls from "+keylisturl)

keylist = urllib.urlopen(keylisturl)

keysjson = json.loads(keylist.read())

keys = keysjson['keys']

logger.info("found "+str(len(keys))+" keys")

c = 1

upcount = 0 # count updated urls
igcount = 0 # count ignored urls (not 200 repo code on get call)
start = time.time()

if not os.path.exists(keydir):
   os.mkdir(keydir)

if not os.path.exists(valdir):
   os.mkdir(valdir)

src = os.getcwd()
dst1 = src + '/' + keydir
dst2 = src + '/' + valdir

for url in keys:
   # e.g.: url = /fragments/marketCollections/en-gb/tennis/OB_EV6633074/-1
   logger.info(str(c)+": handling url "+url)

   riakkey = urllib.quote(url, "")

   fullurl = "http://"+riakipandport+pathprefix+"/"+riakkey
   puturl = "/buckets/fillup/keys/"+riakkey
   logger.debug(str(c)+": getting "+fullurl)

   # We need urllib2 to set header and collect compressed values
   # If we don't need compressed values, we can proceed with the following call instead:
   response = urllib.urlopen(fullurl)
   logger.info(str(c)+": response: "+str(response.code))
   if response.code == 200:
      page = response.read()
   else:
      logger.info(str(c)+": response code was not 200. Ignoring key "+riakkey)
      igcount = igcount + 1

   response.close()

   keyfile = open(str(c)+'_key' , 'w')
   pagefile = open(str(c)+'_res' , 'w')
   keyfile.write(str(url))   
   pagefile.write(str(page))

   kfpath = os.getcwd() + '/' + str(c)+ '_key'
   pfpath = os.getcwd() + '/' + str(c)+ '_res'
   
   shutil.move(kfpath, dst1)
   shutil.move(pfpath, dst2)

   c = c+1
   if shallow and (upcount > 10):
      break

end = time.time()

duration = end - start

