from objects.Link import BS_UE_Link
from src.objects.UE import UserEquipment
from src.settings import *
import numpy as np
import util


def main():
    all_cities = util.load_cities()

    for city in all_cities:
        print("Starting simulation for city:{}".format(city.name))
        base_stations, UE,links = setup(city)
        print("Directing capacities to the users")
        for bs in base_stations:
            bs.direct_capacities()

        print("Creating base line resilience metrics")
        base_line = simulate(base_stations, UE, links)

        print("Resetting base stations and UE")
        reset_all(base_stations,UE)
        print("Failing base stations and links")
        fail(base_stations, links,city)
        print("Connecting UE to BS again")
        connect_UE_BS(UE,base_stations)
        print("Directing capacities to the users")
        for bs in base_stations:
            bs.direct_capacities()

        print("Creating resilience metrics after failure")
        values = simulate(base_stations, UE, links)

        print("------------------------------------------------------")

    pass


def setup(city):
    print("Loading base stations")
    base_stations = util.load(city.min_lat,city.min_lon,city.max_lat,city.max_lon)
    print("Creating links between base stations")
    links = connected_base_stations(base_stations)
    print("Creating UE")
    UE = create_UE(city)
    print("Connecting UE to BS")
    connect_UE_BS(UE,base_stations)
    return base_stations, UE, links


def connected_base_stations(base_stations):
    links = list()
    len_base_stations = len(base_stations)
    for i in range(len_base_stations):
        first = base_stations[i]
        for j in range(i + 1, len_base_stations):
            second = base_stations[j]

            if first.radio != second.radio:
                continue

            dist = util.distance(first.lat, first.lon, second.lat, second.lon)
            if dist < BS_BS_RANGE:
                link = first + second
                links.append(link)
    return links


def create_UE(city):
    all_UE = list()
    all_lon = np.random.uniform(city.min_lon, city.max_lon, city.population_amount)
    all_lat = np.random.uniform(city.min_lat, city.max_lat, city.population_amount)
    all_cap = np.random.randint(UE_CAPACITY_MIN, UE_CAPACITY_MAX, city.population_amount)
    for i in range(city.population_amount):
        lon = all_lon[i]
        lat = all_lat[i]

        new_UE = UserEquipment(i, lon, lat, all_cap[i])
        all_UE.append(new_UE)


    return all_UE


def connect_UE_BS(UE, base_stations):
    for user in UE:
        closest_bs = None
        for j in range(len(base_stations)):
            bs = base_stations[j]
            dist = util.distance(user.lat, user.lon, bs.lat, bs.lon)
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


def fail(base_stations, links,city):
    # TODO: determine how well each BS will function when an error occured
    if LARGE_DISASTER:
        random_lat = np.random.uniform(city.min_lat,city.max_lat,1)[0]
        random_lon = np.random.uniform(city.min_lon,city.max_lon,1)[0]


        for BS in base_stations:
            dist = util.distance(BS.lat, BS.lon, random_lat, random_lon)
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

    iso_users = util.isolated_users(UE)
    percentage_received_service = util.received_service(UE)
    average_distance_to_bs = util.avg_distance(UE)

    iso_systems = util.isolated_systems(base_stations)

    print(iso_users, percentage_received_service, average_distance_to_bs,iso_systems)


def reset_all(base_stations,UE):
    for bs in base_stations:
        bs.reset()

    for user in UE:
        user.reset()

if __name__ == '__main__':
    main()
