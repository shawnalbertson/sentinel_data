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

    band.display(resolution)






#
