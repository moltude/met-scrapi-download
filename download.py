import mechanize
import json
import urllib2
import os
import urllib

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
		except urllib2.HTTPError, e:
			print '404 error on ' + url
			return

	try: 
		obj_id=nomnom['id']
	except KeyError:
		print '*** ERROR NO ID PRESENT *** ' + url
		return

	# calculate folder to store
	# that was a blunt and chaotic rewrite of some java and deservers a cleanup
	str_obj_id = ''
	if (obj_id < 1000):
		str_obj_id = str(obj_id)
		while (len(str_obj_id) < 3):
			str_obj_id = '0' + str_obj_id
		str_obj_id = "0" + "/" + str_obj_id
	else:
		str_obj_id=str(obj_id)[0:len(str_obj_id)-3]+'/'+str(obj_id)[len(str_obj_id)-3:]

	path = path + str_obj_id + '/'
	# store locally
	if not os.path.exists(path):
		os.makedirs(path)

	# full file path
	path = path+str(obj_id)+'.json'
	if not os.path.exists(path):
		# write .json file to @path with formatting
		with open(path, 'w') as outfile:
	  		outfile.write(json.dumps(nomnom, sort_keys=True,indent=4, separators=(',', ': ')))
	pass


# Will load every page from scrapi. 
# Should then download the json for each object and store it locally
url = "http://scrapi.org/ids?page=1"
last_page=''
while last_page != url:
	try:
		response = mechanize.urlopen(url)
		nomnom = json.load(response)	
		url = nomnom['_links']['next']['href']
		last_page = nomnom['_links']['last']['href']
		
		print url
		# get each object
		objects = nomnom['collection']['items']
		for o in objects:
			get_object(o['href'])

	except urllib2.HTTPError, e:
		print '404 on ' + url
