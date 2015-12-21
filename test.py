import fiona
import utm
import ogr, osr

from shapely.geometry import shape
with fiona.open('./shapefiles/paradasRutas.shp', 'r') as input:
  for pt in input:
    codigo = pt['properties']['COD_RUTA']
    #print codigo
    num_seq = pt['properties']['NUM_SECUEN']
    #print num_seq
    x = str(shape(pt['geometry']).x)
    y = str(shape(pt['geometry']).y)
    
    print pt['geometry']
    #print x + "," + y
           

    pointX = shape(pt['geometry']).x
    pointY = shape(pt['geometry']).y

    # Spatial Reference System
    inputEPSG = 3857
    outputEPSG = 4326

    # create a geometry from coordinates
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(pointX, pointY)

    # create coordinate transformation
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(inputEPSG)

    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(outputEPSG)

    coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

    # transform point
    point.Transform(coordTransform)

    # print point in EPSG 4326
    print point.GetX(), point.GetY()




           #print utm.to_latlon(340000, 5710000, 32, 'U')
           #coord = utm.to_latlon(float(x), float(y), 31, 'U')
           #print coord
