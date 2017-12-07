#!/usr/bin/env python

import sys
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
import numpy as np
from pathlib2 import Path

BAR_WIDTH = .5
BAR_HEIGHT = .5


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

    lons = np.array([-13.7, -10.8, -13.2, -96.8, -7.99, 7.5, -17.3, -3.7])
    lats = np.array([9.6, 6.3, 8.5, 32.7, 12.5, 8.9, 14.7, 40.39])
    deaths = np.array([1192, 2964, 1250, 1, 5, 8, 0, 0])
    places = np.array(['Guinea', 'Liberia', 'Sierra Leone','United States', 'Mali', 'Nigeria', 'Senegal', 'Spain'])

    x, y = map(lons, lats)

    ax.bar3d(x, y, np.zeros(len(x)), 2, 2, deaths, color= 'r', alpha=0.8)

    plt.show()


if __name__ == '__main__':
    assert len(sys.argv) == 4, ('Incorrect usage, use this format:\n'
                                'python <map.shp> <map.geojson> <points.csv>'
                                )

    map_shp_filename = sys.argv[1]
    map_geojson_filename = sys.argv[2]
    points_filename = sys.argv[3]
    render_map(map_shp_filename, map_geojson_filename, points_filename)
