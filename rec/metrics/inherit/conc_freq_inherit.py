#!/usr/bin/env python

from __future__ import with_statement
from collections import defaultdict
from numpy import *
from operator import itemgetter
import sys, os, math

from metrics.infogain import compute_stats
from object.libsvm_object import *
from graph.graph_loader import getsims

def compute_conc(objects, cats, infogain, ft, fc, ftc, num_objects, num_cats, sup):
    for i in range(0, len(objects)):
        conc = 0.0
        for t in objects[i]:
            if ft[t] > sup:
                conc += ftc[t][cats[i]] / ft[t]
        conc /= len(objects[i])
        print conc


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s <libsvm file> <freq. min.>" % sys.argv[0]
        sys.exit(-1)

    libsvm_file = open(sys.argv[1])
    sup = int(sys.argv[2])
    #print "Herdar top", g, "termos"
    objects_and_cats = get_objects(libsvm_file)
    libsvm_file.close()
    libsvm_file = open(sys.argv[1])
    stats = compute_stats(libsvm_file, 1)
    compute_conc(objects_and_cats[0], objects_and_cats[1], stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], sup)
    libsvm_file.close()


