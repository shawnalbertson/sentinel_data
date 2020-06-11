# sentinel_data
## Overview
This project is a part of Encarna Medina-Lopez's work at the University of Edinburgh.
It is designed to interpret GeoTIFF files from the Sentinel-2 MultiSpectral Instrument
which gathers satellite data from across the globe. More information about this data
can be found here: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2.

The scripts runProcessing.py and gdalClasses.py work to load and read the
data in from a Sentinel-2 GeoTIFF file, identify the presence of clouds, and use this
information to modify another GeoTIFF file.

## Libraries

### GDAL
Follow instructions at: https://gdal.org/download.html

### Matplotlib
Follow instruction at: https://matplotlib.org/users/installing.html

### NumPy
Follow instructions at: https://scipy.org/install.html

### Pandas
Follow instructions at: https://pandas.pydata.org/getting_started.html

### mplcursors
Follow instructions at: https://pypi.org/project/mplcursors/

## Running the program
Download the appropriate libraries and scripts from this repository.

Open runProcessing.py in a text editor. In the function chooseFile(), change the
file names to match their location on your machine.

You need two files to run these scripts. The raw file from Sentinel-2 should be
called original_file, and the processed file from Medina-Lopez's neural net should
be called processed_file.

To change specifics about the Matplotlib visualization, changes should be made
in the geoDisplay() function in runProcessing.py. 
