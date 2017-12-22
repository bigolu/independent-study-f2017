#!/usr/bin/env python

import sys
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
import numpy as np
from pathlib2 import Path
from pnpoly import pnpoly

# width and height, respectively, of bars
DELTA_X = .0030
DELTA_Y = .0030

# colors used for bars
RED = '#ff0000'
YELLOW = '#ffff00'
ORANGE = '#FFA500'


def get_map_minmax(map_file):
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
    map_minmax = get_map_minmax(map_geojson)
    map = Basemap(llcrnrlon=map_minmax[0], llcrnrlat=map_minmax[1],
                  urcrnrlon=map_minmax[2], urcrnrlat=map_minmax[3],)

    # get map data
    # remove filename extension
    map_shp_filename = map_shp_filename.replace('.shp', '')
    map_data = map.readshapefile(map_shp_filename, 'map')
    map_boundaries = map_data[4]

    # draw map
    ax.add_collection3d(map_boundaries)

    # load polygons
    polygons = []
    with open(map_geojson_filename, 'r') as f:
        geojson = json.load(f)
        tmp = [polygon['geometry']['coordinates'][0]
               for polygon
               in geojson['features']]
        for polygon in tmp:
            polygons.append([tuple(point) for point in polygon])

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

    # list of colors for each bar
    colors = [RED if occurence > .66
              else (ORANGE if occurence > .33 else YELLOW)
              for occurence in occurences]

    # convert points for display on a cartesian map
    lons = np.array([point[0] for point in centroids])
    lats = np.array([point[1] for point in centroids])
    x, y = map(lons, lats)
    # convert other map args to np.arrays
    delta_z = np.array(occurences)
    z = np.zeros(len(x))

    # populate map with bars
    ax.bar3d(x, y, z, DELTA_X, DELTA_Y, delta_z, color=colors, alpha=0.8)

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
