import math

import util


class BS_BS_Link:
    def __init__(self, device1, device2):
        self.device1 = device1
        self.device2 = device2

        self.functional = 1
        pass

    def other(self, BS):
        if self.device1 is BS:
            return self.device2

        if self.device2 is BS:
            return self.device1

        return None

    def __str__(self):
        return "Link between {} and {}".format(self.device1, self.device2)


class BS_UE_Link:
    def __init__(self, ue, base_station, distance:float):
        self.ue = ue
        self.base_station = base_station
        self.distance = distance

        self.functional = 1

    @property
    def shannon_capacity(self):
        return util.shannon_capacity(self.base_station.getBandwidth(self.ue),self.base_station.signal_strength,self.distance)

    @property
    def SNR(self):
        return util.SNR(self.base_station.signal_strength,self.distance)


    def __str__(self):
        return "Link between {} and {}".format(self.ue, self.base_station)
