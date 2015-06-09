"""
 HTTP requests to Geonames API
"""
import logging
import requests
from retrying import retry

logging.basicConfig(level=logging.DEBUG)

# would ideally come from a config file...
uname = "robertsudwarts"

@retry(wait_fixed=2000)
def geonames_timezone(lat, lng):
    """For a givem latitude/longitude, return a timezone (eg "Europe/Londo")
    for use with pytz to adjust UTC to local time

    As openweathermap uses UTC for times, the values given for
    eg sunrise/sunset are meaningless. By calling Geonames with the
    latitude/longitude, we can return the `timezoneId` for use with pytz

    see utils.localized_datetime()
    """

    url = 'http://api.geonames.org/timezoneJSON'

    params = {
        'lat': lat,
        'lng': lng,
        'username': uname
    }

    r = requests.get(url, params=params)
    return r.json()

def get_timezone(lat, lng):
    """
    shortcut to return only the timezoneId as a string
    """
    data = geonames_timezone(lat, lng)
    return data['timezoneId']


# @retry(wait_fixed=2000)
# def geo_by_id(id):
#     """request to Geonames.org for more details about a geoname id

#     (unfortunately this is xml only, you'd have to jump though some
#     lxml hoops in order to scrape this satisfactorily)
#     """
#     url = 'http://api.geonames.org/get'
#     params = {
#         'geonameId': id,
#         'username': uname,
#         'style': 'full',
#     }
#     r = requests.get(url, params=params)
#     return r
