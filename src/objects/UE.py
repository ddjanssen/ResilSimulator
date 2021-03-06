from objects.Link import BS_UE_Link

class UserEquipment:
    def __init__(self, id: int, lon: float, lat: float, capacity: int):
        self.id = id
        self.requested_capacity = capacity
        self.lon = lon
        self.lat = lat
        self.link = None
        pass

    def set_base_station(self, link: BS_UE_Link):
        self.link = link

    @property
    def SNR(self):
        return self.link.SNR

    def __str__(self):
        return "UE[{}], bandwith: {}, lon: {}, lat: {}".format(self.id, self.requested_capacity, self.lon, self.lat)

    def reset(self):
        self.link = None
