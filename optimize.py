import pandas as pd
import numpy as np
from truck_distance import truck_distance

def optimize(state, survival, max_survival, optimal_state, beta, gamma):
    
    trucks = 1
    stationids_capacities = pd.read_csv('stationids_capacities.csv')
    station_ids = stationids_capacities[stationids_capacities.columns[0]].values
    station_count = np.zeros((len(station_ids)))
    ones = np.ones((len(station_ids)))

    #initialization
    distance = 0
    stop = False
    new_survival = np.copy(survival)
    visited = []
    not_visited = np.zeros(len(state))
    best_visited = []
    best_reward = 0
    danger = min(min(survival), 7200)
    #print(f'danger, {danger}')

    #iterate over the stations
    while not stop:
        #find the station with the lowest survival time
        
        index = np.argmin(survival + not_visited * 1e9)
        #print(f'index: {index}')
        #print(f'index {index}')
        new_survival[index] = max_survival[index]
        #print(f'new survival {new_survival[index]}')
    
        #update visited station list
        not_visited[index] = 1
        visited.append(index)
    
        #calculate the new reward
        new_reward = min(np.min(new_survival), 7200) - danger
        #print(f'reward {new_reward}')
        #print(f'visited {visited}')
        distance = truck_distance(visited, trucks)
        #print(f'distance {distance} visited {visited}')
        new_penalty = beta * trucks + gamma * np.mean(distance)
        #print(f'penalty, {new_penalty}')
        #print(f'visited {visited}')
    
        if (new_reward - new_penalty > best_reward):
            best_visited = visited[:]
            best_reward = new_reward - new_penalty
        
        survival_visited = []
        for i in range(len(visited)):
            survival_visited.append(max_survival[visited[i]])

        #print(f'max_survival {max_survival}')
        #print(f'not_visited {not_visited}, survival_visited {survival_visited}')
    #stop if adding the station does not increase the reward
        if (sum(not_visited) == len(not_visited) or (np.min(survival_visited) < np.min(survival + not_visited * 1e9))):
            stop = True
            visited = best_visited[:]
            state[visited] = optimal_state[visited]
            #print(f'visited stations {visited}')
            distance = truck_distance(visited, trucks)
            condition = np.isin(station_ids, visited)
            station_count = np.where(condition, ones, 0)

    if (distance == 0):
        trucks = 0
        
    return state, trucks, distance, station_count
