from django.test import TestCase
from django.test import RequestFactory
import pytest

from .carsim.get_cars import get_cars
from .utils import get_linreg


dummy_data = {0:0, 2:2}
expected_result =  {
    'intercept': 0.0,
    'p_value': 0.0,
    'r_squared': 1.0,
    'slope': 1.0,
    'std_err': 0.0,
    'x1': 0,
    'x2': 2,
    'y1': 0.0,
    'y2': 2.0
}

def test_cars_positive():
    for i in range(1000):
        assert get_cars(0) >= 0


def test_get_linreg_size_2():
    result = get_linreg(dummy_data)
    assert get_linreg(dummy_data) == expected_result
