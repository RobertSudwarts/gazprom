
from nose.tools import *
from geonames_requests import *


def test_gettimezone():
    lat = 47.01
    lng = 10.20
    expected = u"Europe/Vienna"
    val = get_timezone(lat, lng)
    eq_(val, expected)
