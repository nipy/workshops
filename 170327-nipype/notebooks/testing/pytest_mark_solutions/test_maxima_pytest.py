from maxima import find_maxima
import pytest

@pytest.mark.parametrize("input, expected_maxima", [
        ([1, 2, 1, 0],     [1]   ),
        ([-1, 2, 1, 3, 2], [1, 3]),
        ([4, 3, 4, 3],     [0, 2]),
        ([1, 2, 3],        [2]   )
        ])
def test_maxima(input, expected_maxima):
    assert find_maxima(input) == expected_maxima
