
#UNTITLED6 Summary of this function goes here
#Detailed explanation goes here
import numpy as np
def truck_distance(stations: list, trucks: int):
#load distance matrices
    station_distance = np.load('station_distances.npz')
    station_distance_base = np.load('station_distances_from_base.npz')

    distance_matrix = station_distance['distances']
    from_base = station_distance_base['distances']

    if (len(stations) == 0):
        distance = 0
        
        return distance

    #start from station closest to base
    not_visited = stations[:]
    distance = min(from_base[not_visited])
    the_next = np.argmin(from_base[not_visited])
    visited = []
    visited.append(not_visited[the_next])
    del not_visited[the_next]

    #find the closest station and loop
    while(len(visited) < len(stations)):
        d = distance_matrix[visited[-1], :]
        hop = min(d[not_visited])
        the_next = np.argmin(d[not_visited])
        visited.append(not_visited[the_next])
        del not_visited[the_next]
        distance = distance + hop

    #return to base
    distance = distance + from_base[visited[-1]]
    
    return distance