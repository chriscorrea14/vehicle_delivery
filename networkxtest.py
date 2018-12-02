from location import *
import pandas as pd
import numpy as np
from math import sin, cos, radians, sqrt, asin

locdict = {}
locdict["Los Angeles"] = Location("Los Angeles", 34.05, -118.25)
locdict["New York"] = Location("New York", 40.7128, -74.0060)


def distance(location1, location2):
    lat1, lat2 = location1.getLat(), location2.getLat()
    long1 = location1.getLon()
    long2 = location2.getLon()
    c = 2 * asin(sqrt(
        sin((lat1 - lat2) / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin((long1 - long2) / 2.0) ** 2
    ))
    return 1.2 * 3959 * c

print(locdict["Los Angeles"])
print(locdict["New York"])
print(distance(locdict["Los Angeles"], locdict["New York"]) / 1.2)
