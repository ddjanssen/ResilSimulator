from objects.Link import BS_UE_Link
from src.objects.BaseStation import BaseStation
from src.objects.UE import UserEquipment
from src.util import distance

import numpy as np

def main_test():
    channel_test()
    pass


def base_station_test():
    BS = BaseStation("LTE",204,8,404,123123,0,5,52,1000,106,1,12941189449,13842455404,0)
    dummyUE = UserEquipment(0,5.0001,52.004,20)
    pass


def channel_test():
    AMOUNT_OF_DEVICES = 15

    BS = BaseStation("LTE", 204, 8, 404, 123123, 0, 5, 52, 1000, 106, 1, 12941189449, 13842455404, 0)
    all_cap = np.random.randint(5,30,AMOUNT_OF_DEVICES)
    dummy_lat, dummyLon = 52.004,5.0001
    dist = distance(dummy_lat,dummyLon,52,5)

    for i in range(AMOUNT_OF_DEVICES):
        dummyUE = UserEquipment(0,dummyLon,dummy_lat,all_cap[i])
        link = BS_UE_Link(dummyUE,BS,dist)
        BS.add_UE(link)
        dummyUE.set_base_station(link)


    BS.direct_capacities()
    print(BS)




if __name__ == '__main__':
    main_test()
