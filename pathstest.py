from location import *
from vdcgraph import *

G = VDCGraph()

print("Testing VDC paths")
print(G.shortestPath('3A', '3F'))
print(G.shortestPathLength('3A', '3F'))

print("Testing dealer paths")
