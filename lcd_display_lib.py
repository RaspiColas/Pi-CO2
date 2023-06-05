#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------------------------------#
#													#
#				lcd_display_lib.py	        		#
#				by N.Mercouroff						#
#													#
#---------------------------------------------------#

"""


"""
# from pmsensor import co2sensor
# import subprocess
from os import path
from time import strftime
import I2C_LCD_driver

debug = False

PATH_PREFIX = path.dirname(path.abspath(__file__)) + '/'
LOG_FILENAME = PATH_PREFIX + "log_co2.log"

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
#		Display text
#-------------------------------------------------

def display_text(text1, text2 = None):
	"""
		Displaying text1 & text2 LCD display  
	"""
	tolog("Displaying message '%s' & '%s' on display..." % (text1, text2))
	try:
		mylcd = I2C_LCD_driver.lcd()
		if not text2:
			text2 = text1
			text1 = strftime('%H:%M:%S')
		mylcd.lcd_display_string(text1, 1)
		mylcd.lcd_display_string(text2, 2)
		tolog("...display ok")
		return True
	except Exception as e:
		tolog('...error displaying message: %s' % (e), True)
		return False


#-------------------------------------------------
#		Main
#-------------------------------------------------

if __name__ == '__main__':
	tolog("Sending text to display")
	no_err = display_text("Ceci...", "...est un texte")
	if no_err:
		tolog("...display ok")
	else:
		tolog("...display error")

#-------------------------------------------------
#----- FIN DE LA LIBRARY -------------------------
#-------------------------------------------------
