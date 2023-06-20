import numpy as np
import pandas as pd
import find_distance

stationids_capacities = pd.read_csv('stationids_capacities.csv')
station_ids = stationids_capacities[stationids_capacities.columns[0]]
M = len(station_ids)
ids = station_ids
distances = np.zeros((M,M))
station_positions = np.load('station_positions.npz')
positions = station_positions['positions']

for i in range(M):
    for j in range(M):
        id1 = np.where(station_ids == ids[i])
        id2 = np.where(station_ids == ids[j])
        distances[i, j] = find_distance.find_distance(positions[:, id1], positions[:, id2])

np.savez('station_distances',distances = distances, station_ids = station_ids)