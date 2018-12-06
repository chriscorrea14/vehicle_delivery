from location import *
from vdcgraph import *

G = VDCGraph()

print("Testing VDC paths")
print(G.shortestPath('3A', '3F'))
print(G.shortestPathLength('3A', '3F'))

print("Testing dealer paths")
print("15344 is a dealer of 3F:")
print(str('15344' in G.getVDCs()['3F'].getDealers().keys()))
print("Distance from 15344 to 3F:")
print(G.getDealers()['15344'].getVDCDist())
print("Shortest path 3A to 3F:")
print(G.shortestPath('3A', 15344))
print(G.shortestPathLength('3A', 15344))