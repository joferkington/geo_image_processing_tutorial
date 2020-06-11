import numpy as np
import matplotlib.pyplot as plt
import skimage.io
import skimage.segmentation
import skimage.measure
import scipy.ndimage

from context import data
from context import utils

# Amphibolite under cross polars (from BGS, see data/bgs_rock/README.md)
xpl_rgb = skimage.io.imread(data.bgs_rock.amphibolite_xpl)

# Let's use the center of the image to avoid needing to worry about the edges.
xpl_rgb = xpl_rgb[500:3000, 1000:4000, :]

# This attempts to group locally similar colors. It's kmeans in 5 dimensions
# (RGB + XY).  N_segments and compactness are the main "knobs" to turn.
grains = skimage.segmentation.slic(xpl_rgb, sigma=0.5, multichannel=True,
                                   n_segments=1500, compactness=0.1)

# It's hard to color each grain with a unique color, so we'll show boundaries
# in yellow instead of coloring them like we did before.
overlay = skimage.segmentation.mark_boundaries(xpl_rgb, grains)

# Now let's extract information about each individual grain we've classified.
# In this case, we're only interested in orientation, but there's a lot more
# we could extract.
info = skimage.measure.regionprops(grains)

# And calculate the orientation of the long axis of each grain...
angles = []
for item in info:
    cov = item['inertia_tensor']
    azi = np.degrees(np.arctan2((-2 * cov[0, 1]), (cov[0,0] - cov[1,1])))
    angles.append(azi)

# Make bidirectional (quick hack for plotting)
angles = angles + [x + 180 for x in angles]

# Now display the segmentation and a rose diagram
fig = plt.figure(constrained_layout=True)
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2, projection='polar', theta_offset=np.pi/2,
                      theta_direction=-1)
ax1.imshow(overlay)
ax2.hist(np.radians(angles), bins=60)

ax1.set(xticks=[], yticks=[])
ax2.set(xticklabels=[], yticklabels=[], axisbelow=True)
plt.show()
