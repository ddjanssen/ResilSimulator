import util
from objects.City import City
from objects.Metrics import Metrics
from settings import SAVE_CSV_PATH
import csv


def load():
    sub_city_results = dict()

    print("importing file")
    with open(SAVE_CSV_PATH,newline='') as f:


        filereader = csv.DictReader(f)
        for row in filereader:

            city = str(row["city"])
            severity = int(row["severity"])
            isolated_users = float(row["isolated_users"]) if row["isolated_users"] != '' else None
            received_service = float(row["received_service"]) if row["received_service"] != '' else None
            received_service_half = float(row["received_service_half"]) if row["received_service_half"] != '' else None
            avg_distance = float(row["avg_distance"]) if row["avg_distance"] != '' else None
            isolated_systems = float(row["isolated_systems"]) if row["isolated_users"] != '' else None

            if city not in sub_city_results:
                sub_city_results[city] = []

            while severity >= len(sub_city_results[city]):
                sub_city_results[city].append(Metrics())

            sub_city_results[city][severity].add_metric((isolated_users,received_service,received_service_half,avg_distance,isolated_systems))


    city_results = dict()
    for city in sub_city_results:
        city_results[City(city,0,0,0,0,0)] = sub_city_results[city]

    print("Plotting results")
    util.create_plot(city_results)


if __name__ == '__main__':
    load()
