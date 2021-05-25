from src.objects.BaseStation import BaseStation
from src.objects.UE import UserEquipment
from src.util import distance


def main_test():
    base_station_test()
    pass


def base_station_test():
    BS = BaseStation("LTE",204,8,404,123123,0,5,52,1000,106,1,12941189449,13842455404,0)
    dummyUE = UserEquipment(0,5.0001,52.004,20)
    dummyUE.set_base_station(BS,distance(BS.lat,BS.lon,dummyUE.lat,dummyUE.lon))
    print(BS.shannon_capacity(dummyUE))
    pass


if __name__ == '__main__':
    main_test()
