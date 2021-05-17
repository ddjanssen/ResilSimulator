import csv
from objects.BaseStation import BaseStation
from settings import CSV_PATH

def load():
    all_basestations = list()


    with open(CSV_PATH,newline='') as f:
        filereader = csv.DictReader(f)

        print("Loading base station")
        i = 0
        print(i,end='')
        for row in filereader:
            if i % 100 == 0:
                print('\r',end='')
                print("Loaded base stations:{}".format(i),end='')
            new_basestation = BaseStation(row["radio"],row["mcc"],row["net"],row["area"],row["cell"],row["unit"],row["lon"],row["lat"],row["range"],row["samples"],row["changeable"],row["created"],row["updated"],row["averageSignal"])
            all_basestations.append(new_basestation)
            i += 1

        print('\r', end='')
        print("Loaded base stations:{}".format(i))
        print("Done with loading")


if __name__ == '__main__':
    load()

