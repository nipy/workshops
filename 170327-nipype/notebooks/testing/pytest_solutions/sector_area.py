import math

def sector_area(radius1, radius2, angle_deg):
    angle_rad = (2 * math.pi / 360) * angle_deg # changing degrees to radians
    area = 0.5 * (radius1**2 - radius2**2) * angle_rad
    return area
