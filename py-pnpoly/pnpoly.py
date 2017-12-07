class PolygonGrid():
    DEFAULT_X = 50
    DEFAULT_Y = 50

    def __init__(self, geojson, x=DEFAULT_X, y=DEFAULT_Y):
        self.x = x or self.DEFAULT_X
        self.y = y or self.DEFAULT_Y
        self.polygons = self.extract_polygons(geojson)
        self.minx, self.miny, self.maxx, self.maxy = \
            self.get_minmax(self.polygons)
        self.xstep, self.ystep = self.get_step()
        self.grid = self.init_grid()

    def init_grid(self):
        grid = [[]*self.y for i in range(self.x)]

        for i, polygon in enumerate(self.polygons):
            for point in polygon:
                x, y = ((point[1]-self.miny) / self.ystep,
                        (point[0]-self.minx) / self.xstep)

                grid[x][y].append(i)

        return grid

    def extract_polygons(self, geojson):
        return [polygon['geometry']['coordinates'][0]
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
        gridx, gridy = self.pointToGridIndex(x, y)
        candidates = self.grid_regions[gridx][gridy]
        return(candidates)


def pnpoly(geojson, points):
    p_grid = PolygonGrid(geojson)
    occurences = [0 * len(p_grid.polygons)]

    for point in points:
        x, y = point[1], point[0]
        canidate_polygons = p_grid.get_canidate_polygons(x, y)

        for polygon_index in canidate_polygons:
            polygon = p_grid.polygons[polygon_index]
            # do pnpoly
            in_polygon = False
            # ughhhh

            if in_polygon:
                occurences[polygon_index] += 1
                break

    return occurences


if __name__ == '__main__':
    pass
