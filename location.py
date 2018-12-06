from math import sin, cos, radians, sqrt, asin
from distances import distance

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

    def toDealer(self):
        return Dealer(self.getName(), self.getLat(), self.getLon())

    def __str__(self):
        return self.name + " Lat: " + str(self.getLat()) + " Lon: " + str(self.getLon())

class Dealer(Location):
    vdc = None
    vdcDist = None
    deadline = None

    def __init__(self, name, lat, lon, vdc = None):
        super().__init__(name, lat, lon)
        self.vdc = vdc
        if vdc is not None:
            self.vdcDist = distance(self, vdc)

    def getVDC(self):
        return self.vdc

    def setVDC(self, vdc):
        self.vdc = vdc
        self.vdcDist = distance(self, vdc)

    def getVDCDist(self):
        return self.vdcDist

    def __str__(self):
        vdcname = "None"
        vdcdist = "N/A"
        if self.vdc is not None:
            vdcname = self.vdc.getName()
            vdcdist = self.vdc.getVDCDist()
        return super().__str__() + " VDC: " + vdcname + " Distance: " + vdcdist

class VDC(Location):

    cap = 0
    rail = False
    dealerDict = {}

    def __init__(self, name, lat, lon, cap, rail):
        super().__init__(name, lat, lon)
        self.cap = cap
        self.rail = rail
        self.dealerDict = {}

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

    def getDealers(self):
        return self.dealerDict

    def addDealer(self, dealer):
        # Note this is not automatically bidirectional! You have to manually have to add the VDC to the dealer.
        if dealer is None:
            return
        self.dealerDict[dealer.getName()] = dealer

    def removeDealer(self, dealer):
        if isinstance(dealer, String):
            del self.dealerDict[dealer]
        if isinstance(dealer, Dealer):
            del self.dealerDict[dealer.getName()]

    def __str__(self):
        output = super().__str__() + " Capacity: " + str(self.getCap()) + " Rail Available: " + str(self.getRail())
        output += "\nDealers: " + self.dealerDict.values().__str__()
        return output

