from settings import ACTIVITY


class City:
    def __init__(self,name,min_lat,min_lon,max_lat,max_lon,population_amount):
        self.name = name
        self.min_lat = float(min_lat)
        self.min_lon = float(min_lon)
        self.max_lat = float(max_lat)
        self.max_lon = float(max_lon)
        self.population_amount = int((ACTIVITY * int(population_amount)) // 1)

    @property
    def abbreviation(self):
        name = self.name
        if name == "Amsterdam":
            return "Ams"
        elif name == "Arnhem":
            return "Arn"
        elif name == "Assen":
            return "Ass"
        elif name == "Den Bosch":
            return "Bos"
        elif name == "Den Haag":
            return "Haa"
        elif name == "Enschede":
            return "Ens"
        elif name == "Groningen":
            return "Gro"
        elif name == "Haarlem":
            return "Hrm"
        elif name == "Leeuwarden":
            return "Lee"
        elif name == "Lelystad":
            return "Lel"
        elif name == "Maastricht":
            return "Maa"
        elif name == "Middelburg":
            return "Mid"
        elif name == "Rotterdam":
            return "Rot"
        elif name == "Utrecht":
            return "Utr"
        elif name == "Zwolle":
            return "Zwo"

        return "error"