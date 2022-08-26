import math

_conversion_factor = 0.62137119


def miles_to_kilometers(miles: int) -> int:
    return math.ceil(miles / _conversion_factor)


def kilometers_to_miles(km: int) -> int:
    return math.ceil(km / _conversion_factor)
