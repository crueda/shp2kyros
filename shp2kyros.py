#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# autor: Carlos Rueda
# date: 2015-12-21
# mail: carlos.rueda@deimos-space.com
# version: 1.0

##################################################################################
# version 1.0 release notes:
# Initial version
##################################################################################

import time
import datetime
import os
import sys
import utm
import logging, logging.handlers

#### VARIABLES #########################################################
MAX_THREADS = 51

INTERNAL_LOG_FOLDER = "/var/log/correos/shp2kyros.log"
########################################################################

# definimos los logs internos que usaremos para comprobar errores
try:
	logger = logging.getLogger('shp2kyros')
	loggerHandler = logging.handlers.TimedRotatingFileHandler(INTERNAL_LOG_FOLDER, 'midnight', 1, backupCount=10)
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	loggerHandler.setFormatter(formatter)
	logger.addHandler(loggerHandler)
	logger.setLevel(logging.DEBUG)
except:
	print '------------------------------------------------------------------'
	print '[ERROR] Error writing log at %s' % INTERNAL_LOG_FOLDER 
	print '[ERROR] Please verify path folder exits and write permissions'
	print '------------------------------------------------------------------'
	exit()

########################################################################
# Definicion de clases
#
########################################################################








def main():
	
	queryHeader = "INSERT INTO routes (SHAPE) VALUES ( GeomFromText( \' LineString("
	queryFooter = ") \' ) )"
	queryBody = ""

	with open('./rutas0.txt') as fp:
		for line in fp:

			vline = line.split(" ")
			nelement = 0
			for element in vline:
				nelement += 1
				vcoord = element.split(",")
				lat = float(vcoord[1])
				lon = float(vcoord[0])

				point_utm = utm.from_latlon(lat, lon)
				if (nelement==1):
					queryBody = queryBody + str(point_utm[0]) + " " + str(point_utm[1])
				else:
					queryBody = queryBody + "," + str(point_utm[0]) + " " + str(point_utm[1])			

			query = queryHeader + queryBody + queryFooter + ";"
			print query

if __name__ == '__main__':
    main()
