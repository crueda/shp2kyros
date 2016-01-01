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
vRoute = []

LOG_FOLDER = "/var/log/correos/shp2kyros.log"

queryHeader = "INSERT INTO routes (SHAPE) VALUES ( GeomFromText( \' LineString("
queryFooter = ") \' ) )"

# Spatial Reference System
inputEPSG = 3857
outputEPSG = 4326

########################################################################

# definimos los logs internos que usaremos para comprobar errores
try:
	logger = logging.getLogger('shp2kyros')
	loggerHandler = logging.handlers.TimedRotatingFileHandler(LOG_FOLDER, 'midnight', 1, backupCount=10)
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	loggerHandler.setFormatter(formatter)
	logger.addHandler(loggerHandler)
	logger.setLevel(logging.DEBUG)
except:
	print '------------------------------------------------------------------'
	print '[ERROR] Error writing log at %s' % LOG_FOLDER 
	print '[ERROR] Please verify path folder exits and write permissions'
	print '------------------------------------------------------------------'
	exit()

########################################################################
# Definicion de clases
#
########################################################################

class Route():
	cod = None
	vPoint = []
	def __init__(self, cod):
		self.cod = cod

class Point():
	sequence = None
	description = None
	hour_out = None
	hour_in = None
	lat = None
	lon = None
	def __init__(self, sequence, description, hour_out, hour_in, lat, lon):
		self.sequence = sequence
		self.description = description
		self.hour_out = hour_out
		self.hour_in = hour_in
		self.lat = lat
		self.lon = lon

def searchRoute(cod):
	global vRoute
	for route in vRoute:
		if (route.cod == cod):
			return route
	return None

def main():
	
	# Leer nombre de fichero shapefile
	file_name = sys.argv[1]

	# fichero sql de salida
	file_out = sys.argv[2]
	fichero_sql = open(file_out, 'w')

    # create coordinate transformation
	inSpatialRef = osr.SpatialReference()
	inSpatialRef.ImportFromEPSG(inputEPSG)
	outSpatialRef = osr.SpatialReference()
	outSpatialRef.ImportFromEPSG(outputEPSG)

	logger.info("Abriendo shapefile: " + file_name)

	with fiona.open(file_name, 'r') as input:
		nelement = 0
  		for pt in input:
  			# Propiedades especificas
			codigo = pt['properties']['COD_RUTA']
			secuencia = pt['properties']['NUM_SECUEN']
			descripcion = pt['properties']['DES_PUNTO_']
			llegada = pt['properties']['FEC_LLEGAD']
			salida = pt['properties']['FEC_SALIDA']
    		    		
    		# Coordenadas
			pointX = shape(pt['geometry']).x
			pointY = shape(pt['geometry']).y

    		# create a geometry from coordinates and transform
			point = ogr.Geometry(ogr.wkbPoint)
			point.AddPoint(pointX, pointY)
			coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
			point.Transform(coordTransform)

			longitude = point.GetX()
			latitude = point.GetY()

			logger.debug ("-> PUNTO DE RUTA: " + str(codigo))
			logger.debug ("	  - Secuencia: 		 " + str(secuencia))
			logger.debug ("	  - Descripcion: 	 " + str(descripcion))
			logger.debug ("	  - Hora de llegada: " + str(llegada))
			logger.debug ("	  - Hora de salida:  " + str(salida))
			logger.debug ("	  - Latitud:  		 " + str(latitude))
			logger.debug ("	  - Longitud:  		 " + str(longitude))

			newPoint = Point(secuencia, descripcion, salida, llegada, latitude, longitude)
			route = searchRoute(codigo)
			if (route != None):
				route.vPoint.append (newPoint)
			else:
				newRoute = Route (codigo)
				newRoute.vPoint.append (newPoint) 
				vRoute.append (newRoute)

	#Escribir en fichero de salida
	logger.info("Escribiendo fichero de salida: " + file_out)

	for route in vRoute:
		nelement = 0
		queryBody = ""
		for point in route.vPoint:
			nelement += 1
			if (nelement==1):
				queryBody = queryBody +  " " + str(point.sequence) + " " + str(point.description)
				#queryBody = queryBody +  " " + str(point.lat) + " " + str(point.lon)
			else:
				queryBody = queryBody + "," + str(point.sequence) + " " + str(point.description)			
				#queryBody = queryBody + "," + str(point.lat) + " " + str(point.lon)			
		query = queryHeader + queryBody + queryFooter + ";"
		logger.info(str(query)+"\n")
		fichero_sql.writelines(str(query)+"\n")
		

	fichero_sql.close

if __name__ == '__main__':
	main()
