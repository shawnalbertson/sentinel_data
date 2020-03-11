import numpy as np
import numpy.ma as ma

def cloudFilter(band):
    """
    Assumes that you are passing in band 16 of unprocessed data - cloud mask
    Returns boolean array of clouds
    """
    if band.bandNumber != 16:
        print("This array does not contain cloud mask data!")

    else:
# 16th Band has cloud mask where:
#           1 in 2**10 place for opaque clouds and
#           1 in 2**11 place for cirrus clouds

# ma.masked_where(condition, array).mask returns boolean array
#           False where condition is met (not sure about this)
# Condition is based on cloud mask definition from band 16 (see above)

        return ma.masked_where(band.array == 2048, band.array).mask
