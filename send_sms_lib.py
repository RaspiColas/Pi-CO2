#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------------------------------#
#													#
#				send_sms.py library		       		#
#				by N.Mercouroff						#
#													#
#---------------------------------------------------#

from os import system, path
from time import strftime
import ConfigParser
import urllib2

debug = False
param = {}

PATH_PREFIX = path.dirname(path.abspath(__file__)) + '/'
LOG_FILENAME = PATH_PREFIX + "log_co2.log"

CONFIG_FILENAME = PATH_PREFIX + 'co2.conf'
SMS_URL = "https://smsapi.free-mobile.fr/sendmsg"

HTTPErrorCode = {
    200: "Requête traitée avec succès le SMS a été envoyé sur votre mobile",
    400: "La syntaxe de la requête est erronée",
    402: "Trop de SMS ont été envoyés en trop peu de temps.",
    403: "Vous n’avez pas activé le service ou vous avez fait une erreur dans le login ou le mot de passe.",
    500: "Erreur interne du serveur. Réessayez ultérieurement.",
    999: "Erreur inconnue. Réessayez ultérieurement."
}


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
#		Read config
#-------------------------------------------------

def get_conf():
	global param

	tolog("Loading the configuration file...")
	try:
		config = ConfigParser.ConfigParser()
		config.read(CONFIG_FILENAME)

		param["user1"] = config.get('SMS', 'user')
		param["pass1"] = config.get('SMS', 'pass')
		tolog("...success loading config")
		return True

	except Exception as e:
		tolog('...error reading config file %s: %s' % (CONFIG_FILENAME, e), True)
		return False


#-------------------------------------------------
#		Send SMS
#-------------------------------------------------

def convert_text(text):
	return text.replace(' ', '%20')


def send_text_sms(text):
	"""
		Sending text by SMS  
	"""
	tolog("Sending message '%s' by SMS..." % (text))

	no_err = get_conf()
	if not no_err:
		return False

	msg = "%21Alerte%20" + convert_text(text)
	api_url = "%s?user=%s&pass=%s&msg=%s" % (SMS_URL, param["user1"], param["pass1"], msg)
	try:
		req = urllib2.Request(api_url)
		rep = urllib2.urlopen(req)
		HTTPError = rep.getcode()
		tolog("...return code %s: %s" % (HTTPError, HTTPErrorCode[HTTPError]))
		return True
	except Exception as e:
		tolog('...error Service smsapi.free-mobile.fr: %s' % (e), True)
		return False


#-------------------------------------------------
#		Main
#-------------------------------------------------

if __name__ == '__main__':
	tolog("Sending text to SMS")
	no_err = send_text_sms("Ceci est un SMS")
	if no_err:
		tolog("...display ok")
	else:
		tolog("...display error")

#-------------------------------------------------
#----- FIN DE LA LIBRARY -------------------------
#-------------------------------------------------
