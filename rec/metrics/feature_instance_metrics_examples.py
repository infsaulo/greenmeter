#!/usr/bin/env python

from __future__ import with_statement
from collections import defaultdict
from numpy import *
from operator import itemgetter
from object.libsvm_object import *
from metrics.term_metrics import compute_all_stats

import sys, os, math


def compute_all(stats, filename, map_libsvm_hash, map_hash_string, k, f):
    infogain = stats[1]
    ft = stats[0]
    ftc = stats[4]
    N = stats[5]
    file = open(filename)
    num_objects = 0
    object = get_next_object(file)
    while object != None:
        ID = object[2]
        print ID
        cat = object[0]
        print "CATEGORY_ID:", cat
        mean_ig = 0.0
        mean_conc = 0.0
        mean_ig_conc = 0.0
        aiff = 0.0
        num_objects += 1
        top_terms = defaultdict(float)
        concentration = defaultdict(float)
        for term in object[1]:
            top_terms[term] = infogain[term]
            concentration[term] = ftc[term][cat]/ft[term]
        n = 0
        for pair in sorted(top_terms.items(), key=itemgetter(1), reverse=True):
            if n >= k:
                break
            term = pair[0]
            if ft[term] < f:
                continue
            ig = pair[1]
            conc = concentration[term]
            ig_conc = ig*conc
            iff =  math.log(N/ft[term])
            print "%s\t%16.15f\t%16.15f\t%16.15f\t%16.15f" % (map_hash_string[map_libsvm_hash[term]], ig, conc, ig_conc, iff)
            mean_ig += ig
            mean_conc += conc
            mean_ig_conc += ig_conc
            aiff += iff
            n += 1
        if n != 0:
            mean_ig /= n
            mean_conc /= n
            mean_ig_conc /= n
            aiff /= n
        print "MEAN:\t%16.15f\t%16.15f\t%16.15f\t%16.15f" % (mean_ig, mean_conc, mean_ig_conc, aiff)
        object = get_next_object(file)
    file.close()

def read_map_int_string(filename):
    file = open(filename)
    m = defaultdict()
    for line in file:
        split = line.split()
        i = int(split[len(split) - 1])
        s = split[0]
        m[i] = s
    file.close()
    return m

def read_map_int_int(filename):
    file = open(filename)
    m = defaultdict(int)
    for line in file:
        split = line.split()
        i = int(split[1])
        s = int(split[0])
        m[i] = s
    file.close()
    return m
    

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "usage: %s <input file> <LIBSVM to HASH> <HASH TO STRING> [k (top terms) f (freq. min)]" % sys.argv[0]
        sys.exit(-1)
    filename = sys.argv[1]
    stats = compute_all_stats(filename)
    map_libsvm_hash = read_map_int_int(sys.argv[2])
    map_hash_string = read_map_int_string(sys.argv[3])
    #print map_hash_string
    k = 999999999
    f = 1
    if len(sys.argv) == 6:
        k = int(sys.argv[4])
        f = int(sys.argv[5])
    #print "#IG\t#Conc.\t#WeightedConc.\t#AIFF"
    compute_all(stats, filename, map_libsvm_hash, map_hash_string, k, f)



