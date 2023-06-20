
def add_trip(traveling: list, arrival_time: int, station: int):
#   UNTITLED4 Summary of this function goes here
#   Detailed explanation goes here

    if (len(traveling) == 0):
        traveling.append([arrival_time, station])
        return traveling

    bikes = len(traveling)

    for i in range(bikes):
        if (arrival_time < traveling[i][0]):
            traveling.insert(i, [arrival_time, station])
            return traveling

    traveling.append([arrival_time, station])
    
    return traveling

