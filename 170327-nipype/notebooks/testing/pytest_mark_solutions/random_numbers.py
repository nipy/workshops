import random
import numpy as np


def mean_random_numbers():
    a = random.sample(range(-100, 100), 10)
    mean = np.absolute(a).mean()
    return mean
