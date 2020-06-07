"""
Example of one possible solution to the "combine nearby seamounts into one"
take-home question.
"""
import numpy as np
import matplotlib.pyplot as plt
import rasterio as rio
import scipy.ndimage

from context import data
from context import utils

# Let's repeat some key steps of `seamount_detection.py` to separate seamounts
with rio.open(data.gebco.seamounts, 'r') as src:
    bathy = src.read(1)
    cellsize = src.transform.a

background = scipy.ndimage.uniform_filter(bathy, int(0.5 / cellsize))
threshold = bathy > (background + 500)

cleaned = scipy.ndimage.median_filter(threshold, 15)
orig_labels, orig_count = scipy.ndimage.label(cleaned)

# Now let's try to combine any seamounts that are within 20 pixels of each other
combined = scipy.ndimage.binary_closing(cleaned, iterations=20)

# And we'll fill holes on the result, as we don't want any doughnuts
filled = scipy.ndimage.binary_fill_holes(combined)

# Separate into non-touching features
final_labels, final_count = scipy.ndimage.label(filled)

# Compare the differences... Note the "tails" connecting features that are just
# barely within the threshold of each other.
fig, ax = plt.subplots()
ax.imshow(bathy, cmap='Blues_r', vmax=0, label='Bathymetry')
ax.set(title=f'{orig_count} Seamounts Before Combining, {final_count} After')

layers = [
    ax.imshow(np.ma.masked_equal(threshold, 0), label='Threshold'),
    ax.imshow(np.ma.masked_equal(cleaned, 0), label='Cleaned'),
    ax.imshow(np.ma.masked_equal(orig_labels, 0), cmap='tab20',
              label='Orig Labels'),
    ax.imshow(np.ma.masked_equal(combined, 0), label='Combined'),
    ax.imshow(np.ma.masked_equal(final_labels, 0), cmap='tab20',
              label='Final Labels'),
]

ax.set(xticks=[], yticks=[])
fig.tight_layout()
utils.Toggler(*layers).show()
