import csv
import pandas as pd
import numpy as np
from math import sin, cos, radians, sqrt, asin

class Location:

    lat, lon = 0, 0

    def __init__(self, name, lat, lon):
        self.name = str(name)
        self.lat = radians(lat)
        self.lon = radians(lon)

    def isVDC(self):
        return False

    def getName(self):
        return self.name

    def getLat(self):
        return self.lat

    def getLon(self):
        return self.lon

    def setLat(self, lat):
        self.lat = lat

    def setLon(self, lon):
        self.lon = lon

    def toVDC(self, cap, rail):
        return VDC(self.getName(), self.getLat(), self.getLon(), cap, rail)

    def __str__(self):
        return self.name + " Lat: " + str(self.getLat()) + " Lon: " + str(self.getLon())

class VDC(Location):

    cap = 0
    rail = False

    def __init__(self, name, lat, lon, cap, rail):
        super().__init__(name, lat, lon)
        self.cap = cap
        self.rail = rail

    def isVDC(self):
        return True;

    def getCap(self):
        return self.cap

    def getRail(self):
        return self.rail

    def setCap(self, cap):
        self.cap = cap

    def setRail(self, rail):
        self.rail = rail

    def __str__(self):
        return super().__str__() + " Capacity: " + str(self.getCap()) + " Rail Available: " + str(self.getRail())