import math

from src.objects.Link import Link
from math import sin, cos, sqrt, atan2, radians


class BaseStation:
    def __init__(self,radio,mcc,net,area,cell,unit,lon,lat,range,samples,changeable,created,updated,averageSignal):
        self.radio = radio
        self.mcc = mcc
        self.net = net
        self.area = int(area)
        self.cell = int(cell)
        self.unit = int(unit)
        self.lon = float(lon)
        self.lat = float(lat)
        self.range = float(range)
        self.samples = int(samples)
        self.changeable = int(changeable)
        self.created = int(created)
        self.updated = int(updated)
        self.averageSignal = float(averageSignal)

        self.connected_UE = list()

        self.connectedBS = list()
        self.links = list()


        # TODO: DETERMINE HOW THE BADNWITHS SHOULD BE USED
        # FOR EXAMPLE THE BANDWITHS PER CHANNEL ON LTE IS: 1.4,3,5,10,15,20 MHz but that is different on GSM and UMTS networks
        #
        # NUMBER BETWEEN 0 AND 1 THAT REPRESENTS HOW FUNCTIONAL THE BASE STATION IS
        # INITIALLY THIS IS 1 BECAUSE A BASE STATION SHOULD FUNCTION PROPERLY BEFORE IT MAL FUNCTIONS
        self.functional = 1

    def __str__(self):
        return "Base station[{}], lon:{}, lat:{}, radio:{}, LAC: {}".format(self.cell,self.lon,self.lat,self.radio,self.net)


    def malfunction(self,new_functional):
        self.functional = new_functional

    def add_link(self,other,link):
        self.connectedBS.append(other)
        self.links.append(link)

    def __add__(self, other):
        self.connectedBS.append(other)
        new_link = Link(self,other)
        self.links.append(new_link)
        other.add_link(self,new_link)
        return new_link

    def add_UE(self,UE):
        self.connected_UE.append(UE)


    def shannon_capacity(self,UE):
        # TODO change the numbers to be dynamic
        bandwith_for_user = 20  #1.4, 3, 5, 10, 15, 20 MHz for lte base stations per band total bands: 5
        signal_strength = 43 #for lte basestations
        signal_noise = -20
        SNR = signal_strength/signal_noise
        capacity = bandwith_for_user * math.log2(1 + SNR)
        return capacity








