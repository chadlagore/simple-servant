from django.test import TestCase
from django.test import RequestFactory
import pytest

from .carsim.get_cars import get_cars
from .utils import floor_date

def test_cars_positive():
    for i in range(1000):
        assert get_cars(0) >= 0


def test_floor_date():
    assert floor_date(1490955890.0, 'daily') == 1490943600.0
    assert floor_date(1490955890.0, 'monthly') == 1488355200.0
    assert floor_date(1490955890.0, 'yearly') == 1483257600.0
