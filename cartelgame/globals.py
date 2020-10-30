PRACTICE = 1
ACTUAL = 2
INTERVALS = {
    1: (0, 2),
    2: (0, 3),
    3: (1, 3),
    4: (1, 4),
    5: (2, 4),
    6: (2, 5),
    7: (3, 5),
    8: (3, 6),
    9: (4, 6),
    10: (4, 7),
    11: (5, 7),
    12: (5, 8),
    13: (6, 8),
    14: (6, 9),
    15: (7, 9),
    16: (7, 10),
    17: (8, 10),
    18: (8, 11),
    19: (9, 12),
    20: (9, 12),
}

import random
NUM_CAUGHT = { key: random.randint(*curr_interval) for key, curr_interval in INTERVALS.items() }