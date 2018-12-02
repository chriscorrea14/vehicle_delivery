from location import *
from distances import distance
import pandas as pd
import numpy as np
from math import sin, cos, radians, sqrt, asin

locdict = {}
locdict["Los Angeles"] = Location("Los Angeles", 34.05, -118.25)
locdict["New York"] = Location("New York", 40.7128, -74.0060)

print(locdict["Los Angeles"])
print(locdict["New York"])
print(distance(locdict["Los Angeles"], locdict["New York"]) / 1.2)
