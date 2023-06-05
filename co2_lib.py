#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------------------------------#
#													#
#				co2.py library		        		#
#				by N.Mercouroff						#
#													#
#---------------------------------------------------#

"""
source: https://monitorserviceatelierueda.blogspot.com/2018/11/how-to-measure-room-co2-concentration.html

"""
from os import system, path
from time import strftime

debug = False

PATH_PREFIX = path.dirname(path.abspath(__file__)) + '/'
LOG_FILENAME = PATH_PREFIX + "log_co2.log"
TEMP_FILE = PATH_PREFIX + "temp.txt"
TABLE_FILE = PATH_PREFIX + "co2_val.tsv"


#-------------------------------------------------
#		Utilities
#-------------------------------------------------

def tolog(txt, forceprint=False):
	"""
		Logs events and prints it if forceprint = True
	"""
	if debug or forceprint:
		print(txt)
	now = strftime('%Y/%m/%d %H:%M:%S')
	msg = "%s\t%s" % (now, txt)
	with open(LOG_FILENAME, 'a') as file:
		file.write(msg + "\n")
	return


#-------------------------------------------------
#		Manage CO2 data
#-------------------------------------------------

def fetch_co2():
	tolog("Fetching CO2 data...")
	try:
		system("sudo python -m mh_z19 > %s" % (TEMP_FILE))

		with open(TEMP_FILE, "r") as data_file:
			line = data_file.read()
			val = line[8:-2]
		tolog("...CO2 value = %s" % (val))
		return val

	except Exception as e:
		tolog("...error fetching CO2: %s" % (e), True)
		return None


def store_co2(val):
	tolog("Recording CO2 data...")
	try:
		now = strftime('%Y/%m/%d %H:%M:%S')
		val_st = now + '\t' + val
		with open(TABLE_FILE, "a") as table_file:
			table_file.write(val_st + '\n')
		tolog("...data stored at %s" % (now))
		return True
	except Exception as e:
		tolog("...error recording CO2 data: %s" % (e), True)
		return False


#-------------------------------------------------
#		Main
#-------------------------------------------------

def get_co2():
	val = fetch_co2()
	if val:
		no_err = store_co2(val)
	return val


if __name__ == '__main__':
	
	# ppm = co2sensor.read_mh_z19("/dev/ttyS0")
	# ppm = co2sensor.read_mh_z19("/dev/serial0")

	# result = subprocess.run(['python', '-m mh_z19'], stdout=subprocess.PIPE)
	# ppm = result.stdout
	# print("CO2 concentration is {} ppm".format(ppm))

	tolog("Processing CO2 data...")
	val = get_co2()
	if val:
		tolog("...ok processing CO2 data")
	else:
		tolog("...error processing CO2 data")
	print("CO2 = %s PPM" %(val))

#-------------------------------------------------
#----- FIN DE LA LIBRARY -------------------------
#-------------------------------------------------
