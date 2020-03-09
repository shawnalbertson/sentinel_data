import matplotlib.pyplot as plt
import numpy as np

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """Remap a value from one interval to another.
    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].
    """
# Assumes that input_interval_end > input_interval_start and output_interval_end > output_interval_start
    diff1 = input_interval_end-input_interval_start
    diff2 = output_interval_end-output_interval_start

# Finds the variation in range size as a ratio
    ratio = diff2/diff1

    return output_interval_start + ratio*(val-input_interval_start)

def display(array,resolution = 50):
    """
    Displays original data graphically
    """
    fig = plt.figure(figsize = (12, 12))
    ax = fig.add_subplot(111)
    plt.contourf(array, cmap = "viridis",
    levels = list(range(0, int(np.amax(array))+resolution, resolution)))
    plt.title("Yosemite")
    cbar = plt.colorbar()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
