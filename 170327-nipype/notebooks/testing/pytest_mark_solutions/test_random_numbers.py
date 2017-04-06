import random
import numpy as np
from random_numbers import mean_random_numbers
import pytest, sys

@pytest.mark.xfail(sys.version_info < (3,0),
                   reason="random api is different in python2")
def test_random_numbers():
    random.seed(3)
    np.testing.assert_almost_equal(mean_random_numbers(), 47)
