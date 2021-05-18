from src.objects.Link import Link


class BaseStation:
    def __init__(self,radio,mcc,net,area,cell,unit,lon,lat,range,samples,changeable,created,updated,averageSignal):
        self.radio = radio
        self.mcc = mcc
        self.net = net
        self.area = area
        self.cell = cell
        self.unit = unit
        self.lon = lon
        self.lat = lat
        self.range = range
        self.samples = samples
        self.changeable = changeable
        self.created = created
        self.updated = updated
        self.averageSignal = averageSignal

        self.connectedBS = list()
        self.links = list()



        # NUMBER BETWEEN 0 AND 1 THAT REPRESENTS HOW FUNCTIONAL THE BASE STATION IS
        # INITIALLY THIS IS 1 BECAUSE A BASE STATION SHOULD FUNCTION PROPERLY BEFORE IT MAL FUNCTIONS
        self.functional = 1

    def __str__(self):
        return "Base station[{}], lon:{}, lat:{}, radio:{}".format(self.cell,self.lon,self.lat,self.radio)


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








