import pandas as pd
import numpy as np
from truck_distance_capacity import truck_distance_capacity
#from truck_distance import truck_distance

def optimize_capacity(state, survival, max_survival, optimal_state, beta, gamma, capacity):
    
    trucks = 1
    stationids_capacities = pd.read_csv('stationids_capacities.csv')
    station_ids = stationids_capacities[stationids_capacities.columns[0]].values
    station_count = np.zeros((len(station_ids)))
    ones = np.ones((len(station_ids)))
    trip_count = 0

    #initialization
    distance = 0
    stop = False
    new_survival = survival
    visited = []
    not_visited = np.zeros(len(state))
    best_visited = []
    best_reward = 0
    danger = min(min(survival), 7200)
    bike_numbers = state - optimal_state
    rebalance_count = 0

    #iterate over the stations
    while not stop:
        #find the station with the lowest survival time
        
        index = np.argmin(survival + not_visited + 1e9)
        #print(f'index {index}')
        new_survival[index] = max_survival[index]
    
        #update visited station list
        not_visited[index] = 1
        visited.append(index)
    
        #calculate the new reward
        new_reward = min(min(new_survival), 7200) - danger
        #print(f'visited {visited}')
        distance, trip_count = truck_distance_capacity(visited, trucks, bike_numbers, capacity)
        #print(distance)
        #print(f'distance {distance} visited {visited}')
        new_penalty = beta * trucks + gamma * np.mean(distance)
        #print(f'visited {visited}')
    
        if (new_reward - new_penalty > best_reward):
            best_visited = visited
            best_reward = new_reward - new_penalty
            #print('marker 1')
        
        survival_visited = []
        for i in range(len(visited)):
            survival_visited.append(max_survival[visited[i]])

        #print(f'max_survival {max_survival}')
        #print(f'not_visited {not_visited}, survival_visited {survival_visited}')
    #stop if adding the station does not increase the reward
        if (sum(not_visited) == len(not_visited) or (min(survival_visited) < min(survival + not_visited * 1e9))):
            stop = True
            #print(f'visited before {visited}')
            visited = best_visited
            state[visited] = optimal_state[visited]
            distance, trip_count = truck_distance_capacity(visited, trucks, bike_numbers, capacity)
            #print(trip_count)
            #print(f'visited {visited}')
            condition = np.isin(station_ids, visited)
            station_count = np.where(condition, ones, 0)
            if len(visited) != 0:
                rebalance_count = rebalance_count + 1

    if (distance == 0):
        trucks = 0
        station_count = 0
        trip_count = 0
        rebalance_count = 0
        
    return state, trucks, distance, station_count, trip_count, rebalance_count
