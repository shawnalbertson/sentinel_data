import gdal
import numpy as np
import matplotlib.pyplot as plt
from helperFunctions import *


# def display(array,resolution = 50):
#     """
#     Displays original data graphically
#     """
#     fig = plt.figure(figsize = (12, 12))
#     ax = fig.add_subplot(111)
#     plt.contourf(array, cmap = "viridis",
#     levels = list(range(0, int(np.amax(array))+resolution, resolution)))
#     plt.title("Yosemite")
#     cbar = plt.colorbar()
#     plt.gca().set_aspect('equal', adjustable='box')
#     plt.show()

# class Dataset:
#     def __init__(self, filename):



# Register GDAL driver
gdal.AllRegister()

# Local .tif file locations
og_wlm = 'data/landmask_20161130T110422_20161130T130757_T31UCT.tif'
og_wlm_processed = 'data/landmask_20161130T110422_20161130T130757_T31UCT_processed.tif'

# Create a Dataset object from first file location using 'Open'
ds1 = gdal.Open(og_wlm)

# # Raster size, and number of rasters are properties (not methods) of the Dataset object
# Raw data has 16 bands, processed has 2 bands
num_bands = ds1.RasterCount
cols = ds1.RasterXSize
rows = ds1.RasterYSize


# # For investigating 1 band at a time
for band in [1]:
    num_values = 0
    # Create a Band object, timeout if the band does not exist
    try:
        srcband = ds1.GetRasterBand(band)
    except RuntimeError:
        print('Band (%i) not found' % band)
        sys.exit(1)

# Create numpy array of data entries
    array = srcband.ReadAsArray().astype(np.float)
    array[np.isnan(array)] = 0
    display(array)




# To figure out how many valid entries are in the array
    # for dimension in array:
    #     for element in dimension:
    #         # if not np.isnan(element):
    #         if element == 0:
    #             num_values += 1
    # print(band, ":", num_values)



# Hopefully don't need this depending on what Florian's script yields
    # def visualize(array):
    #     # Find remapping ratio to rescale array within RGB range
    #     pass
