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

The model comprises:

  * core functionality to request (REST) data from openweathermaps
  * additional (REST) functionality to return timezones for UTC/date
    conversion from Geonames
  * unit tests
  * A client/server model to store data in a MongoDB
  * A flask web application to display, chart and analyse current
    and forecast weather

note:  the unit tests use the nose package

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

Once the flask server is running the default (ie http://localhost:5000) is to
query London (using metric units) but the following parameters will also work:

      * http://localhost:5000/?city=Paris,FR
      * http://localhost:5000/?city=Rome,IT&units=imperial
      * http://localhost:5000/?city=Mumbai,IN&units=kelvin


Installation
-------------

$ git clone git@github.com:RobertSudwarts/gazprom.git

A conda-requirements.txt has been included in the repository so the following
should work to create a new conda environment:

  $ conda create -n <env> --file conda-requirements.txt

However, in case of difficulties the following should pretty much cover it:

  $ conda create -n <env> bokeh numpy scipy pandas flask pymongo statsmodels nose

.. warning::
   I am aware of one package which is **not** available directly via conda
   so `$ pip install retrying` will be required in addition.
   I have created a binstar package of the retrying module but you may have
   limited mileage with `conda install -c https://conda.binstar.org/yqe retrying`

Running
----------

For the web application, simply:

  (env) python flaskapp.py

For the data model, two seperate shells/terminals are required,

  * (env) python stream_current_weather.py
  * followed by
  * (env) python tail_current_weather.py
