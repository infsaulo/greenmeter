from collections import defaultdict
from object.libsvm_object import *

import sys, os, math

def compute_instance_spread(files):
    spread = defaultdict(float)

    for file in files:
        block = get_next_object(file)
        for t in block[1]:
            spread[t] += 1
    return spread

