from csvreader import *
import networkx as nx
from distances import distance
import matplotlib.pyplot as plt

#locdict = readData()

locdict = {}
locdict["Los Angeles"] = Location("Los Angeles", 34.05, -118.25)
locdict["New York"] = Location("New York", 40.7128, -74.0060)
locdict["London"] = Location("London", 51.5074, -0.1278)
locdict["Tokyo"] = Location("Tokyo", 35.6895, 139.6917)



G = nx.Graph()
G.add_nodes_from(locdict.keys())

for loc1 in locdict.keys():
    for loc2 in locdict.keys():
        G.add_edge(loc1, loc2, weight = distance(locdict[loc1], locdict[loc2]))

print(G.edges.data('weight'))
'''
plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
'''
