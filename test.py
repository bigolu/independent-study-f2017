# Take a json
# Read the json
# create a dictionary from the json
# the dictionary should be a list of lists?
# go through pnpoly.py and see what the purpose of the gjson is
# first use a dictionary in a simple manner
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry import MultiPoint
import json
from pprint import pprint
class PolygonThang():
	def __init__(self, geojson):
		gj = self.openGeojson(geojson)
		self.polygons = self.extract_polygons(gj)
	def openGeojson(self, geojson):
		g = json.load(open(geojson))
		return g
	def extract_polygons(self, geojson):
		return [polygon['geometry']['coordinates'][0] 
                for polygon
                in geojson['features']] 

polygonthing = PolygonThang("data/polygons/estonia_lithuania.geojson")
#Polygonthing.polygons is a list of polygons, which have a list of points
print("POLYGONS: " + str(len(polygonthing.polygons)))

polygon1 = MultiPoint(polygonthing.polygons[0]).convex_hull
polygon2 = MultiPoint(polygonthing.polygons[1]).convex_hull

point = Point(2.1, 2.1)

print("Does polygon contain point? " + str(polygon1.contains(point)))
print("Does polygon contain point/overlap? " + str(polygon1.intersects(point)))




