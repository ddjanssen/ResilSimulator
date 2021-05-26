from objects.Link import BS_UE_Link
from src.objects.UE import UserEquipment
from src.settings import *
import numpy as np
from src.util import distance, load


def main():
    setup()

    pass


def setup():
    base_stations = load()
    connected_base_stations(base_stations)
    UE = create_UE(base_stations)
    return base_stations, UE


def connected_base_stations(base_stations):
    print("Creating links")
    links = list()
    len_base_stations = len(base_stations)
    print("Creating links for Basestations:{}/{}".format(0, len_base_stations), end='')
    for i in range(len_base_stations):
        first = base_stations[i]
        print('\r', end='')
        print("Creating links for Basestations:{}/{}".format(i, len_base_stations), end='')
        for j in range(i + 1, len_base_stations):
            second = base_stations[j]
            if first.radio != second.radio:
                continue

            dist = distance(first.lat, first.lon, second.lat, second.lon)
            if dist < BS_BS_RANGE:
                link = first + second
                links.append(link)

    print('\r', end='')
    print("Creating links for Base Stations: {}/{}".format(len_base_stations, len_base_stations))
    print("Amount of links created: {}".format(len(links)))
    print("Done with creating links")
    return links


def create_UE(base_stations):
    all_UE = list()
    all_lon = np.random.uniform(MIN_LON, MAX_LON, POPULATION_AMOUNT)
    all_lat = np.random.uniform(MIN_LAT, MAX_LAT, POPULATION_AMOUNT)
    all_cap = np.random.randint(UE_CAPACITY_MIN, UE_CAPACITY_MAX, POPULATION_AMOUNT)
    print("Created UE:{}".format(0), end='')
    for i in range(POPULATION_AMOUNT):
        if i % 100 == 0:
            print('\r', end='')
            print("Created UE:{}".format(i), end='')

        lon = all_lon[i]
        lat = all_lat[i]

        closest_bs = None

        for j in range(len(base_stations)):
            bs = base_stations[j]
            dist = distance(lat, lon, bs.lat, bs.lon)
            if dist < bs.range:
                if not closest_bs:
                    closest_bs = (bs, dist)
                    continue

                closest_bs = closest_bs if dist > closest_bs[1] else (bs, dist)

        if closest_bs:
            new_UE = UserEquipment(i, lon, lat, all_cap[i])
            new_link = BS_UE_Link(new_UE,closest_bs[0],closest_bs[1])
            closest_bs[1].add_UE(new_link)
            new_UE.set_base_station(new_link)
            all_UE.append(new_UE)

    print('\r', end='')
    print("Created UE:{}".format(POPULATION_AMOUNT))
    print("Done with creating UE")

    return all_UE


def fail(base_stations):
    # TODO: determine how well each BS will function when an error occured
    if LARGE_DISASTER:
        for BS in base_stations:
            dist = distance(BS.lat, BS.lon, LOC_LAT, LOC_LON)
            if dist < RADIUS:
                # When closer to the epicentre the BS will function less good
                BS.malfunction(1 - (dist / RADIUS))

    elif MALICIOUS_ATTACK:
        pass
    elif SMALL_ERRORS:
        pass

    pass


def simulate(base_stations, links):
    # TODO: create a simulation that simulates packet flow etc
    # TODO: also determines the resilience
    pass


if __name__ == '__main__':
    main()
