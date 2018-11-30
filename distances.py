import pandas as pd
import numpy as np
from math import sin, cos, radians, sqrt, asin

def distance(locations_table, location1, location2):
    # Defined on bottom of page 14 of Intro to Informs
    if isinstance(location1, str) and location1.isdigit():
        location1 = int(location1)
    if isinstance(location2, str) and location2.isdigit():
        location2 = int(location2)

    row1, row2 = locations_table.loc[location1], locations_table.loc[location2]
    lat1, long1 = radians(row1['Latitude']), radians(row1['Longitude'])
    lat2, long2 = radians(row2['Latitude']), radians(row2['Longitude'])

    c = 2 * asin(sqrt(
      sin((lat1 - lat2)/2.0)**2 + cos(lat1) * cos(lat2) * sin((long1 - long2)/2.0)**2
    ))
    return 1.2 * 3959 * c

def closest_vdc(locations_table, dealer):
    print(locations_table.head(20))

if __name__ == '__main__':
    locations = pd.read_excel(io='data/location.xlsx', sheet_name='LocationLatLong')
    locations = locations.set_index('Location')
    print locations.head(20)
    print "Distance from location 2 to location 17 is: ", distance(locations, 2, 17)