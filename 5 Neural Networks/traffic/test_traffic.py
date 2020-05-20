import pytest

from traffic import *

def test_load_data():
    images, labels = load_data('gtsrb-small')
    assert len(images) == len(labels)
    assert len(labels) == 30 * (18 + 5 + 5)
    assert images[0].shape[0] == IMG_WIDTH 
    assert images[0].shape[1] == IMG_HEIGHT
    assert images[-1].shape[0] == IMG_WIDTH 
    assert images[-1].shape[1] == IMG_HEIGHT
    assert type(labels[0]) == int