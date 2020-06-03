import numpy as np
import matplotlib.pyplot as plt
import rasterio as rio
import scipy.ndimage

from context import data
from context import utils

with rio.open(data.gebco.seamounts, 'r') as src:
    bathy = src.read(1)
    cellsize = src.transform.a # Cells are square and N-S in this case

# First let's try a simple threshold based on absolute depth
# Depth in meters
simple_threshold = bathy > -3500

# Next let's try thresholding based on being more than 500m above a local
# Average within a 0.5 degree moving window.
background = scipy.ndimage.uniform_filter(bathy, int(0.5 / cellsize))
better_threshold = bathy > (background + 500)

# And we'll apply some cleanup to the thresholded result
filled = scipy.ndimage.binary_fill_holes(better_threshold)
cleaned = scipy.ndimage.median_filter(filled, 15)
labels, count = scipy.ndimage.label(cleaned)

# And now let's compare all of those operations
fig, ax = plt.subplots()
ax.imshow(bathy, cmap='Blues_r', vmax=0, label='Bathymetry')

layers = [
    ax.imshow(np.ma.masked_equal(simple_threshold, 0), label='Simple'),
    ax.imshow(background, cmap='Blues_r', vmax=0, vmin=bathy.min(),
              label='Filtered Bathy'),
    ax.imshow(np.ma.masked_equal(better_threshold, 0), label='Better'),
    ax.imshow(np.ma.masked_equal(filled, 0), label='Filled'),
    ax.imshow(np.ma.masked_equal(cleaned, 0), label='Cleaned'),
    ax.imshow(np.ma.masked_equal(labels, 0), label='Labeled'),
]

utils.Toggler(*layers).show()
