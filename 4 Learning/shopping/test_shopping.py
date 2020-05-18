import pytest

from shopping import *

def test_load_data():
    evidence, labels = load_data('shopping.csv')
    assert len(evidence) == 12330
    assert len(evidence) == len(labels)

    evidence0 = [0, 0, 0, 0, 1, 0, 0.2, 0.2, 0, 0, 1, 1, 1, 1, 1, 1, 0]
    labels0 = 0
    assert evidence[0] == evidence0
    assert labels[0] == labels0
    assert type(evidence[0]) == list
    assert len(evidence[0]) == 17

    evidence12329 = [0, 0, 0, 0, 3, 21.25, 0, 0.066666667, 0, 0, 10, 3, 2, 1, 2, 0, 1]
    labels12329 = 0
    assert evidence[12329] == evidence12329
    assert labels[12329] == labels12329
    assert type(evidence[12329]) == list
    assert len(evidence[12329]) == 17


