import gdal
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from helperFunctions import *
import time

class Data:
    def __init__(self, filename):
        """
        Create a Dataset object
        Define important Dataset values
        """
# Create a Dataset object from first file location using 'Open'
        self.dataset = gdal.Open(filename)

# Define number of bands in file and x-y size of file
        self.num_bands = self.dataset.RasterCount
        self.cols = self.dataset.RasterXSize
        self.rows = self.dataset.RasterYSize

    def getBandArray(self, bandNumber):
        """
        Create a Band object
        Get data in Band as an array
        Display the array
        """
        try:
            band = self.dataset.GetRasterBand(bandNumber)
        except RuntimeError:
            print('Band (%i) not found' % bandNumber)
            sys.exit(1)
        array = band.ReadAsArray().astype(np.float)

# This line seems unnecessary when using matplotlib.pyplot.contourf
        # array[np.isnan(array)] = 0
        return array

    def display(self, bandArray, resolution=50):
        """
        Visualize the band using matplot lib contourf
        """
        fig = plt.figure(figsize = (12, 12))
        ax = fig.add_subplot(111)
        plt.contourf(bandArray, cmap = "viridis",
        levels = list(range(0, int(np.amax(bandArray))+resolution, resolution)))
        plt.title("Example band visualization")
        cbar = plt.colorbar()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def getClouds(self):
        """
        Get information about cloud location to inform cloud mask

        TODO: Use class structure to better store cloudMask array
        """
        if self.num_bands != 16:
            print("There's no cloud data here! Did you pass in the processed dataset?")
        else:
# 16th Band has cloud mask where:
#           1 in 2**10 place for opaque clouds and
#           1 in 2**11 place for cirrus clouds
# Should be zero otherwise, so >= condition should work (better but longer version commented below)

# Self.clouds is the array from the cloud mask band
            self.clouds = self.getBandArray(16)

# Use numpy masked module,
# masked_where().mask returns boolean array, anywhere that meets condition returns False
# Condition is based on cloud mask definition from band 16 (see above)
            return ma.masked_where(self.clouds == 2048, self.clouds).mask

            # opaqueMask = ma.masked_where(self.clouds, self.clouds==1024).mask
            # cirrusMask = ma.masked_where(self.clouds, self.clouds==2048).mask
            # self.cloudMask = np.logical_or(opaqueMask, cirrusMask)


# Local .tif file locations
og_wlm = 'data/landmask_20161130T110422_20161130T130757_T31UCT.tif'
og_wlm_processed = 'data/landmask_20161130T110422_20161130T130757_T31UCT_processed.tif'

# # Visualize the first band of the unprocessed data
unprocessed = Data(og_wlm)
array = unprocessed.getBandArray(1)
# unprocessed.display(array, 100)

# # Access the processed data
processed = Data(og_wlm_processed)
salinity = processed.getBandArray(1)
temp = processed.getBandArray(2)

# # Attempt to redefine any pixel with cloud cover as 0
# # ~ is logical not, because of logical array being swapped True/False
# temp[~unprocessed.getClouds()] = 0

# # Visualize the processed data
# processed.display(salinity)
# processed.display(temp)
