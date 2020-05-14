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

# 16th Band has cloud mask where:
#           1 in 2**10 place for opaque clouds and
#           1 in 2**11 place for cirrus clouds


# Make mask to filter clouds array based on parameters above
    cloudMask = ma.masked_where(cloudBand.clean >= 1024, cloudBand.array).mask
    band.array[cloudMask] = np.nan

# Cut values outside of cutoff bounds
    band.array[band.clean > band.upperCutoff]=np.nan
    band.array[band.clean < band.lowerCutoff]=np.nan

# Remove 'filtered' values (previously left for counting)
    band.array[band.clean == np.pi] = np.nan


    band.display(resolution)

def helpLowerCutoff(band, binNum):
    """
    Want to make a histogram to represent where data is
    """
    # band.array[band.clean>band.mean+band.std*3]=0
    binSize, bounds = np.histogram(band.clean[band.clean!=0], binNum)
    print(binSize)
    biggestBin = np.max(binSize)
    print(biggestBin)
    for x in binSize:
        if x > biggestBin*.003:
            binLevel = np.where(binSize==x)[0][0]
            return bounds[binLevel]

    # return bounds[binLevel]





#
