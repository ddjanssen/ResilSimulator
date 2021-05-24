from math import sin, cos, sqrt, atan2, radians

from src.util import distance


class UserEquipment:
    def __init__(self,id,lon,lat,capacity):

        self.id = id
        self.requested_capacity = capacity
        self.lon = lon
        self.lat = lat
        self.base_station = None
        self.bs_distance = None
        pass


    @property
    def distance(self):
        if not self.base_station:
            return -1

        if not self.bs_distance:
            return self.bs_distance

        return distance(self.lat,self.lon,self.base_station.lat,self.base_station.lon)


    def set_base_station(self,base_station, distance):
        self.base_station = base_station
        self.bs_distance = distance
        base_station.add_UE(self)

    def __str__(self):
        return "UE[{}], bandwith: {}, lon: {}, lat: {}, \nClosest Base Station: {}".format(self.id,self.requested_capacity,self.lon,self.lat,str(self.base_station))