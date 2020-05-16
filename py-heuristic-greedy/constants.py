import os

min_swaps = {
    4: 1,
    5: 3,
    6: 4,
    7: 4,
    8: 7,
    9: 8,
    10: 10,
    11: 12,
    12: 15,
    13: 18,
    14: 21,
    15: 24,
    16: 29,
    17: 33,
    18: 38,
    19: 43,
    20: 47,
    21: 54,
    22: 60,
    30: 116,
}

PWD = os.path.dirname(__file__)
LOGS_DIR = os.path.join(PWD, "logs")
CHECKPOINT_DIR = os.path.join(PWD, "checkpoint")
LOGS_FULL_DIR = LOGS_DIR + "_full"
CHECKPOINT_FULL_DIR = CHECKPOINT_DIR + "_full"
