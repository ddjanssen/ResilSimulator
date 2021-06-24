import math

import util
from settings import CHANNEL_BANDWIDTHS, SIGNAL_NOISE


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
    def __init__(self, ue, base_station, distance:float,signal_deduction:float=1):
        self.ue = ue
        self.base_station = base_station
        self.distance = distance
        self.signal_deduction = signal_deduction
        self.functional = 1

        self.second_param_capacity = util.second_param_capacity(self.base_station.signal_strength,self.distance)

        self.bandwidthneeded = None

        if self.second_param_capacity != 0:
            b = self.ue.requested_capacity / self.second_param_capacity

            bandwidth_length = len(CHANNEL_BANDWIDTHS)
            for bandwidth in range(bandwidth_length):
                if b > bandwidth:
                    if bandwidth == 0:
                        self.bandwidthneeded = CHANNEL_BANDWIDTHS[0]
                    else:
                        self.bandwidthneeded = CHANNEL_BANDWIDTHS[bandwidth - 1]
                    break

                if bandwidth == bandwidth_length - 1:
                    self.bandwidthneeded = CHANNEL_BANDWIDTHS[-1]

    @property
    def shannon_capacity(self):
        return self.base_station.getBandwidth(self.ue) * self.second_param_capacity * self.signal_deduction

        # return util.shannon_capacity(self.base_station.getBandwidth(self.ue),self.base_station.signal_strength,self.distance)

    @property
    def SNR(self):
        return util.SNR(self.base_station.signal_strength,self.distance)


    def set_signal_noise(self,new_noise):
        self.signal_noise = new_noise
        self.second_param_capacity = util.second_param_capacity(self.base_station.signal_strength,self.distance)



    def __str__(self):
        return "Link between {} and {}".format(self.ue, self.base_station)
