from location import *
import csv

def readData():
    locdict = {}
    with open("LocationLatLong.csv", newline = '', encoding='utf-8') as csvfile:
        locreader = csv.reader(csvfile, dialect='excel', delimiter=',')
        for row in locreader:
            locdict[str(row[0])] = Location(name = str(row[0]), lat = float(row[2]), lon = float(row[3]))

    #Convert the Locations that are VDCs to VDCs
    with open("ExistingVDC.csv", newline = '', encoding='utf-8') as csvfile:
        vdcreader = csv.reader(csvfile, dialect = 'excel', delimiter = ',')
        for row in vdcreader:
            locname = str(row[0])
            loc = locdict[locname]
            locdict[locname] = loc.toVDC(cap = float(row[1]), rail = bool(row[2]))

    #Convert the rest of the Locations to Dealers
    for loc in locdict.keys():
        if not locdict[loc].isVDC():
            locdict[loc] = locdict[loc].toDealer()

    return locdict