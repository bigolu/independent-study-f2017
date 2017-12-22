#!/bin/bash

# install pip dependencies
. venv/bin/activate
pip install -r requirements.txt

# install geos
cd basemap-1.1.0/geos-3.3.3
export GEOS_DIR="/usr/local"
./configure --prefix=$GEOS_DIR
make; make install
cd ../

# install basemap
python setup.py install
