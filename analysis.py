import pandas as pd
from openweathermap_requests import *

UNITS = 'metric'
params = {'q': 'London', 'units': UNITS}
forecast_data = forecast_weather_req(params=params)

# create a dict from the forecast data
d = {pd.to_datetime(rw['dt_txt']): rw['main'] for rw in forecast_data['list']}

# create a pandas datafrom from the forecast data
df = pd.DataFrame.from_dict(d, orient='index')

# we can now print out the descriptive data, which is itself a data frame
descr = df[['temp','temp_max', 'temp_min']].describe()

'''
descr.columns gives us
Index([u'temp', u'temp_max', u'temp_min'], dtype='object')

type(descr.temp)
Out[17]: pandas.core.series.Series

so to get the mean temperature:
descr.temp['mean']
the minimum
descr.temp['min']

There's not that much to say, really...

I want a flask app... which will query and show the data
The bokeh plot we can figure out at the end...
'''
