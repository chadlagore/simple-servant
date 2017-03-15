from django.test import TestCase
from django.test import RequestFactory
import pytest

from .carsim.get_cars import get_cars


def test_cars_positive():
    for i in range(1000):
        assert get_cars(0) >= 0
