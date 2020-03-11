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
        self.dataObject = gdal.Open(filename)

# Define number of bands in file and x-y size of file
        self.num_bands = self.dataObject.RasterCount
        self.cols = self.dataObject.RasterXSize
        self.rows = self.dataObject.RasterYSize


class Band:
    def __init__(self, dataset, bandNumber):
        self.dataset = dataset
        self.bandNumber = bandNumber

# def getArray(self):
        try:
# GetRasterBand is a method of my 'Data' class's GDAL dataset object
            self.band = dataset.dataObject.GetRasterBand(self.bandNumber)
        except RuntimeError:
            print('Band (%i) not found' % self.bandNumber)
            sys.exit(1)
        self.array = self.band.ReadAsArray().astype(np.float)

# Set all instances of NaN to 0
        self.array[np.isnan(self.array)] = 0

    def display(self, resolution=50):
        """
        Visualize the band using matplot lib contourf
        """
        fig = plt.figure(figsize = (12, 12))
        ax = fig.add_subplot(111)
        plt.contourf(self.array, cmap = "viridis",
        levels = list(range(0, int(np.amax(self.array))+resolution, resolution)))
        plt.title("Example band visualization")
        cbar = plt.colorbar()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def getClouds(self):
        """
        Get information about cloud location to inform cloud mask

        TODO: Use class structure to better store cloudMask array
        """
        if self.dataset.num_bands != 16:
            print("There's no cloud data here! Did you pass in the correct dataset?")
        else:
# 16th Band has cloud mask where:
#           1 in 2**10 place for opaque clouds and
#           1 in 2**11 place for cirrus clouds
# Should be zero otherwise, so >= condition should work (better but longer version commented below)

# Self.clouds is the array from the cloud mask band
            self.clouds = self.getArray(16)

# Use numpy masked module,
# masked_where().mask returns boolean array, anywhere that meets condition returns False
# Condition is based on cloud mask definition from band 16 (see above)

            # opaqueMask = ma.masked_where(self.clouds, self.clouds==1024).mask
            # cirrusMask = ma.masked_where(self.clouds, self.clouds==2048).mask
            # self.cloudMask = np.logical_or(opaqueMask, cirrusMask)

def cloudFilter(band):
    """
    Assumes that you are passing in band 16 of unprocessed data - cloud mask
    Returns boolean array of clouds
    """
    if band.bandNumber != 16:
        print("There's no cloud data here! Did you pass in the correct array?")

    else:
        return ma.masked_where(band.array == 2048, band.array).mask


# Local .tif file locations
og_wlm = 'data/landmask_20161130T110422_20161130T130757_T31UCT.tif'
og_wlm_processed = 'data/landmask_20161130T110422_20161130T130757_T31UCT_processed.tif'




# processed = Data(og_wlm_processed)
# temp = Band(processed, 2)
# temp.display()

unprocessed = Data(og_wlm)
# array1 = Band(unprocessed, 1)
# array1.display(100)
clouds = Band(unprocessed, 16)
print(cloudFilter(clouds).astype(float).sum())
