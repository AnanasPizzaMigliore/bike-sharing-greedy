import numpy as np
def truck_distance_capacity(stations: list, trucks: int, bike_numbers: np.array, capacity: int):
#load distance matrices
    station_distance = np.load('station_distances.npz')
    station_distance_base = np.load('station_distances_from_base.npz')

    distance_matrix = station_distance['distances']
    from_base = station_distance_base['distances']
    trip_count = 1

    if (len(stations) == 0):
        distance = 0
        trip_count = 0
        
        return distance, trip_count

    #start from station closest to base
    #print(f'stations: {stations}')
    not_visited = stations[:]
    #distance = np.min(from_base[not_visited])
    #the_next = np.argmin(from_base[not_visited])
    visited = []
    #visited.append(not_visited[the_next])
    #del not_visited[the_next]
    temp_numbers = bike_numbers[:]
    distance = 0
       

    while(len(visited) < len(stations)):
        if np.sum(temp_numbers[not_visited]) >= 0:
            carrying = 0
        else:
            carrying = capacity
        if len(not_visited) == 0: 
            break
            #print(f'visited and stations {len(visited)} and {len(stations)}')
        start_distance = np.min(from_base[not_visited])
            #print(f'not visited {not_visited}')
        distance = distance + start_distance
        the_next = np.argmin(from_base[not_visited])
        visited.append(not_visited[the_next])
        del not_visited[the_next]
        temp_not_visited = not_visited[:]
        d = distance_matrix[visited[-1], :]
        met = False
        while not met:
            if len(temp_not_visited) == 0:
                distance = distance + from_base[visited[-1]]
                    #print('marker 1')
                    #print(temp_numbers[not_visited])
                trip_count = trip_count + 1
                break
                #print(f'temp not visited {len(temp_not_visited)}')
            hop = np.min(d[temp_not_visited])
            the_next = np.argmin(d[temp_not_visited])
            if 0 <= carrying + temp_numbers[the_next] <= capacity:
                carrying = carrying + temp_numbers[the_next]
                temp_numbers[the_next] = 0
                visited.append(temp_not_visited[the_next])
                not_visited.remove(temp_not_visited[the_next])
                distance = distance + hop
                met = True
            else:
                del temp_not_visited[the_next]
    
    distance = distance + from_base[visited[-1]]
    #print(distance)
    #print(trip_count)
    return distance, trip_count