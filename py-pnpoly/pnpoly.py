
import json
class PolygonGrid():
    DEFAULT_X = 50
    DEFAULT_Y = 50

    #geoJson is just a dictionary
    #geoJson isn't the file, it's when it's loaded in already
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
        print(self.y)
        print(self.x)
        #grid = [[]*self.y for i in range(self.x)] 
        grid = [[[] for x in range(self.x+1)] for y in range(self.y+1) ]

        for i, polygon in enumerate(self.polygons):
            print("This thing: " + str(i))
            for point in polygon:
                print("point" + str(point))
                x, y = ((point[1]-self.minx) / self.xstep,
                        (point[0]-self.miny) / self.ystep)
                x = int(x)
                print(str(x) + " and " + str(y))
                y = int(y)
                grid[x][y].append(i)
        return grid

    def extract_polygons(self, geojson): #array of all the regions
        return [polygon['geometry']['coordinates'][0] #list of all the coordinates
                for polygon
                in geojson['features']] 
                
    def get_minmax(self, polygons):
        minx, miny, maxx, maxy = float('inf'), float('inf'), 0.0, 0.0
        for i, polygon in enumerate(polygons):
            for point in polygon:
                y, x = point
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


"""

polygon_grid = PolygonGrid("../data/polygons/estonia_lithuania.geojson")


print("steps: :::")
print(polygon_grid.xstep)

print(polygon_grid.ystep)
for i, polygon in enumerate(polygon_grid.grid):
    print(i, polygon)
    print("\n")
"""   





