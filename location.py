import csv

class Location:
    lat, lon  = 0, 0

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def isVDC(self):
        return False

    def getLat(self):
        return self.lat

    def getLon(self):
        return self.lon

    def setLat(self, lat):
        self.lat = lat

    def setLon(self, lon):
        self.lon = lon

class VDC(Location):
    cap = 0
    rail = False

    def __init__(self, lat, lon, cap, rail):
        super().__init__(self, lat, lon)
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
