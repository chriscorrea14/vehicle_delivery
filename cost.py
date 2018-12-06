# script to calculate the cost of a given graph
from distances import distance, closest_vdc
import pandas as pd
import csv
from vdcgraph import VDCGraph
import sys

DELIVER_BY = pd.Timedelta(days=10)

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
        self.vdc_graph = VDCGraph()
        self.preprocess_shipping_reqs()
        self.locations = pd.read_excel(io='data/location.xlsx', sheet_name='LocationLatLong').set_index('Location')

    # We will think about a vehicle being built as "in transit" and arriving at the plant
    # when it's done building
    def preprocess_shipping_reqs(self):
        reqs = pd.read_csv('data/Problem_VehicleShipmentRequirement.csv')
        # DELETE ME.  JUST FOR TESTING PURPOSES
        reqs = reqs.loc[0:1000]
        full_paths = reqs.apply(lambda req: self.vdc_graph.shortestPath(req['Plant'], req['Dealer'])[1:], axis=1)
        in_transit = pd.concat(
            [
                reqs['VIN'].rename('vin'),
                reqs['Plant'].rename('next_loc'),
                full_paths.rename('full_path'),
                (pd.to_datetime(reqs['Plant_Arrival_Time']) + DELIVER_BY).rename('end_time'),
                pd.to_datetime(reqs['Plant_Arrival_Time']).rename('arrive_time')
            ],
            axis=1
        )
        self.in_transit = in_transit.sort_values(by='arrive_time')
        self.num_cars_to_be_built = len(in_transit)

    def run(self):
        # current_time = self.in_transit.loc[next_car_built_idx, 'arrive_time']
        cost = 0
        while not self.waiting_cars.empty or not self.in_transit.empty:
            if self.waiting_cars.empty:
                self.process_in_transit()
            elif self.in_transit.empty:
                cost += self.process_waiting_cars()
            else:
                next_in_transit = self.in_transit.loc[0]
                next_waiting_car = self.waiting_cars.loc[0]
                if next_in_transit['arrive_time'] < next_waiting_car['leave_time']:
                    self.process_in_transit()
                else:
                    cost += self.process_waiting_cars()
        return cost

    # AKA the car is arriving at it's next location
    def process_in_transit(self):
        next_car = self.in_transit.loc[0]
        self.waiting_cars = self.waiting_cars.append({
            'vin':         next_car['vin'],
            'current_loc': next_car['next_loc'],
            'next_loc':    next_car['full_path'][0],
            'full_path':   next_car['full_path'][1:],
            'end_time':    next_car['end_time'],
            'leave_time':  None ????????????
        }, ignore_index=True)
        self.waiting_cars = self.waiting_cars.sort_values(by='leave_time') # ideally use insertion sort here
        self.in_transit = self.in_transit.iloc[1:]

    # AKA the car needs to leave now for the next spot.  will take any cars with it
    def process_waiting_cars(self):
        next_waiting_car = self.waiting_cars.loc[0]
        same_path = self.waiting_cars[ # cars that can go with the next waiting car
            (self.waiting_cars['current_loc'] == next_waiting_car['current_loc']) & 
            (self.waiting_cars['next_loc']    == next_waiting_car['next_loc'])
        ]
        
        if len(next_car['full_path']) > 0: # If car is not at it's final location
            # Changing leave_time column to arrive_time at next location
            same_path['leave_time'] = next_waiting_car['leave_time'] + PATH_TIME ??????????
            same_path = same_path.drop(columns=['current_loc']).rename(index=str, columns={'leave_time': 'arrive_time'})
            self.in_transit = self.in_transit.append(same_path)


if __name__ == '__main__':
    # TODOS:
    # 1. if you reach vdc capacity, then process those
    # 2. if enough vehicles reach a location to ship in one truck / train, leave then even though they don't have to leave right away
    # 3. insertion sort
    # 4. leave time in process_in_trasit
    policy = CostCalculatingPolicy()
    policy.run()