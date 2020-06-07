"""
Illustrates saving things back to a geotiff and vectorizing to a shapefile
"""
import numpy as np
import matplotlib.pyplot as plt
import rasterio as rio
import rasterio.features
import scipy.ndimage
import fiona
import shapely.geometry as geom

from context import data
from context import utils


# First, let's reproduce the labeled array of seamounts and areas
with rio.open(data.gebco.seamounts, 'r') as src:
    bathy = src.read(1)
    cellsize = src.transform.a # Cells are square and N-S in this case

background = scipy.ndimage.uniform_filter(bathy, int(0.5 / cellsize))
better_threshold = bathy > (background + 500)
cleaned = scipy.ndimage.median_filter(better_threshold, 15)
filled = scipy.ndimage.binary_fill_holes(cleaned)
labels, count = scipy.ndimage.label(filled)

# ------ Save as a geotiff ---------------------------------------------------
# Next, let's save the result as a geotiff. Because our data is the same size
# as the original raster, it's quite straight-forward:

# We'll copy over all settings from the original, but change two...
with rio.open(data.gebco.seamounts, 'r') as src:
    profile = src.profile.copy()

# Background features are 0, so we'll make that nodata/transparent.
profile['nodata'] = 0
profile['dtype'] = labels.dtype

# And let's actually write out the new geotiff...
with rio.open('regions_flagged_as_seamounts.tif', 'w', **profile) as dst:
    dst.write(labels, 1)

# ------ Save as a shapefile -------------------------------------------------
# Now let's vectorize the results and save them as a shapefile

# Just to make things a bit more interesting, let's go ahead and calculate some
# additional information to save in the shapefile's attribute table.
deepest = scipy.ndimage.maximum(bathy, labels, np.arange(count) + 1)
shallowest = scipy.ndimage.minimum(bathy, labels, np.arange(count) + 1)

# We'll need the affine transformation and the projection to go from pixel
# indices to actual locations. Let's grab those from the original geotiff.
with rio.open(data.gebco.seamounts, 'r') as src:
    transform = src.transform
    crs = src.crs

# Now let's specify our output shapefile's format...
meta = {'crs': crs, 'schema': {}, 'driver': 'ESRI Shapefile'}
meta['schema']['geometry'] = 'Polygon'
# And now we'll define the fields in the attribute table
meta['schema']['properties'] = {'raster_id': 'int',
                                'deepest': 'int',
                                'shallowest': 'int'}


# We don't want the background 0 to be a feature, so let's mask it out.
labels = np.ma.masked_equal(labels, 0)

with fiona.open('regions_flagged_as_seamounts.shp', 'w', **meta) as dst:

    vectors = rio.features.shapes(labels, transform=transform, connectivity=8)
    for poly, val in vectors:
        val = int(val) # shapes returns a float, even when the input is ints.

        # The polygon we get here will have stairsteps along each pixel edge.
        # This part is optional, but it's often useful to simplify the geometry
        # instead of saving the full "stairstep" version.
        poly = geom.shape(poly).simplify(cellsize)
        poly = geom.mapping(poly) # Back to a dict

        record = {'geometry': poly,
                  'properties': {'deepest': int(deepest[val-1]),
                                 'shallowest': int(shallowest[val-1]),
                                 'raster_id': val}}
        dst.write(record)
