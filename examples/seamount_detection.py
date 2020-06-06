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
cleaned = scipy.ndimage.median_filter(better_threshold, 15)
filled = scipy.ndimage.binary_fill_holes(cleaned)
labels, count = scipy.ndimage.label(filled)

# And now let's compare all of those operations
fig, ax = plt.subplots()
ax.imshow(bathy, cmap='Blues_r', vmax=0, label='Bathymetry')

layers = [
    ax.imshow(np.ma.masked_equal(simple_threshold, 0), label='Simple'),
    ax.imshow(background, cmap='Blues_r', vmax=0, vmin=bathy.min(),
              label='Filtered Bathy'),
    ax.imshow(np.ma.masked_equal(better_threshold, 0), label='Better'),
    ax.imshow(np.ma.masked_equal(cleaned, 0), label='Cleaned'),
    ax.imshow(np.ma.masked_equal(filled, 0), label='Filled'),
    ax.imshow(np.ma.masked_equal(labels, 0), label='Labeled', cmap='tab20'),
]

ax.set(xticks=[], yticks=[])
fig.tight_layout()
utils.Toggler(*layers).show()

# Now let's look at area distribution. In this projection (geographic) the area
# of a pixel varies by latitude.
i, j = np.mgrid[:bathy.shape[0], :bathy.shape[1]]
with rio.open(data.gebco.seamounts, 'r') as src:
    lon, lat = src.xy(j, i)

# In square km. ~111.32 is 1 degree in km at the equator
area = (cellsize * 111.32)**2 * np.cos(np.radians(lat))

# Now we'll sum by zone in our labeled seamount array
areas = scipy.ndimage.sum(area, labels, np.arange(count)+1)

# And let's have a look at the distribution...
fig, ax = plt.subplots()
ax.hist(areas, bins=40)
ax.set(xlabel='Area in $km^2$', ylabel='Number of seamounts')
plt.show()
