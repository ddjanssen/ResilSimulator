from settings import ACTIVITY


class City:
    def __init__(self,name,min_lat,min_lon,max_lat,max_lon,population_amount):
        self.name = name
        self.min_lat = float(min_lat)
        self.min_lon = float(min_lon)
        self.max_lat = float(max_lat)
        self.max_lon = float(max_lon)
        self.population_amount = int((ACTIVITY * int(population_amount)) // 1)