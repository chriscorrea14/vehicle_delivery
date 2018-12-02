from csvreader import *
import networkx as nx
from distances import distance

locdict = readData()
locdict = {k:v for (k, v) in locdict.items() if v.isVDC()}

G = nx.Graph()
G.add_nodes_from(locdict.keys())

for loc1 in locdict.keys():
    for loc2 in locdict.keys():
        G.add_edge(loc1, loc2, weight = distance(locdict[loc1], locdict[loc2]))

def shortestPath(loc1, loc2):
    # Given two string identifiers for VDCs, return the shortest path between them as determined by Dijkstra's.
    # Eventually need to extend this to dealers, but I'll deal with that later.
    return(nx.dijkstra_path(G, loc1, loc2))