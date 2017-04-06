import random
import numpy as np
from random_numbers import mean_random_numbers


def test_random_numbers():
    random.seed(3)
    np.testing.assert_almost_equal(mean_random_numbers(), 47)
