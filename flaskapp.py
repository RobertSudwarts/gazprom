import pandas as pd
from openweathermap_requests import *
from geonames_requests import get_timezone

from flask import Flask, render_template, request
from bokeh_chart import forecast_chart
from utils import ts, localized_datetime

app = Flask(__name__)


def forecast_temperatures(params):
    '''request forecast temperatures and return a pandas dataframe of the data
    '''
    forecast_data = forecast_weather_req(params=params)

    # create a dict from the forecast data
    d = {pd.to_datetime(rw['dt_txt']): rw['main'] for rw in forecast_data['list']}

    # create a pandas datafrom from the forecast data
    df = pd.DataFrame.from_dict(d, orient='index')

    return df

def current_weather(params):
    current_data = current_weather_req(params=params)
    return current_data


def timeseries_model(df):
    '''
    There are a million and one ways of computing OLS etc
    '''
    temps = df.temp
    X = pd.Series(range(1, len(temps) + 1), index=temps.index)
    model = pd.ols(y=temps, x=X, intercept=True)

    return model


@app.route('/')
def home():

    loc = request.args.get('city')
    units = request.args.get('units')

    params = {
        'q': loc if loc else 'London,uk',
        'units': units if units else 'metric'
    }

    print loc, units

    df_forecast = forecast_temperatures(params)
    # we can now print out the descriptive data, which is itself a data frame
    descr = df_forecast[['temp','temp_max', 'temp_min']].describe()

    current = current_weather(params)
    current_ico_url = icon_src(current['weather'][0]['icon'])

    tbl = descr.to_html()
    # replace pandas html output class with bootstrap's
    forecast_tbl = tbl.replace(
        'border="1" class="dataframe"',
        'class="table table-striped"'
    )

    model = timeseries_model(df_forecast)

    chart_script, chart_div = forecast_chart(df_forecast,
                                             model.y_fitted,
                                             units if units else 'metric')

    tz = get_timezone(lat=current['coord']['lat'],
                      lng=current['coord']['lon'])

    sunup = localized_datetime(ts(current['sys']['sunrise']), tz)
    sundown = localized_datetime(ts(current['sys']['sunset']), tz)

    return render_template(
        'index.html',
        current_weather=current,
        forecast_temp_descr=forecast_tbl,
        current_icon=current_ico_url,
        chart_script=chart_script,
        chart_div=chart_div,
        sunup=sunup.strftime("%H:%M"),
        sundown=sundown.strftime("%H:%M"),
        model=str(model.summary).replace("\n","<br/>")
        )

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
