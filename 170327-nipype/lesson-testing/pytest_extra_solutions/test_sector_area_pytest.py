import math
from sector_area import sector_area

import pytest


@pytest.mark.parametrize("rad1, rad2, ang", [(2, 1, 30), (10, 5, 270)])
def test_gt0(rad1, rad2, ang):
    assert sector_area(rad1, rad2, ang) > 0

@pytest.mark.parametrize("inputs, expected", [
        ([5, 1, 0],   0           ),
        ([5, 0, 360], math.pi * 25)
        ])
def test_expected(inputs, expected):
    assert sector_area(*inputs) == expected

@pytest.mark.xfail
@pytest.mark.parametrize("inputs", [[5, 1, -30], [5, 7, 360]])
def test_exception(inputs, expected):
    with pytest.raises.Exception:
        assert sector_area(*inputs)

