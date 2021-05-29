import numpy as np

CSV_PATH = "data/204.csv"


UE_CAPACITY_MIN = 10
UE_CAPACITY_MAX = 100





# CITY SPECIFIC PARAMETERS
MIN_LON = 6.827288
MAX_LON = 6.930415

MIN_LAT = 52.185100
MAX_LAT = 52.252363

POPULATION_AMOUNT = 158553



#BASE STATION PROPERTIES
BS_BS_RANGE = 2000

MCL = 70 #in db
HEIGHT_ABOVE_BUILDINGS = 20
CARRIER_FREQUENCY = 900
BASE_POWER = 80

MODEL_A = -18 * np.log10(HEIGHT_ABOVE_BUILDINGS) + 21 * np.log10(CARRIER_FREQUENCY) + BASE_POWER
MODEL_B = 40 * (1 - 4 * (10 ** -3) * HEIGHT_ABOVE_BUILDINGS)

OPEN_CHANNELS = 5
CHANNEL_BANDWIDTHS = [20,15,10,5,3,1.4]


# RISKS ENABLED

# if a large disaster occured, for instance a natural disaster or a depending failure
LARGE_DISASTER = True
LOC_LON = 5.827290
LOC_LAT = 52.19
RADIUS = 300

# malicious attacks on a certain region, for instance a DDoS
MALICIOUS_ATTACK = False

# small individual errors on some base stations
SMALL_ERRORS = False

















