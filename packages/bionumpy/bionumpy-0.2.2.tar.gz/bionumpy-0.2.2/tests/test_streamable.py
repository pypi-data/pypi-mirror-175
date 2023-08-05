import pytest
from bionumpy.streams import streamable, BnpStream
import numpy as np


@pytest.fixture
def a():
    return np.arange(20)


@pytest.fixture
def b():
    return np.arange(20)[::-1]*3


@pytest.fixture
def a_stream():
    return [i*np.arange(20) for i in range(5)]


def func(a, b):
    return a+b


def test_without_stream(a, b):
    new_func = streamable()(func)
    np.testing.assert_equal(new_func(a, b), func(a, b))


def test_with_stream(a_stream, b):
    new_func = streamable()(func)
    for true, result in zip((func(a, b) for a in a_stream),
                            new_func(BnpStream(a_stream), b)):
        np.testing.assert_equal(result, true)


def test_with_stream_and_print(a_stream, b):
    new_func = streamable()(func)
    stream = BnpStream(a_stream)
    print(stream)
    for true, result in zip((func(a, b) for a in a_stream),
                            new_func(stream, b)):
        np.testing.assert_equal(result, true)


def test_with_stream_reduction(a_stream, b):
    new_func = streamable(sum)(func)
    true = sum((func(a, b) for a in a_stream))
    result = new_func(BnpStream(a_stream), b)
    np.testing.assert_equal(result, true)
