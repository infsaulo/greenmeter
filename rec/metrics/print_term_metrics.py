#!/usr/bin/env python

from __future__ import with_statement
from collections import defaultdict
from numpy import *
from operator import itemgetter
from object.libsvm_object import *
from cooccur import compute_cooccur_and_entropy
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
    if len(sys.argv) != 5:
        print "usage: %s <libsvm file> <termmap> <minsup> <minconf>" % sys.argv[0]
        sys.exit(-1)

    minsup = float(sys.argv[3])
    minconf = float(sys.argv[4])
    ft = compute_freq(sys.argv[1])
    ids_file = open(sys.argv[2])
    m = id2string(ids_file)
    ids_file.close()
    (confidences, entropy) = compute_cooccur_and_entropy(sys.argv[1], ft, minsup, minconf)

    for t in ft:
        #if t not in m:
        #    continue
        if t in entropy:
            print m[t], ft[t], entropy[t]
        else:
            print m[t], ft[t], 100.0

