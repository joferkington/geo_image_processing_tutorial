Geologic Image Processing Tutorial - Transform 2020
--------------------------------------------------

You can find a recording of this tutorial at: https://www.youtube.com/watch?v=3ZvRVB6Eeq4&feature=youtu.be

This repository contains the material for the geologic image processing
tutorial given on June 11th, 2020 at the Transform 2020 virtual
conference.  

There's also an [upcoming workshop](https://www.nordicsrg.com/events) held by
the [Nordic Sedimentary Research Group](https://www.nordicsrg.com/) that will
use this tutorial.

Binder Setup
------------

If you don't have a local python setup yet, you can run this tutorial in your
browser by clicking
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/joferkington/geo_image_processing_tutorial/master?filepath=01%20-%20Introduction.ipynb)

However, there is a limit to how many people can use binder for this repo at
any given time.  If you're comfortable running things locally, consider
following the instructions below. Getting a local python installation set up
will also allow you to work with your own data.

Conda Setup
-----------

The easiest way to get a complete local installation is to use Anaconda.  You
can find an [overview and download
link](https://www.anaconda.com/products/individual) on their main page as well
as [more complete installation
instructions](https://docs.anaconda.com/anaconda/install/).

To create the conda environment for this tutorial run:

```
conda env create -f environment.yml
```

The environment is called `t20-thu-images` to match the Transform2020 slack
channel and avoid conflicts with other tutorial's environment names. To switch
to that environment, you'd use:

```
conda activate t20-thu-images
```

or select the environment when starting anaconda from the gui launcher.  After
that, you'd launch `jupyter` and select the first notebook in this tutorial.

Manual Setup
------------

Alternatively, the requirements for this are quite minimal, and you may already
have what you need installed. This depends on:

  * rasterio
  * matplotlib
  * scipy
  * scikit-image
  * jupyter

Any relatively recent version of the above libraries should be fine. We're not
depending on any bleeding-edge functionality. In principle, these examples
should work with python 2.7 as well as 3.5 or greater.  However, things have
not been tested extensively with python 2.7, and I'd recommend using python 3.5
or greater if you're setting things up from scratch.


