
# ** DIMESNIOS table ** 
# id -- key
# obj_id -- text # met museum object id 
# value -- float # the dimension value in cms
# notes -- text assocaited with this value 


# volumne_area\
# obj_id text
# value real
# type text

# Donna 

import sqlite3

#c.execute('''CREATE TABLE dimensions
#             (obj_id text, value real, notes text)''')



# removes objects with more than 3 or less than two dimesions 
def remove_rows (): 
	conn = sqlite3.connect('met-dim.db')
	c = conn.cursor()

	for row in c.execute('SELECT DISTINCT obj_id, COUNT(*) FROM dimensions GROUP BY obj_id ORDER BY COUNT(*)' ):
		if( 1 == int(row[1]) or int(row[1]) >= 4):
			del_cur = conn.cursor()
			del_cur.execute("DELETE FROM dimensions WHERE obj_id = '%s';" % row[0])
			conn.commit()

	conn.close()

	return

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def calculate (obj_id): 
	conn = sqlite3.connect('met-dim.db', timeout=1)
	c = conn.cursor()
	values = []
	calc_val = 0
	dim_type = ''

	for row in c.execute ("SELECT value FROM dimensions WHERE obj_id = '%s';" % obj_id):
		if is_number(row[0]):
			values.append(row[0])	 
	conn.commit()
	conn.close()

	# calaculate the area
	for value in values: 
		if calc_val == 0:
			calc_val = value
		else: 
			calc_val = calc_val*value

	# get the type
	if(len(values) == 2 ): # if two-dimensional object
		dim_type='area'
	else:
		dim_type='volume'

	# insert area/volum into volume_area table
	conn = sqlite3.connect('met-dim.db', timeout=1)
	insert = conn.cursor()
	insert.execute("INSERT INTO volumne_area VALUES (?,?,?)", (obj_id,calc_val,dim_type))
	conn.commit()
	conn.close()

	pass
# end calculate

def populate_vol_area_table():

	drop_vol_area_table()
	# remove bad rows from dimensions table
	remove_rows()

	conn = sqlite3.connect('met-dim.db')
	c = conn.cursor()
	# get the volume for each object in dimensions
	c.execute('SELECT DISTINCT obj_id FROM dimensions' )
	rows = c.fetchall( )
	conn.close()
	# for row in c.execute('SELECT obj_id FROM dimensions' ):
	for row in rows:
		calculate(row[0])
	
	
# end def

def drop_vol_area_table():
	conn = sqlite3.connect('met-dim.db')
	c = conn.cursor()
	# delete everything from table
	c.execute ('DELETE FROM volumne_area')
	conn.commit()	
	conn.close()

def dump_pop(): 
	conn = sqlite3.connect('met-dim.db')
	c = conn.cursor()
	for row in c.execute("SELECT * FROM volumne_area"):
		print row


drop_vol_area_table()
# calculate('8108')
# calculate('8108')
populate_vol_area_table()
dump_pop()
