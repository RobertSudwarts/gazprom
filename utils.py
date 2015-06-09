"""
misc functions
"""
import pytz
import datetime

# this should be used in preference to pandas.to_datetime,
# (unless pandas is being imported anyway... )
ts = lambda t: datetime.datetime.utcfromtimestamp(int(t))

def degrees_to_cardinal(d):
    '''Compute cardinal directions from a float

    note: this is approximate...
    '''
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((d + 11.25)/22.5)
    return dirs[ix % 16]


def localized_datetime(dt, timezone):
    assert isinstance(dt, datetime.datetime), "a datetime is required"

    tz = pytz.timezone(timezone)
    local_datetime = pytz.utc.localize(dt, is_dst=None).astimezone(tz)
    return local_datetime
