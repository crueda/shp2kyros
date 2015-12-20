#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# autor: Carlos Rueda
# fecha: 2015-12-15
# mail: carlos.rueda@deimos-space.com

import time
import datetime
import os
import sys
import utm
import logging, logging.handlers

# establecemos el formato segun el formato de los logs
format = "%H:%M:%S"

# obtenemos la hora actual
now_time = datetime.datetime.now()
now = now_time.strftime(format)
#print (now , ' -> routekml2geo - START')

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

			#u = utm.from_latlon(41.3, 0.12)
			point_utm = utm.from_latlon(lat, lon)
			if (nelement==1):
				queryBody = queryBody + str(point_utm[0]) + " " + str(point_utm[1])
			else:
				queryBody = queryBody + "," + str(point_utm[0]) + " " + str(point_utm[1])
			#print queryBody
			

		query = queryHeader + queryBody + queryFooter + ";"
		print query

		#print line


# obtenemos la hora actual
now_time = datetime.datetime.now()
now = now_time.strftime(format)
#print (now , ' -> routekml2geo - END')