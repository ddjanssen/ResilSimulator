from settings import OPEN_CHANNELS, CHANNEL_BANDWIDTHS, BASE_POWER
from src.objects.Link import BS_BS_Link, BS_UE_Link
import util


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

        self.channels = list()
        for g in range(OPEN_CHANNELS):
            self.channels.append(Channel(g))

        self.signal_strength = 10 ** (BASE_POWER/10)

        # TODO: DETERMINE HOW THE BADNWITHS SHOULD BE USED
        # FOR EXAMPLE THE BANDWITHS PER CHANNEL ON LTE IS: 1.4,3,5,10,15,20 MHz but that is different on GSM and UMTS networks
        #
        # NUMBER BETWEEN 0 AND 1 THAT REPRESENTS HOW FUNCTIONAL THE BASE STATION IS
        # INITIALLY THIS IS 1 BECAUSE A BASE STATION SHOULD FUNCTION PROPERLY BEFORE IT MAL FUNCTIONS
        self.functional = 1

    def __str__(self):
        startmsg = "Base station[{}], lon:{}, lat:{}, radio:{}, LAC: {}".format(self.cell, self.lon, self.lat, self.radio, self.net)
        for channel in self.channels:
            startmsg += "\n{}".format(str(channel))
        return startmsg

    def malfunction(self, new_functional):
        self.functional = new_functional

    def add_link(self, link: BS_BS_Link):
        self.connected_BS.append(link)

    def __add__(self, other):
        new_link = BS_BS_Link(self, other)
        self.connected_BS.append(new_link)
        other.add_link(new_link)
        return new_link

    def add_UE(self, link: BS_UE_Link):
        # TODO fix channel layers
        self.connected_UE_links.append(link)
        self.connected_UE.append(link.ue)

    def direct_capacities(self):
        UE = sorted(self.connected_UE, key=lambda ue: ue.requested_capacity)
        minimum_band_needed = dict()
        bandwidth_length = len(CHANNEL_BANDWIDTHS)

        for ue in UE:
            bandwidthneeded = None
            for bandwidth in range(bandwidth_length):
                service = util.shannon_capacity(CHANNEL_BANDWIDTHS[bandwidth], self.signal_strength, ue.link.distance)
                if service < ue.requested_capacity:
                    if bandwidth == 0:
                        bandwidthneeded = CHANNEL_BANDWIDTHS[0]
                    else:
                        bandwidthneeded = CHANNEL_BANDWIDTHS[bandwidth - 1]

                    break

                if bandwidth == bandwidth_length - 1:
                    bandwidthneeded = CHANNEL_BANDWIDTHS[-1]

            if bandwidthneeded not in minimum_band_needed:
                minimum_band_needed[bandwidthneeded] = list()

            minimum_band_needed[bandwidthneeded].append(ue)

        for bandwidth in CHANNEL_BANDWIDTHS:
            if bandwidth not in minimum_band_needed:
                continue

            ues = minimum_band_needed[bandwidth]
            for ue in ues:
                channel = max(self.channels,key=lambda c:(c.productivity,c.band_left))
                channel.add_devices(ue,bandwidth)


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
                print("Too many devices connected to this base station")
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


