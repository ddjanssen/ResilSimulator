import math

from objects.BaseStation import BaseStation
from objects.UE import UserEquipment


class BS_BS_Link:
    def __init__(self, device1: BaseStation, device2: BaseStation):
        self.device1 = device1
        self.device2 = device2

        self.functional = 1
        pass

    def other(self, BS:BaseStation):
        if self.device1 is BS:
            return self.device2

        if self.device2 is BS:
            return self.device1

        return None

    def __str__(self):
        return "Link between {} and {}".format(self.device1, self.device2)


class BS_UE_Link:
    def __init__(self, ue: UserEquipment, base_station: BaseStation, distance:float):
        self.ue = ue
        self.base_station = base_station
        self.distance = distance

        self.functional = 1

    @property
    def shannon_capacity(self):
        # TODO change the numbers to be dynamic
        bandwith_for_user = 20  # 1.4, 3, 5, 10, 15, 20 MHz for lte base stations per band total bands: 5
        signal_strength = 43  # for lte basestations
        signal_noise = -20
        SNR = signal_strength / signal_noise
        capacity = bandwith_for_user * math.log2(1 + SNR)
        return capacity

    def __str__(self):
        return "Link between {} and {}".format(self.ue, self.base_station)
