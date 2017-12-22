from shapely.geometry import Point
from shapely.geometry import MultiPoint
import json
import csv


class PolygonGrid():

    DEFAULT_X = 20
    DEFAULT_Y = 20

    def __init__(self, polygons, x=DEFAULT_X, y=DEFAULT_Y):
        self.x = x
        self.y = y
        self.polygons = [MultiPoint(polygon).convex_hull
                         for polygon in polygons]
        self.minx, self.miny, self.maxx, self.maxy = self.get_minmax()
        self.xstep, self.ystep = self.get_step()
        self.grid = self.init_grid()

    def init_grid(self):
        grid = [[[] for x in range(self.x+1)] for y in range(self.y+1)]

        for i, polygon in enumerate(self.polygons):
            for lon, lat in polygon.exterior.coords:
                # converting a latitude coordinate to the x, y format
                # of a 2D matrix
                x, y = self.point_to_grid_index(lon, lat)
                grid[x][y].append(i)

        self.populate_grid(grid)

        return grid

    def populate_grid(self, grid):
        # Goes through initialized grid to populate the empty boxes with
        # correct region
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                x, y = self.find_coordinates_in_box(i, j)
                grid[i][j].extend(self.find_regions(x, y))
                grid[i][j] = list(set(grid[i][j]))

    def find_coordinates_in_box(self, i, j):
        # Given i,j of a 2D matrix, return appropriate latitude and longitude
        lon = float(i) * self.xstep
        lat = float(j) * self.ystep

        return (lon, lat)

    def find_regions(self, x, y):
        # Given latitude and longitude, return regions associated
        # with those coordinates
        point = Point(x, y)
        region_list = [i for i, polygon in enumerate(self.polygons)
                       if polygon.contains(point) or polygon.intersects(point)]

        return region_list

    def get_minmax(self):
        minx, miny, maxx, maxy = float('inf'), float('inf'), 0.0, 0.0

        for polygon in self.polygons:
            cur_minx, cur_miny, cur_maxx, cur_maxy = polygon.bounds
            minx = min(minx, cur_minx)
            miny = min(miny, cur_miny)
            maxx = max(maxx, cur_maxx)
            maxy = max(maxy, cur_maxy)

        return (minx, miny, maxx, maxy)

    def get_step(self):
        return ((self.maxx - self.minx) / float(self.x),
                (self.maxy-self.miny) / float(self.y))

    def point_to_grid_index(self, lon, lat):
        # Latitude system is ascending as it goes up, whilst 2D matrix ascends
        # going down.
        x = int((lon - self.minx) / self.xstep)
        y = int((lat - self.miny) / self.ystep)

        return x, y

    def get_candidate_polygons(self, lon, lat):
        x, y = self.point_to_grid_index(lon, lat)
        candidates = self.grid[x][y]

        return candidates

    def __str__(self):
        return '\n\n'.join(['{}: {}'.format(i, row)
                            for i, row in enumerate(self.grid)])


def csv_rows(csv_file, indices, formatters):
    with open(csv_file, 'rb') as f:
        csv_reader = csv.reader(f, delimiter=' ')

        for row in csv_reader:
            new_row = [row[index] for index in indices]
            new_row = [formatters[i](new_row[i]) for i in range(len(new_row))]

            yield new_row


def pnpoly(polygons, points_path):
    points = csv_rows(points_path, [1, 2], [float, float])
    p_grid = PolygonGrid(polygons)
    occurences = [0] * len(p_grid.polygons)

    for lon, lat in points:
        point = Point(lon, lat)
        candidate_polygons = p_grid.get_candidate_polygons(lon, lat)

        for polygon_index in candidate_polygons:
            polygon = p_grid.polygons[polygon_index]

            if polygon.contains(point):
                occurences[polygon_index] += 1

    return occurences


# tests
if __name__ == '__main__':
    polygons = []
    with open("data/polygons/estonia_lithuania.geojson", 'r') as f:
        geojson = json.load(f)
        tmp = [polygon['geometry']['coordinates'][0]
               for polygon
               in geojson['features']]
        for polygon in tmp:
            polygons.append([tuple(point) for point in polygon])

    polygon_grid = PolygonGrid(polygons)
    print polygon_grid
