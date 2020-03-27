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

# ma.masked_where(condition, array).mask returns boolean array
# Condition is based on cloud mask definition from band 16 (see above)

    mask = ma.masked_where(np.nan_to_num(cloudBand.array) >= 1024, cloudBand.array).mask
    band.array[mask] = np.nan
    # print(band.upperCutoff)
    band.display(resolution)
