
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

    def __str__(self):
        return "Base station[{}], lon:{}, lat:{}, radio:{}".format(self.cell,self.lon,self.lat,self.radio)






