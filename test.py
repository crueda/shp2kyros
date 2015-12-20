import fiona
import utm
from shapely.geometry import shape
with fiona.open('./shapefiles/paradasRutas.shp', 'r') as input:
    with open('ho1a.txt', 'w') as output:
       for pt in input:
           #id = pt['properties']['id']
           codigo = pt['properties']['COD_RUTA']
           print codigo
           num_seq = pt['properties']['NUM_SECUEN']
           print num_seq
           #cover = pt['properties']['cover']
           x = str(shape(pt['geometry']).x)
           y = str(shape(pt['geometry']).y)
           #print pt['geometry'].x
           print x + "," + y
           #print utm.to_latlon(340000, 5710000, 32, 'U')
           #coord = utm.to_latlon(float(x), float(y), 31, 'U')
           #print coord
