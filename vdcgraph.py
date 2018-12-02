import csv
from csvreader import *
import networkx as nx
from distances import distance
from math import sin, cos, radians, sqrt, asin



class VDCGraph:
    #Wrapper class for networkx's Graph class
    locdict = {}
    G = None
    paths = None
    pathLengths = None

    def __init__(self):
        self.locdict = readData()
        #Throwing all of the dealers away as a first pass
        self.locdict = {k:v for (k, v) in self.locdict.items() if v.isVDC()}
        G = nx.Graph()
        G.add_nodes_from(self.locdict.keys())
        for loc1 in self.locdict.keys():
            for loc2 in self.locdict.keys():
                G.add_edge(loc1, loc2, weight=distance(self.locdict[loc1], self.locdict[loc2]))

        self.paths = dict(nx.all_pairs_dijkstra_path(G))
        self.pathLengths = dict(nx.all_pairs_dijkstra_path_length(G))

    def getVDCs(self):
        return {k:v for (k, v) in self.locdict.items() if v.isVDC()}

    def shortestPath(self, loc1, loc2):
        # Given two string identifiers for VDCs, return the shortest path between them as determined by Dijkstra's.
        # Eventually need to extend this to dealers, but I'll deal with that later.
        # There's probably bugs with routing through VDCs, but I'll deal with that later.
        return self.paths[loc1][loc2]

    def shortestPathLength(self, loc1, loc2):
        return self.pathLengths[loc1][loc2]