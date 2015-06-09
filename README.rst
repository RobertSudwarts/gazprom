tasks
--------

  * extract min, max and average temperature for single day
  * retry decorator for HTTP function
  * store data appropriately
  * apply above to forecast series
  * analysis of data set
  * tests for each step of the above

Model
-------

The model comprises N distinct parts

  * core functionality to request (REST) data from openweathermaps
  * additional (REST) functionality to return timezones for UTC/date
    conversion from Geonames
  * A client/server model to store data in a MongoDB
  * A flask web application to display, chart and analyse current
    and forecast weather

todos
^^^^^^
The fullest possible model (for multiple users) would be for the web
application to draw its data directly from the database.  The Mongo
client/server modules (stream_current_weather.py & tail_current_weather.py)
use objects which could be extended, parameterised and threaded to query and
store data from multiple (even all!) locations available
(see http://openweathermap.org/help/city_list.txt for the full list)

The flask web application draws its data directly via HTTP request -- this is
only for simplicity's sake.

Once the flask server is running (localhost:5000) the default is to query
London (using metric units) but the following will also work eg:

      localhost:5000
      localhost:5000/?city=Paris,FR
      http://localhost:5000/?city=Paris,FR&units=imperial
      http://localhost:5000/?city=Paris,FR&units=imperial



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
