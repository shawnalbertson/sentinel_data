import gdal
import numpy as np
import numpy.ma as ma
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
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




## Trying to figure out geographic location
    def geoTrans(self):
        geoTrans = self.dataObject.GetGeoTransform()
        return geoTrans

    def spatialRef(self):
        spatialRef = self.dataObject.GetSpatialRef()
        return spatialRef

    def projectRef(self):
        projectRef = self.dataObject.GetProjectionRef()
        return projectRef

    def project(self):
        project = self.dataObject.GetProjection()
        return project

##



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

# Make alternative array for comparing (numpy doesn't like '>' with np.nan)
        self.clean = np.nan_to_num(self.array)

# Calculate .5% quantile as cutoff to make visualization cleaner
        quant = .005
        self.lowerCutoff = int(np.quantile(self.clean[self.clean!=0],quant))
        self.upperCutoff = int(np.quantile(self.clean[self.clean!=0],1-quant))


# Gather important statistics accounting for nan
# Standard deviation, mean, min, and max
        self.std = np.nanstd(self.array)
        self.mean = np.nanmean(self.array)
        self.min = int(np.nanmin(self.array))
        self.max = int(np.nanmax(self.array))
        self.length = len(self.array.flatten())


    def display(self, resolution=50):
        """
        Visualize the band using matplot lib contourf
        """
        # fig = plt.figure(figsize = (12, 12))
        # ax = fig.add_subplot(111)

        fig, ax = plt.subplots(figsize = (12,12))
        thisPlot = plt.contourf(self.array, cmap = "ocean",
        levels = list(range(self.lowerCutoff, self.upperCutoff, resolution)))

        plt.title("%s | Lower cutoff = %d, Upper cutoff = %d" % (self.name, self.lowerCutoff, self.upperCutoff))
        cbar = plt.colorbar()
        plt.gca().set_aspect('equal', adjustable='box')


        cursor =  mplcursors.cursor()
        #
        # @cursor.connect("add")
        # def on_add(sel):
        #     ann = sel.annotation
        #     # `cf.collections.index(sel.artist)` is the index of the selected line
        #     # among all those that form the contour plot.
        #     # `cf.cvalues[...]` is the corresponding value.
        #     ann.set_text("{}\nz={:.3g}".format(
        #         ann.get_text(), cf.cvalues[cf.collections.index(sel.artist)]))


# This shows data point on mouse hover - very slow
        # mplcursors.cursor(hover=True)

        plt.show()






# Local .tif file locations
og = 'files/original.tif'
og_wlm = 'files/original_landmask.tif'
og_wlm_processed = 'files/processed_landmask.tif'


# Import all datasets
original = Data(og)
unprocessed = Data(og_wlm)
processed = Data(og_wlm_processed)


# Establish band objects
someUnprocessed = Band(unprocessed, 3, 3, "some landmask")
cloudBand = Band(original, 16, 3, "Cloud Mask")
salinity = Band(processed, 1, 3, "Salinity")
temp = Band(processed, 2, 3, "Temperature")

# print(original.geoTrans())
# print(original.spatialRef())
# print(original.projectRef())
# print(original.project())


# testArray = salinity
# print(np.count_nonzero(np.isnan(testArray.array)))
# print(np.count_nonzero(testArray.array==0))



# runProcessing(salinity, cloudBand, 10)
# print(salinity.name, make_histogram(salinity))


# runProcessing(temp, cloudBand, 10)
# print(temp.name, make_histogram(temp))
# print(temp.length*.001)

# print(.001*len(salinity.array.flatten()))
