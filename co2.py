#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------------------------------#
#													#
#				co2_every1h.py		        		#
#				by N.Mercouroff						#
#													#
#---------------------------------------------------#

"""
	source: https://monitorserviceatelierueda.blogspot.com/2018/11/how-to-measure-room-co2-concentration.html

Cablage:

Sonde CO2:

Vin -> GPIO 4 (5V)
GND -> GPIO 6 (GND)
Tx -> GPIO 10 (RXD)
Rx -> GPIO 8 (TXD)

Ecran LCD:

GND -> GPIO 9 (GND)
VCC -> GPIO 2 (5V)
SDA -> GPIO 3 (SDA)
SCL -> GPIO 5 (SCL)

"""
from os import system, path
from time import strftime
import lcd_display_lib
import send_sms_lib
import co2_lib
import ConfigParser

debug = True

PATH_PREFIX = path.dirname(path.abspath(__file__)) + '/'
LOG_FILENAME = PATH_PREFIX + "log_co2.log"
# CO2_MAX = 1000	Lu dans config
CONFIG_FILENAME = PATH_PREFIX + 'co2.conf'
TABLE_FILENAME = PATH_PREFIX + "co2_val.tsv"
HTML_FILENAME = '/var/www/html/data_co2.htm'

param = {}


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


def get_conf():
	global param

	tolog("Loading the configuration file...")
	try:
		config = ConfigParser.ConfigParser()
		config.read(CONFIG_FILENAME)

		param["co2max"] = int(config.get('CO2', 'co2max'))
		tolog("...success loading config")
		return True

	except Exception as e:
		tolog('...error reading config file %s: %s' % (CONFIG_FILENAME, e), True)
		return False


#-------------------------------------------------
#		Collect C02 data
#-------------------------------------------------

NB_VAL = 120

def copy_co2_val():
	tolog('Copie du fichier %s des données...' % (TABLE_FILENAME))

	try:
		with open(TABLE_FILENAME, 'r') as data_file:
			data_lines = data_file.readlines()
			l = len(data_lines)
			i = max(0, l-NB_VAL)
			html_text = ''
			while True:
				html_text +=  data_lines[i] 
				i += 1
				if i >= l:
					tolog('Les %s lignes de %s ont toutes été copiées !' %(i, TABLE_FILENAME))
					break
		with open(HTML_FILENAME, 'w') as data_file:
			data_file.write(html_text)

		tolog('...copie du fichier %s OK' %(TABLE_FILENAME))
		return True

	except Exception as e:
		tolog("...erreur lors de la copie du fichier : %s" %(e), True)
		return False


#-------------------------------------------------
#		Main
#-------------------------------------------------

def co2():
	no_err = get_conf()
	if not no_err:
		return False

	val = co2_lib.get_co2()
	if not val:
		return False

	if int(val) > param["co2max"]:
		no_err = send_sms_lib.send_text_sms("Alerte C02 = %s PPM" % (val))

	copy_co2_val()

	no_err = lcd_display_lib.display_text("CO2 = %s PPM" % (val))
	return no_err


if __name__ == '__main__':

	tolog("Processing CO2 data...")
	no_err = co2()
	if no_err:
		tolog("...ok processing CO2 data")
	else:
		tolog("...error processing CO2 data")

#-------------------------------------------------
#----- FIN DU PROGRAMME --------------------------
#-------------------------------------------------
