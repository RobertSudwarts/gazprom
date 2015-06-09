
from nose.tools import *
from utils import *
import datetime

def test_degrees_to_cardinal():
    degrees = 10
    eq_("N", degrees_to_cardinal(degrees))

    degrees = 160
    eq_("SSE", degrees_to_cardinal(degrees))


def test_ts():
    t = "1433435100"
    eq_(ts(t), datetime.datetime(2015, 6, 4, 16, 25))


def test_localized_datetime():
    '''test localized_datetime

    this test will only pass during the summer  :)
    '''
    dt = datetime.datetime(2015, 6, 4, 16, 25)
    expected = dt + datetime.timedelta(hours=1)
    val = localized_datetime(dt, "Europe/London").replace(tzinfo=None)
    eq_(val, expected)
