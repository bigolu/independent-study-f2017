# independent-study-f2017

This script creates a 3D bar plot to visualize the frequency of your data on a map.

![alt text][sample_figure]
<p style="text-align: center;">
cellphone tower usage in Shenzhen, China by region
</p>

## Setup
* from the root directory, run `./setup.sh` ( may require sudo)
* this starts the virtualenv, installs the dependencies and other libraries that [basemap](https://matplotlib.org/basemap/users/installing.html) depends on

## Usage
* run `python <map.shp> <map.geojson> <points.csv>`
* `<map.shp>` this file should be a shapefile describing the map that you would like displayed in the background. If you already have a geojson with this information, you can convert it to a shapefile using this [tool](http://mapshaper.org/)
* `map.geojson` this file should be a geojson describing the map that is displayed in the background. It should contain the same information as `<map.shp>`
* `points.csv` should have the points of the data you want to plot. each row should have the form `1 lon lat *` where 1 represents the first column (this can be anything), followed by the longitude and latitude, followed by any extra data. Everything except for the 2nd and 3rd columns will be ignored.
* sample files have been included in the [sample_data]() directory

## Plot description
* all points will be mapped to a region from `map.geojson` and a bar will be placed in the center of the region where its height reflects how many points were contained in the region
* Bars are color coded where yellow = low number of occurences, orange = medium, and red = high


[sample_figure]: https://github.com/bigolu/independent-study-f2017/raw/master/assets/sample_plot.png "sample figure"
