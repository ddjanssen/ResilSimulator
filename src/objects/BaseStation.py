from settings import OPEN_CHANNELS, CHANNEL_BANDWIDTHS, BASE_POWER
from src.objects.Link import BS_BS_Link, BS_UE_Link
import util
import math

class BaseStation:
    def __init__(self, radio, mcc, net, area, cell, unit, lon, lat, range_bs, samples, changeable, created, updated, averageSignal):
        self.radio = radio
        self.mcc = mcc
        self.net = net
        self.area = int(area)
        self.cell = int(cell)
        self.unit = int(unit)
        self.lon = float(lon)
        self.lat = float(lat)
        self.range_bs = float(range_bs)
        self.samples = int(samples)
        self.changeable = int(changeable)
        self.created = int(created)
        self.updated = int(updated)
        self.averageSignal = float(averageSignal)

        self.connected_UE_links = list()
        self.connected_UE = list()
        self.connected_BS = list()

        self.minimum_band_needed = dict()


        self.channels = list()
        for g in range(OPEN_CHANNELS):
            self.channels.append(Channel(g))

        self.signal_strength = BASE_POWER
        self.functional = 1

    def __str__(self):
        startmsg = "Base station[{}], lon:{}, lat:{}, radio:{}, LAC: {}".format(self.cell, self.lon, self.lat, self.radio, self.net)
        for channel in self.channels:
            startmsg += "\n{}".format(str(channel))
        return startmsg

    def malfunction(self, new_functional):
        self.functional = new_functional
        self.create_new_channels()

    def add_link(self, link: BS_BS_Link):
        self.connected_BS.append(link)

    def __add__(self, other):
        new_link = BS_BS_Link(self, other)
        self.connected_BS.append(new_link)
        other.add_link(new_link)
        return new_link

    def add_UE(self, link: BS_UE_Link):
        self.connected_UE_links.append(link)
        self.connected_UE.append(link.ue)

        if link.bandwidthneeded not in self.minimum_band_needed:
            self.minimum_band_needed[link.bandwidthneeded] = list()

        self.minimum_band_needed[link.bandwidthneeded].append(link.ue)
        channel = max(self.channels, key=lambda c: (c.productivity, c.band_left))
        channel.add_devices(link.ue, link.bandwidthneeded)

    def direct_capacities(self):
        self.create_new_channels()
        self.connected_UE = sorted(self.connected_UE, key= lambda x: x.link.bandwidthneeded,reverse=True)
        for UE in self.connected_UE:
            channel = max(self.channels, key=lambda c: (c.productivity, c.band_left))
            channel.add_devices(UE, UE.link.bandwidthneeded)


    @property
    def overflow(self):
        for UE in self.connected_UE:
            if self.getBandwidth(UE) == 0:
                return True

        return False

    def remove_UE(self,UE_link):
        self.connected_UE_links.remove(UE_link)
        self.connected_UE.remove(UE_link.ue)

    def getBandwidth(self,UE):
        for channel in self.channels:
            bandwidth = channel.getBandwidth(UE)
            if bandwidth is not None:
                return bandwidth
        return 0

    def create_new_channels(self):
        z = math.floor(OPEN_CHANNELS * self.functional)
        self.channels.clear()
        for g in range(z):
            self.channels.append(Channel(g))


    def reset(self):
        self.functional = 1
        self.create_new_channels()
        self.connected_UE.clear()
        self.connected_UE_links.clear()

    def get_copy(self):
        return BaseStation(self.radio, self.mcc, self.net, self.area, self.cell, self.unit, self.lon, self.lat, self.range_bs, self.samples, self.changeable, self.created, self.updated, self.averageSignal)

class Channel:
    def __init__(self,id):
        self.id = id
        self.devices = dict()

        self.desired_band = dict()

    def add_devices(self, UE, minimumbandwidth):
        self.devices[UE] = minimumbandwidth
        self.desired_band[UE] = minimumbandwidth

        while self.band_left < 0:
            device = max(self.devices,key=lambda d: self.devices[d])
            stop_next= False
            for i in CHANNEL_BANDWIDTHS:
                if stop_next:
                    stop_next = False
                    break

                if self.devices[device] == i:
                    stop_next = True

            if stop_next:
                self.devices[device] = 0
                break

            self.devices[device] = i


    @property
    def band_left(self):
        return CHANNEL_BANDWIDTHS[0] - sum([self.devices[d] for d in self.devices])

    @property
    def connected_devices(self):
        return len(self.devices)

    @property
    def productivity(self):
        if len(self.devices) == 0:
            return 1
        return sum(self.devices.values())/sum(self.desired_band.values())

    def __str__(self):
        msg = "Channel[{}]:".format(self.id)
        for device in self.devices:
            msg += "\n{} Desired Bandwidth:{}, Actual Bandwidth:{}".format(device,self.desired_band[device],self.devices[device])

        return msg

    def getBandwidth(self, UE):
        if UE not in self.devices:
            return None

        return self.devices[UE]


    def reset(self):
        self.devices.clear()
        self.desired_band.clear()




