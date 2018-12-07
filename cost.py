# script to calculate the cost of a given graph
from distances import distance_table
import pandas as pd
import csv
from vdcgraph import VDCGraph
import sys
from copy import deepcopy
import time
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import argparse

DELIVER_BY = pd.Timedelta(days=20)

class CostCalculatingPolicy():
    def __init__(self, lambdaa=1, rail=False):
        # Cars waiting at various VDCs to be sent to dealers
        self.waiting_cars = pd.DataFrame(columns=[
            'vin', 
            'current_loc', 
            'transit_type', 
            'next_loc', 
            'full_path', 
            'end_time', # when current_time == end_time, the car better be at the end
            'leave_time' # when current_time == leave_time, the car needs to leave
        ])
        self.vdc_graph = VDCGraph(lambdaa, rail)
        self.preprocess_shipping_reqs()
        self.locations = pd.read_excel(io='data/location.xlsx', sheet_name='LocationLatLong').set_index('Location')
        self.num_cars = []

    # We will think about a vehicle being built as "in transit" and arriving at the plant
    # when it's done building
    def preprocess_shipping_reqs(self):
        # if os.path.exists('data/sorted_reqs.csv'):
        #     self.in_transit = pd.read_csv('data/sorted_reqs.csv')
        # else:
        reqs = pd.read_csv('data/Problem_VehicleShipmentRequirement.csv')
        reqs = reqs.sort_values(by='Plant_Arrival_Time').iloc[0:10000]
        print reqs.head()
        full_paths = reqs.apply(lambda req: self.vdc_graph.shortestPath(req['Plant'], req['Dealer']), axis=1)
        self.in_transit = pd.concat(
            [
                reqs['VIN'].rename('vin'),
                reqs['Plant'].rename('next_loc'),
                full_paths.rename('full_path'),
                (pd.to_datetime(reqs['Plant_Arrival_Time']) + DELIVER_BY).rename('end_time'),
                pd.to_datetime(reqs['Plant_Arrival_Time']).rename('arrive_time')
            ],
            axis=1
        )
        #     self.in_transit.to_csv('data/sorted_reqs.csv', encoding='utf-8', index=False)
        # self.in_transit = self.in_transit.iloc[0:5000]

    def run(self):
        # current_time = self.in_transit.loc[next_car_built_idx, 'arrive_time']
        print 'Current Cars:'
        # print self.in_transit.head(100)
        # print '\n'
        cost = 0
        i = 0
        a = time.time()
        len_waiting, len_transit, both = [], [], []
        while not self.waiting_cars.empty or not self.in_transit.empty:
            if self.waiting_cars.empty:
                self.process_in_transit()
            elif self.in_transit.empty:
                cost += self.process_waiting_cars()
            else:
                next_in_transit = self.in_transit.iloc[0]
                next_waiting_car = self.waiting_cars.iloc[0]
                if next_in_transit['arrive_time'] < next_waiting_car['leave_time']:
                    self.process_in_transit()
                else:
                    cost += self.process_waiting_cars()
            # if i > 20:
            #     print 'Timestep:', i
            #     print 'In Transit:'
            #     print self.in_transit.head(10)
            #     print 'Waiting at a VDC:'
            #     print self.waiting_cars.head(10)
            #     print 'Current Cost:', cost
            #     raw_input('Press enter to continue\n\n\n')
            if i % 100 == 0:
                len_transit.append(len(self.in_transit))
                len_waiting.append(len(self.waiting_cars))
                both.append(len(self.in_transit) + len(self.waiting_cars))
            if i % 1000 == 0:
                print 'Iteration: {}, Cost: {}, num_waiting: {}, num_in_transit: {}'.format(
                    i, 
                    cost, 
                    len(self.waiting_cars), 
                    len(self.in_transit)
                )
            i += 1
        x = np.arange(len(both)) * 100
        plt.plot(x, both, 'r', label='Number of Cars Not Yet at Final Dest.')
        plt.plot(x, len_waiting, 'g', label='Number of Cars Waiting')
        plt.plot(x, len_transit, 'b', label='Number of Cars In Transit')
        plt.title('Number of Cars Travelling at each Timestep')
        plt.legend()
        plt.xlabel('Timestep')
        plt.show()

        plt.hist(self.num_cars)
        plt.title('Histogram of Number of Cars per Trip (Higher = More Efficient)')
        plt.xlabel('Number of Cars')
        # plt.xlim((0,10))
        plt.ylabel('Frequency')
        plt.show()

        print 'Iteration: {}, Cost: {}, num_waiting: {}, num_in_transit: {}'.format(
            i, 
            cost, 
            len(self.waiting_cars), 
            len(self.in_transit)
        )
        print 'Total time: ', time.time() - a
        return cost

    # AKA the car is arriving at it's next location
    def process_in_transit(self):
        next_car = self.in_transit.iloc[0]
        full_path = deepcopy(next_car['full_path'])

        transit_time = 0

        full_path.insert(0,(None, next_car['next_loc']))
        for cur_loc, next_loc in zip(full_path[:-1], full_path[1:]):
            travel_time_per_mile = 10 if next_loc[1] == 'rail' else 30
            transit_time += distance_table(self.locations, cur_loc[1], next_loc[1]) / travel_time_per_mile
        transit_time = pd.Timedelta(hours=transit_time)

        self.waiting_cars = self.waiting_cars.append({
            'vin':          next_car['vin'],
            'current_loc':  next_car['next_loc'],
            'transit_type': full_path[1][0],
            'next_loc':     full_path[1][1],
            'full_path':    full_path[2:],
            'end_time':     next_car['end_time'],
            'leave_time':   next_car['end_time'] - transit_time
        }, ignore_index=True)
        self.waiting_cars = self.waiting_cars.sort_values(by='leave_time') # ideally use insertion sort here
        self.in_transit = self.in_transit.iloc[1:]

    # AKA the car needs to leave now for the next spot.  will take any cars with it
    def process_waiting_cars(self):
        next_waiting_car = self.waiting_cars.iloc[0]
        # cars that can go with the next waiting car
        matching_cars_mask = (self.waiting_cars['current_loc'] == next_waiting_car['current_loc']) & \
            (self.waiting_cars['next_loc']    == next_waiting_car['next_loc'])
        same_path = self.waiting_cars[matching_cars_mask]
        
        if next_waiting_car['transit_type'] == 'rail':
            travel_time_per_mile = 10
            cost_per_mile = 3
            fixed_cost = 2000
            same_path = same_path.iloc[0:20]
        else:
            travel_time_per_mile = 20
            cost_per_mile = 4
            fixed_cost = 20
            same_path = same_path.iloc[0:10]
        self.num_cars.append(len(same_path))

        path_length = distance_table(self.locations, next_waiting_car['current_loc'], next_waiting_car['next_loc'])
        path_time = path_length / travel_time_per_mile
        cost = fixed_cost + cost_per_mile * path_length
        
        if len(next_waiting_car['full_path']) > 0: # If car is not at it's final location
            # Changing leave_time column to arrive_time at next location
            same_path.loc[:,'leave_time'] = next_waiting_car['leave_time'] + pd.Timedelta(hours=path_time)
            same_path = same_path.drop(columns=['current_loc', 'transit_type']).rename(index=str, columns={'leave_time': 'arrive_time'})
            self.in_transit = self.in_transit.append(same_path, sort=False).sort_values(by='arrive_time')

        self.waiting_cars.drop(self.waiting_cars[matching_cars_mask].index, inplace=True)
        return cost

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lambdaa', type=float, default=1.0, help='What shortest Path Param to use')
    parser.add_argument('--rail', action='store_true', default=False, help='Whether to use rail or not')
    args = parser.parse_args()

    pd.options.mode.chained_assignment = None
    policy = CostCalculatingPolicy(args.lambdaa, args.rail)
    policy.run()