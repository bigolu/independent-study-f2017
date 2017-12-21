#!/usr/bin/env python

import sys
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
import numpy as np
from pathlib2 import Path
from pnpoly import pnpoly

DELTA_X = .5
DELTA_Y = .5
DELTA_Y_SCALE_FACTOR = 10


def get_map_boundaries(map_file):
    with map_file.open() as f:
        geojson = json.load(f)
        polygon_coords = [polygon['geometry']['coordinates'][0]
                          for polygon
                          in geojson['features']]
        all_coords = [coord_pair
                      for coord_list
                      in polygon_coords
                      for coord_pair
                      in coord_list]

        llcrnrlon = min([coord_pair[0] for coord_pair in all_coords])
        llcrnrlat = min([coord_pair[1] for coord_pair in all_coords])
        urcrnrlon = max([coord_pair[0] for coord_pair in all_coords])
        urcrnrlat = max([coord_pair[1] for coord_pair in all_coords])

        return (llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat)


def csv_rows(csv_file, indices, formatters):
    with open(csv_file, 'rb') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            new_row = [row[index] for index in indices]
            new_row = [formatters[i](new_row[i]) for i in range(new_row)]
            yield new_row


def render_map(map_shp_filename, map_geojson_filename, points_filename):
    map_shp = Path(map_shp_filename)
    map_geojson = Path(map_geojson_filename)
    points_file = Path(points_filename)

    assert map_shp.exists(), 'Could not find {}'.format(map_shp)
    assert map_geojson.exists(), 'Could not find {}'.format(map_geojson)
    assert points_file.exists(), 'Could not find {}'.format(points_file)

    # TODO: figure out what this stuff does
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_axis_off()
    ax.azim = 270
    ax.dist = 7
    ax.set_title('3D Bar Plot')

    # define map boundaries
    map_boundaries = get_map_boundaries(map_geojson)
    map = Basemap(llcrnrlon=map_boundaries[0], llcrnrlat=map_boundaries[1],
                  urcrnrlon=map_boundaries[2], urcrnrlat=map_boundaries[3],)

    # get map data
    # remove filename extension
    map_shp_filename = map_shp_filename.replace('.shp', '')
    map_data = map.readshapefile(map_shp_filename, 'map')
    shenzhen_region_boundaries = map_data[4]

    # draw map
    ax.add_collection3d(shenzhen_region_boundaries)

    # load points TODO: this in the polygon file
    points = csv_rows(points_filename, [1, 2], [float, float])

    # load polygons
    polygons = None
    with open(map_geojson_filename, 'r') as f:
        geojson = json.load(f)
        polygons = [polygon['geometry']['coordinates'][0]
                    for polygon
                    in geojson['features']]

    # create centroid list (where the bars will be placed in each polygon)
    centroids = []
    for polygon in polygons:
        lon_avg = np.mean([point[0] for point in polygon])
        lat_avg = np.mean([point[1] for point in polygon])
        centroids.append([lon_avg, lat_avg])

    # get occurences of points in polygons
    occurences = pnpoly(polygons, points_filename)
    # feature scale occurences
    occurences_min = min(occurences)
    occurences_max = max(occurences)
    occurences_range = occurences_max - occurences_min
    occurences = [float((occurence - occurences_min)) / float(occurences_range)
                  for occurence in occurences]
    # scale occurences to increase bar height
    occurences = [DELTA_Y_SCALE_FACTOR * occurence
                  for occurence in occurences]

    # convert points for display on a cartesian map
    lons = np.array([point[0] for point in centroids])
    lats = np.array([point[1] for point in centroids])
    x, y = map(lons, lats)
    # convert other map args to np.arrays
    delta_z = np.array(occurences)
    z = np.zeroes(len(x))

    # populate map with bars
    ax.bar3d(x, y, z, DELTA_X, DELTA_Y, delta_z, color='r', alpha=0.8)

    # render map
    plt.show()


if __name__ == '__main__':
    assert len(sys.argv) == 4, ('usage: '
                                'python <map.shp> <map.geojson> <points.csv>'
                                )

    map_shp_filename = sys.argv[1]
    map_geojson_filename = sys.argv[2]
    points_filename = sys.argv[3]
    render_map(map_shp_filename, map_geojson_filename, points_filename)
