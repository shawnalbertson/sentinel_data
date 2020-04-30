import numpy as np
import numpy.ma as ma

def runProcessing(band, cloudBand, resolution):
    """
        Runs cutAnomolies to trim data of unwanted data/ extremes on a band
        Visualizes the resulting band using numpy contourf
    """

    # band.cutAnomolies(sdLimit)

    if cloudBand.bandNumber != 16:
        print("This array does not contain cloud mask data!")
        return

#     cleanCloud = np.nan_to_num(cloudBand.array)
#     cleanBand = np.nan_to_num(band.array)
#
# 16th Band has cloud mask where:
#           1 in 2**10 place for opaque clouds and
#           1 in 2**11 place for cirrus clouds



# Make array alternative that ignores nan values for comparison
    cleanCloud = np.nan_to_num(cloudBand.array)
    cleanBand = np.nan_to_num(band.array)

# Make mask to filter clouds array
    cloudMask = ma.masked_where(cleanCloud >= 1024, cloudBand.array).mask
    band.array[cloudMask] = np.nan

# Cut values outside of cutoff bounds
    band.array[cleanBand > band.upperCutoff]=np.nan
    band.array[cleanBand < band.lowerCutoff]=np.nan


    band.display(resolution)

def make_histogram(band):
    """
    Want to make a histogram to represent where data is
    """
    np.histogram(band.array)
