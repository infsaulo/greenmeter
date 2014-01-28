#!/usr/bin/env python

from __future__ import with_statement
from collections import defaultdict
from numpy import *
from operator import itemgetter
from object.libsvm_object import *
from .term_metrics import compute_all_stats
from stats.stats import *
import sys, os, math

def compute_all(stats, filename, k, fmin, fmax):
    infogain = stats[1]
    ft = stats[0]
    fc = stats[6]
    ftc = stats[4]
    N = stats[5]
    file = open(filename)
    num_objects = 0
    object = 0
    while object != None:
        object = get_next_object(file)
        if object == None:
            break
        ID = object[2]
        cat = object[0]
        if cat < 0:
            print
            continue
        list_ig = []
        list_conc = []
        list_ig_conc = []
        list_iff = []
        list_crf = []
        num_objects += 1
        top_terms = defaultdict(float)
        concentration = defaultdict(float)
        crf = defaultdict(float)
        for term in object[1]:
            top_terms[term] = infogain[term]
            concentration[term] = ftc[term][cat]/ft[term]
            den = (ft[term] - ftc[term][cat]) / (N - fc[cat])
            if den != 0:
                crf[term] = (ftc[term][cat]/fc[cat]) / den
            else:
                crf[term] = sys.maxint
        n = 0
        for pair in sorted(top_terms.items(), key=itemgetter(1), reverse=True):
            if n >= k:
                break
            term = pair[0]
            if ft[term] < fmin or ft[term] > fmax:
                continue
            ig = pair[1]
            list_ig.append(ig)
            list_conc.append(concentration[term])
            list_ig_conc.append(ig * concentration[term])
            list_iff.append(math.log(N/ft[term]))
            list_crf.append(crf[term])
            n += 1
        if n != 0:
            mean_ig = mean(list_ig)
            mean_conc = mean(list_conc)
            mean_ig_conc = mean(list_ig_conc)
            aiff = mean(list_iff)
            mean_crf = mean(list_crf)
            print "%s\t%16.15f\t%16.15f\t%16.15f\t%16.15f\t%16.15f\t%d" % (ID, mean_ig, mean_conc, mean_ig_conc, aiff, mean_crf, n)
        else:
            print
    file.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: %s <input file> [<k (top terms)> <fmin> <fmax>]" % sys.argv[0]
        sys.exit(-1)

    filename = sys.argv[1]
    stats = compute_all_stats(filename)
    k = 999999999
    fmin = 1
    fmax = 999999999

    if len(sys.argv) > 4:
        k = int(sys.argv[2])
        fmin = int(sys.argv[3])
        fmax = int(sys.argv[4])
    print "#ID\t#IG\t#CONC.\t#WCONC.\t#AIFF\t#CRF\t#NUM_WORDS"
    compute_all(stats, filename, k, fmin, fmax)



