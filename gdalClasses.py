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

class Band:
    """
    Band class to access data from particular band in dataset
    Creates array of data
    """
    def __init__(self, dataset, bandNumber, name):
        self.dataset = dataset
        self.bandNumber = bandNumber
        self.name = name
        if name == 'Salinity':
            self.unit = 'ppm'
        elif name == 'Temperature':
            self.unit = 'degrees Celsius x10'

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
        quant = .01
        self.lowerCutoff = int(np.quantile(self.clean[self.clean!=0],quant))
        self.upperCutoff = int(np.quantile(self.clean[self.clean!=0],1-quant))


# Gather important statistics accounting for nan
# Standard deviation, mean, min, and max
        self.std = np.nanstd(self.array)
        self.mean = np.nanmean(self.array)
        self.min = int(np.nanmin(self.array))
        self.max = int(np.nanmax(self.array))
        self.length = len(self.array.flatten())


    def display(self, resolution=10):
        """
        Method of band class which can be used to visualize the numpy array
        matplotlib contourf. Does not include geographic information
        """
        fig, ax = plt.subplots(figsize = (12,12))

# Upper and lower bounds determined by cutoffs from quantile filter
        thisPlot = plt.contourf(self.array, cmap = "ocean",
        levels = list(range(self.lowerCutoff, self.upperCutoff, resolution)))

        plt.title("%s | Lower cutoff = %d, Upper cutoff = %d" % (self.name, self.lowerCutoff, self.upperCutoff))
        cbar = plt.colorbar()
        plt.gca().set_aspect('equal', adjustable='box')


        cursor =  mplcursors.cursor()
        plt.show()
