#!/usr/bin/python
import os, sys, logging, hashlib, urllib2, json, getopt

basePath = '/mnt/nfs/sports/betslip/dest'

url = 'http://int-api-sports-sb-riak:8098/buckets/cdnconfig/keys/betslip'
tag = sys.argv[1]

print "RIAK ENDPOINT = " + url
print "TAG = " + tag


try:
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
except urllib2.HTTPError as e:
    logging.warn("Couldn't fetch config from RIAK bucket " + url + " defaulting to {}")
    data = json.loads('{}')

def addToRiak (dirpath, riakKey, url, file):

    if riakKey not in data:
        data[riakKey] = {}
        data[riakKey]['url'] = url
        data[riakKey]['hash'] = ''

    hash = hashlib.md5(open(dirpath + '/' + file,'rb').read()).hexdigest()
    if data[riakKey]['hash'] != hash:
        data[riakKey]['hash'] = hash
        print riakKey + ' -> ' + data[riakKey]['url'] + ' -> ' + hash
        data[riakKey]['lastChangedTag'] = tag

def loopDirectory(dir, target):
    for (dirpath, dirnames, filenames) in os.walk(basePath + dir):

        if 'js/locales' in  target:

            if filenames:

                locale = dirpath.split('/')[-1]
                file = 'betslip.min.js'
                riakKey = locale + '/' + file
                addToRiak(dirpath, riakKey, target + '/' + locale + '/' + file, file);
        else:

            for (file) in filenames:
                addToRiak(dirpath, file, target + '/' + file, file);

loopDirectory('/js/locales', '/betslip/js/locales');
loopDirectory('/css', '/betslip/css');

req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')

try:
    urllib2.urlopen(req, json.dumps(data))
except urllib2.HTTPError as e:
    logging.error("Failed to POST new asset config. Please check the RIAK details passed to the application. Content: " + json.dumps(data))
    sys.exit(1)

print "Finished successfully"
sys.exit(0)
