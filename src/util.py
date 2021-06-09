import math
from math import radians, sin, cos, atan2, sqrt, log10
import csv
import objects.BaseStation as bs
from objects.City import City
from settings import *
import plotly.graph_objects as go
import scipy.stats as st


def load_cities():
    all_cities = list()
    with open(CITY_PATH, newline='') as f:
        filereader = csv.DictReader(f)
        for row in filereader:
            all_cities.append(City(row["name"], row["min_lat"], row["min_lon"], row["max_lat"], row["max_lon"], row["population_amount"]))

    return all_cities


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


def load(min_lat, min_lon, max_lat, max_lon):
    all_basestations = list()
    all_basestations_dict = dict()

    with open(DATA_PATH, newline='') as f:
        filereader = csv.DictReader(f)
        for row in filereader:
            lon = float(row["lon"])
            lat = float(row["lat"])
            if min_lon <= lon <= max_lon and min_lat <= lat <= max_lat:
                if row["area"] not in all_basestations_dict:
                    new_basestation = bs.BaseStation(row["radio"], row["mcc"], row["net"], row["area"], row["cell"], row["unit"], lon, lat, row["range"], row["samples"], row["changeable"], row["created"], row["updated"], row["averageSignal"])
                    all_basestations_dict[row["area"]] = new_basestation
                    all_basestations.append(new_basestation)
                else:
                    # TODO: MAYBE COMBINE COORDINATES
                    pass
    return all_basestations


def SNR(signal_strength, signal_noise):
    return signal_strength / signal_noise


def pathloss(distance):
    return MODEL_A + MODEL_B * log10(distance / 1000)


def isolated_users(UE):
    counter = 0
    for user in UE:
        if user.link is None:
            counter += 1
    return counter


def received_service(UE):
    percentages = []

    for user in UE:
        if user.link is not None:
            perc = 1 if user.link.shannon_capacity / user.requested_capacity else user.link.shannon_capacity / user.requested_capacity
            percentages.append(perc)

    return sum(percentages) / len(percentages) if len(percentages) != 0 else 0


def received_service_half(UE):
    percentages = 0

    for user in UE:
        if user.link is not None:
            if user.link.shannon_capacity / user.requested_capacity < 0.5:
                percentages += 1

    return percentages / len(UE)


def avg_distance(UE):
    distances = []
    for user in UE:
        if user.link:
            distances.append(user.link.distance)

    return sum(distances) / len(distances) if len(distances) != 0 else None  # not 1 user is connected so infinite


def isolated_systems(base_stations):
    systems = 0
    bs_copy = base_stations[:]
    while len(bs_copy) != 0:
        systems += 1
        first = bs_copy.pop(0)
        checked = [link.other(first) for link in first.connected_BS[:]]
        while len(checked) != 0:
            second = checked.pop(0)
            if second in bs_copy:
                bs_copy.remove(second)
                checked = checked + [link.other(second) for link in second.connected_BS[:]]

    return systems


def SNR_averages(UE):
    snrs = [SNR(user.base_station.signal_strength, pathloss(user.distance)) for user in UE]
    return sum(snrs) / len(snrs)


def to_pwr(db):
    return 10 ** (db / 10)


def to_db(pwr):
    return 10 * log10(pwr)


def shannon_capacity(bandwidth, TX, distance):
    RX = TX - max(pathloss(distance) - G_TX - G_RX, MCL)
    SNR = to_pwr(RX) / to_pwr(SIGNAL_NOISE)
    capacity = bandwidth * math.log2(1 + SNR)
    return capacity


def avg(list):
    length = 0
    total_sum = 0

    for i in list:
        if i is not None:
            length += 1
            total_sum += i

    return total_sum / length if length > 0 else -1


def get_x_values():
    if LARGE_DISASTER:
        return [RADIUS_PER_SEVERITY * r for r in range(SEVERITY_ROUNDS)]
    elif MALICIOUS_ATTACK:
        return [(FUNCTIONALITY_DECREASED_PER_SEVERITY * s) for s in range(SEVERITY_ROUNDS)]
    elif SMALL_ERRORS:
        pass


def create_plot(city_results):
    fig = go.Figure()
    x_values = get_x_values()

    for city in city_results:
        results = [m.get_metrics() for m in city_results[city]]
        errors = [m.get_cdf() for m in city_results[city]]
        fig.add_trace(go.Scatter(
            x=x_values,
            y=[r[1] for r in results if r[1]],
            mode='lines+markers',
            name=city.name,
            error_y=dict(
                type='data',
                array=[e[1] for e in errors if e[1]],
                visible=True
            )
        ))

    fig.show()

    pass


def cdf(data, confidence=0.95):
    processed_data = [d for d in data if d]
    if len(processed_data) == 0:
        return 0

    if len(processed_data) == 1:
        return 0

    mean, se = np.mean(processed_data), st.sem(processed_data)
    h = se * st.t.ppf((1 + confidence) / 2, len(processed_data) - 1)
    return h


def create_new_file():
    with open(SAVE_CSV_PATH, 'w', newline='') as f:
        fieldnames = ['city', 'severity', 'isolated_users', 'received_service', 'received_service_half', 'avg_distance', 'isolated_systems']
        csv_writer = csv.writer(f)
        csv_writer.writerow(fieldnames)


def save_data(city, metrics):
    with open(SAVE_CSV_PATH, 'a', newline='') as f:
        csv_writer = csv.writer(f)
        for i in range(SEVERITY_ROUNDS):
            metric = metrics[i].csv_export()
            for m in metric:
                csv_writer.writerow([city.name, i] + m)
