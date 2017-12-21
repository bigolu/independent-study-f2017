from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry import MultiPoint
import json


class PolygonGrid():

    DEFAULT_X = 20
    DEFAULT_Y = 20

    def __init__(self, geojson, x=DEFAULT_X, y=DEFAULT_Y):
        self.x = x or self.DEFAULT_X
        self.y = y or self.DEFAULT_Y
        gj = self.make_geojson(geojson)
        self.polygons = self.extract_polygons(gj)
        self.minx, self.miny, self.maxx, self.maxy = \
            self.get_minmax(self.polygons)
        self.xstep, self.ystep = self.get_step()
        self.grid = self.init_grid()

    def make_geojson(self, geojson):
        g = json.load(open(geojson))
        return g

    def init_grid(self):
        grid = [[[] for x in range(self.x+1)] for y in range(self.y+1) ]
        for i, polygon in enumerate(self.polygons):
            for point in polygon:
                #converting a latitude coordinate to the x, y format of a 2D matrix
                realPoint = (self.maxx - self.minx) - (point[0] - self.minx)
                x, y = (realPoint / self.xstep,
                        (point[1]-self.miny) / self.ystep)
                x = int(x)
                y = int(y)
                grid[x][y].append(i)
        populated_grid = self.populate_grid(grid)
        return populated_grid

    def populate_grid(self, grid):
        #Goes through initialized grid to populate the empty boxes with correct region
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (len(grid[i][j])) == 0:
                    x, y = self.find_coordinates_in_box(i,j)
                    region_list = self.find_regions(x,y)
                    for k in range(len(region_list)):
                        grid[i][j].append(region_list[k])
        return grid
                    
    def find_coordinates_in_box(self,i,j):
        #Given i,j of a 2D matrix, return appropriate latitude and longitude
        x = i*self.xstep
        latit = ((self.maxx - self.minx) - x) + self.minx;
        longit = j*self.ystep + self.miny
        return latit,longit

    def find_regions(self, x, y):
        #Given latitude and longitude, return regions associated with those coordinates
        point = Point(x,y)
        region_list = []
        for i in range(len(self.polygons)):
            polygon = MultiPoint(self.polygons[i]).convex_hull
            if((polygon.contains(point)) or (polygon.intersects(point))):
                region_list.append(i)
        return region_list
                
    def extract_polygons(self, geojson): 
        return [polygon['geometry']['coordinates'][0] 
                for polygon
                in geojson['features']] 
                
    def get_minmax(self, polygons):
        minx, miny, maxx, maxy = float('inf'), float('inf'), 0.0, 0.0
        for i, polygon in enumerate(polygons):
            for point in polygon:
                x, y = point
                maxx = max(maxx, x)
                maxy = max(maxy, y)
                minx = min(minx, x)
                miny = min(miny, y)
        return(minx, miny, maxx, maxy)

    def get_step(self):
        return ((self.maxx - self.minx) / float(self.x),
                (self.maxy-self.miny) / float(self.y))

    def point_to_grid_index(self, latit, longit):
        #Latitude system is ascending as it goes up, whilst 2D matrix ascends going down.
        latitude_to_i_val = (self.maxx - self.minx) - (latit-self.minx) 
        return (latitude_to_i_val / self.xstep,
                (longit - self.miny) / self.ystep)

    def get_candidate_polygons(self, x, y):
        gridx, gridy = self.point_to_grid_index(x, y)
        gridx = int(gridx)
        gridy = int(gridy)
        candidates = self.grid[gridx][gridy]
        return(candidates) 
        

def pnpoly(geojson, points):
    p_grid = PolygonGrid(geojson)
    occurences = [0 * len(p_grid.polygons)] 
    for point in points:
        latit, longit = point[0], point[1]
        candidate_polygons = p_grid.get_candidate_polygons(latit,longit)
        if len(candidate_polygons) == 0:
            continue
        for polygon_index in candidate_polygons:
            polygon = MultiPoint(p_grid.polygons[polygon_index]).convex_hull
            if polygon.contains(point):
                print "true"

if __name__ == '__main__':
    pass




polygon_grid = PolygonGrid("../data/polygons/estonia_lithuania.geojson")
points = [[19,10]]
pnpoly("../data/polygons/estonia_lithuania.geojson", points)

for i, polygon in enumerate(polygon_grid.grid):
    print(i, polygon)
    print("\n")






