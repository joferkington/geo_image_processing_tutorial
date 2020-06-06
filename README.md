Geologic Image Processing Tutorial - Transform 2020
--------------------------------------------------

This repository contains the material for the geologic image processing
tutorial to be given on June 11th, 2020 at the Transform 2020 virtual
conference.  It's currently under very active development and is incomplete,
but feel free to look around and see where things are going!

Conda Setup
-----------

To create the conda environment for this tutorial run:

```
conda env create -f environment.yml
```

The environment is called `t20-thu-images` to match the slack channel and avoid conflicts with other tutorial's environment names.

Alternatively, the requirements for this are quite minimal, and you may already have what you need installed. This depends on:

  * rasterio
  * matplotlib
  * scipy
  * scikit-image

Any relatively recent version of the above libraries should be fine. We're not depending on any bleeding-edge functionality.
