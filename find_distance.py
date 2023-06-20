
import math
def find_distance(p1, p2):
    

    p1 = p1 * 2 * math.pi / 360
    p2 = p2 * 2 * math.pi / 360

    a = math.sin(abs(p1[0]-p1[0]) / 2) ** 2 + math.cos(p1[0]) * math.cos(p2[0]) * math.sin(abs(p2[1]-p1[1]) / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6.371 * 1e6 * c
    
    return distance
