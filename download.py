import mechanize
import json
import urllib2
import os
import urllib
import logging


# Takes an object specific url and gets the JSON then stores the json locally in 
# /data//objects/XXX/XXX/XXXXX.json (zero padded) id dir structure
# 
def get_object(url):
	# core path is the current working directory 
	path= str(os.getcwd()) + '/data/objects/'
	# nomnom is the json response 
	nomnom = ''
	# this while loop is unecessary now that it has been confirmed that many of these 404 errors are 
	# legit and not just dropped connections 
	while nomnom == '':
		try:
			obj_resp = mechanize.urlopen(url)	
			nomnom = json.load(obj_resp)
		except (urllib2.URLError, urllib2.HTTPError, httplib.BadStatusLine) as e:
			logging.warning('HTTP error -- Unable to fetch object...' + url)
			return
		except:
			logging.warning('Something bad happend when fetching object url ' + url)
			return

	try: 
		obj_id=nomnom['id']
	except KeyError:
		logging.error('No ID present in object record...' + url)
		return
	except:
			logging.warning('Something bad happend when grabbing ID ' + url)
			return

	# calculate folder to store
	# that was a blunt and chaotic rewrite of some java and deservers a cleanup
	str_obj_id = str(obj_id)
	if (obj_id < 1000):
		while (len(str(str_obj_id)) < 3):
			str_obj_id = '0' + str_obj_id
		str_obj_id = "0" + "/" + str_obj_id
	else:
		str_obj_id=str_obj_id)[0:len(str_obj_id)-3]+'/'+str_obj_id)[len(str_obj_id)-3:]

	path = path + str_obj_id + '/'
	
	# does the key path /000/000/ exist? Create it? 
	if not os.path.exists(path):
		os.makedirs(path)

	# full file path
	path = path+str(obj_id)+'.json'
	# if the JSON file does not exist then 
	if not os.path.exists(path):
		# logging 
		logging.info('Writing JSON file...' + path)
		# write JSON file to @path with formatting
		with open(path, 'w') as outfile:
	  		outfile.write(json.dumps(nomnom, sort_keys=True,indent=4, separators=(',', ': ')))
	pass

# Will load every page from scrapi. 
# Should then download the json for each object and store it locally

# Setup logging 
logging.basicConfig(filename='./logs/scrapi.log', filemode='w', level=logging.INFO)

url = "http://scrapi.org/ids?page=1"
last_page=''

while last_page != url:
	try:
		response = mechanize.urlopen(url)
		nomnom = json.load(response)
		url = nomnom['_links']['next']['href']
		last_page = nomnom['_links']['last']['href']
		
		logging.info('Fetching page...' + url)

		# get each object
		objects = nomnom['collection']['items']
		for o in objects:
			get_object(o['href'])

	except (urllib2.URLError,urllib2.HTTPError) as e:
		logging.warning('Unable to fetch page (likely 404)...' + url)
	except:
			logging.warning('Something bad happend when fetching page...' + url)
		
		




