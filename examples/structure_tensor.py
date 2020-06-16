"""
Using a structure tensor for lineament analysis.
"""
import numpy as np
import matplotlib.pyplot as plt
import rasterio as rio

from skimage.feature import structure_tensor, structure_tensor_eigvals

from context import data

with rio.open(data.naip.lineaments, 'r') as src:
    image = src.read()

# This assumes a grayscale image. For simplicity, we'll just use RGB mean.
data = image.astype(float).mean(axis=0)

# Compute the structure tensor. This is basically local gradient similarity.
# We're getting three components at each pixel that correspond to a 2x2
# symmetric matrix. i.e. [[axx, axy],[axy, ayy]]
axx, axy, ayy = structure_tensor(data, sigma=2.5, mode='mirror')

# Then we'll compute the eigenvalues of that matrix.
v1, v2 = structure_tensor_eigvals(axx, axy, ayy)

# And calculate the eigenvector corresponding to the largest eigenvalue.
dx, dy = v1 - axx, -axy

# We have a vector at each pixel now.  However, we don't really care about all
# of them, only those with a large magnitude.  Also, we don't need to worry
# about every pixel, as adjacent values are very highly correlated. Therefore,
# let's only consider every 10th pixel in each direction.

# Top 10th percentile of magnitude
mag = np.hypot(dx, dy)
selection = mag > np.percentile(mag, 90)

# Every 10th pixel (skipping left edge due to boundary effects)
ds = np.zeros_like(selection)
ds[::10, 10::10] = True
selection = ds & selection


# Now we'll visualize the selected (large) structure tensor directions both
# superimposed on the image and as a rose diagram...
fig = plt.figure(constrained_layout=True)
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2, projection='polar', theta_offset=np.pi/2,
                      theta_direction=-1)

ax1.imshow(np.moveaxis(image, 0, -1))

y, x = np.mgrid[:dx.shape[0], :dx.shape[1]]

no_arrow = dict(headwidth=0, headlength=0, headaxislength=0)
ax1.quiver(x[selection], y[selection], dx[selection], dy[selection],
           angles='xy', units='xy', pivot='middle', color='red', **no_arrow)


# We actually want to be perpendictular to the direction of change.. i.e.
# we want to point _along_ the lineament. Therefore we'll subtract 90 degrees.
# (Could have just gotten the direction of the smaller eigenvector, but we
# need to base the magnitude on the largest eigenvector.)
angle = np.arctan2(dy[selection], dx[selection]) - np.pi/2
angle = np.concatenate([angle, angle + np.pi]) # Make bidirectional
ax2.hist(angle.ravel(), bins=120, edgecolor='C0', color='C0')

ax1.set(xticks=[], yticks=[])
ax2.set(yticklabels=[], xticklabels=[], axisbelow=True)

plt.show()
