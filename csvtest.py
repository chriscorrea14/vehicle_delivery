from location import *
import pandas as pd
import numpy as np
from math import sin, cos, radians, sqrt, asin

locdict = {}

def readLocations():
    with open("LocationLatLong.csv", newline = '', encoding='utf-8') as csvfile:
        locreader = csv.reader(csvfile, dialect='excel', delimiter=',')
        for row in locreader:
            locdict[str(row[0])] = Location(str(row[0]), float(row[2]), float(row[3]))

def readVDC():
    with open("ExistingVDC.csv", newline = '', encoding='utf-8') as csvfile:
        vdcreader = csv.reader(csvfile, dialect = 'excel', delimiter = ',')
        for row in vdcreader:
            locname = str(row[0])
            loc = locdict[locname]
            locdict[locname] = loc.toVDC(cap = float(row[1]), rail = bool(row[2]))

readLocations()
readVDC()