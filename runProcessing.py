import gdal
import osr
import numpy as np
import numpy.ma as ma
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import mplcursors

from gdalClasses import *

def chooseFile():
    """
    Choose which image you would like to visualize

!!    Change file locations for your computer     !!
    """

    desired = input("'a'-> aveiro | 'b' -> britain | 'c' -> cayo_largo | 'k' -> kuwait: ")

    if desired == "a":
        original_file = "files/aveiro.tif"
        processed_file = "files/aveiro_processed.tif"
        return original_file, processed_file
    elif desired == "b":
        original_file = "files/britain.tif"
        processed_file = "files/britain_processed.tif"
        return original_file, processed_file
    elif desired == "c":
        original_file = "files/cayo_largo.tif"
        processed_file = "files/cayo_largo_processed.tif"
        return original_file, processed_file
    elif desired == "k":
        original_file = "files/kuwait.tif"
        processed_file = "files/kuwait_processed.tif"
        return original_file, processed_file

    else:
        print("This is not a region you have defined")
        chooseFile()
    return



def makeCloudMask(band, cloudBand):
    """
    Arguments:
        band: processed Band object, salinity or temperature
        cloudBand: cloud mask Band object from original image

    Returns:
        New numpy array with clouds set to np.nan
    """


# Make sure the cloudBand really has information about clouds
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

    return band.array

def getCoords(data):
    """
    Arguments:
        data: Data object containing original metadata
        band: Band object containing array of values
    Returns:
        pair of 2 tuples with geographic bounds of image
    """
# Get the geo transform matrix
    xoffset, px_w, rot1, yoffset, px_h, rot2 = data.dataObject.GetGeoTransform()

# get CRS from dataset
    crs = osr.SpatialReference()
# Grabs this information from Data class
    crs.ImportFromWkt(data.dataObject.GetProjectionRef())

# Create lat/long crs with WGS84 datum
    crsGeo = osr.SpatialReference()
    crsGeo.ImportFromEPSG(4326) #4326 is the EPSG id of lat/long crs

    t = osr.CoordinateTransformation(crs, crsGeo)

# Initialize list to use later as pandas DataFrame
    latList = []
    longList = []

# X and y are pixel location, used to convert to coordinate in space
    for x in range(data.cols):
        for y in range(data.rows):
            posX = px_w * x + rot1 * y + xoffset
            posY = rot2 * x + px_h * y + yoffset

            (lat, long, z) = t.TransformPoint(posX, posY)

# Add to list containing lat, long, and relevant data
            latList.append(lat)
            longList.append(long)

# Find geographic bounds by finding first and last value
    latBounds = (latList[0], latList[-1])
    longBounds = (longList[0], longList[-1])

    return latBounds, longBounds


def makeDataFrame(data, band, cloudBand):
    """
    Arguments:
        data: Data object containing original metadata
        band: Band object containing array of values
        cloudBand: cloud mask Band object from original image

    Returns:
        Pandas DataFrame of data with appropriate latitude and longitude values
    """
# Get array, filtering clouds
    array = makeCloudMask(band, cloudBand)

# latBounds and longBounds are each 2 tuples with first and last lat and long
    latBounds, longBounds = getCoords(data)

# Create lists of latitudes and longitudes based on the size of the original image
# This ensures no conflict with dimensions later on
    lats = np.linspace(latBounds[0], latBounds[-1], data.rows)
    longs = np.linspace(longBounds[0], longBounds[-1], data.cols)

# Create pandas DataFrame
    df = DataFrame(array, index=lats, columns=longs)

    return df


def geoDisplay(data, band, cloudBand):
    """
    Arguments:
        data: Data object containing original metadata
        band: Band object containing array of values
        cloudBand: cloud mask Band object from original image

    Results in matplotlib countour plot of data
    """
    df = makeDataFrame(data, band, cloudBand)

    Longitude = df.columns.values
    Y = df.index.values
    Z = df.values
    x,y = np.meshgrid(Longitude, Y)


    resolution = int(input("Choose graphic resolution (5 is a good place to start): "))
    cf = plt.contourf(x,y,Z, cmap = "ocean",
# Change the resolution of the contour plot by changing the last number in range
    levels = list(range(band.lowerCutoff, band.upperCutoff, resolution)))

    plt.title("%s" % band.name)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    cbar = plt.colorbar(shrink = .75, orientation = 'horizontal')
    cbar.ax.set_xlabel('%s in %s' % (band.name, band.unit))
    plt.gca().set_aspect('equal', adjustable='box')


# Add click to show data point feature
    cursor =  mplcursors.cursor()
# The next eight lines taken from https://mplcursors.readthedocs.io/en/stable/examples/contour.html
    @cursor.connect("add")
    def on_add(sel):
        ann = sel.annotation
        # `cf.collections.index(sel.artist)` is the index of the selected line
        # among all those that form the contour plot.
        # `cf.cvalues[...]` is the corresponding value.
        ann.set_text("{}\nz={:.3g}".format(
            ann.get_text(), cf.cvalues[cf.collections.index(sel.artist)]))

    plt.show()


def run(temp, salinity):
    """
    Arguments:
        temp: data from processed image containing temperature information
        salinity: data from processed image containing salinity information
    """
# Asks for input so you can choose which graphic to visualize
    take = input("'t' -> temperature, 's' -> salinity: ")

# Displays temp or salinity depending on your input
    if take == "t":
        geoDisplay(prData, temp, cloudBand)
    elif take == 's':
        geoDisplay(prData, salinity, cloudBand)


## Call functions necessary to run program

# Choose which files you want to investigate
original, processed = chooseFile()

# Get cloud information
ogData = Data(original)
cloudBand = Band(ogData, 16, "Cloud Mask")

# Get bands of salinity and temperature - band names should not change
prData = Data(processed)
salinity = Band(prData, 1, "Salinity")
temp = Band(prData, 2, "Temperature")


# Run the program
run(temp, salinity)






#
