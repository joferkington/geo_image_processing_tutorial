#! /bin/sh
# From https://www.bgs.ac.uk/data/britrocks/britrocks.cfc?method=viewSamples&sampleId=157565
# Under Open Government License: http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
# Using gdal to retrieve data from IIP viewer
gdal_translate 'IIP:http://www.largeimages.bgs.ac.uk/cgi-bin/iipsrv.fcgi?FIF=/opndata/Petrology_Images/ThinSections_JP2/290000/294119.jp2' N1495_xpl.jpg -of JPEG
gdal_translate 'IIP:http://www.largeimages.bgs.ac.uk/cgi-bin/iipsrv.fcgi?FIF=/opndata/Petrology_Images/ThinSections_JP2/290000/294120.jp2' N1495_ppl.jpg -of JPEG
