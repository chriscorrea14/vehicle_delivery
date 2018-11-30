from location import *
import pandas as pd
import numpy as np
from math import sin, cos, radians, sqrt, asin

locdict = {}

with open("LocationLatLong.csv", newline = '', encoding='utf-8') as csvfile:
    locreader = csv.reader(csvfile, dialect='excel', delimiter=',')
    for row in locreader:
        locdict[str(row[0])] = Location(str(row[0]), float(row[2]), float(row[3]))


with open("ExistingVDC.csv", newline = '', encoding = 'utf-8') as csvfile:
    vdcreader = csv.reader(csvfile, dialect = 'excel', delimiter = ',')
    for row in vdcreader:
        locname = str(row[0])
        loc = locdict[locname]
        locdict[locname] = VDC(loc, float(row[1]), bool(row[2]))


for i in range(0, 6, 1):
    print(list(locdict.values())[i])