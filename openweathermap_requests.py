"""HTTP requests to openweather API

The retry/exception handling is complicated by the fact that if an *unknown*
location (eg 'XXXXX') is queried, rather than returning an HTTP error, a valid
json response is returned but with a message and a results['cod']=='404'.

Remembering that the decorators are dealt with in reverse order ie
@code(@retry(request)), the request is made and only when a response has been
returned (ie @retry has finished), is @code evaluated which will raise a
LocationError if necessary.

Interesting to note that this behaviour has been raised on their forum.
https://openweathermap.desk.com/customer/portal/questions/9944207-list-of-expected-error-codes
"""
import logging
import requests
from retrying import retry

BASE_URL = 'http://api.openweathermap.org/data/2.5/'

logging.basicConfig(level=logging.DEBUG)

__all__ = ['current_weather_req', 'forecast_weather_req', 'icon_src']

class LocationError(Exception):
    '''custom error class'''
    pass


def code(func):
    '''Decorator to evaluate 'code' (the 'response code') supplied by the
       data returned by the call to openweathermap.
    '''
    def wrapper(*args, **kw):
        results = func(*args, **kw)
        # import pdb; pdb.set_trace()
        if 'cod' in results and results['cod'] == '404':
            logging.warning("city was not recognised.")
            raise LocationError
        return results
    return wrapper


@code
@retry(wait_fixed=2000)
def current_weather_req(params={'q': 'London,uk'}, as_json=True):
    """
        Request for current weather
    """
    logging.info("making current weather request")
    url = BASE_URL + 'weather'
    r = requests.get(url, params=params)
    return r.json() if as_json else r


@code
@retry(wait_fixed=2000)
def forecast_weather_req(params={'q': 'London,uk'}, as_json=True):
    """
        Request for forecast weather
    """
    logging.info("making forecast weather request")
    url = BASE_URL + 'forecast/city'
    r = requests.get(url, params=params)

    return r.json() if as_json else r


# return url to be used as `src` for http img
# eg '10d' ->> 'http:.../w/10d.png'
icon_src = lambda code: 'http://openweathermap.org/img/w/' + code + '.png'
