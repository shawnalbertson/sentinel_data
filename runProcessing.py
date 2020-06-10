import gdal
import numpy as np
import numpy.ma as ma
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

from gdalClasses import *

def chooseFile():
    """
    Choose which image you would like to visualize
    """

    desired = input("'a'-> aveiro | 'b' -> britain | 'c' -> cayo_largo | 'k' -> kuwait: ")

    if desired == "a":
        original_file = "files/aveiro.tif"
        processed_file = "files/aveiro_processed.tif"
    elif desired == "b":
        original_file = "files/britain.tif"
        processed_file = "files/britain_processed.tif"
    elif desired == "c":
        original_file = "files/cayo_largo.tif"
        processed_file = "files/cayo_largo_processed.tif"
    elif desired == "k":
        original_file = "files/kuwait.tif"
        processed_file = "files/kuwait_processed.tif"

    else:
        print("This is not a region you have defined")
        chooseFile()
    return original_file, processed_file



def visualize(band, cloudBand, resolution):
    """
        Runs cutAnomolies to trim data of unwanted data/ extremes on a band
        Visualizes the resulting band using numpy contourf
    """

    # band.cutAnomolies(sdLimit)

    if cloudBand.bandNumber != 16:
        print("This array does not contain cloud mask data!")
        return

# 16th Band has cloud mask where:
#           1 in 2**10 place for opaque clouds and
#           1 in 2**11 place for cirrus clouds


# Make mask to filter clouds array based on parameters above
    cloudMask = ma.masked_where(cloudBand.clean >= 1024, cloudBand.array).mask
    band.array[cloudMask] = np.nan

# Cut values outside of cutoff bounds
    band.array[band.clean > band.upperCutoff]=np.nan
    band.array[band.clean < band.lowerCutoff]=np.nan

    band.display(resolution)


def run():
    take = input("'t' -> temperature, 's' -> salinity: ")
    if take == "t":
        visualize(temp, cloudBand, 5)
    elif take == 's':
        visualize(salinity, cloudBand, 5)


original, processed = chooseFile()

# Get cloud information
ogData = Data(original)
cloudBand = Band(ogData, 16, "Cloud Mask")

# Get bands of salinity and temperature
prData = Data(processed)
salinity = Band(prData, 1, "Salinity")
temp = Band(prData, 2, "Temperature")

run()
