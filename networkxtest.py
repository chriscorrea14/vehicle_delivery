from csvreader import *
import networkx as nx
import matplotlib.pyplot as plt

def distance(location1, location2):
    lat1, lat2 = location1.getLat(), location2.getLat()
    long1 = location1.getLon()
    long2 = location2.getLon()
    c = 2 * asin(sqrt(
        sin((lat1 - lat2) / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin((long1 - long2) / 2.0) ** 2
    ))
    return 1.2 * 3959 * c

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
