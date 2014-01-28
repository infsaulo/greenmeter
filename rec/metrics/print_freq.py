#!/usr/bin/env python

from __future__ import with_statement
from collections import defaultdict
from numpy import *
from operator import itemgetter
from object.libsvm_object import *
from term_freq import compute_freq


def id2string(file):
    dict = {}
    for line in file:
        spl = line.split()
        string = spl[0]
        id = int(spl[1])
        dict[id] = string
    return dict


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s <libsvm file> <termmap>" % sys.argv[0]
        sys.exit(-1)

    ft = compute_freq(sys.argv[1])
    m = id2string(open(sys.argv[2]))
    for t in ft:
        print m[t], ft[t]



