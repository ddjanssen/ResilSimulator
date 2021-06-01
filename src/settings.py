import numpy as np

DATA_PATH = "data/204.csv"
CITY_PATH = "data/city.csv"



UE_CAPACITY_MIN = 10
UE_CAPACITY_MAX = 100


# CITY SPECIFIC PARAMETERS
ACTIVITY = 0.007

#BASE STATION PROPERTIES
BS_BS_RANGE = 4000

MCL = 70 #in db
HEIGHT_ABOVE_BUILDINGS = 20
CARRIER_FREQUENCY = 2000
BASE_POWER = 43
G_TX = 15
G_RX = 0

MODEL_A = -18 * np.log10(HEIGHT_ABOVE_BUILDINGS) + 21 * np.log10(CARRIER_FREQUENCY) + 80
MODEL_B = 40 * (1 - 4 * (10 ** -3) * HEIGHT_ABOVE_BUILDINGS)

OPEN_CHANNELS = 5
CHANNEL_BANDWIDTHS = [20,15,10,5,3,1.4]

SIGNAL_NOISE = -100

# RISKS ENABLED

# if a large disaster occured, for instance a natural disaster or a depending failure
LARGE_DISASTER = True
POWER_OUTAGE = True
LOC_LON = 6.90
LOC_LAT = 52.19
RADIUS = 5000

# malicious attacks on a certain region, for instance a DDoS
MALICIOUS_ATTACK = False

# small individual errors on some base stations
SMALL_ERRORS = False

















