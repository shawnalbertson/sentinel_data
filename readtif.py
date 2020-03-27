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
        self.array = self.band.ReadAsArray().astype(np.float)


        self.std = np.std(self.array)
        self.mean = np.mean(self.array)
        #
        self.upperCutoff = self.mean + self.cutoff * self.std

        # TODO: Figure out why this throws the RuntimeWarning for invalid value
        # TODO: Figure out a good way to cut lower bounded data in the 1-10 range
        #           Maybe try to visualize data distribution in a histogram
        self.array[np.nan_to_num(self.array) > self.upperCutoff] = np.nan


        self.max = int(np.amax(np.nan_to_num(self.array)[np.nonzero(np.nan_to_num(self.array))]))
        self.min = int(np.amin(np.nan_to_num(self.array)[np.nonzero(np.nan_to_num(self.array))]))

        # print(self.name, " ", self.max, self.min, "stds (old,new): %s, %s" % (self.std, self.std_new))


    def display(self, resolution=50):
        """
        Visualize the band using matplot lib contourf
        """
        fig = plt.figure(figsize = (12, 12))
        ax = fig.add_subplot(111)
        thisPlot = plt.contourf(self.array, cmap = "ocean",
        levels = list(range(self.min, self.max+resolution, resolution)))
        plt.title("Temperature data | Clouds present -> 0")
        cbar = plt.colorbar()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def cutAnomolies(self, cutoff):
        """
        Trim any values more than 'cutoff' standard deviations from mean in dataset
        Originally implemented to ignore outliers in salinity processed data
        """

        pass


# Local .tif file locations
og = 'data/20161130T110422_20161130T130757_T31UCT.tif'
og_wlm = 'data/landmask_20161130T110422_20161130T130757_T31UCT.tif'
og_wlm_processed = 'data/landmask_20161130T110422_20161130T130757_T31UCT_processed.tif'

# Import all datasets
original = Data(og)
unprocessed = Data(og_wlm)
processed = Data(og_wlm_processed)


# Establish band objects
cloudBand = Band(original, 16, 4, "Cloud Mask")
salinity = Band(processed, 1, 3, "Salinity")
temp = Band(processed, 2, 3, "Temperature")




# runProcessing(temp, cloudBand, 50)
runProcessing(salinity, cloudBand, 10)





#
