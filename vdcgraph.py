import csv
from csvreader import *
import networkx as nx
import pandas as pd
from distances import distance
from math import sin, cos, radians, sqrt, asin
import sys

class VDCGraph:
    #Wrapper class for networkx's Graph class
    locdict = {}
    dealerDict = {}
    vdcDict = {}
    G = None
    vdcPaths = None
    vdcPathLengths = None

    def __init__(self, lambdaa=1, rail=False):
        self.rail = rail
        self.locdict = readData()

        #Split the locations into dealers and vdcs
        self.vdcDict = {k:v for (k, v) in self.locdict.items() if v.isVDC()}
        self.dealerDict = {k:v for (k, v) in self.locdict.items() if not v.isVDC()}


        self.G = nx.Graph()
        #add all vdcs to graph
        self.G.add_nodes_from(self.vdcDict.keys())

        # Graph distances between vdcs
        for loc1 in self.vdcDict.keys():
            for loc2 in self.vdcDict.keys():
                self.G.add_edge(loc1, loc2, weight=distance(self.vdcDict[loc1], self.vdcDict[loc2])**lambdaa)

        # Generate paths and lengths between VDCs
        self.vdcPaths = dict(nx.all_pairs_dijkstra_path(self.G))
        self.vdcPathLengths = dict(nx.all_pairs_dijkstra_path_length(self.G))

        # Add dealers to the graph

        # Add dealers
        self.G.add_nodes_from(self.dealerDict.keys())
        # For each dealer find nearest VDC
        for dealer in self.dealerDict.values():
            nearestvdc = min(self.vdcDict.values(), key = lambda x: distance(dealer, x))
            # Add information to the VDCs/dealers
            dealer.setVDC(nearestvdc)
            nearestvdc.addDealer(dealer)

            # Add edge to graph
            self.G.add_edge(dealer.getName(), nearestvdc.getName(), weight = distance(dealer, nearestvdc))



    def getVDCs(self):
        return self.vdcDict

    def getDealers(self):
        return self.dealerDict

    def shortestPath(self, loc1, loc2):
        # Given two string identifiers where the first is a VDC,
        # return the shortest path between them as determined by Dijkstra's, excluding the start.
        loc1, loc2 = str(loc1), str(loc2)
        if loc2 in self.vdcDict.keys():
            path = self.vdcPaths[loc1][loc2]
        if loc2 in self.dealerDict.keys():
            path = self.vdcPaths[loc1][self.dealerDict[loc2].getVDC().getName()] + [loc2]
        if self.rail:
            rail = []
            for i in range(1, len(path)):
                rail.append(self.locdict[path[i-1]].hasRailPath(self.locdict[path[i]]))
        else:
            rail = ['truck'] * len(path)
        path = path[1:]
        output = list(zip(rail, path))
        return output

    def shortestPathLength(self, loc1, loc2):
        loc1, loc2 = str(loc1), str(loc2)
        if loc2 in self.vdcDict.keys():
            return self.vdcPathLengths[loc1][loc2]
        if loc2 in self.dealerDict.keys():
            return self.vdcPathLengths[loc1][self.dealerDict[loc2].getVDC().getName()] + self.dealerDict[loc2].getVDCDist()

if __name__ == '__main__':
    VDCGraph()
