

London weather model
-----------------------

tasks:

    * extract min, max and average temperature for single day - done
    * retry decorator for HTTP function - done(!)
    * store data appropriately
        -- data could be stored in numerous formats
           (sqlite, text file, pickled etc) but as the datatype
           returned is JSON, MongoDB is an obvious candidate
    * apply above to forecast series
    * analysis of data set
    * tests for each step of the above

So we're going to have a listener -- problem is that there could
be multiple locations...
Are you actually going to *use* the stored data???

Capped(!!)
collections
  current_location
  forecast_location



Installation
-------------

Install new conda environment using the main requirements file

$ git clone

$ cd weather...

$ conda create -n <envname> --file conda-requirements.txt

Install 'requirements' package from binstar
conda install -c https://conda.binstar.org/rsudwarts requirements

or:

pip install requirements
