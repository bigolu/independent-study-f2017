
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry import MultiPoint
import json
class PolygonGrid():
    DEFAULT_X = 10
    DEFAULT_Y = 10

    #geoJson is just a dictionary
    #geoJson isn't the file, it's when it's loaded in already
    #we need to initilize the grid before we 
    def __init__(self, geojson, x=DEFAULT_X, y=DEFAULT_Y):
        self.x = x or self.DEFAULT_X
        self.y = y or self.DEFAULT_Y
        gj = self.makeGeojson(geojson)
        self.polygons = self.extract_polygons(gj)
        self.minx, self.miny, self.maxx, self.maxy = \
            self.get_minmax(self.polygons)
        self.xstep, self.ystep = self.get_step()
        self.grid = self.init_grid()

    def makeGeojson(self, geojson):
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
        #populating grid to see which regions are associated with empty boxes in 2D grid
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (len(grid[i][j])) == 0:
                    x, y = self.findCoordinatesInBox(i,j)
                    regionList = self.findRegion(x,y)
                    for k in range(len(regionList)):
                        grid[i][j].append(regionList[k])
        return grid
                    
    def findCoordinatesInBox(self,i,j):
        x = i*self.xstep
        latx = ((self.maxx - self.minx) - x) + self.minx;
        y = j*self.ystep + self.miny
        return latx,y

    def findRegion(self, x, y):
        point = Point(x,y)
        regionList = []
        for i in range(len(self.polygons)):
            polygon = MultiPoint(self.polygons[i]).convex_hull
            if((polygon.contains(point)) or (polygon.intersects(point))):
                regionList.append(i)
        return regionList
                
    
    def extract_polygons(self, geojson): #array of all the regions
        return [polygon['geometry']['coordinates'][0] #list of all the coordinates
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

    def point_to_grid_index(self, x, y):
        return ((x - self.minx) / self.xstep,
                (y - self.miny) / self.ystep)

    def get_canidate_polygons(self, x, y):
        gridx, gridy = self.point_to_grid_index(x, y)
        candidates = self.grid_regions[gridx][gridy]
        return(candidates) #listOfIntegers
        #candidate polygons are indexes, grabbing from self.grid. 
        

#this pnpoly is after preprocessing because it's using get candidate polygons
def pnpoly(geojson, points):
    p_grid = PolygonGrid(geojson)
    occurences = [0 * len(p_grid.polygons)] 

    for point in points:
        x, y = point[1], point[0]
        canidate_polygons = p_grid.get_canidate_polygons(x, y)
        #run pn poly on that set of coordinates and the polygons
        for polygon_index in canidate_polygons:

            polygon = p_grid.polygons[polygon_index] #polygon is a list of lists, inner lists are long and lat'

            in_polygon = False
            # see if these points are in the poly

            if in_polygon:
                occurences[polygon_index] += 1
                break

    return occurences

if __name__ == '__main__':
    pass




polygon_grid = PolygonGrid("../data/polygons/estonia_lithuania.geojson")


for i, polygon in enumerate(polygon_grid.grid):
    print(i, polygon)
    print("\n")






