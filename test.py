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

polygonthing = PolygonThang("data/polygons/districts/districts.geojson")
pprint(polygonthing.polygons)
#Polygonthing.polygons is a list of polygons, which have a list of points
print("POLYGONS: " + str(len(polygonthing.polygons)))

polygon1 = MultiPoint(polygonthing.polygons[0]).convex_hull
polygon2 = MultiPoint(polygonthing.polygons[1]).convex_hull
polygon3 = MultiPoint(polygonthing.polygons[2]).convex_hull
polygon4 = MultiPoint(polygonthing.polygons[3]).convex_hull
print("Polygon 2 is ")

pprint(polygonthing.polygons[1])

pointNot = Point(5, 1)
point1 = Point(114.052612, 22.581395)
point2 = Point(113.85061499999999, 22.525673)
point3 = Point(114.066039, 22.757837)
point4 = Point(114.223908, 22.552209)
#polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
#polygontwo = MultiPoint([[0,1],[0,0],[1,1],[1,0]]).convex_hull

#print(polygon.contains(point))
#print(polygontwo.contains(point))

print("Does polygon contain point? " + str(polygon1.contains(pointNot)))
print("Does polygon contain point? " + str(polygon2.contains(pointNot)))
print("Does polygon contain point? " + str(polygon3.contains(pointNot)))
print("Does polygon contain point? " + str(polygon4.contains(pointNot)))



