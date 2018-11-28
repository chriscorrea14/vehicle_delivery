# script to calculate the cost of a given graph
from distances import distance, closest_vdc
import pandas as pd
import csv

DELIVER_BY = pd.Timedelta(days=10)

def paths(plants, dealers):
    return plants, dealers

class CostCalculatingPolicy():
    def __init__(self):
        # Cars waiting at various VDCs to be sent to dealers
        self.waiting_cars = pd.DataFrame(columns=[
            'vin', 
            'current_loc', 
            'next_loc', 
            'full_path', 
            'end_time', # when current_time == end_time, the car better be at the end
            'leave_time' # when current_time == leave_time, the car needs to leave
        ])
        self.preprocess_shipping_reqs()

    # We will think about a vehicle being built as "in transit" and arriving at the plant
    # when it's done building
    def preprocess_shipping_reqs(self):
        reqs = pd.read_csv('data/Problem_VehicleShipmentRequirement.csv')
        # DELETE ME.  JUST FOR TESTING PURPOSES
        reqs = reqs.loc[0:1000]
        next_locs, full_paths = paths(reqs['Plant'], reqs['Dealer'])
        in_transit = pd.concat(
            [
                reqs['VIN'].rename('vin'),
                next_locs.rename('next_locs'),
                full_paths.rename('full_paths'),
                (pd.to_datetime(reqs['Plant_Arrival_Time']) + DELIVER_BY).rename('end_time'),
                pd.to_datetime(reqs['Plant_Arrival_Time']).rename('arrive_time')
            ],
            axis=1
        )
        self.in_transit = in_transit.sort_values(by='arrive_time')
        self.num_cars_to_be_built = len(in_transit)

    def run(self, locations):
        current_time = in_transit.loc[next_car_built_idx, 'arrive_time']
        cost = 0
        while not self.waiting_cars.empty and not self.in_transit.empty:
            if self.waiting_cars.empty:
                cost += self.process_in_transit()
            elif self.in_transit.empty:
                cost += self.process_waiting_cars()
            else:
                next_in_transit = self.in_transit.loc[0]
                next_waiting_car = self.waiting_cars.loc[0]
                if next_in_transit['arrive_time'] < next_waiting_car['leave_time']:
                    cost += self.process_in_transit()
                else:
                    cost += self.process_waiting_cars()
        return cost

    # AKA the car is arriving at it's next location
    def process_in_transit(self, car_in_transit):
        # if you reach vdc capacity, then process those
        next_in_transit = self.in_transit.loc[0]

    # AKA the car needs to leave now for the next spot.  will take any cars with it
    def process_waiting_cars(self):
        next_waiting_car = self.waiting_cars.loc[0]
        same_path = self.waiting_cars[ # cars that can go with the next waiting car
            (self.waiting_cars['current_loc'] == next_waiting_car['current_loc']) & 
            (self.waiting_cars['next_loc'] == next_waiting_car['next_loc'])
        ]


if __name__ == '__main__':
    locations = pd.read_excel(io='data/location.xlsx', sheet_name='LocationLatLong')
    locations = locations.set_index('Location')
    run(locations)