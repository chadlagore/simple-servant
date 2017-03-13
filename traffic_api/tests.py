from django.test import TestCase
import pytest


# A test test?
def inc(x):
    return x + 1

def test_answer():
    assert inc(4) == 5
