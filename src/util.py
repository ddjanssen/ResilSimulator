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


def pathloss(distance):
    return (MODEL_A + MODEL_B * log10(distance / 1000)) + sqrt(10) * np.random.random()


def isolated_users(UE):
    counter = 0
    for user in UE:
        if user.link is None:
            counter += 1
    return counter / len(UE)


def received_service(UE):
    percentages = []

    for user in UE:
        if user.link is not None:
            percentages.append(1 if user.link.shannon_capacity / user.requested_capacity > 1 else user.link.shannon_capacity / user.requested_capacity)
        else:
            percentages.append(0)

    return sum(percentages) / len(percentages) if len(percentages) != 0 else 0


def received_service_half(UE):
    counter = 0

    for user in UE:
        if user.link is not None:
            if user.link.shannon_capacity / user.requested_capacity >= 0.5:
                counter += 1

    return counter / len(UE)


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
    snrs = []
    for user in UE:
        if user.link:
            snrs.append(user.SNR)
        else:
            snrs.append(0)
    return sum(snrs) / len(snrs) if len(snrs) > 0 else 0


def active_base_stations(BS):
    return sum([1 if bs.functional >= 0.2 else 0 for bs in BS])


def connected_UE_BS(base_stations):
    return sum([len(bs.connected_UE) for bs in base_stations]) / len(base_stations)


def to_pwr(db):
    return 10 ** (db / 10)


def to_db(pwr):
    return 10 * log10(pwr)


def shannon_capacity(bandwidth, TX, distance):
    RX = TX - max(pathloss(distance) - G_TX - G_RX, MCL)
    SNR = to_pwr(RX) / to_pwr(SIGNAL_NOISE)
    capacity = bandwidth * math.log2(1 + SNR)
    return capacity


def second_param_capacity(TX, distance):
    return math.log2(1 + SNR(TX, distance))


def SNR(TX, distance):
    RX = TX - max(pathloss(distance) - G_TX - G_RX, MCL)
    SNR = to_pwr(RX) / to_pwr(SIGNAL_NOISE)
    return SNR


def avg(list):
    length = 0
    total_sum = 0

    for i in list:
        if i is not None:
            length += 1
            total_sum += i

    return total_sum / length if length > 0 else -1


def getUnit(index):
    if index == 0:
        return "#Isolated Users"
    elif index == 1:
        return "Satisfaciton level (%)"
    elif index == 2:
        return "50% Satisfaction level (%)"
    elif index == 3:
        return "Avg. Distance to BS (meters)"
    elif index == 4:
        return "#Isolated Systems"
    elif index == 5:
        return "#Active BS"
    elif index == 6:
        return "Avg. SNR (ratio)"
    elif index == 7:
        return "Avg. #users connected to BS"
    else:
        return "Error"


def get_x_values():
    if LARGE_DISASTER:
        return [RADIUS_PER_SEVERITY * r for r in range(SEVERITY_ROUNDS)], "Radius disaster (meters)"
    elif MALICIOUS_ATTACK:
        return [(FUNCTIONALITY_DECREASED_PER_SEVERITY * s) for s in range(SEVERITY_ROUNDS)], "Functionality decreased of BS"
    elif ENVIRONMENTAL_RISK:
        return [s* ENV_SIGNAL_DEDUC_PER_SEVERITY for s in range(SEVERITY_ROUNDS)], "Signal strength reduced (%)"
    elif INCREASING_REQUESTED_DATA:
        return [s for s in range(SEVERITY_ROUNDS)], "Severity level of increasing data"


def create_plot(city_results):
    x_values, unit = get_x_values()

    for z in [0]:
        fig = go.Figure()
        for city in city_results:
            results = [m.get_metrics() for m in city_results[city]]
            errors = [m.get_cdf() for m in city_results[city]]
            fig.add_trace(go.Scatter(
                x=x_values,
                y=[r[z] for r in results if r[z] is not None],
                mode='lines+markers',
                name=city.abbreviation,
                error_y=dict(
                    type='data',
                    array=[e[z] for e in errors if e[z] is not None],
                    visible=True
                )
            ))
        fig.update_layout(xaxis_title=unit, yaxis_title=getUnit(z), legend=dict(yanchor="bottom", y=0.2, xanchor="left", x=0.05))
        fig.show()

    pass


def cdf(data, confidence=0.95):
    processed_data = [d for d in data if d is not None]
    if len(processed_data) == 0 or len(processed_data) == 1:
        return 0

    mean, se = np.mean(processed_data), st.sem(processed_data)
    h = se * st.t.ppf((1 + confidence) / 2, len(processed_data) - 1)
    return h


def create_new_file():
    with open(SAVE_CSV_PATH, 'w', newline='') as f:
        fieldnames = ['city', 'severity', 'isolated_users', 'received_service', 'received_service_half', 'avg_distance', 'isolated_systems', 'active_base_stations', 'avg_snr', 'connected_UE_BS']
        csv_writer = csv.writer(f)
        csv_writer.writerow(fieldnames)


def save_data(city, metrics):
    with open(SAVE_CSV_PATH, 'a', newline='') as f:
        csv_writer = csv.writer(f)
        for i in range(SEVERITY_ROUNDS):
            metric = metrics[i].csv_export()
            for m in metric:
                csv_writer.writerow([city.name, i] + m)
