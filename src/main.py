from objects.Link import BS_UE_Link
from src.objects.UE import UserEquipment
from src.settings import *
import numpy as np
from src.util import distance, load, isolated_users, received_service, avg_distance


def main():
    base_stations, UE, links = setup()
    for bs in base_stations:
        bs.direct_capacities()
    base_line = simulate(base_stations, UE, links)

    reset_all(base_stations,UE)
    fail(base_stations, links)
    connect_UE_BS(UE,base_stations)
    for bs in base_stations:
        bs.direct_capacities()

    values = simulate(base_stations, UE, links)

    pass


def setup():
    base_stations = load()
    links = connected_base_stations(base_stations)
    UE = create_UE()
    connect_UE_BS(UE,base_stations)
    return base_stations, UE, links


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


def create_UE():
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

        new_UE = UserEquipment(i, lon, lat, all_cap[i])
        all_UE.append(new_UE)

    print('\r', end='')
    print("Created UE:{}".format(POPULATION_AMOUNT))
    print("Done with creating UE")

    return all_UE


def connect_UE_BS(UE, base_stations):
    for user in UE:
        closest_bs = None
        for j in range(len(base_stations)):
            bs = base_stations[j]
            dist = distance(user.lat, user.lon, bs.lat, bs.lon)
            if dist < bs.range_bs and bs.functional > 0:
                if not closest_bs:
                    closest_bs = (bs, dist)
                    continue

                if dist < closest_bs[1] and bs.functional >= closest_bs[0].functional:
                    closest_bs = (bs, dist)
                elif bs.functional > closest_bs[0].functional:
                    closest_bs = (bs, dist)

        if closest_bs:
            new_link = BS_UE_Link(user, closest_bs[0], closest_bs[1])
            closest_bs[0].add_UE(new_link)
            user.set_base_station(new_link)


def fail(base_stations, links):
    # TODO: determine how well each BS will function when an error occured
    if LARGE_DISASTER:
        for BS in base_stations:
            dist = distance(BS.lat, BS.lon, LOC_LAT, LOC_LON)
            if dist < RADIUS:
                # When closer to the epicentre the BS will function less good
                if POWER_OUTAGE:
                    BS.malfunction(0)
                else:
                    BS.malfunction(1 - (dist / RADIUS))

    elif MALICIOUS_ATTACK:
        pass
    elif SMALL_ERRORS:
        pass

    pass


def simulate(base_stations, UE, links):
    # TODO: create a simulation that simulates packet flow etc
    # TODO: also determines the resilience

    iso_users = isolated_users(UE)
    percentage_received_service = received_service(UE)
    average_distance_to_bs = avg_distance(UE)

    print(iso_users, percentage_received_service, average_distance_to_bs)


def reset_all(base_stations,UE):
    for bs in base_stations:
        bs.reset()

    for user in UE:
        user.reset()

if __name__ == '__main__':
    main()
