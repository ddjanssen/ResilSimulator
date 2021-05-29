import math
from math import radians, sin, cos, atan2, sqrt, log10
import csv
import objects.BaseStation as bs
from settings import *


def distance(lat1, lon1, lat2, lon2):
    r = 6378.137
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)

    diff_lat = lat2 - lat1
    diff_lon = lon2 - lon1

    a = sin(diff_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(diff_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r * c
    return distance * 1000


def load():
    all_basestations = list()
    all_basestations_dict = dict()

    with open(CSV_PATH, newline='') as f:
        filereader = csv.DictReader(f)

        print("Loading base station")
        i = 0
        print(i, end='')
        for row in filereader:
            if i % 100 == 0:
                print('\r', end='')
                print("Loaded base stations:{}".format(i), end='')

            lon = float(row["lon"])
            lat = float(row["lat"])
            if MIN_LON <= lon <= MAX_LON and MIN_LAT <= lat <= MAX_LAT:
                # TODO: ASK IF THE LOCAL AREA CODE CAN BE USED TO COMBINE CELLS
                if row["area"] not in all_basestations_dict:
                    new_basestation = bs.BaseStation(row["radio"], row["mcc"], row["net"], row["area"], row["cell"], row["unit"], lon, lat, row["range"], row["samples"], row["changeable"], row["created"], row["updated"], row["averageSignal"])
                    all_basestations_dict[row["area"]] = new_basestation
                    all_basestations.append(new_basestation)
                else:
                    # TODO: MAYBE COMBINE COORDINATES
                    pass
            i += 1

        print('\r', end='')
        print("Loaded base stations:{}".format(len(all_basestations)))
        print("Done with loading")

    return all_basestations


def SNR(signal_strength, signal_noise):
    return signal_strength / signal_noise


def pathloss(distance):
    return MODEL_A + MODEL_B * log10(distance)


def isolated_users(UE):
    counter = 0
    for user in UE:
        if user.link is None:
            counter += 1
    return counter


def received_service(UE):
    percentages = [(user.link.shannon_capacity if user.link else 0) / user.requested_capacity for user in UE]
    return sum(percentages) / len(percentages)


def avg_distance(UE):
    distances = []
    for user in UE:
        if user.link:
            distances.append(user.link.distance)

    return sum(distances) / len(distances)


def SNR_averages(UE):
    snrs = [SNR(user.base_station.signal_strength, pathloss(user.distance)) for user in UE]
    return sum(snrs) / len(snrs)


def shannon_capacity(bandwidth, signal_strength, distance):
    signal_noise = pathloss(distance)
    SNR = signal_strength / (10 ** (signal_noise/10))
    capacity = bandwidth * math.log2(1 + SNR)
    return capacity
