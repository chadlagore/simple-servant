from django.test import TestCase
from django.test import RequestFactory
import pytest

from .carsim.get_cars import get_cars
from .utils import get_linreg


dummy_data = {0:0, 2:2, 3:4}
expected_result =  {
    "slope": 1.2857142857142856,
    "intercept": -0.1428571428571428,
    "r_squared": 0.9642857142857141,
    "p_value": 0.12103771832367702,
    "std_err": 0.24743582965269748,
    "y1": -0.1428571428571428,
    "y2": 3.714285714285714,
    "x1": 0,
    "x2": 3
}


def test_cars_positive():
    for i in range(1000):
        assert get_cars(0) >= 0


def test_get_linreg_size_2():
    result = get_linreg(dummy_data)
    assert result == expected_result
