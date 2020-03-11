# sentinel_data
## Overview
This project is a part of Encarna Medina-Lopez's work at the University of Edinburgh.
It is designed to interpret GeoTIFF files from the Sentinel-2 MultiSpectral Instrument
which gathers satellite data from across the globe. More information about this data
can be found here: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2.

Specifically, the scripts readtif.py and helperFunctions.py work to load and read the
data in from a Sentinel-2 GeoTIFF file, identify the presence of clouds, and use this
information to modify another GeoTIFF file.

## Libraries

### GDAL
Follow instructions at: https://gdal.org/download.html

### Matplotlib
Follow instruction at: https://matplotlib.org/users/installing.html

### NumPy
Follow instructions at: https://scipy.org/install.html

## Running the program
Download the appropriate libraries and scripts from this repository. Open readtif.py
and change the file names depending on their location on your machine. The current
arrangement assumes you have three files on hand: 2 from Sentinel-2 data and one
which you want to modify. The 2 Sentinel-2 files should be called "original" and
"unprocessed." The final file should be called "processed."

Finally, uncomment one or both of the last two blocks of code and run readtif.py
in python. This will open a matplotlib figure window with the result.
