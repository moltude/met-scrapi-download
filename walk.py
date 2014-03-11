import os
import mechanize
import json
from pprint import pprint
import re
import sqlite3

#x = 1
#while True:
#	response = mechanize.urlopen('http://yuagstg.its.yale.edu/mediaTools/restserver?action=GetIDShotIngestHelpText')
#	print 'opened' + str(x)
#	x=x+1

conn = sqlite3.connect('./db/met-dim.db')
c = conn.cursor()

# walkthrough -- 
# break measurements apart and try to find between a set of measurements that contians either 2 or 3 dimension values.

for root, dirs, files in os.walk("/Users/scottwilliams/Code/Python/met-scrapi-download/data/objects/", topdown=False):
	for name in files:
		if name.endswith(".json"):
			o_file = os.path.join(root,name)
			# print (o_file)
			json_data=open(o_file)
			data = json.load(json_data)
			try: 
				dim=data['dimensions']
				o_id=data['id']
				if isinstance(dim, unicode):
					regExp = re.compile('\(.*?\)')
					matches = re.findall(regExp, dim.encode('ascii', 'ignore'))
					print matches

					if(len(matches)>1): 
						print str(o_id) + ' || ' + dim.encode('ascii', 'ignore')
						for match in matches: 
							if 'cm' in match: 
								values = re.findall(r'\d+.\d+', match)
								for value in values:
									c.execute("INSERT INTO dimensions VALUES (?,?,'')", (o_id,value))
									conn.commit()								
			except KeyError:
				print 'erro -- no dimensions '
			json_data.close()

conn.close()