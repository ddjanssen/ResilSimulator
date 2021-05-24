from math import radians, sin, cos, atan2, sqrt
import csv
from objects.BaseStation import BaseStation
from settings import CSV_PATH, MAX_LAT,MIN_LAT,MAX_LON,MIN_LON

def distance(lat1,lon1,lat2,lon2):
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



    with open(CSV_PATH,newline='') as f:
        filereader = csv.DictReader(f)

        print("Loading base station")
        i = 0
        print(i,end='')
        for row in filereader:
            if i % 100 == 0:
                print('\r',end='')
                print("Loaded base stations:{}".format(i),end='')

            lon = float(row["lon"])
            lat = float(row["lat"])
            if MIN_LON <= lon <= MAX_LON and MIN_LAT <= lat <= MAX_LAT:
                # TODO: ASK IF THE LOCAL AREA CODE CAN BE USED TO COMBINE CELLS
                if row["area"] not in all_basestations_dict:
                    new_basestation = BaseStation(row["radio"], row["mcc"], row["net"], row["area"], row["cell"], row["unit"], lon, lat, row["range"], row["samples"], row["changeable"], row["created"], row["updated"], row["averageSignal"])
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