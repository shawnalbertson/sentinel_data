import gdal, gdalconst
import numpy as np
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """Remap a value from one interval to another.

    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].
    """
# Assumes that input_interval_end > input_interval_start and output_interval_end > output_interval_start
    diff1 = input_interval_end-input_interval_start
    diff2 = output_interval_end-output_interval_start

# Finds the variation in range size as a ratio
    ratio = diff2/diff1

    return output_interval_start + ratio*(val-input_interval_start)



# Register GDAL driver
gdal.AllRegister()

# Local .tif file locations
og_wlm = 'sizewell/landmask_20161130T110422_20161130T130757_T31UCT.tif'
og_wlm_processed = 'sizewell/landmask_20161130T110422_20161130T130757_T31UCT_processed.tif'

# Create a Dataset object from first file location using 'Open'
ds1 = gdal.Open(og_wlm_processed)


# # Raster size, and number of rasters are properties (not methods) of the Dataset object
# Raw data has 16 bands, processed has 2 bands
num_bands = ds1.RasterCount
cols = ds1.RasterXSize
rows = ds1.RasterYSize

# geotransform = ds1.GetGeoTransform()
# originX = geotransform[0]                         # top left x coord (unit?)
# originY = geotransform[3]                         # top left y coord (unit?)
# pixelWidth = geotransform[1]                      # x_dim of pixel (unit?)
# pixelHeight = geotransform[5]                     # y_dim of pixel (unit?)
# print(originX, originY, pixelWidth, pixelHeight)


# # For investigating 1 band at a time
for band in range(1, num_bands + 1):
    num_values = 0
    # Create a Band object, timeout if the band does not exist
    try:
        srcband = ds1.GetRasterBand(band)
    except RuntimeError:
        print('Band (%i) not found' % band)
        sys.exit(1)

# Create numpy array of data entries
    array = srcband.ReadAsArray()
    # print(np.amax(array))
    print(srcband.GetColorInterpretation())


# To figure out how many valid entries are in the array
    # for dimension in array:
    #     for element in dimension:
    #         # if not np.isnan(element):
    #         if element == 0:
    #             num_values += 1
    # print(band, ":", num_values)


    def visualize(array):
        # Find remapping ratio to rescale array within RGB range
        pass














# # Using masked array to view data
# ar = srcband.ReadAsArray()
# mar = np.ma.masked_array(ar, np.isnan(ar))
# print(mar)
