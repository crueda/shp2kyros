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

import fiona
import utm
import ogr, osr

from shapely.geometry import shape

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

    # Spatial Reference System
	inputEPSG = 3857
	outputEPSG = 4326
    # create coordinate transformation
	inSpatialRef = osr.SpatialReference()
	inSpatialRef.ImportFromEPSG(inputEPSG)
	outSpatialRef = osr.SpatialReference()
	outSpatialRef.ImportFromEPSG(outputEPSG)

	with fiona.open('./shapefiles/paradasRutas.shp', 'r') as input:
		nelement = 0
  		for pt in input:
  			# Propiedades especifica
			codigo = pt['properties']['COD_RUTA']
			num_seq = pt['properties']['NUM_SECUEN']
    		
    		# Coordenadas
			pointX = shape(pt['geometry']).x
			pointY = shape(pt['geometry']).y

    		# create a geometry from coordinates
			point = ogr.Geometry(ogr.wkbPoint)
			point.AddPoint(pointX, pointY)

			coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

    		# transform point
			point.Transform(coordTransform)

   			# print point in EPSG 4326
    		#print point.GetX(), point.GetY()

			nelement += 1
			lon = point.GetX()
			lat = point.GetY()

			#point_utm = utm.from_latlon(lat, lon)
			#x = str(point_utm[0])
			#y = str(point_utm[1])

			if (nelement==1):
				queryBody = queryBody +  " " + str(lat) + " " + str(lon)
			else:
				queryBody = queryBody + "," + str(lat) + " " + str(lon)			

			query = queryHeader + queryBody + queryFooter + ";"
			print query

if __name__ == '__main__':
    main()
