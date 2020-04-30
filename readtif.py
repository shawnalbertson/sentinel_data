import gdal
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from helperFunctions import *
import time

class Data:
    """
    Dataset class to hold important values and open file
    """
    def __init__(self, file):
# Create a Dataset object from first file location using 'Open'
        self.dataObject = gdal.Open(file)

# Define number of bands in file and x-y size of file
        self.num_bands = self.dataObject.RasterCount
        self.cols = self.dataObject.RasterXSize
        self.rows = self.dataObject.RasterYSize

class Band:
    """
    Band class to access data from particular band in dataset
    Creates array of data
    """
    def __init__(self, dataset, bandNumber, SDcutoff, name):
        self.dataset = dataset
        self.bandNumber = bandNumber
        self.name = name
        self.cutoff = SDcutoff

# def getArray(self):
        try:
# GetRasterBand is a method of my 'Data' class's GDAL dataset object
            self.band = dataset.dataObject.GetRasterBand(self.bandNumber)
        except RuntimeError:
            print('Band (%i) not found' % self.bandNumber)
            sys.exit(1)

# Get array
        self.array = self.band.ReadAsArray().astype(np.float)

# Gather important statistics accoutning for nan
# Standard deviation, mean, min, and max
        self.std = np.nanstd(self.array)
        self.mean = np.nanmean(self.array)
        self.min = int(np.nanmin(self.array))
        self.max = int(np.nanmax(self.array))



        self.upperCutoff = int(self.mean + self.cutoff * self.std)
        # self.upperCutoff = 180

# This is a hard coded value that may want to change depending on the data
        self.lowerCutoff = 100



    def display(self, resolution=50):
        """
        Visualize the band using matplot lib contourf
        """
        fig = plt.figure(figsize = (12, 12))
        ax = fig.add_subplot(111)
        thisPlot = plt.contourf(self.array, cmap = "ocean",
        levels = list(range(self.lowerCutoff, self.upperCutoff, resolution)))
        plt.title("Temperature")
        cbar = plt.colorbar()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def cutAnomolies(self):
        """
        Trim any values more than 'cutoff' standard deviations from mean in dataset
        Originally implemented to ignore outliers in salinity processed data
        """
        pass
        # self.array[np.nan_to_num(self.array)>self.upperCutoff]=np.nan


# Local .tif file locations
og = 'files/original.tif'
og_wlm = 'files/original_landmask.tif'
og_wlm_processed = 'files/processed_landmask.tif'


# Import all datasets
original = Data(og)
unprocessed = Data(og_wlm)
processed = Data(og_wlm_processed)


# Establish band objects
someUnprocessed = Band(unprocessed, 3, 4, "some landmask")
cloudBand = Band(original, 16, 4, "Cloud Mask")
salinity = Band(processed, 1, 3.5, "Salinity")
temp = Band(processed, 2, 3, "Temperature")

# testArray = salinity
# print(np.count_nonzero(np.isnan(testArray.array)))
# print(np.count_nonzero(testArray.array==0))



runProcessing(temp, cloudBand, 10)
# runProcessing(salinity, cloudBand, 10)
