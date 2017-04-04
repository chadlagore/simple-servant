from django.test import TestCase
from django.test import RequestFactory
import pytest

from .carsim.get_cars import get_cars
from .utils import floor_date

def test_cars_positive():
    for i in range(1000):
        assert get_cars(0) >= 0


def test_floor_date():
    assert floor_date(1490821240, 'daily') == 1490770800
