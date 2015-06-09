
from nose.tools import *
from openweathermap_requests import *
from openweathermap_requests import LocationError


def test_current():
    data = current_weather_req()
    assert_is_instance(data, dict)


@raises(LocationError)
def test_current_bad_location():
    params = {'q': 'this place does not exist'}
    current_weather_req(params=params)


def test_forecast():
    data = forecast_weather_req()
    assert_is_instance(data, dict)


@raises(LocationError)
def test_forecast_bad_location():
    params = {'q': 'you wont find this place either'}
    forecast_weather_req(params=params)


def test_img_url():
    expected = 'http://openweathermap.org/img/w/10d.png'
    img_url = icon_src('10d')
    eq_(img_url, expected)
