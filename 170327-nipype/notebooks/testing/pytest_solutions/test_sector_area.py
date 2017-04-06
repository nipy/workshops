import math
from sector_area import sector_area

def test_gt0():
    for rad1, rad2, ang in [(2, 1, 30), (10, 5, 270)]:
        assert sector_area(rad1, rad2, ang) > 0


def test_angle0():
    assert sector_area(5, 1, 0) == 0


def test_full():
    assert sector_area(5, 0, 360) == math.pi * 25
